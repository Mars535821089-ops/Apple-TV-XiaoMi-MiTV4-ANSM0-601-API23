package ai.rplay.carcast;

/** Experimental coordinator. Only observation may advance a path; never Select. */
public final class CnSpatialNavigator implements CnFocusProbe.Completion {
    private static final Object LOCK=new Object();
    private static volatile CnSpatialNavigator current;
    private static volatile boolean unknown;
    private final CnSpatialPath path;
    private final long started;
    private CnSpatialNavigator(int direction){path=new CnSpatialPath(direction);started=CnProbeHost.now();}
    public static boolean busy(){return current!=null;}
    public static boolean uncertain(){return unknown;}
    public static void stop(){
        synchronized(LOCK){if(current!=null)unknown=true;current=null;CnFocusProbe.cancel();}
    }
    public static void cancel(){
        synchronized(LOCK){current=null;unknown=false;CnFocusProbe.cancel();}
    }
    public static void request(int direction){
        synchronized(LOCK){
            if(current!=null || unknown || CnFocusProbe.busy()) return;
            try {
                current=new CnSpatialNavigator(direction);
                current.step();
            } catch(OutOfMemoryError failure){current=null;unknown=true;CnFocusProbe.cancel();}
        }
    }
    private void finish(boolean uncertain,String reason){
        if(current!=this)return;
        current=null;unknown=uncertain;
        CnProbeHost.log("spatial "+reason+" elapsedMs="+(CnProbeHost.now()-started));
    }
    private void step(){
        if(current!=this)return;
        if(CnProbeHost.now()-started>60000){finish(true,"deadline; stopped");return;}
        // Probe performs only bounded frame reads and enqueues transport. It
        // never synchronously calls native code while this lock is held.
        if(!CnFocusProbe.request(path.wheel(),this))finish(true,"unavailable; stopped");
    }
    public void complete(int[] from,int[] to){
        synchronized(LOCK){
            if(current!=this)return;
            try {
                int result=path.observe(from,to);
                if(result==0 || result==2){step();return;}
                if(result==1)finish(false,"target reached");
                else if(result==3)finish(false,"origin restored; no target");
                else finish(true,"unconfirmed focus; stopped");
            } catch(OutOfMemoryError failure){
                // Probe already retired itself before this callback. It cannot
                // clean a stranded coordinator on our behalf.
                current=null;unknown=true;CnFocusProbe.cancel();
            }
        }
    }
}
