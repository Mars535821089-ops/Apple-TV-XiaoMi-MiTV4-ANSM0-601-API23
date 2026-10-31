import ai.rplay.carcast.CnFocusProbe;
import ai.rplay.carcast.CnProbeHost;
import java.util.Arrays;
public final class FocusProbeTest {
    private static final class Result implements CnFocusProbe.Completion {
        int count; int[] from,to;
        public void complete(int[] a,int[] b){count++;from=a;to=b;}
    }
    private static int[] selected(int top){int[] a=new int[320*180];Arrays.fill(a,0xff202020);for(int y=top;y<top+22;y++)for(int x=80;x<250;x++)a[y*320+x]=0xffeeeeee;return a;}
    private static void check(boolean b,String m){if(!b)throw new AssertionError(m);}
    private static void reset(){CnFocusProbe.cancel();CnProbeHost.reset();}
    private static void start(){reset();CnProbeHost.pixels=selected(40);CnFocusProbe.request(1);}
    public static void main(String[] args){
        reset();CnFocusProbe.request(1);check(CnProbeHost.inputs==0&&!CnFocusProbe.busy(),"missing frame must send no input");
        start();CnFocusProbe.request(-1);check(CnProbeHost.inputs==1,"busy request must not add another move");
        CnProbeHost.clock=1200;CnProbeHost.tick();
        check(CnProbeHost.frameReads==1,"no new video frame must not trigger another GPU readback");
        CnProbeHost.pixels=selected(80);CnProbeHost.serial=2;CnProbeHost.clock=1300;CnProbeHost.tick();
        check(CnFocusProbe.busy(),"one changed frame is not stable");
        CnProbeHost.clock=1400;CnProbeHost.tick();check(CnFocusProbe.busy(),"focus rectangle must remain settled long enough");
        CnProbeHost.clock=1500;CnProbeHost.tick();
        check(!CnFocusProbe.busy()&&CnProbeHost.last.contains("rect=80,80,250,102"),"a fresh event-driven frame can settle without another video update");
        check(CnProbeHost.frameReads==2,"settling a cached fresh frame must not repeatedly read the GPU");
        start();CnProbeHost.pixels=selected(80);CnProbeHost.clock=1500;CnProbeHost.tick();
        CnProbeHost.clock=1800;CnProbeHost.tick();check(CnFocusProbe.busy(),"pre-input frame serial must never confirm a new focus");
        start();CnProbeHost.clock=3301;CnProbeHost.tick();
        check(CnFocusProbe.busy()&&CnProbeHost.inputs==1,"a delayed wireless frame must remain observable without another input");
        CnProbeHost.pixels=selected(80);CnProbeHost.serial=2;CnProbeHost.clock=3600;CnProbeHost.tick();
        CnProbeHost.clock=3800;CnProbeHost.tick();check(!CnFocusProbe.busy(),"late frame must still settle normally");
        start();CnProbeHost.clock=8501;CnProbeHost.tick();check(!CnFocusProbe.busy()&&CnProbeHost.inputs==1,"timeout cannot send additional input");
        start();Runnable obsolete=CnProbeHost.pending;CnFocusProbe.cancel();obsolete.run();
        check(CnProbeHost.pending==null&&!CnFocusProbe.busy(),"cancelled callback must not resurrect work");
        start();CnProbeHost.pixels=null;CnProbeHost.serial=2;CnProbeHost.clock=1300;CnProbeHost.tick();
        check(!CnFocusProbe.busy()&&CnProbeHost.inputs==1,"lost frame must cancel without another move");
        reset();CnProbeHost.pixels=selected(40);CnFocusProbe.request(2);check(CnProbeHost.inputs==0,"unsupported input must be rejected");
        reset();CnProbeHost.pixels=selected(40);
        CnProbeHost.onFrame=new Runnable(){public void run(){CnFocusProbe.cancel();}};
        CnFocusProbe.request(1);check(CnProbeHost.inputs==0&&!CnFocusProbe.busy(),"cancellation during capture must prevent publication and input");
        reset();CnProbeHost.pixels=selected(40);CnProbeHost.blocked=true;CnFocusProbe.request(1);
        check(CnProbeHost.inputs==0,"queued input must prevent probe startup");
        start();CnFocusProbe.cancel();CnProbeHost.deliver();check(CnProbeHost.deliveries==0,"cancelled queued report must not reach transport");
        reset();CnProbeHost.pixels=selected(40);CnProbeHost.failFrame=true;CnFocusProbe.request(1);
        check(CnProbeHost.inputs==0&&!CnFocusProbe.busy(),"capture allocation failure must not crash or send input");
        start();CnProbeHost.failFrame=true;CnProbeHost.serial=2;CnProbeHost.clock=1300;CnProbeHost.tick();
        check(!CnFocusProbe.busy(),"analysis-frame allocation failure must cancel safely");
        reset();CnProbeHost.pixels=selected(40);Result result=new Result();
        check(CnFocusProbe.request(1,result),"navigation must be able to start one observed step");
        CnProbeHost.pixels=selected(80);CnProbeHost.serial=2;CnProbeHost.clock=1300;CnProbeHost.tick();
        CnProbeHost.clock=1500;CnProbeHost.tick();
        check(result.count==1 && result.from[1]==40 && result.to[1]==80,"observed step must return actual old and new focus");
        reset();CnProbeHost.pixels=selected(40);result=new Result();CnFocusProbe.request(1,result);
        CnProbeHost.clock=8501;CnProbeHost.tick();
        check(result.count==1 && result.from==null && result.to==null,"timeout must report an unknown step rather than inventing position");
        reset();CnProbeHost.pixels=selected(40);result=new Result();CnFocusProbe.request(1,result);
        Runnable late=CnProbeHost.pending;CnFocusProbe.cancel();late.run();
        check(result.count==0,"external cancellation must not continue a navigation path");
        start();CnProbeHost.pixels=selected(80);CnProbeHost.serial=2;CnProbeHost.clock=1300;CnProbeHost.tick();
        CnProbeHost.renderGeneration++;CnProbeHost.pixels=selected(120);CnProbeHost.clock=1500;CnProbeHost.tick();
        check(!CnFocusProbe.busy()&&!CnProbeHost.last.contains("rect="),"reused frame serial on a new texture cannot confirm cached old focus");
        reset();CnProbeHost.pixels=selected(40);
        CnProbeHost.onFrame=new Runnable(){public void run(){CnProbeHost.renderGeneration++;}};
        CnFocusProbe.request(1);check(CnProbeHost.inputs==0,"texture replacement during baseline capture must send no input");
        System.out.println("PASS: focus probe freshness, render generation, queue ownership, cancellation, allocation, timeout and observed-step contracts");
    }
}
