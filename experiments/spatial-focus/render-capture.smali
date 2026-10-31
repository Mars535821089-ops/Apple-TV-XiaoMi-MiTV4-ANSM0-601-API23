
# Reads this app's existing video texture into bounded transient arrays only.
.method public static captureProbeFrame()[I
 .locals 10
 const/4 v8,0x0
 :try_start
 sget-object v0,Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
 if-eqz v0,:empty
 invoke-virtual {v0},Landroid/view/View;->hasWindowFocus()Z
 move-result v1
 if-eqz v1,:empty
 invoke-virtual {v0},Landroid/view/View;->isShown()Z
 move-result v1
 if-eqz v1,:empty
 invoke-virtual {v0},Landroid/view/TextureView;->isAvailable()Z
 move-result v1
 if-eqz v1,:empty
 invoke-static {},Lai/rplay/carcast/SettingsActivity;->g()Z
 move-result v1
 if-eqz v1,:empty
 const/16 v1,0x140
 const/16 v2,0xb4
 invoke-virtual {v0,v1,v2},Landroid/view/TextureView;->getBitmap(II)Landroid/graphics/Bitmap;
 move-result-object v8
 if-eqz v8,:empty
 move-object v0,v8
 const v1,0xe100
 new-array v1,v1,[I
 const/4 v2,0x0
 const/16 v3,0x140
 const/4 v4,0x0
 const/4 v5,0x0
 const/16 v6,0x140
 const/16 v7,0xb4
 invoke-virtual/range {v0 .. v7},Landroid/graphics/Bitmap;->getPixels([IIIIIII)V
 invoke-virtual {v8},Landroid/graphics/Bitmap;->recycle()V
 return-object v1
 :try_end
 .catch Ljava/lang/RuntimeException; {:try_start .. :try_end} :failed
 .catch Ljava/lang/OutOfMemoryError; {:try_start .. :try_end} :failed
 :failed
 move-exception v9
 if-eqz v8,:empty
 invoke-virtual {v8},Landroid/graphics/Bitmap;->recycle()V
 :empty
 const/4 v0,0x0
 return-object v0
.end method
.method public static captureProbeVersion()J
 .locals 2
 sget-object v0,Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
 if-eqz v0,:empty
 iget-wide v0,v0,Lai/rplay/carcast/CnRender;->frames:J
 return-wide v0
 :empty
 const-wide/16 v0,-0x1
 return-wide v0
.end method
