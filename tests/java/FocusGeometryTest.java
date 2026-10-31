import ai.rplay.carcast.CnFocusGeometry;
import java.util.Arrays;

public final class FocusGeometryTest {
    private static final int W=320, H=180, DARK=0xff202020, LIGHT=0xffeeeeee;
    private static int cases;
    private static int[] frame() { int[] f=new int[W*H]; Arrays.fill(f,DARK); return f; }
    private static void box(int[] f,int l,int t,int r,int b,int color) {
        for(int y=t;y<b;y++) for(int x=l;x<r;x++) f[y*W+x]=color;
    }
    private static void rect(int[] before,int[] after,String name) {
        int[] actual=CnFocusGeometry.analyze(before,after,W,H);
        if(actual==null || actual.length<5 || actual[0]!=80 || actual[1]!=80 || actual[2]!=250 || actual[3]!=102)
            throw new AssertionError(name+": expected [80,80,250,102], got "+Arrays.toString(actual));
        cases++;
    }
    private static void none(int[] before,int[] after,String name) {
        if(CnFocusGeometry.analyze(before,after,W,H)!=null) throw new AssertionError(name+": unsafe focus guess");
        cases++;
    }
    public static void main(String[] args) {
        int[] a=frame(),b=frame(); box(a,80,40,250,62,LIGHT); box(b,80,80,250,102,LIGHT);
        rect(a,b,"adjacent list rows");
        box(b,100,87,140,94,0xff111111); rect(a,b,"text holes in selected row");
        box(a,260,15,310,65,0xffffffff); box(b,260,15,310,65,0xffffffff);
        rect(a,b,"unchanged white icon");
        for(int i=0;i<100;i++) { int x=40+(i*37)%270,y=(i*53)%180; if(y<30) b[y*W+x]=0xffdddddd; }
        rect(a,b,"isolated background noise");
        a=frame(); b=frame(); box(b,0,0,25,20,LIGHT); none(a,b,"sidebar clock");
        none(a,a,"no change");
        b=frame(); box(b,40,0,320,180,LIGHT); none(a,b,"whole-page transition");
        b=frame(); box(b,70,35,250,55,LIGHT); box(b,70,90,250,110,LIGHT);
        none(a,b,"two equally likely controls");
        none(null,b,"missing before frame");
        if(CnFocusGeometry.analyze(new int[2],new int[2],320,180)!=null) throw new AssertionError("invalid dimensions");
        cases++;
        System.out.println("PASS: "+cases+" focus geometry cases");
    }
}
