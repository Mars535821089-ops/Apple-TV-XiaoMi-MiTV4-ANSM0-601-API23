package ai.rplay.carcast;

/** Bounded diagnostic only: one rotary step, then text geometry, never Select. */
public final class CnFocusProbe implements Runnable {
    public interface Completion { void complete(int[] from,int[] to); }
    private static final Object LOCK=new Object();
    private static volatile CnFocusProbe current;
    private static int epoch, nextToken=0x1000;
    private int[] before, candidate, after;
    private final int[] stats=new int[24];
    private long started, baselineVersion, candidateVersion, observedVersion, settledSince;
    private long sampledVersion=Long.MIN_VALUE;
    private long renderGeneration;
    private int wheel, token;
    private Completion completion;
    private String beforeSummary,afterSummary="none";
    private boolean sampled,late;
    private static String summary(int[] pixels) {
        if(pixels==null)return "missing";
        int hash=1,opaque=0,bright=0;long light=0;
        for(int y=0;y<180;y++)for(int x=32;x<320;x++) {
            int c=pixels[y*320+x],r=(c>>>16)&255,g=(c>>>8)&255,b=c&255;
            int l=(r*77+g*150+b*29)>>>8;
            hash=31*hash+c;light+=l;if((c>>>24)>=128)opaque++;if(l>=130)bright++;
        }
        StringBuilder labels=new StringBuilder();
        for(int row=0;row<2;row++)for(int col=0;col<4;col++) {
            int count=0,left=67+col*66,top=62+row*74;
            for(int y=top;y<top+11;y++)for(int x=left;x<left+20;x++) {
                int c=pixels[y*320+x],l=(((c>>>16)&255)*77+((c>>>8)&255)*150+(c&255)*29)>>>8;
                if(l>=130)count++;
            }
            if(labels.length()>0)labels.append('/');labels.append(count);
        }
        return Integer.toHexString(hash)+","+opaque+","+bright+","+(light/(288*180))+" labels="+labels;
    }

    private CnFocusProbe() {}
    public static boolean busy() { return current!=null; }
    public static boolean validToken(int token) {
        synchronized(LOCK) { CnFocusProbe p=current; return p!=null && p.token==token; }
    }
    public static void cancel() {
        synchronized(LOCK) {
            epoch++;
            CnFocusProbe p=current;current=null;
            CnProbeHost.clear();
            if(p!=null){p.before=null;p.after=null;}
        }
    }
    private void finish(String message) {
        finish(message,null,null);
    }
    private void finish(String message,int[] from,int[] to) {
        Completion listener;
        synchronized(LOCK) {
            if(current!=this) return;
            listener=completion;
            cancel();
            CnProbeHost.log(message);
        }
        // Callers may enqueue the next observed step. Never call them under LOCK.
        if(listener!=null) listener.complete(from,to);
    }
    public static void request(int direction) {
        request(direction,null);
    }
    public static boolean request(int direction,Completion completion) {
        final int stamp;
        synchronized(LOCK) {
            if(current!=null || (direction!=-1 && direction!=1) || !CnProbeHost.ready()) return false;
            stamp=epoch;
        }
        CnFocusProbe p=null;
        try {
            p=new CnFocusProbe();p.renderGeneration=CnProbeHost.generation();p.before=CnProbeHost.frame();
            if(p.before==null) {
                synchronized(LOCK) { if(epoch==stamp && current==null) CnProbeHost.log("unavailable frame; no input sent"); }
                return false;
            }
            p.wheel=direction;p.started=CnProbeHost.now();p.baselineVersion=CnProbeHost.version();
            p.beforeSummary=summary(p.before);
            synchronized(LOCK) {
                if(epoch!=stamp || current!=null || !CnProbeHost.ready()
                    || CnProbeHost.generation()!=p.renderGeneration) return false;
                if(++nextToken<0x1000) nextToken=0x1000;
                p.token=nextToken;p.completion=completion;current=p;
                CnProbeHost.log("start wheel="+direction+" baseline="+p.baselineVersion+" summary="+p.beforeSummary);
                // Only enqueue here, never call native transport while holding LOCK.
                CnProbeHost.send(direction,p.token);
                CnProbeHost.post(p,250);
            }
            return true;
        } catch(OutOfMemoryError failure) {
            if(p!=null) p.finish("probe allocation failed; cancelled");
            return false;
        }
    }
    private static boolean same(int[] a,int[] b) {
        if(a==null || b==null) return false;
        for(int i=0;i<4;i++) if(Math.abs(a[i]-b[i])>2) return false;
        return true;
    }
    public void run() {
        if(current!=this) return;
        try {
            if(CnProbeHost.generation()!=renderGeneration){finish("render generation changed; probe cancelled");return;}
            long elapsed=CnProbeHost.now()-started;
            if(elapsed>2200 && !late){late=true;CnProbeHost.log("late frame observation; no additional input wheel="+wheel);}
            if(elapsed>7000) {
                finish("no stable focus wheel="+wheel+" baseline="+baselineVersion+" observed="+observedVersion
                    +" candidateVersion="+candidateVersion+" changed="+stats[0]+" best="+stats[1]+" second="+stats[2]
                    +" bounds="+stats[3]+","+stats[4]+","+stats[5]+","+stats[6]+" fill="+stats[7]
                    +" mask="+stats[8]+" raw="+stats[9]+","+stats[10]+","+stats[11]+","+stats[12]+","+stats[13]+","+stats[14]
                    +" edge="+stats[15]+" luma="+stats[16]+","+stats[17]+","+stats[18]+","+stats[19]+","+stats[20]+","+stats[21]+","+stats[22]+","+stats[23]
                    +" beforeSummary="+beforeSummary+" afterSummary="+afterSummary);return;
            }
            long version=CnProbeHost.version();observedVersion=version;
            if(version>baselineVersion) {
                int[] found=candidate;
                if(version!=sampledVersion) {
                    after=CnProbeHost.frame();
                    if(after==null) { finish("frame lost; probe cancelled");return; }
                    if(CnProbeHost.generation()!=renderGeneration){finish("render replaced during capture; probe cancelled");return;}
                    sampledVersion=version;afterSummary=summary(after);
                    found=CnFocusGeometry.analyze(before,after,320,180,stats);
                }
                if(!sampled){sampled=true;CnProbeHost.log("sample elapsedMs="+elapsed+" changed="+stats[0]+" summary="+afterSummary);}
                if(found!=null && same(candidate,found) && elapsed-settledSince>=150) {
                    int[] origin=completion==null?null:CnFocusGeometry.analyze(after,before,320,180);
                    if(completion!=null && !CnFocusGeometry.sameScene(before,after,320,180,origin,found)) {
                        finish("scene changed or source unknown; spatial step stopped");return;
                    }
                    finish("rect="+found[0]+","+found[1]+","+found[2]+","+found[3]
                        +" confidence="+found[4]+" elapsedMs="+elapsed+" wheel="+wheel,origin,found);return;
                }
                if(!same(candidate,found)) settledSince=elapsed;
                candidate=found;candidateVersion=version;
            }
            synchronized(LOCK) { if(current==this) CnProbeHost.post(this,100); }
        } catch(OutOfMemoryError failure) {
            finish("analysis allocation failed; probe cancelled");
        }
    }
}
