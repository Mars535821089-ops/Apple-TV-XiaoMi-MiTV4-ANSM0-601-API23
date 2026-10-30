"""Local UI-only Chinese and D-pad adaptation; do not change native/protocol code."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).parent / 'carcast-cn-src'
PKG = ROOT / 'smali/ai/rplay/carcast'
TEXT = {
    '⚙':'设置','Nothing playing':'暂无播放',
    'Track info from the iPhone shows here':'此处显示 iPhone 正在播放的信息',
    'Settings':'设置','General':'通用','Phones':'手机','Phone':'手机','Display':'显示',
    'Car':'车辆','Car logo':'车辆图标','Car name':'车辆名称','Modes':'功能模式',
    'Mirroring':'屏幕镜像','AirPlay':'隔空播放','Wireless':'无线连接',
    'Ready to Cast':'准备连接','Off':'未启用','Connected':'已连接',
    'Waiting for iPhone':'等待 iPhone','Connect':'连接','Connect wirelessly':'无线连接',
    'Add phone':'添加手机','Pair over Bluetooth':'通过蓝牙配对',
    'Set up CarPlay':'设置 CarPlay','Step by step':'连接向导',
    '🧭  New here? Set up CarPlay step by step':'🧭  首次使用？打开 CarPlay 连接向导',
    '🧭  Set up CarPlay step by step':'🧭  CarPlay 连接向导',
    'Set up CarPlay step by step':'CarPlay 连接向导',
    'Start':'启动','Stop':'停止','Back':'返回','Next':'下一步','Done':'完成',
    'Close':'关闭','Remove':'移除','Removed':'已移除','Selected':'已选择',
    'Tap to use':'选择使用','Open CarPlay':'打开 CarPlay','CarPlay connected':'CarPlay 已连接',
    'Mirroring connected':'镜像已连接','Mirroring the iPhone':'正在显示 iPhone 镜像',
    'AirPlay from the iPhone':'接收 iPhone 隔空播放','Plug in to start':'插入数据线以启动',
    'USB cable':'USB 数据线','Bluetooth + Wi-Fi':'蓝牙 + Wi-Fi',
    '1 · How will the iPhone connect?':'1 · 选择 iPhone 连接方式',
    'You can use both later; this sets up the one you pick.':'以后可使用两种方式；现在先设置所选方式。',
    '2 · Which Wi-Fi should CarPlay use? ':'2 · 选择 CarPlay 使用的 Wi-Fi ',
    '3 · Pair the iPhone':'3 · 配对 iPhone','4 · Connect':'4 · 建立连接',
    'This device\'s Wi-Fi':'电视当前 Wi-Fi',
    'This device\'s Wi-Fi network':'使用电视当前 Wi-Fi 网络',
    'This device is on “':'电视当前连接“',
    'The iPhone joins the network this device is on. ':'iPhone 将使用电视当前连接的网络。',
    'The iPhone joins “':'iPhone 将连接“',
    '”, the network this device is on. ':'”，与电视处于同一网络。',
    '”: using it is simplest (enter its password once).':'”：可直接使用此网络，只需填写一次密码。',
    'Wi-Fi password':'Wi-Fi 密码','Show password':'显示密码',
    'Android can\'t read a saved network\'s password, so enter it once.':'Android 无法读取已保存的网络密码，请在此输入一次。',
    "Enter the Wi-Fi password in Settings (Android cannot read a saved network's password)":'请在设置中填写 Wi-Fi 密码（Android 无法读取已保存的密码）',
    'Private hotspot':'独立热点','Mobile hotspot':'系统热点','Wi-Fi Direct':'Wi-Fi 直连',
    'Private hotspot, created by CarCast (nothing to type, no internet)':'由 CarCast 创建独立热点，无需填写；不提供互联网。',
    'Mobile hotspot from Android settings (shares internet; enter its name and password)':'使用 Android 系统热点，可共享网络；需填写名称和密码。',
    'Wi-Fi Direct, created by CarCast (5 GHz, nothing to type)':'由 CarCast 建立 5 GHz Wi-Fi 直连，无需填写。',
    'Wi-Fi Direct needs nothing typed. (To use this device\'s Wi-Fi network instead, Android must allow Location so CarCast can read the network\'s name.)':'Wi-Fi 直连无需填写信息。使用电视当前 Wi-Fi 时，需允许位置权限以读取网络名称。',
    'This device creates its own network when you press Start; its name and password are sent to the iPhone automatically. Keep Wi-Fi on.':'启动后电视会创建独立网络，自动将名称和密码发送至 iPhone。请保持 Wi-Fi 开启。',
    'Turn on the hotspot in Android\'s Settings → Hotspot & tethering, then enter its name and password here (Android doesn\'t let apps read them). The iPhone joins it and keeps its internet.':'先在 Android 设置中开启热点，再在此填写热点名称和密码。iPhone 将加入该热点并使用其网络。',
    'Hotspot name':'热点名称','Hotspot password':'热点密码',
    'Hotspot channel (optional; blank = auto)':'热点信道（可选；留空为自动）',
    'Open hotspot settings':'打开系统热点设置','Wi-Fi hand-off':'Wi-Fi 切换方式',
    'Wi-Fi interface (blank = auto)':'Wi-Fi 网卡（留空为自动）',
    '<unknown ssid>':'<无法读取网络名称>',
    'Pair new phone':'配对新手机','Pair new device':'配对新设备',
    'Make this device discoverable':'允许附近设备发现电视',
    'No paired iPhone yet — tap Pair new phone.':'尚未配对 iPhone，请选择“配对新手机”。',
    'None paired':'暂无已配对手机','Looking for phones…':'正在查找手机…',
    'Turn Bluetooth on first':'请先开启蓝牙','Bluetooth is not available':'此设备无法使用蓝牙',
    'Bluetooth scan not allowed':'未获准搜索蓝牙设备','Bluetooth scan permission needed':'需要蓝牙搜索权限',
    'Tap Start to allow Bluetooth access.':'请选择“启动”并允许访问蓝牙。',
    'Tap the phone, then Forget':'选择手机后可取消配对',
    '1 phone':'1 部手机',' phones':' 部手机',
    'Tap Add phone and pick the iPhone, then confirm the code on both. Keep the iPhone\'s Bluetooth on. Already paired phones are shown below.':'选择“添加手机”，选中 iPhone，并在两端确认配对码。请保持 iPhone 蓝牙开启；已配对手机显示在下方。',
    'Pair once, then tap Connect — or let the iPhone connect when it\'s near. Or just plug it in with a USB cable.':'首次配对后选择“连接”，或让 iPhone 在附近自动连接；也可使用 USB 数据线。',
    'Tap Connect. On the iPhone, tap Allow / Use CarPlay when asked (only the first time). If nothing happens in 30 s, turn the iPhone\'s Bluetooth off and on, then try again.\n\nOr connect from the iPhone: Settings → Bluetooth → tap “':'选择“连接”，首次连接时在 iPhone 上允许使用 CarPlay。如果30秒内没有响应，请重新开启 iPhone 蓝牙再试。\n\n也可在 iPhone 设置 → 蓝牙中选择“',
    '”. CarCast keeps listening while it runs, so CarPlay starts the same way.':'”。CarCast 运行期间会持续等待连接。',
    '1. Tap Start below.\n2. Plug the iPhone in with a USB cable.\n3. Allow access on this device, and tap Trust on the iPhone.\n4. CarPlay opens on its own.':'1. 选择下方“启动”。\n2. 用 USB 数据线连接 iPhone。\n3. 在电视上允许访问，并在 iPhone 上选择“信任”。\n4. CarPlay 将自动打开。',
    'CarPlay runs over Wi-Fi once the iPhone connects over Bluetooth.':'通过蓝牙建立连接后，CarPlay 将通过 Wi-Fi 传输。',
    '✅ CarPlay is connected — you\'re done.':'✅ CarPlay 已连接，设置完成。',
    'CarPlay is on another phone':'CarPlay 当前正在另一部手机上使用',
    'CarPlay is on the car screen':'CarPlay 画面已在接收屏幕显示',
    'CarPlay is running in the background — tap CarPlay to go back':'CarPlay 正在后台运行，选择 CarPlay 即可返回。',
    'Plug in your iPhone with a USB cable':'请使用 USB 数据线连接 iPhone',
    'Plug in your iPhone, or tap it below to connect wirelessly':'插入 iPhone 数据线，或选择下方手机进行无线连接。',
    'Tap Start, then plug in your iPhone or connect it wirelessly':'选择“启动”，再用数据线或无线方式连接 iPhone。',
    'Tap Start, then plug in your iPhone to mirror its screen':'选择“启动”，再插入 iPhone 数据线以显示镜像。',
    'Tap Start, then AirPlay from your iPhone':'选择“启动”，然后在 iPhone 上使用隔空播放。',
    'Tap Start, then on the iPhone: Control Center → Screen Mirroring.\nOr plug it in with a USB cable.':'选择“启动”，再在 iPhone 控制中心选择“屏幕镜像”；也可使用 USB 数据线。',
    'Tap Start, then cast from a DLNA app (BubbleUPnP, iQiyi, Bilibili, Youku…)':'选择“启动”，再从爱奇艺、哔哩哔哩、优酷等支持 DLNA 的应用投屏。',
    'CarPlay — wired or wireless CarPlay':'CarPlay：有线或无线车载界面',
    'Mirroring — AirPlay screen mirroring, or USB':'屏幕镜像：隔空镜像或 USB 镜像',
    'AirPlay — videos and music pushed from the iPhone':'隔空播放：接收 iPhone 视频与音乐',
    'DLNA — casts from Android phones and video apps':'DLNA：接收安卓手机与视频应用投屏',
    'Choose which modes are enabled and appear as tabs on the home screen.':'选择要启用的功能；启用后会显示在首页。',
    'Receiver name':'接收端名称','Mirroring resolution':'镜像分辨率',
    '1280 × 720 (lighter on Wi-Fi and the decoder)':'1280 × 720（降低网络和解码负担）',
    'Full screen: zoom the mirrored screen and videos to fill (crops the edges)':'全屏填充镜像与视频（可能裁剪边缘）',
    'AirPlay in Mirroring mode (off: USB cable only)':'镜像模式允许隔空连接（关闭后仅使用 USB）',
    'AirPlay password: none':'隔空播放密码：未设置','AirPlay password: set':'隔空播放密码：已设置',
    'AirPlay is on as “':'隔空播放已启用，名称为“','DLNA is on as “':'DLNA 已启用，名称为“',
    'Name, resolution, password and on/off take effect the next time you tap Start.':'名称、分辨率、密码及开关修改将在下次启动时生效。',
    'What iPhones show under Screen Mirroring and in the AirPlay menu. Leave blank for “':'这是 iPhone 镜像和隔空播放菜单中显示的名称；留空使用“',
    'What DLNA apps (BubbleUPnP, iQiyi, Bilibili, Youku…) list among their TVs. Leave blank for “':'这是爱奇艺、哔哩哔哩、优酷等投屏列表中显示的名称；留空使用“',
    '” — on the iPhone: Control Center → Screen Mirroring, or the AirPlay button in a video or music app.':'”：请在 iPhone 控制中心选择屏幕镜像，或在视频、音乐应用中选择隔空播放。',
    '” — on the iPhone: Control Center → Screen Mirroring.\nOr plug it in with a USB cable.':'”：请在 iPhone 控制中心选择屏幕镜像，或使用 USB 数据线。',
    '” — pick it in your app\'s cast / TV list.':'”：请在应用的投屏列表中选择该名称。',
    '”. Takes effect the next time you tap Start.':'”。将在下次启动时生效。',
    'UPnP AV version':'UPnP AV 版本','1 — MediaRenderer:1 (most compatible)':'1 — MediaRenderer:1（兼容性优先）',
    '2 — MediaRenderer:2 (still answers version-1 apps)':'2 — MediaRenderer:2（兼容版本1应用）',
    'Start at boot (in the selected mode: CarPlay, Mirroring or AirPlay)':'开机自启（使用所选 CarPlay、镜像或隔空播放模式）',
    'Allow “Display over other apps” so CarCast can open its screen after boot':'请允许“显示在其他应用上层”，以便开机后自动打开 CarCast。',
    'Listen on Wi-Fi/LAN at start (box mode: network senders such as Cafari can connect, no Bluetooth needed)':'启动时监听局域网（盒子模式：Cafari 等发送端无需蓝牙即可连接）',
    'Allow CarCast to manage the iPhone\'s Bluetooth (needed for CarPlay audio)':'允许 CarCast 管理 iPhone 蓝牙连接（CarPlay 音频需要）',
    'Release Bluetooth after the Wi-Fi handoff (as a car does)':'切换至 Wi-Fi 后释放蓝牙连接（模拟车机行为）',
    'Bluetooth MAC — About device → Bluetooth address (Android hides it from apps)':'蓝牙 MAC 地址：见“关于设备 → 蓝牙地址”（Android 不向应用公开）',
    'Car logo set — reconnect the iPhone to see it':'车辆图标已设置，重新连接 iPhone 后生效。',
    'Built-in logos…':'内置图标…','Choose image':'选择图片','Could not use that image: ':'无法使用该图片：',
    'Label (e.g. GLE 450)':'显示名称（例如 GLE 450）',
    'The name the iPhone shows for this car in CarPlay. Leave blank for “':'这是 iPhone 在 CarPlay 中显示的车辆名称；留空使用“',
    'Shown as the car\'s app on the CarPlay home screen. Pick a built-in logo, or use your own square image, 256×256 px or larger (PNG with a transparent background looks best); other shapes are center-cropped. Sent to the iPhone at 120, 180 and 256 px. Takes effect on the next connection.':'车辆图标显示在 CarPlay 首页。可选内置图标，或使用至少256×256像素的正方形图片；推荐透明背景 PNG。将在下次连接时生效。',
    'Driving position':'驾驶位置','Left-hand drive':'左舵','Right-hand drive':'右舵',
    'CarPlay puts its dock on the driver\'s side. Takes effect on the next connection.':'CarPlay 将侧栏放在驾驶员一侧，下次连接时生效。',
    'Night mode (dark CarPlay; also switches a running session)':'夜间模式（深色 CarPlay，当前连接也会切换）',
    'Display resolution':'画面分辨率','Width':'宽度','Height':'高度',
    'Knob only':'仅旋钮操作','No knob input':'不使用旋钮输入',
    'Video playback (show video while parked)':'视频播放（停车时显示视频）',
    'Instrument cluster (CarPlay alt screen — maps / turn card on a second display)':'仪表盘副屏（显示地图或转向提示）',
    'CarPlay Ultra: the iPhone\'s gauge cluster, drawn by CarCast with simulated car data (turns on the instrument cluster and vehicle state)':'CarPlay Ultra：使用模拟车辆数据绘制 iPhone 仪表盘（同时启用副屏和车辆状态）',
    'Cluster':'仪表盘','Cluster content':'仪表盘内容','On screen':'屏幕内显示',
    'Map':'地图','Navigation app decides (map + turn card)':'由导航应用决定（地图与转向提示）',
    'Turn-by-turn card only':'仅逐向导航提示','Show ETA on the cluster map':'在仪表盘地图上显示预计到达时间',
    'Two cluster streams: map + turn-by-turn card side by side':'双副屏：并排显示地图与转向提示',
    'CarPlay draws navigation on the cluster (maps, turn cards); applies the next time you tap Start.':'在副屏上显示导航地图和转向提示；下次启动时生效。',
    'Cluster: resolution (blank = the preset\'s) and its width on this screen, % of the main screen. Applies the next time you tap Start.':'设置副屏分辨率（留空使用预设值）以及其占主屏宽度的百分比；下次启动时生效。',
    'Now Playing card (track, artist and artwork from the iPhone, like a car cluster)':'正在播放卡片（显示 iPhone 的曲名、歌手和封面）',
    'Vehicle state protocol (Route Sharing · CarPlay Ultra data channel; takes effect on the next connection)':'车辆状态协议（路线共享与 CarPlay Ultra 数据通道；下次连接时生效）',
    'Takes effect on the next connection.':'下次连接时生效。',
    ' + cluster':' + 仪表盘','Debug options':'调试选项','Developer':'开发者',
    'Match macOS identity (debug: no BT MAC, deviceID C2:A5…, no iAP2 over Wi-Fi)':'模拟 macOS 身份（调试选项：不使用蓝牙 MAC 和 Wi-Fi iAP2）',
    'Asset version (1)':'资源版本（1）','SDK (26.0)':'SDK（26.0）',
    'Theme asset id (44C9FA31EC)':'主题资源 ID（44C9FA31EC）',
    'Share logs':'分享日志','Send CarCast\'s log after a failed connect':'连接失败时，可手动分享 CarCast 日志。',
    'Permission needed: ':'需要权限：',
    'Association unavailable — connecting anyway':'无法关联设备，将继续尝试连接',
    'Not associated — Bluetooth may stay connected and audio stay on the iPhone':'设备未关联：蓝牙可能保持连接，声音可能仍由 iPhone 播放。',
    'VPN not allowed — wired (USB) CarPlay needs it; wireless still works':'尚未允许 VPN：USB CarPlay 需要此权限；无线连接仍可使用。',
    'Test build expired':'测试版已到期',
    'This CarCast test build is more than 90 days old and no longer runs. Install the current build to carry on.':'此 CarCast 测试版已超过90天有效期，请安装新的官方版本后继续使用。',
    'this build expired ':'此测试版已到期 ', ' day(s) ago':' 天',
}

def q(value):
    return json.dumps(value, ensure_ascii=False)

helper = '''.class public final Lai/rplay/carcast/CnUi;
.super Ljava/lang/Object;
.field private static final words:Ljava/util/HashMap;

.method static constructor <clinit>()V
    .locals 3
    new-instance v0, Ljava/util/HashMap;
    invoke-direct {v0}, Ljava/util/HashMap;-><init>()V
'''
for source, target in TEXT.items():
    helper += f'    const-string v1, {q(source)}\n    const-string v2, {q(target)}\n'
    helper += '    invoke-virtual {v0, v1, v2}, Ljava/util/HashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;\n'
helper += '''    sput-object v0, Lai/rplay/carcast/CnUi;->words:Ljava/util/HashMap;
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
'''
# Translate long display phrases only; do not replace short words inside phone/network names.
for source in sorted(TEXT, key=len, reverse=True):
    if len(source) >= 12 and ' ' in source:
        helper += f'    const-string v2, {q(source)}\n    const-string v3, {q(TEXT[source])}\n'
        helper += '    invoke-virtual {v0, v2, v3}, Ljava/lang/String;->replace(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;\n    move-result-object v0\n'
helper += '''    return-object v0
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
'''
focus = '''.class public final Lai/rplay/carcast/CnFocus;
.super Ljava/lang/Object;
.implements Landroid/view/View$OnFocusChangeListener;

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public onFocusChange(Landroid/view/View;Z)V
    .locals 3
    if-eqz p2, :normal
    const v0, 0x3f851eb8
    goto :scale
    :normal
    const/high16 v0, 0x3f800000
    :scale
    invoke-virtual {p1, v0}, Landroid/view/View;->setScaleX(F)V
    invoke-virtual {p1, v0}, Landroid/view/View;->setScaleY(F)V
    invoke-virtual {p1}, Landroid/view/View;->getBackground()Landroid/graphics/drawable/Drawable;
    move-result-object v0
    instance-of v1, v0, Landroid/graphics/drawable/GradientDrawable;
    if-eqz v1, :done
    check-cast v0, Landroid/graphics/drawable/GradientDrawable;
    const/4 v1, 0x3
    if-eqz p2, :dim
    const v2, -0x9e5b01
    goto :stroke
    :dim
    const/4 v1, 0x1
    const v2, -0xcfbf9e
    :stroke
    invoke-virtual {v0, v1, v2}, Landroid/graphics/drawable/GradientDrawable;->setStroke(II)V
    :done
    return-void
.end method
'''

counts = {'text': 0, 'hint': 0, 'focus': 0}
for path in PKG.glob('*.smali'):
    if path.name in {'CnUi.smali', 'CnFocus.smali'}:
        continue
    original = path.read_text()
    changed = original
    for old, new, key in [
        ('Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V', 'Lai/rplay/carcast/CnUi;->text(Landroid/widget/TextView;Ljava/lang/CharSequence;)V', 'text'),
        ('Landroid/widget/TextView;->setHint(Ljava/lang/CharSequence;)V', 'Lai/rplay/carcast/CnUi;->hint(Landroid/widget/TextView;Ljava/lang/CharSequence;)V', 'hint'),
        ('Landroid/view/View;->setOnClickListener(Landroid/view/View$OnClickListener;)V', 'Lai/rplay/carcast/CnUi;->click(Landroid/view/View;Landroid/view/View$OnClickListener;)V', 'focus'),
    ]:
        pattern = r'invoke-virtual(\/range)? (\{[^}]+\}), ' + re.escape(old)
        def replace(m):
            return 'invoke-static' + (m.group(1) or '') + ' ' + m.group(2) + ', ' + new
        changed, count = re.subn(pattern, replace, changed)
        counts[key] += count
    if changed != original:
        path.write_text(changed)
(PKG / 'CnUi.smali').write_text(helper)
(PKG / 'CnFocus.smali').write_text(focus)
assert counts['text'] >= 20 and counts['focus'] >= 10, counts
print({'translations': len(TEXT), 'hooks': counts, 'native_libraries_modified': False})
