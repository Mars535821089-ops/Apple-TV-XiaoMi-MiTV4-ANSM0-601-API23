.class public final Lai/rplay/carcast/CnReconnect;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;
.field private static task:Lai/rplay/carcast/CnReconnect;
.field private context:Landroid/content/Context;
.field private handler:Landroid/os/Handler;
.field private attempts:I

.method private constructor <init>(Landroid/content/Context;)V
    .locals 2
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    invoke-virtual {p1}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;
    move-result-object p1
    iput-object p1, p0, Lai/rplay/carcast/CnReconnect;->context:Landroid/content/Context;
    new-instance v0, Landroid/os/Handler;
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
    move-result-object v1
    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
    iput-object v0, p0, Lai/rplay/carcast/CnReconnect;->handler:Landroid/os/Handler;
    return-void
.end method

.method public static start(Landroid/content/Context;)V
    .locals 4
    if-eqz p0, :done
    sget-object v0, Lai/rplay/carcast/CnReconnect;->task:Lai/rplay/carcast/CnReconnect;
    if-nez v0, :done
    new-instance v0, Lai/rplay/carcast/CnReconnect;
    invoke-direct {v0, p0}, Lai/rplay/carcast/CnReconnect;-><init>(Landroid/content/Context;)V
    sput-object v0, Lai/rplay/carcast/CnReconnect;->task:Lai/rplay/carcast/CnReconnect;
    iget-object v1, v0, Lai/rplay/carcast/CnReconnect;->handler:Landroid/os/Handler;
    const-wide/16 v2, 0x3a98
    invoke-virtual {v1, v0, v2, v3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
    :done
    return-void
.end method

.method public static cancel()V
    .locals 3
    sget-object v0, Lai/rplay/carcast/CnReconnect;->task:Lai/rplay/carcast/CnReconnect;
    const/4 v1, 0x0
    sput-object v1, Lai/rplay/carcast/CnReconnect;->task:Lai/rplay/carcast/CnReconnect;
    if-eqz v0, :done
    iget-object v2, v0, Lai/rplay/carcast/CnReconnect;->handler:Landroid/os/Handler;
    invoke-virtual {v2, v0}, Landroid/os/Handler;->removeCallbacks(Ljava/lang/Runnable;)V
    :done
    return-void
.end method

.method public static remember(Landroid/content/Context;Ljava/lang/String;)V
    .locals 2
    if-eqz p1, :done
    invoke-static {p1}, Landroid/bluetooth/BluetoothAdapter;->checkBluetoothAddress(Ljava/lang/String;)Z
    move-result v0
    if-eqz v0, :done
    const-string v0, "carcast"
    const/4 v1, 0x0
    invoke-virtual {p0, v0, v1}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
    move-result-object v0
    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    const-string v1, "cn.reconnect.target"
    invoke-interface {v0, v1, p1}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V
    :done
    return-void
.end method

.method public run()V
    .locals 9
    sget-object v0, Lai/rplay/carcast/CnReconnect;->task:Lai/rplay/carcast/CnReconnect;
    if-ne v0, p0, :done
    sget-object v0, Lai/rplay/carcast/CarPlayService;->A:Lai/rplay/carcast/CarPlayService;
    if-eqz v0, :stop
    sget-boolean v1, Lai/rplay/carcast/CarPlayService;->v:Z
    if-eqz v1, :stop
    const-string v1, "carplay"
    sget-object v2, Lai/rplay/carcast/CarPlayService;->w:Ljava/lang/String;
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v1
    if-eqz v1, :stop
    invoke-static {}, Lai/rplay/carcast/SettingsActivity;->g()Z
    move-result v1
    if-nez v1, :stop
    sget-boolean v1, Lai/rplay/carcast/CarPlayActivity;->h:Z
    if-nez v1, :stop
    iget v1, p0, Lai/rplay/carcast/CnReconnect;->attempts:I
    const/4 v2, 0x6
    if-ge v1, v2, :stop
    :try_start
    invoke-static {}, Landroid/bluetooth/BluetoothAdapter;->getDefaultAdapter()Landroid/bluetooth/BluetoothAdapter;
    move-result-object v1
    if-eqz v1, :stop
    invoke-virtual {v1}, Landroid/bluetooth/BluetoothAdapter;->isEnabled()Z
    move-result v2
    if-eqz v2, :stop
    iget-object v2, p0, Lai/rplay/carcast/CnReconnect;->context:Landroid/content/Context;
    const-string v3, "carcast"
    const/4 v4, 0x0
    invoke-virtual {v2, v3, v4}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
    move-result-object v3
    const-string v5, "cn.reconnect.target"
    const/4 v6, 0x0
    invoke-interface {v3, v5, v6}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    move-result-object v3
    if-nez v3, :connect
    invoke-virtual {v1}, Landroid/bluetooth/BluetoothAdapter;->getBondedDevices()Ljava/util/Set;
    move-result-object v1
    invoke-interface {v1}, Ljava/util/Set;->iterator()Ljava/util/Iterator;
    move-result-object v1
    :phones
    invoke-interface {v1}, Ljava/util/Iterator;->hasNext()Z
    move-result v5
    if-eqz v5, :found
    invoke-interface {v1}, Ljava/util/Iterator;->next()Ljava/lang/Object;
    move-result-object v5
    check-cast v5, Landroid/bluetooth/BluetoothDevice;
    invoke-virtual {v5}, Landroid/bluetooth/BluetoothDevice;->getName()Ljava/lang/String;
    move-result-object v7
    if-eqz v7, :phones
    const-string v8, "iPhone"
    invoke-virtual {v7, v8}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v7
    if-eqz v7, :phones
    if-nez v3, :stop
    invoke-virtual {v5}, Landroid/bluetooth/BluetoothDevice;->getAddress()Ljava/lang/String;
    move-result-object v3
    goto :phones
    :found
    if-eqz v3, :stop
    invoke-static {v2, v3}, Lai/rplay/carcast/CnReconnect;->remember(Landroid/content/Context;Ljava/lang/String;)V
    :connect
    new-instance v1, Landroid/content/Intent;
    const-class v5, Lai/rplay/carcast/CarPlayService;
    invoke-direct {v1, v2, v5}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
    const-string v5, "ai.rplay.carcast.CONNECT"
    invoke-virtual {v1, v5}, Landroid/content/Intent;->setAction(Ljava/lang/String;)Landroid/content/Intent;
    const-string v5, "address"
    invoke-virtual {v1, v5, v3}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;
    invoke-static {v2, v1}, Lai/rplay/carcast/CarPlayService;->p(Landroid/content/Context;Landroid/content/Intent;)V
    const-string v1, "CnReconnect"
    const-string v2, "Retrying the authorized paired iPhone"
    invoke-static {v1, v2}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
    :try_end
    .catch Ljava/lang/RuntimeException; {:try_start .. :try_end} :failed
    goto :later
    :failed
    move-exception v1
    const-string v1, "CnReconnect"
    const-string v2, "Connection retry unavailable; preserving Bluetooth settings"
    invoke-static {v1, v2}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;)I
    :later
    sget-object v0, Lai/rplay/carcast/CnReconnect;->task:Lai/rplay/carcast/CnReconnect;
    if-ne v0, p0, :done
    iget v1, p0, Lai/rplay/carcast/CnReconnect;->attempts:I
    add-int/lit8 v1, v1, 0x1
    iput v1, p0, Lai/rplay/carcast/CnReconnect;->attempts:I
    const/4 v2, 0x3
    invoke-static {v1, v2}, Ljava/lang/Math;->min(II)I
    move-result v1
    const/16 v2, 0x3a98
    shl-int/2addr v2, v1
    int-to-long v2, v2
    iget-object v0, p0, Lai/rplay/carcast/CnReconnect;->handler:Landroid/os/Handler;
    invoke-virtual {v0, p0, v2, v3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
    return-void
    :stop
    sget-object v0, Lai/rplay/carcast/CnReconnect;->task:Lai/rplay/carcast/CnReconnect;
    if-ne v0, p0, :done
    const/4 v0, 0x0
    sput-object v0, Lai/rplay/carcast/CnReconnect;->task:Lai/rplay/carcast/CnReconnect;
    :done
    return-void
.end method
