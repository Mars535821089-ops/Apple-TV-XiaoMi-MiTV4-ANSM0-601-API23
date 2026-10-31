import ai.rplay.carcast.CnFocusProbe;
import ai.rplay.carcast.CnProbeHost;
import java.util.Arrays;
public final class FocusProbeTest {
    private static int[] selected(int top){int[] a=new int[320*180];Arrays.fill(a,0xff202020);for(int y=top;y<top+22;y++)for(int x=80;x<250;x++)a[y*320+x]=0xffeeeeee;return a;}
    private static void check(boolean b,String m){if(!b)throw new AssertionError(m);}
    private static void reset(){CnFocusProbe.cancel();CnProbeHost.reset();}
    private static void start(){reset();CnProbeHost.pixels=selected(40);CnFocusProbe.request(1);}
    public static void main(String[] args){
        reset();CnFocusProbe.request(1);check(CnProbeHost.inputs==0&&!CnFocusProbe.busy(),"missing frame must send no input");
        start();CnFocusProbe.request(-1);check(CnProbeHost.inputs==1,"busy request must not add another move");
        CnProbeHost.pixels=selected(80);CnProbeHost.serial=2;CnProbeHost.clock=1300;CnProbeHost.tick();
        check(CnFocusProbe.busy(),"one changed frame is not stable");
        CnProbeHost.clock=1400;CnProbeHost.tick();check(CnFocusProbe.busy(),"same video serial cannot confirm stability");
        CnProbeHost.serial=3;CnProbeHost.clock=1500;CnProbeHost.tick();
        check(!CnFocusProbe.busy()&&CnProbeHost.last.contains("rect=80,80,250,102"),"stable fresh frames must produce geometry");
        start();CnProbeHost.clock=3301;CnProbeHost.tick();check(!CnFocusProbe.busy()&&CnProbeHost.inputs==1,"timeout cannot send additional input");
        start();Runnable obsolete=CnProbeHost.pending;CnFocusProbe.cancel();obsolete.run();
        check(CnProbeHost.pending==null&&!CnFocusProbe.busy(),"cancelled callback must not resurrect work");
        start();CnProbeHost.pixels=null;CnProbeHost.clock=1300;CnProbeHost.tick();
        check(!CnFocusProbe.busy()&&CnProbeHost.inputs==1,"lost frame must cancel without another move");
        reset();CnProbeHost.pixels=selected(40);CnFocusProbe.request(2);check(CnProbeHost.inputs==0,"unsupported input must be rejected");
        System.out.println("PASS: focus probe fresh-frame, overlap, timeout, cancellation and missing-frame contracts");
    }
}
