package ai.rplay.carcast;

/** Bounded diagnostic only: one rotary step, then text geometry, never Select. */
public final class CnFocusProbe implements Runnable {
    private static volatile CnFocusProbe current;
    private int[] before;
    private int[] candidate;
    private long started, baselineVersion, candidateVersion;
    private int wheel;
    private final int[] stats=new int[8];
    private long observedVersion;

    private CnFocusProbe() {}
    public static boolean busy() { return current!=null; }
    public static void cancel() {
        CnProbeHost.clear();
        if(current!=null) current.before=null;
        current=null;
    }
    public static void request(int direction) {
        if(current!=null || (direction!=-1 && direction!=1)) return;
        CnFocusProbe p=new CnFocusProbe();
        p.before=CnProbeHost.frame();
        if(p.before==null) { CnProbeHost.log("unavailable frame; no input sent"); return; }
        p.wheel=direction;
        p.started=CnProbeHost.now();
        p.baselineVersion=CnProbeHost.version();
        current=p;
        CnProbeHost.send(direction);
        CnProbeHost.post(p,250);
    }
    private static boolean same(int[] a,int[] b) {
        if(a==null || b==null) return false;
        for(int i=0;i<4;i++) if(Math.abs(a[i]-b[i])>2) return false;
        return true;
    }
    public void run() {
        if(current!=this) return;
        long elapsed=CnProbeHost.now()-started;
        if(elapsed>2200) { CnProbeHost.log("no stable focus wheel="+wheel+" baseline="+baselineVersion+" observed="+observedVersion
                +" candidateVersion="+candidateVersion+" changed="+stats[0]+" best="+stats[1]+" second="+stats[2]
                +" bounds="+stats[3]+","+stats[4]+","+stats[5]+","+stats[6]+" fill="+stats[7]); cancel(); return; }
        long version=CnProbeHost.version();
        observedVersion=version;
        int[] after=CnProbeHost.frame();
        if(after==null) { CnProbeHost.log("frame lost; probe cancelled");cancel();return; }
        if(version>baselineVersion) {
            int[] found=CnFocusGeometry.analyze(before,after,320,180,stats);
            if(found!=null && same(candidate,found) && version!=candidateVersion) {
                CnProbeHost.log("rect="+found[0]+","+found[1]+","+found[2]+","+found[3]
                    +" confidence="+found[4]+" elapsedMs="+elapsed+" wheel="+wheel);
                cancel(); return;
            }
            candidate=found;
            candidateVersion=version;
        }
        CnProbeHost.post(this,100);
    }
}
