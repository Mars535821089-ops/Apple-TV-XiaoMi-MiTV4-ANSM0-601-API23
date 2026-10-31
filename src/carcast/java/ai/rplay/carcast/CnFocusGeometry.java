package ai.rplay.carcast;

/** Candidate detector for selected regions in dark CarPlay frames.
 * All arrays are transient. Uncertain or unsupported changes return null.
 */
public final class CnFocusGeometry {
    private CnFocusGeometry() {}
    /** Conservative continuity guard, not a semantic button/page identity. */
    public static boolean sameScene(int[] before,int[] after,int width,int height,int[] from,int[] to) {
        if(before==null || after==null || before.length!=width*height || after.length!=before.length
            || from==null || to==null || from.length<4 || to.length<4) return false;
        int changed=0,area=0;
        for(int y=0;y<height;y++)for(int x=width/10;x<width;x++) {
            if(inside(x,y,from)||inside(x,y,to))continue;
            area++;int i=y*width+x;
            if(Math.abs(luma(before[i])-luma(after[i]))>=28)changed++;
        }
        return area>0 && changed*100L<=area*4L;
    }
    private static boolean inside(int x,int y,int[] r){return x>=r[0]-4 && x<r[2]+4 && y>=r[1]-4 && y<r[3]+4;}

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
        int paperBefore=0,paperAfter=0;
        for(int y=0;y<height;y++)for(int x=left;x<width;x++) {
            int i=y*width+x;
            if(paper(before[i]))paperBefore++;
            if(paper(after[i]))paperAfter++;
        }
        boolean lightTheme=paperBefore*100L>area*60L && paperAfter*100L>area*60L;
        byte[] mask=new byte[before.length];
        for(int y=0;y<height;y++) for(int x=left;x<width;x++) {
            int i=y*width+x, old=luma(before[i]), now=luma(after[i]);
            if(Math.abs(now-old)>=28) changed++;
            int c=after[i], r=(c>>>16)&255, g=(c>>>8)&255, b=c&255;
            int spread=Math.max(r,Math.max(g,b))-Math.min(r,Math.min(g,b));
            int delta=lightTheme?old-now:now-old;
            if(stats!=null && stats.length>=24 && (c>>>24)>=128 && delta>=20 && spread<=40) stats[16+Math.min(7,now/32)]++;
            if((c>>>24)>=128 && (lightTheme?now<=110:now>=130) && delta>=35 && spread<=40) {mask[i]=1;maskCount++;}
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
            boolean ring=false;int w=r-l,h=b-t;
            if(w>=12 && h>=12 && w<=120 && h<=120 && w<=2*h && h<=2*w
                    && n*100L>=rect*8L && n*100L<=rect*55L) {
                int sectors=0,band=0;long radius=(long)w*h;radius*=radius;
                for(int j=0;j<tail;j++) {
                    int i=queue[j],y=i/width,x=i-y*width;
                    long dx=(long)(2*x-l-r+1)*h,dy=(long)(2*y-t-b+1)*w;
                    long d=dx*dx+dy*dy;
                    if(d*100>=radius*45 && d*100<=radius*140) {
                        band++;int quadrant=(dx>=0?0:2)+(dy>=0?0:1);
                        sectors|=1<<(quadrant*2+(Math.abs(dx)>=Math.abs(dy)?0:1));
                    }
                }
                ring=sectors==255 && band*100L>=n*70L;
            }
            if(stats!=null && stats.length>=16 && n==stats[9]) stats[15]=edgeHits*1000/Math.max(1,perimeter);
            if(n<16 || r-l<8 || b-t<3 || (n*100L<rect*38L && !outline && !ring)) continue;
            if(n>best) {
                second=best;best=n;bestL=l;bestT=t;bestR=r;bestB=b;bestFill=n*1000/rect;
            } else second=Math.max(second,n);
        }
        if(stats!=null) { stats[1]=best;stats[2]=second;stats[3]=bestL;stats[4]=bestT;stats[5]=bestR;stats[6]=bestB;stats[7]=bestFill; }
        if(best==0 || second*100L>=best*70L) return null;
        return new int[]{bestL,bestT,bestR,bestB,bestFill,changed};
    }
    private static boolean paper(int c) {
        int r=(c>>>16)&255,g=(c>>>8)&255,b=c&255;
        return (c>>>24)>=128 && luma(c)>=180
            && Math.max(r,Math.max(g,b))-Math.min(r,Math.min(g,b))<=40;
    }
}
