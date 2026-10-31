package ai.rplay.carcast;
public final class CnProbeHost {
    public static int[] pixels;
    public static long clock,serial;
    public static int inputs;
    public static Runnable pending;
    public static String last="";
    public static int[] frame(){return pixels==null?null:pixels.clone();}
    public static long version(){return serial;}
    public static long now(){return clock;}
    public static void send(int wheel){if(wheel!=1&&wheel!=-1)throw new AssertionError("unexpected input");inputs++;}
    public static void post(Runnable r,long delay){pending=r;}
    public static void clear(){pending=null;}
    public static void log(String s){last=s;}
    public static void tick(){Runnable r=pending;pending=null;if(r!=null)r.run();}
    public static void reset(){pixels=null;clock=1000;serial=1;inputs=0;pending=null;last="";}
}
