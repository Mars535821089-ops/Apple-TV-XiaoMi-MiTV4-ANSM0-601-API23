package ai.rplay.carcast;

/** Candidate detector for selected regions in dark CarPlay frames.
 * All arrays are transient. Uncertain or unsupported changes return null.
 */
public final class CnFocusGeometry {
    private CnFocusGeometry() {}

    private static int luma(int color) {
        return (((color >>> 16) & 255)*77 + ((color >>> 8) & 255)*150 + (color & 255)*29) >>> 8;
    }

    /** Returns left, top, exclusive right/bottom, confidence, changed pixels. */
    public static int[] analyze(int[] before, int[] after, int width, int height) {
        return analyze(before,after,width,height,null);
    }
    public static int[] analyze(int[] before, int[] after, int width, int height, int[] stats) {
        if(stats!=null) java.util.Arrays.fill(stats,0);
        if(before==null || after==null || width<40 || height<30 || width>640 || height>360
                || before.length!=width*height || after.length!=before.length) return null;
        int left=width/10, changed=0, area=(width-left)*height, maskCount=0;
        byte[] mask=new byte[before.length];
        for(int y=0;y<height;y++) for(int x=left;x<width;x++) {
            int i=y*width+x, old=luma(before[i]), now=luma(after[i]);
            if(Math.abs(now-old)>=28) changed++;
            int c=after[i], r=(c>>>16)&255, g=(c>>>8)&255, b=c&255;
            int spread=Math.max(r,Math.max(g,b))-Math.min(r,Math.min(g,b));
            if(stats!=null && stats.length>=24 && (c>>>24)>=128 && now-old>=20 && spread<=40) stats[16+Math.min(7,now/32)]++;
            if((c>>>24)>=128 && now>=130 && now-old>=35 && spread<=40) {mask[i]=1;maskCount++;}
        }
        if(stats!=null) { stats[0]=changed; if(stats.length>=16) stats[8]=maskCount; }
        if(changed<16 || changed*100L>area*45L) return null;
        int[] queue=new int[before.length];
        int best=0, second=0, bestL=0,bestT=0,bestR=0,bestB=0, bestFill=0;
        for(int start=0;start<mask.length;start++) {
            if(mask[start]!=1) continue;
            int head=0,tail=1,n=0,l=width,t=height,r=0,b=0;
            queue[0]=start; mask[start]=2;
            while(head<tail) {
                int i=queue[head++],y=i/width,x=i-y*width;
                n++; l=Math.min(l,x);r=Math.max(r,x+1);t=Math.min(t,y);b=Math.max(b,y+1);
                for(int dy=-1;dy<=1;dy++) for(int dx=-1;dx<=1;dx++) {
                    if(dx==0 && dy==0) continue;
                    int nx=x+dx,ny=y+dy;
                    if(nx<left || nx>=width || ny<0 || ny>=height) continue;
                    int next=ny*width+nx;
                    if(mask[next]==1) {mask[next]=2;queue[tail++]=next;}
                }
            }
            int rect=(r-l)*(b-t);
            if(stats!=null && stats.length>=16 && n>stats[9]) {
                stats[9]=n;stats[10]=l;stats[11]=t;stats[12]=r;stats[13]=b;stats[14]=n*1000/rect;
            }
            int edgeHits=0,perimeter=2*((r-l)+(b-t))-4;
            for(int x=l;x<r;x++) {
                if(mask[t*width+x]==2) edgeHits++;
                if(b-t>1 && mask[(b-1)*width+x]==2) edgeHits++;
            }
            for(int y=t+1;y<b-1;y++) {
                if(mask[y*width+l]==2) edgeHits++;
                if(r-l>1 && mask[y*width+r-1]==2) edgeHits++;
            }
            boolean outline=r-l>=12 && b-t>=12 && edgeHits*100L>=perimeter*40L;
            if(stats!=null && stats.length>=16 && n==stats[9]) stats[15]=edgeHits*1000/Math.max(1,perimeter);
            if(n<16 || r-l<8 || b-t<3 || (n*100L<rect*38L && !outline)) continue;
            if(n>best) {
                second=best;best=n;bestL=l;bestT=t;bestR=r;bestB=b;bestFill=n*1000/rect;
            } else second=Math.max(second,n);
        }
        if(stats!=null) { stats[1]=best;stats[2]=second;stats[3]=bestL;stats[4]=bestT;stats[5]=bestR;stats[6]=bestB;stats[7]=bestFill; }
        if(best==0 || second*100L>=best*70L) return null;
        return new int[]{bestL,bestT,bestR,bestB,bestFill,changed};
    }
}
