import ai.rplay.carcast.CnSpatialPath;

public final class SpatialPathTest {
    private static int[] r(int x,int y){return new int[]{x,y,x+40,y+40};}
    private static void check(int got,int want,String label){if(got!=want)throw new AssertionError(label+": expected "+want+", got "+got);}
    public static void main(String[] args){
        int[] music=r(120,20),maps=r(185,20),messages=r(250,20),playing=r(55,94),lexus=r(120,94);
        CnSpatialPath p=new CnSpatialPath(20);
        check(p.observe(music,maps),0,"Down must not select right-hand item");
        check(p.observe(maps,messages),0,"Down keeps looking within row");
        check(p.observe(messages,playing),0,"Down rejects wrong column");
        check(p.observe(playing,lexus),1,"Down reaches same column");
        p=new CnSpatialPath(19);
        check(p.observe(lexus,playing),0,"Up must not move left");
        check(p.observe(playing,messages),0,"Up rejects wrong column");
        check(p.observe(messages,maps),0,"Up keeps looking for source column");
        check(p.observe(maps,music),1,"Up reaches same column");
        p=new CnSpatialPath(22);check(p.observe(r(60,5),r(90,5)),1,"Right reaches adjacent tab");
        p=new CnSpatialPath(21);check(p.observe(r(90,5),r(60,5)),1,"Left reaches adjacent tab");
        int[] row1={38,27,313,55},row2={38,55,313,83};
        p=new CnSpatialPath(20);check(p.observe(row1,row2),1,"Down list row");
        p=new CnSpatialPath(19);check(p.observe(row2,row1),1,"Up list row");
        p=new CnSpatialPath(22);check(p.observe(messages,playing),2,"Right must not jump into next row");
        check(p.wheel(),-1,"rollback reverses wheel");
        check(p.observe(playing,messages),3,"rollback verifies exact source");
        p=new CnSpatialPath(22);p.observe(messages,playing);
        check(p.observe(playing,maps),4,"non-invertible rollback stops immediately");
        p=new CnSpatialPath(20);p.observe(music,maps);
        check(p.observe(maps,music),4,"same coordinates after a forward cycle cannot prove original control identity");
        p=new CnSpatialPath(20);check(p.observe(music,maps),0,"begin path");
        check(p.observe(playing,lexus),4,"unexpected old focus invalidates path");
        p=new CnSpatialPath(20);int[] old=r(40,40);
        for(int i=1;i<=12;i++){int[] next=r(40+i*15,40);check(p.observe(old,next),i==12?2:0,"bounded search "+i);old=next;}
        p=new CnSpatialPath(20);check(p.observe(null,music),4,"unknown source stops");
        p=new CnSpatialPath(20);check(p.observe(music,music),4,"unconfirmed move stops");
        System.out.println("PASS: spatial directions, beam alignment, bounded search and verified rollback");
    }
}
