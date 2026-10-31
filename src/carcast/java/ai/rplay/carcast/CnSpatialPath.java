package ai.rplay.carcast;

/** Pure bounded path policy. No frame, Android or transport side effects. */
public final class CnSpatialPath {
    // 0 continue, 1 reached, 2 rollback, 3 restored, 4 uncertain/abort.
    private final int direction, sign;
    private final int[][] path=new int[13][];
    private int count;
    private boolean rolling,done;
    public CnSpatialPath(int direction) {
        if(direction<19 || direction>22) throw new IllegalArgumentException("direction");
        this.direction=direction;sign=direction==19 || direction==21?-1:1;
    }
    private static boolean valid(int[] r) {
        return r!=null && r.length>=4 && r[0]>=32 && r[1]>=0 && r[2]<=320 && r[3]<=180
            && r[2]>r[0] && r[3]>r[1];
    }
    private static boolean same(int[] a,int[] b) {
        if(!valid(a)||!valid(b)) return false;
        for(int i=0;i<4;i++) if(Math.abs(a[i]-b[i])>3) return false;
        return true;
    }
    private static int[] copy(int[] r){return new int[]{r[0],r[1],r[2],r[3]};}
    private int finish(int result){done=true;return result;}
    public int wheel() { return rolling?-sign:sign; }
    public int observe(int[] from,int[] to) {
        if(done || !valid(from) || !valid(to) || same(from,to)) return finish(4);
        if(path[0]==null) path[0]=copy(from);
        if(!same(from,path[count])) return finish(4);
        if(rolling) {
            if(count==0 || !same(to,path[count-1])) return finish(4);
            return --count==0?finish(3):2;
        }
        if(same(to,path[0])) return finish(4);
        path[++count]=copy(to);
        int[] origin=path[0];
        boolean horizontal=direction>=21;
        int axis=horizontal?0:1, cross=horizontal?1:0;
        int delta=((to[axis]+to[axis+2])-(origin[axis]+origin[axis+2]))*sign;
        boolean beam=Math.min(to[cross+2],origin[cross+2])-Math.max(to[cross],origin[cross])>=4;
        if(delta>8 && beam) return finish(1);
        // Never cross into another row to satisfy a horizontal key, or wrap
        // behind the requested vertical half-plane while searching a column.
        if(count>=12 || delta<-8 || (horizontal && !beam)) {rolling=true;return 2;}
        return 0;
    }
}
