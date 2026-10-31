import ai.rplay.carcast.*;
import java.util.Arrays;

public final class SpatialNavigatorTest {
    static int[] frame(int x,int y){int[] a=new int[320*180];Arrays.fill(a,0xff202020);for(int j=y;j<y+30;j++)for(int i=x;i<x+40;i++)a[j*320+i]=0xffeeeeee;return a;}
    static void check(boolean ok,String label){if(!ok)throw new AssertionError(label);}
    static void reset(int x,int y){CnSpatialNavigator.cancel();CnFocusProbe.cancel();CnProbeHost.reset();CnProbeHost.pixels=frame(x,y);}
    static void move(int x,int y){CnProbeHost.pixels=frame(x,y);CnProbeHost.serial++;CnProbeHost.clock+=300;CnProbeHost.tick();CnProbeHost.clock+=200;CnProbeHost.tick();}
    public static void main(String[] args){
        reset(120,20);CnSpatialNavigator.request(20);
        check(CnSpatialNavigator.busy()&&CnProbeHost.inputs==1,"Down must start one observed step");
        CnSpatialNavigator.request(22);check(CnProbeHost.inputs==1,"busy direction must not add input backlog");
        move(185,20);check(CnSpatialNavigator.busy()&&CnProbeHost.inputs==2,"right-hand intermediate item cannot satisfy Down");
        move(250,20);move(55,94);move(120,94);
        check(!CnSpatialNavigator.busy()&&!CnSpatialNavigator.uncertain()&&CnProbeHost.inputs==4,"Down must finish at same-column item");
        reset(250,20);CnSpatialNavigator.request(22);move(55,94);
        check(CnSpatialNavigator.busy()&&CnProbeHost.lastWheel==-1,"row wrap must start verified rollback");
        move(250,20);check(!CnSpatialNavigator.busy()&&!CnSpatialNavigator.uncertain(),"verified rollback finishes at source");
        reset(120,20);CnSpatialNavigator.request(20);CnProbeHost.clock+=2301;CnProbeHost.tick();
        check(!CnSpatialNavigator.busy()&&CnSpatialNavigator.uncertain()&&CnProbeHost.inputs==1,"unknown movement cannot issue blind rollback");
        CnSpatialNavigator.request(22);check(CnProbeHost.inputs==1,"unknown focus requires explicit cancel before another direction");
        CnSpatialNavigator.stop();check(CnSpatialNavigator.uncertain(),"volume or unrelated keys cannot unlock uncertain Select");
        reset(120,20);CnSpatialNavigator.request(20);Runnable late=CnProbeHost.pending;
        CnSpatialNavigator.cancel();late.run();check(!CnSpatialNavigator.busy()&&CnProbeHost.inputs==1,"background cancellation must not start another step");
        reset(120,20);CnSpatialNavigator.request(20);move(185,20);late=CnProbeHost.pending;
        CnSpatialNavigator.cancel();late.run();check(CnProbeHost.inputs==2,"cancelling intermediate path cannot roll back in background");
        reset(120,20);CnSpatialNavigator.request(20);CnSpatialNavigator.stop();
        check(!CnSpatialNavigator.busy()&&CnSpatialNavigator.uncertain(),"unrelated key stops movement without claiming a known position");
        System.out.println("PASS: observed spatial coordination, busy gating, safe failure and background cancellation");
    }
}
