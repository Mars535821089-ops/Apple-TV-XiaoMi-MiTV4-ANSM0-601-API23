package ai.rplay.carcast;
public final class CnProbeHost {
    public static int[] pixels;
    public static long clock,serial;
    public static int inputs,deliveries,pendingToken;
    public static boolean blocked,failFrame;
    public static Runnable onFrame;
    public static Runnable pending;
    public static String last="";
    public static int[] frame(){
        if(failFrame)throw new OutOfMemoryError("controlled frame allocation");
        int[] result=pixels==null?null:pixels.clone();
        Runnable hook=onFrame;onFrame=null;if(hook!=null)hook.run();return result;
    }
    public static boolean ready(){return !blocked;}
    public static void deliver(){
        boolean allowed=true;
        try {allowed=((Boolean)CnFocusProbe.class.getMethod("validToken",int.class).invoke(null,pendingToken)).booleanValue();}
        catch(NoSuchMethodException oldBehavior){}catch(Exception e){throw new AssertionError(e);}
        if(allowed)deliveries++;
    }
    public static long version(){return serial;}
    public static long now(){return clock;}
    public static void send(int wheel){send(wheel,0);}
    public static void send(int wheel,int token){if(wheel!=1&&wheel!=-1)throw new AssertionError("unexpected input");inputs++;pendingToken=token;}
    public static void post(Runnable r,long delay){pending=r;}
    public static void clear(){pending=null;}
    public static void log(String s){last=s;}
    public static void tick(){Runnable r=pending;pending=null;if(r!=null)r.run();}
    public static void reset(){pixels=null;blocked=false;failFrame=false;onFrame=null;deliveries=0;pendingToken=0;clock=1000;serial=1;inputs=0;pending=null;last="";}
}
