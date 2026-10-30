.class public final Lai/rplay/carcast/CnUi;
.super Ljava/lang/Object;
.field private static final words:Ljava/util/HashMap;

.method static constructor <clinit>()V
    .locals 3
    new-instance v0, Ljava/util/HashMap;
    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V
    const-string v1, "Settings"
    const-string v2, "设置"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "General"
    const-string v2, "通用"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Phones"
    const-string v2, "手机"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Phone"
    const-string v2, "手机"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Display"
    const-string v2, "显示"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Car"
    const-string v2, "车辆"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Car logo"
    const-string v2, "车辆图标"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Car name"
    const-string v2, "车辆名称"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Modes"
    const-string v2, "功能模式"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Mirroring"
    const-string v2, "屏幕镜像"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "AirPlay"
    const-string v2, "隔空播放"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Wireless"
    const-string v2, "无线连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Ready to Cast"
    const-string v2, "准备连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Off"
    const-string v2, "未启用"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Connected"
    const-string v2, "已连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Waiting for iPhone"
    const-string v2, "等待 iPhone"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Connect"
    const-string v2, "连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Connect wirelessly"
    const-string v2, "无线连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Add phone"
    const-string v2, "添加手机"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Pair over Bluetooth"
    const-string v2, "通过蓝牙配对"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Set up CarPlay"
    const-string v2, "设置 CarPlay"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Step by step"
    const-string v2, "连接向导"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "🧭  New here? Set up CarPlay step by step"
    const-string v2, "🧭  首次使用？打开 CarPlay 连接向导"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "🧭  Set up CarPlay step by step"
    const-string v2, "🧭  CarPlay 连接向导"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Set up CarPlay step by step"
    const-string v2, "CarPlay 连接向导"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Start"
    const-string v2, "启动"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Stop"
    const-string v2, "停止"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Back"
    const-string v2, "返回"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Next"
    const-string v2, "下一步"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Done"
    const-string v2, "完成"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Close"
    const-string v2, "关闭"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Remove"
    const-string v2, "移除"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Removed"
    const-string v2, "已移除"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Selected"
    const-string v2, "已选择"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap to use"
    const-string v2, "选择使用"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Open CarPlay"
    const-string v2, "打开 CarPlay"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay connected"
    const-string v2, "CarPlay 已连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Mirroring connected"
    const-string v2, "镜像已连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Mirroring the iPhone"
    const-string v2, "正在显示 iPhone 镜像"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "AirPlay from the iPhone"
    const-string v2, "接收 iPhone 隔空播放"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Plug in to start"
    const-string v2, "插入数据线以启动"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "USB cable"
    const-string v2, "USB 数据线"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Bluetooth + Wi-Fi"
    const-string v2, "蓝牙 + Wi-Fi"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "1 · How will the iPhone connect?"
    const-string v2, "1 · 选择 iPhone 连接方式"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "You can use both later; this sets up the one you pick."
    const-string v2, "以后可使用两种方式；现在先设置所选方式。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "2 · Which Wi-Fi should CarPlay use? "
    const-string v2, "2 · 选择 CarPlay 使用的 Wi-Fi "
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "3 · Pair the iPhone"
    const-string v2, "3 · 配对 iPhone"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "4 · Connect"
    const-string v2, "4 · 建立连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "This device's Wi-Fi"
    const-string v2, "电视当前 Wi-Fi"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "This device's Wi-Fi network"
    const-string v2, "使用电视当前 Wi-Fi 网络"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "This device is on “"
    const-string v2, "电视当前连接“"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "The iPhone joins the network this device is on. "
    const-string v2, "iPhone 将使用电视当前连接的网络。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "The iPhone joins “"
    const-string v2, "iPhone 将连接“"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "”, the network this device is on. "
    const-string v2, "”，与电视处于同一网络。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "”: using it is simplest (enter its password once)."
    const-string v2, "”：可直接使用此网络，只需填写一次密码。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Wi-Fi password"
    const-string v2, "Wi-Fi 密码"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Show password"
    const-string v2, "显示密码"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Android can't read a saved network's password, so enter it once."
    const-string v2, "Android 无法读取已保存的网络密码，请在此输入一次。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Enter the Wi-Fi password in Settings (Android cannot read a saved network's password)"
    const-string v2, "请在设置中填写 Wi-Fi 密码（Android 无法读取已保存的密码）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Private hotspot"
    const-string v2, "独立热点"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Mobile hotspot"
    const-string v2, "系统热点"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Wi-Fi Direct"
    const-string v2, "Wi-Fi 直连"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Private hotspot, created by CarCast (nothing to type, no internet)"
    const-string v2, "由 CarCast 创建独立热点，无需填写；不提供互联网。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Mobile hotspot from Android settings (shares internet; enter its name and password)"
    const-string v2, "使用 Android 系统热点，可共享网络；需填写名称和密码。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Wi-Fi Direct, created by CarCast (5 GHz, nothing to type)"
    const-string v2, "由 CarCast 建立 5 GHz Wi-Fi 直连，无需填写。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Wi-Fi Direct needs nothing typed. (To use this device's Wi-Fi network instead, Android must allow Location so CarCast can read the network's name.)"
    const-string v2, "Wi-Fi 直连无需填写信息。使用电视当前 Wi-Fi 时，需允许位置权限以读取网络名称。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "This device creates its own network when you press Start; its name and password are sent to the iPhone automatically. Keep Wi-Fi on."
    const-string v2, "启动后电视会创建独立网络，自动将名称和密码发送至 iPhone。请保持 Wi-Fi 开启。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Turn on the hotspot in Android's Settings → Hotspot & tethering, then enter its name and password here (Android doesn't let apps read them). The iPhone joins it and keeps its internet."
    const-string v2, "先在 Android 设置中开启热点，再在此填写热点名称和密码。iPhone 将加入该热点并使用其网络。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Hotspot name"
    const-string v2, "热点名称"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Hotspot password"
    const-string v2, "热点密码"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Hotspot channel (optional; blank = auto)"
    const-string v2, "热点信道（可选；留空为自动）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Open hotspot settings"
    const-string v2, "打开系统热点设置"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Wi-Fi hand-off"
    const-string v2, "Wi-Fi 切换方式"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Wi-Fi interface (blank = auto)"
    const-string v2, "Wi-Fi 网卡（留空为自动）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "<unknown ssid>"
    const-string v2, "<无法读取网络名称>"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Pair new phone"
    const-string v2, "配对新手机"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Pair new device"
    const-string v2, "配对新设备"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Make this device discoverable"
    const-string v2, "允许附近设备发现电视"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "No paired iPhone yet — tap Pair new phone."
    const-string v2, "尚未配对 iPhone，请选择“配对新手机”。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "None paired"
    const-string v2, "暂无已配对手机"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Looking for phones…"
    const-string v2, "正在查找手机…"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Turn Bluetooth on first"
    const-string v2, "请先开启蓝牙"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Bluetooth is not available"
    const-string v2, "此设备无法使用蓝牙"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Bluetooth scan not allowed"
    const-string v2, "未获准搜索蓝牙设备"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Bluetooth scan permission needed"
    const-string v2, "需要蓝牙搜索权限"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap Start to allow Bluetooth access."
    const-string v2, "请选择“启动”并允许访问蓝牙。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap the phone, then Forget"
    const-string v2, "选择手机后可取消配对"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "1 phone"
    const-string v2, "1 部手机"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, " phones"
    const-string v2, " 部手机"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap Add phone and pick the iPhone, then confirm the code on both. Keep the iPhone's Bluetooth on. Already paired phones are shown below."
    const-string v2, "选择“添加手机”，选中 iPhone，并在两端确认配对码。请保持 iPhone 蓝牙开启；已配对手机显示在下方。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Pair once, then tap Connect — or let the iPhone connect when it's near. Or just plug it in with a USB cable."
    const-string v2, "首次配对后选择“连接”，或让 iPhone 在附近自动连接；也可使用 USB 数据线。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap Connect. On the iPhone, tap Allow / Use CarPlay when asked (only the first time). If nothing happens in 30 s, turn the iPhone's Bluetooth off and on, then try again.\n\nOr connect from the iPhone: Settings → Bluetooth → tap “"
    const-string v2, "选择“连接”，首次连接时在 iPhone 上允许使用 CarPlay。如果30秒内没有响应，请重新开启 iPhone 蓝牙再试。\n\n也可在 iPhone 设置 → 蓝牙中选择“"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "”. CarCast keeps listening while it runs, so CarPlay starts the same way."
    const-string v2, "”。CarCast 运行期间会持续等待连接。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "1. Tap Start below.\n2. Plug the iPhone in with a USB cable.\n3. Allow access on this device, and tap Trust on the iPhone.\n4. CarPlay opens on its own."
    const-string v2, "1. 选择下方“启动”。\n2. 用 USB 数据线连接 iPhone。\n3. 在电视上允许访问，并在 iPhone 上选择“信任”。\n4. CarPlay 将自动打开。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay runs over Wi-Fi once the iPhone connects over Bluetooth."
    const-string v2, "通过蓝牙建立连接后，CarPlay 将通过 Wi-Fi 传输。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "✅ CarPlay is connected — you're done."
    const-string v2, "✅ CarPlay 已连接，设置完成。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay is on another phone"
    const-string v2, "CarPlay 当前正在另一部手机上使用"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay is on the car screen"
    const-string v2, "CarPlay 画面已在接收屏幕显示"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay is running in the background — tap CarPlay to go back"
    const-string v2, "CarPlay 正在后台运行，选择 CarPlay 即可返回。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Plug in your iPhone with a USB cable"
    const-string v2, "请使用 USB 数据线连接 iPhone"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Plug in your iPhone, or tap it below to connect wirelessly"
    const-string v2, "插入 iPhone 数据线，或选择下方手机进行无线连接。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap Start, then plug in your iPhone or connect it wirelessly"
    const-string v2, "选择“启动”，再用数据线或无线方式连接 iPhone。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap Start, then plug in your iPhone to mirror its screen"
    const-string v2, "选择“启动”，再插入 iPhone 数据线以显示镜像。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap Start, then AirPlay from your iPhone"
    const-string v2, "选择“启动”，然后在 iPhone 上使用隔空播放。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap Start, then on the iPhone: Control Center → Screen Mirroring.\nOr plug it in with a USB cable."
    const-string v2, "选择“启动”，再在 iPhone 控制中心选择“屏幕镜像”；也可使用 USB 数据线。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Tap Start, then cast from a DLNA app (BubbleUPnP, iQiyi, Bilibili, Youku…)"
    const-string v2, "选择“启动”，再从爱奇艺、哔哩哔哩、优酷等支持 DLNA 的应用投屏。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay — wired or wireless CarPlay"
    const-string v2, "CarPlay：有线或无线车载界面"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Mirroring — AirPlay screen mirroring, or USB"
    const-string v2, "屏幕镜像：隔空镜像或 USB 镜像"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "AirPlay — videos and music pushed from the iPhone"
    const-string v2, "隔空播放：接收 iPhone 视频与音乐"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "DLNA — casts from Android phones and video apps"
    const-string v2, "DLNA：接收安卓手机与视频应用投屏"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Choose which modes are enabled and appear as tabs on the home screen."
    const-string v2, "选择要启用的功能；启用后会显示在首页。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Receiver name"
    const-string v2, "接收端名称"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Mirroring resolution"
    const-string v2, "镜像分辨率"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "1280 × 720 (lighter on Wi-Fi and the decoder)"
    const-string v2, "1280 × 720（降低网络和解码负担）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Full screen: zoom the mirrored screen and videos to fill (crops the edges)"
    const-string v2, "全屏填充镜像与视频（可能裁剪边缘）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "AirPlay in Mirroring mode (off: USB cable only)"
    const-string v2, "镜像模式允许隔空连接（关闭后仅使用 USB）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "AirPlay password: none"
    const-string v2, "隔空播放密码：未设置"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "AirPlay password: set"
    const-string v2, "隔空播放密码：已设置"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "AirPlay is on as “"
    const-string v2, "隔空播放已启用，名称为“"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "DLNA is on as “"
    const-string v2, "DLNA 已启用，名称为“"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Name, resolution, password and on/off take effect the next time you tap Start."
    const-string v2, "名称、分辨率、密码及开关修改将在下次启动时生效。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "What iPhones show under Screen Mirroring and in the AirPlay menu. Leave blank for “"
    const-string v2, "这是 iPhone 镜像和隔空播放菜单中显示的名称；留空使用“"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "What DLNA apps (BubbleUPnP, iQiyi, Bilibili, Youku…) list among their TVs. Leave blank for “"
    const-string v2, "这是爱奇艺、哔哩哔哩、优酷等投屏列表中显示的名称；留空使用“"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "” — on the iPhone: Control Center → Screen Mirroring, or the AirPlay button in a video or music app."
    const-string v2, "”：请在 iPhone 控制中心选择屏幕镜像，或在视频、音乐应用中选择隔空播放。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "” — on the iPhone: Control Center → Screen Mirroring.\nOr plug it in with a USB cable."
    const-string v2, "”：请在 iPhone 控制中心选择屏幕镜像，或使用 USB 数据线。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "” — pick it in your app's cast / TV list."
    const-string v2, "”：请在应用的投屏列表中选择该名称。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "”. Takes effect the next time you tap Start."
    const-string v2, "”。将在下次启动时生效。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "UPnP AV version"
    const-string v2, "UPnP AV 版本"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "1 — MediaRenderer:1 (most compatible)"
    const-string v2, "1 — MediaRenderer:1（兼容性优先）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "2 — MediaRenderer:2 (still answers version-1 apps)"
    const-string v2, "2 — MediaRenderer:2（兼容版本1应用）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Start at boot (in the selected mode: CarPlay, Mirroring or AirPlay)"
    const-string v2, "开机自启（使用所选 CarPlay、镜像或隔空播放模式）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Allow “Display over other apps” so CarCast can open its screen after boot"
    const-string v2, "请允许“显示在其他应用上层”，以便开机后自动打开 CarCast。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Listen on Wi-Fi/LAN at start (box mode: network senders such as Cafari can connect, no Bluetooth needed)"
    const-string v2, "启动时监听局域网（盒子模式：Cafari 等发送端无需蓝牙即可连接）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Allow CarCast to manage the iPhone's Bluetooth (needed for CarPlay audio)"
    const-string v2, "允许 CarCast 管理 iPhone 蓝牙连接（CarPlay 音频需要）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Release Bluetooth after the Wi-Fi handoff (as a car does)"
    const-string v2, "切换至 Wi-Fi 后释放蓝牙连接（模拟车机行为）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Bluetooth MAC — About device → Bluetooth address (Android hides it from apps)"
    const-string v2, "蓝牙 MAC 地址：见“关于设备 → 蓝牙地址”（Android 不向应用公开）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Car logo set — reconnect the iPhone to see it"
    const-string v2, "车辆图标已设置，重新连接 iPhone 后生效。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Built-in logos…"
    const-string v2, "内置图标…"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Choose image"
    const-string v2, "选择图片"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Could not use that image: "
    const-string v2, "无法使用该图片："
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Label (e.g. GLE 450)"
    const-string v2, "显示名称（例如 GLE 450）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "The name the iPhone shows for this car in CarPlay. Leave blank for “"
    const-string v2, "这是 iPhone 在 CarPlay 中显示的车辆名称；留空使用“"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Shown as the car's app on the CarPlay home screen. Pick a built-in logo, or use your own square image, 256×256 px or larger (PNG with a transparent background looks best); other shapes are center-cropped. Sent to the iPhone at 120, 180 and 256 px. Takes effect on the next connection."
    const-string v2, "车辆图标显示在 CarPlay 首页。可选内置图标，或使用至少256×256像素的正方形图片；推荐透明背景 PNG。将在下次连接时生效。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Driving position"
    const-string v2, "驾驶位置"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Left-hand drive"
    const-string v2, "左舵"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Right-hand drive"
    const-string v2, "右舵"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay puts its dock on the driver's side. Takes effect on the next connection."
    const-string v2, "CarPlay 将侧栏放在驾驶员一侧，下次连接时生效。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Night mode (dark CarPlay; also switches a running session)"
    const-string v2, "夜间模式（深色 CarPlay，当前连接也会切换）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Display resolution"
    const-string v2, "画面分辨率"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Width"
    const-string v2, "宽度"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Height"
    const-string v2, "高度"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Knob only"
    const-string v2, "仅旋钮操作"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "No knob input"
    const-string v2, "不使用旋钮输入"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Video playback (show video while parked)"
    const-string v2, "视频播放（停车时显示视频）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Instrument cluster (CarPlay alt screen — maps / turn card on a second display)"
    const-string v2, "仪表盘副屏（显示地图或转向提示）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay Ultra: the iPhone's gauge cluster, drawn by CarCast with simulated car data (turns on the instrument cluster and vehicle state)"
    const-string v2, "CarPlay Ultra：使用模拟车辆数据绘制 iPhone 仪表盘（同时启用副屏和车辆状态）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Cluster"
    const-string v2, "仪表盘"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Cluster content"
    const-string v2, "仪表盘内容"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "On screen"
    const-string v2, "屏幕内显示"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Map"
    const-string v2, "地图"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Navigation app decides (map + turn card)"
    const-string v2, "由导航应用决定（地图与转向提示）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Turn-by-turn card only"
    const-string v2, "仅逐向导航提示"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Show ETA on the cluster map"
    const-string v2, "在仪表盘地图上显示预计到达时间"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Two cluster streams: map + turn-by-turn card side by side"
    const-string v2, "双副屏：并排显示地图与转向提示"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "CarPlay draws navigation on the cluster (maps, turn cards); applies the next time you tap Start."
    const-string v2, "在副屏上显示导航地图和转向提示；下次启动时生效。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Cluster: resolution (blank = the preset's) and its width on this screen, % of the main screen. Applies the next time you tap Start."
    const-string v2, "设置副屏分辨率（留空使用预设值）以及其占主屏宽度的百分比；下次启动时生效。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Now Playing card (track, artist and artwork from the iPhone, like a car cluster)"
    const-string v2, "正在播放卡片（显示 iPhone 的曲名、歌手和封面）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Vehicle state protocol (Route Sharing · CarPlay Ultra data channel; takes effect on the next connection)"
    const-string v2, "车辆状态协议（路线共享与 CarPlay Ultra 数据通道；下次连接时生效）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Takes effect on the next connection."
    const-string v2, "下次连接时生效。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, " + cluster"
    const-string v2, " + 仪表盘"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Debug options"
    const-string v2, "调试选项"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Developer"
    const-string v2, "开发者"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Match macOS identity (debug: no BT MAC, deviceID C2:A5…, no iAP2 over Wi-Fi)"
    const-string v2, "模拟 macOS 身份（调试选项：不使用蓝牙 MAC 和 Wi-Fi iAP2）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Asset version (1)"
    const-string v2, "资源版本（1）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "SDK (26.0)"
    const-string v2, "SDK（26.0）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Theme asset id (44C9FA31EC)"
    const-string v2, "主题资源 ID（44C9FA31EC）"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Share logs"
    const-string v2, "分享日志"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Send CarCast's log after a failed connect"
    const-string v2, "连接失败时，可手动分享 CarCast 日志。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Permission needed: "
    const-string v2, "需要权限："
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Association unavailable — connecting anyway"
    const-string v2, "无法关联设备，将继续尝试连接"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Not associated — Bluetooth may stay connected and audio stay on the iPhone"
    const-string v2, "设备未关联：蓝牙可能保持连接，声音可能仍由 iPhone 播放。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "VPN not allowed — wired (USB) CarPlay needs it; wireless still works"
    const-string v2, "尚未允许 VPN：USB CarPlay 需要此权限；无线连接仍可使用。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Test build expired"
    const-string v2, "测试版已到期"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "This CarCast test build is more than 90 days old and no longer runs. Install the current build to carry on."
    const-string v2, "此 CarCast 测试版已超过90天有效期，请安装新的官方版本后继续使用。"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "this build expired "
    const-string v2, "此测试版已到期 "
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, " day(s) ago"
    const-string v2, " 天"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "\u2699"
    const-string v2, "设置"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Nothing playing"
    const-string v2, "暂无播放"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v1, "Track info from the iPhone shows here"
    const-string v2, "此处显示 iPhone 正在播放的信息"
    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    sput-object v0, Lai/rplay/carcast/CnUi;->words:Ljava/util/HashMap;
    return-void
.end method

.method public static translate(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;
    .locals 4
    if-eqz p0, :unchanged
    invoke-interface {p0}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;
    move-result-object v0
    sget-object v1, Lai/rplay/carcast/CnUi;->words:Ljava/util/HashMap;
    invoke-virtual {v1, v0}, Ljava/util/HashMap;->get(Ljava/lang/Object;)Ljava/lang/Object;
    move-result-object v2
    if-eqz v2, :fragments
    check-cast v2, Ljava/lang/CharSequence;
    return-object v2
    :fragments
    const-string v2, "Shown as the car's app on the CarPlay home screen. Pick a built-in logo, or use your own square image, 256×256 px or larger (PNG with a transparent background looks best); other shapes are center-cropped. Sent to the iPhone at 120, 180 and 256 px. Takes effect on the next connection."
    const-string v3, "车辆图标显示在 CarPlay 首页。可选内置图标，或使用至少256×256像素的正方形图片；推荐透明背景 PNG。将在下次连接时生效。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap Connect. On the iPhone, tap Allow / Use CarPlay when asked (only the first time). If nothing happens in 30 s, turn the iPhone's Bluetooth off and on, then try again.\n\nOr connect from the iPhone: Settings → Bluetooth → tap “"
    const-string v3, "选择“连接”，首次连接时在 iPhone 上允许使用 CarPlay。如果30秒内没有响应，请重新开启 iPhone 蓝牙再试。\n\n也可在 iPhone 设置 → 蓝牙中选择“"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Turn on the hotspot in Android's Settings → Hotspot & tethering, then enter its name and password here (Android doesn't let apps read them). The iPhone joins it and keeps its internet."
    const-string v3, "先在 Android 设置中开启热点，再在此填写热点名称和密码。iPhone 将加入该热点并使用其网络。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "1. Tap Start below.\n2. Plug the iPhone in with a USB cable.\n3. Allow access on this device, and tap Trust on the iPhone.\n4. CarPlay opens on its own."
    const-string v3, "1. 选择下方“启动”。\n2. 用 USB 数据线连接 iPhone。\n3. 在电视上允许访问，并在 iPhone 上选择“信任”。\n4. CarPlay 将自动打开。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Wi-Fi Direct needs nothing typed. (To use this device's Wi-Fi network instead, Android must allow Location so CarCast can read the network's name.)"
    const-string v3, "Wi-Fi 直连无需填写信息。使用电视当前 Wi-Fi 时，需允许位置权限以读取网络名称。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap Add phone and pick the iPhone, then confirm the code on both. Keep the iPhone's Bluetooth on. Already paired phones are shown below."
    const-string v3, "选择“添加手机”，选中 iPhone，并在两端确认配对码。请保持 iPhone 蓝牙开启；已配对手机显示在下方。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay Ultra: the iPhone's gauge cluster, drawn by CarCast with simulated car data (turns on the instrument cluster and vehicle state)"
    const-string v3, "CarPlay Ultra：使用模拟车辆数据绘制 iPhone 仪表盘（同时启用副屏和车辆状态）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "This device creates its own network when you press Start; its name and password are sent to the iPhone automatically. Keep Wi-Fi on."
    const-string v3, "启动后电视会创建独立网络，自动将名称和密码发送至 iPhone。请保持 Wi-Fi 开启。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Cluster: resolution (blank = the preset's) and its width on this screen, % of the main screen. Applies the next time you tap Start."
    const-string v3, "设置副屏分辨率（留空使用预设值）以及其占主屏宽度的百分比；下次启动时生效。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Pair once, then tap Connect — or let the iPhone connect when it's near. Or just plug it in with a USB cable."
    const-string v3, "首次配对后选择“连接”，或让 iPhone 在附近自动连接；也可使用 USB 数据线。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "This CarCast test build is more than 90 days old and no longer runs. Install the current build to carry on."
    const-string v3, "此 CarCast 测试版已超过90天有效期，请安装新的官方版本后继续使用。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Listen on Wi-Fi/LAN at start (box mode: network senders such as Cafari can connect, no Bluetooth needed)"
    const-string v3, "启动时监听局域网（盒子模式：Cafari 等发送端无需蓝牙即可连接）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Vehicle state protocol (Route Sharing · CarPlay Ultra data channel; takes effect on the next connection)"
    const-string v3, "车辆状态协议（路线共享与 CarPlay Ultra 数据通道；下次连接时生效）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "” — on the iPhone: Control Center → Screen Mirroring, or the AirPlay button in a video or music app."
    const-string v3, "”：请在 iPhone 控制中心选择屏幕镜像，或在视频、音乐应用中选择隔空播放。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap Start, then on the iPhone: Control Center → Screen Mirroring.\nOr plug it in with a USB cable."
    const-string v3, "选择“启动”，再在 iPhone 控制中心选择“屏幕镜像”；也可使用 USB 数据线。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay draws navigation on the cluster (maps, turn cards); applies the next time you tap Start."
    const-string v3, "在副屏上显示导航地图和转向提示；下次启动时生效。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "What DLNA apps (BubbleUPnP, iQiyi, Bilibili, Youku…) list among their TVs. Leave blank for “"
    const-string v3, "这是爱奇艺、哔哩哔哩、优酷等投屏列表中显示的名称；留空使用“"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Enter the Wi-Fi password in Settings (Android cannot read a saved network's password)"
    const-string v3, "请在设置中填写 Wi-Fi 密码（Android 无法读取已保存的密码）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "” — on the iPhone: Control Center → Screen Mirroring.\nOr plug it in with a USB cable."
    const-string v3, "”：请在 iPhone 控制中心选择屏幕镜像，或使用 USB 数据线。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Mobile hotspot from Android settings (shares internet; enter its name and password)"
    const-string v3, "使用 Android 系统热点，可共享网络；需填写名称和密码。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "What iPhones show under Screen Mirroring and in the AirPlay menu. Leave blank for “"
    const-string v3, "这是 iPhone 镜像和隔空播放菜单中显示的名称；留空使用“"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay puts its dock on the driver's side. Takes effect on the next connection."
    const-string v3, "CarPlay 将侧栏放在驾驶员一侧，下次连接时生效。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Now Playing card (track, artist and artwork from the iPhone, like a car cluster)"
    const-string v3, "正在播放卡片（显示 iPhone 的曲名、歌手和封面）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Name, resolution, password and on/off take effect the next time you tap Start."
    const-string v3, "名称、分辨率、密码及开关修改将在下次启动时生效。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Instrument cluster (CarPlay alt screen — maps / turn card on a second display)"
    const-string v3, "仪表盘副屏（显示地图或转向提示）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Bluetooth MAC — About device → Bluetooth address (Android hides it from apps)"
    const-string v3, "蓝牙 MAC 地址：见“关于设备 → 蓝牙地址”（Android 不向应用公开）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Match macOS identity (debug: no BT MAC, deviceID C2:A5…, no iAP2 over Wi-Fi)"
    const-string v3, "模拟 macOS 身份（调试选项：不使用蓝牙 MAC 和 Wi-Fi iAP2）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap Start, then cast from a DLNA app (BubbleUPnP, iQiyi, Bilibili, Youku…)"
    const-string v3, "选择“启动”，再从爱奇艺、哔哩哔哩、优酷等支持 DLNA 的应用投屏。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Full screen: zoom the mirrored screen and videos to fill (crops the edges)"
    const-string v3, "全屏填充镜像与视频（可能裁剪边缘）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Not associated — Bluetooth may stay connected and audio stay on the iPhone"
    const-string v3, "设备未关联：蓝牙可能保持连接，声音可能仍由 iPhone 播放。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "”. CarCast keeps listening while it runs, so CarPlay starts the same way."
    const-string v3, "”。CarCast 运行期间会持续等待连接。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Allow “Display over other apps” so CarCast can open its screen after boot"
    const-string v3, "请允许“显示在其他应用上层”，以便开机后自动打开 CarCast。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Allow CarCast to manage the iPhone's Bluetooth (needed for CarPlay audio)"
    const-string v3, "允许 CarCast 管理 iPhone 蓝牙连接（CarPlay 音频需要）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Choose which modes are enabled and appear as tabs on the home screen."
    const-string v3, "选择要启用的功能；启用后会显示在首页。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "The name the iPhone shows for this car in CarPlay. Leave blank for “"
    const-string v3, "这是 iPhone 在 CarPlay 中显示的车辆名称；留空使用“"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "VPN not allowed — wired (USB) CarPlay needs it; wireless still works"
    const-string v3, "尚未允许 VPN：USB CarPlay 需要此权限；无线连接仍可使用。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Start at boot (in the selected mode: CarPlay, Mirroring or AirPlay)"
    const-string v3, "开机自启（使用所选 CarPlay、镜像或隔空播放模式）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Private hotspot, created by CarCast (nothing to type, no internet)"
    const-string v3, "由 CarCast 创建独立热点，无需填写；不提供互联网。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Android can't read a saved network's password, so enter it once."
    const-string v3, "Android 无法读取已保存的网络密码，请在此输入一次。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay runs over Wi-Fi once the iPhone connects over Bluetooth."
    const-string v3, "通过蓝牙建立连接后，CarPlay 将通过 Wi-Fi 传输。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay is running in the background — tap CarPlay to go back"
    const-string v3, "CarPlay 正在后台运行，选择 CarPlay 即可返回。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap Start, then plug in your iPhone or connect it wirelessly"
    const-string v3, "选择“启动”，再用数据线或无线方式连接 iPhone。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Plug in your iPhone, or tap it below to connect wirelessly"
    const-string v3, "插入 iPhone 数据线，或选择下方手机进行无线连接。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Night mode (dark CarPlay; also switches a running session)"
    const-string v3, "夜间模式（深色 CarPlay，当前连接也会切换）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Wi-Fi Direct, created by CarCast (5 GHz, nothing to type)"
    const-string v3, "由 CarCast 建立 5 GHz Wi-Fi 直连，无需填写。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Release Bluetooth after the Wi-Fi handoff (as a car does)"
    const-string v3, "切换至 Wi-Fi 后释放蓝牙连接（模拟车机行为）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Two cluster streams: map + turn-by-turn card side by side"
    const-string v3, "双副屏：并排显示地图与转向提示"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap Start, then plug in your iPhone to mirror its screen"
    const-string v3, "选择“启动”，再插入 iPhone 数据线以显示镜像。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "You can use both later; this sets up the one you pick."
    const-string v3, "以后可使用两种方式；现在先设置所选方式。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "”: using it is simplest (enter its password once)."
    const-string v3, "”：可直接使用此网络，只需填写一次密码。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "2 — MediaRenderer:2 (still answers version-1 apps)"
    const-string v3, "2 — MediaRenderer:2（兼容版本1应用）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "AirPlay — videos and music pushed from the iPhone"
    const-string v3, "隔空播放：接收 iPhone 视频与音乐"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "The iPhone joins the network this device is on. "
    const-string v3, "iPhone 将使用电视当前连接的网络。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "DLNA — casts from Android phones and video apps"
    const-string v3, "DLNA：接收安卓手机与视频应用投屏"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "AirPlay in Mirroring mode (off: USB cable only)"
    const-string v3, "镜像模式允许隔空连接（关闭后仅使用 USB）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "1280 × 720 (lighter on Wi-Fi and the decoder)"
    const-string v3, "1280 × 720（降低网络和解码负担）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Car logo set — reconnect the iPhone to see it"
    const-string v3, "车辆图标已设置，重新连接 iPhone 后生效。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Mirroring — AirPlay screen mirroring, or USB"
    const-string v3, "屏幕镜像：隔空镜像或 USB 镜像"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "”. Takes effect the next time you tap Start."
    const-string v3, "”。将在下次启动时生效。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Association unavailable — connecting anyway"
    const-string v3, "无法关联设备，将继续尝试连接"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "No paired iPhone yet — tap Pair new phone."
    const-string v3, "尚未配对 iPhone，请选择“配对新手机”。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "” — pick it in your app's cast / TV list."
    const-string v3, "”：请在应用的投屏列表中选择该名称。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Send CarCast's log after a failed connect"
    const-string v3, "连接失败时，可手动分享 CarCast 日志。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "🧭  New here? Set up CarPlay step by step"
    const-string v3, "🧭  首次使用？打开 CarPlay 连接向导"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Hotspot channel (optional; blank = auto)"
    const-string v3, "热点信道（可选；留空为自动）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap Start, then AirPlay from your iPhone"
    const-string v3, "选择“启动”，然后在 iPhone 上使用隔空播放。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Video playback (show video while parked)"
    const-string v3, "视频播放（停车时显示视频）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Navigation app decides (map + turn card)"
    const-string v3, "由导航应用决定（地图与转向提示）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "✅ CarPlay is connected — you're done."
    const-string v3, "✅ CarPlay 已连接，设置完成。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "1 — MediaRenderer:1 (most compatible)"
    const-string v3, "1 — MediaRenderer:1（兼容性优先）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "2 · Which Wi-Fi should CarPlay use? "
    const-string v3, "2 · 选择 CarPlay 使用的 Wi-Fi "
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap Start to allow Bluetooth access."
    const-string v3, "请选择“启动”并允许访问蓝牙。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Plug in your iPhone with a USB cable"
    const-string v3, "请使用 USB 数据线连接 iPhone"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Takes effect on the next connection."
    const-string v3, "下次连接时生效。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay — wired or wireless CarPlay"
    const-string v3, "CarPlay：有线或无线车载界面"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "”, the network this device is on. "
    const-string v3, "”，与电视处于同一网络。"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "1 · How will the iPhone connect?"
    const-string v3, "1 · 选择 iPhone 连接方式"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Bluetooth scan permission needed"
    const-string v3, "需要蓝牙搜索权限"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "🧭  Set up CarPlay step by step"
    const-string v3, "🧭  CarPlay 连接向导"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Wi-Fi interface (blank = auto)"
    const-string v3, "Wi-Fi 网卡（留空为自动）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Make this device discoverable"
    const-string v3, "允许附近设备发现电视"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay is on the car screen"
    const-string v3, "CarPlay 画面已在接收屏幕显示"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Set up CarPlay step by step"
    const-string v3, "CarPlay 连接向导"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "This device's Wi-Fi network"
    const-string v3, "使用电视当前 Wi-Fi 网络"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay is on another phone"
    const-string v3, "CarPlay 当前正在另一部手机上使用"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Show ETA on the cluster map"
    const-string v3, "在仪表盘地图上显示预计到达时间"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Theme asset id (44C9FA31EC)"
    const-string v3, "主题资源 ID（44C9FA31EC）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Bluetooth is not available"
    const-string v3, "此设备无法使用蓝牙"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Bluetooth scan not allowed"
    const-string v3, "未获准搜索蓝牙设备"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Tap the phone, then Forget"
    const-string v3, "选择手机后可取消配对"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Could not use that image: "
    const-string v3, "无法使用该图片："
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "AirPlay from the iPhone"
    const-string v3, "接收 iPhone 隔空播放"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Turn Bluetooth on first"
    const-string v3, "请先开启蓝牙"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "AirPlay password: none"
    const-string v3, "隔空播放密码：未设置"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Turn-by-turn card only"
    const-string v3, "仅逐向导航提示"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Open hotspot settings"
    const-string v3, "打开系统热点设置"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "AirPlay password: set"
    const-string v3, "隔空播放密码：已设置"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Mirroring the iPhone"
    const-string v3, "正在显示 iPhone 镜像"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Mirroring resolution"
    const-string v3, "镜像分辨率"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Label (e.g. GLE 450)"
    const-string v3, "显示名称（例如 GLE 450）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Pair over Bluetooth"
    const-string v3, "通过蓝牙配对"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Mirroring connected"
    const-string v3, "镜像已连接"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "3 · Pair the iPhone"
    const-string v3, "3 · 配对 iPhone"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "This device's Wi-Fi"
    const-string v3, "电视当前 Wi-Fi"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "This device is on “"
    const-string v3, "电视当前连接“"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Looking for phones…"
    const-string v3, "正在查找手机…"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Permission needed: "
    const-string v3, "需要权限："
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "this build expired "
    const-string v3, "此测试版已到期 "
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Waiting for iPhone"
    const-string v3, "等待 iPhone"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Connect wirelessly"
    const-string v3, "无线连接"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "The iPhone joins “"
    const-string v3, "iPhone 将连接“"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "AirPlay is on as “"
    const-string v3, "隔空播放已启用，名称为“"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Display resolution"
    const-string v3, "画面分辨率"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Test build expired"
    const-string v3, "测试版已到期"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "CarPlay connected"
    const-string v3, "CarPlay 已连接"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Bluetooth + Wi-Fi"
    const-string v3, "蓝牙 + Wi-Fi"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Asset version (1)"
    const-string v3, "资源版本（1）"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Plug in to start"
    const-string v3, "插入数据线以启动"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Hotspot password"
    const-string v3, "热点密码"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Driving position"
    const-string v3, "驾驶位置"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Right-hand drive"
    const-string v3, "右舵"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Private hotspot"
    const-string v3, "独立热点"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Pair new device"
    const-string v3, "配对新设备"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "DLNA is on as “"
    const-string v3, "DLNA 已启用，名称为“"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "UPnP AV version"
    const-string v3, "UPnP AV 版本"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Built-in logos…"
    const-string v3, "内置图标…"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Left-hand drive"
    const-string v3, "左舵"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Cluster content"
    const-string v3, "仪表盘内容"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Set up CarPlay"
    const-string v3, "设置 CarPlay"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Wi-Fi password"
    const-string v3, "Wi-Fi 密码"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Mobile hotspot"
    const-string v3, "系统热点"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Wi-Fi hand-off"
    const-string v3, "Wi-Fi 切换方式"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "<unknown ssid>"
    const-string v3, "<无法读取网络名称>"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Pair new phone"
    const-string v3, "配对新手机"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Ready to Cast"
    const-string v3, "准备连接"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Show password"
    const-string v3, "显示密码"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Receiver name"
    const-string v3, "接收端名称"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "No knob input"
    const-string v3, "不使用旋钮输入"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Debug options"
    const-string v3, "调试选项"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Step by step"
    const-string v3, "连接向导"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Open CarPlay"
    const-string v3, "打开 CarPlay"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Wi-Fi Direct"
    const-string v3, "Wi-Fi 直连"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Hotspot name"
    const-string v3, "热点名称"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    const-string v2, "Choose image"
    const-string v3, "选择图片"
    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
    move-result-object v0
    return-object v0
    :unchanged
    return-object p0
.end method

.method public static text(Landroid/widget/TextView;Ljava/lang/CharSequence;)V
    .locals 1
    instance-of v0, p0, Landroid/widget/EditText;
    if-nez v0, :raw
    invoke-static {p1}, Lai/rplay/carcast/CnUi;->translate(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;
    move-result-object p1
    :raw
    invoke-virtual {p0, p1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
    return-void
.end method

.method public static hint(Landroid/widget/TextView;Ljava/lang/CharSequence;)V
    .locals 0
    invoke-static {p1}, Lai/rplay/carcast/CnUi;->translate(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;
    move-result-object p1
    invoke-virtual {p0, p1}, Landroid/widget/TextView;->setHint(Ljava/lang/CharSequence;)V
    return-void
.end method

.method public static click(Landroid/view/View;Landroid/view/View$OnClickListener;)V
    .locals 1
    invoke-virtual {p0, p1}, Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V
    if-eqz p1, :done
    const/4 v0, 0x1
    invoke-virtual {p0, v0}, Landroid/view/View;->setFocusable(Z)V
    new-instance v0, Lai/rplay/carcast/CnFocus;
    invoke-direct {v0}, Lai/rplay/carcast/CnFocus;-><init>()V
    invoke-virtual {p0, v0}, Landroid/view/View;->setOnFocusChangeListener(Landroid/view/View$OnFocusChangeListener;)V
    :done
    return-void
.end method
