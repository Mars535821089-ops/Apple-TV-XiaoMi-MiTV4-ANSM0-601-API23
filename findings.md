# 当前证据与结论

## 已确认

- 设备为 Xiaomi MiTV4-ANSM0，Android 6.0.1/API23，armeabi-v7a。
- CarCast基线为0.3.25，官方APK SHA256 `81ef0a2ce404ac28aa294afd4038c70b6a8d5422685692302d7b2306ff174d5d`。
- audit11 SHA256 `8a21cc7db6ea0499862385fab03d49b45d43654e3f7d0c172d983ab2ff068518`，设备安装包MD5已核对一致。
- ARM32两处非对齐STRD触发SIGBUS，改为等长STR对后无线会话可建立；32个模拟样例通过。
- 原Knob描述符的X/Y是绝对有符号轴，wheel为相对步进。原厂Android UI没有物理遥控器通道。
- 四向全部使用wheel可逐项移动，但不符合用户要求的空间方向。audit11仍为失败候选。
- Aerial1.72具有开机组件和已启用桌面守护；真实重启标识已变化，启动完成后未手动启动桌面时Aerial在前台，本次重启通过。
- 用户已确认电视出声；不能据此宣称无杂音、语音或全链路音频通过。
- 用户进一步确认：iPhone上播放视频，声音由电视输出，声音明显滞后。实际日志出现 MainHighAudio(102) 流结束；需要检查协商与播放缓冲，尚不能断言是特定固定毫秒数或已经修复。
- 新源码构建已重现与设备相同的签名APK SHA256；公开仓库已创建并推送，GitHub REST确认visibility=public。
- 低延迟旧媒体路径实验在本机失败：视频会话可建立，媒体UI播放，但没有电视音频通道。不能通过移除102/103能力来换取表面上的低延迟；恢复audit11继续研究。

## 研究线索（不是本机验收）

- Apple WWDC16《Developing CarPlay Systems Part 1》：非触摸输入包括旋钮、按键和触控板；旋钮最少支持旋转、选择、返回，另可有nudge。
- DiPlay的CarPlayRemoteKeys直接把四方向变成wheel，源码说明CarPlay是rotary-first；这种方式不能满足本项目真实四向要求，不能直接照搬。
- mib2q-carplay-rgi的TouchpadController把触控板变为四向DPAD事件，通过原厂DSI bridge发送。需要继续追踪DSI语义如何变成线上HID，不能把它的1/2/3/4数值直接发给本机。
- CarPlay是手机渲染的视频界面，没有已证实可用的按钮树。不得把电视Accessibility空树当作手机按钮不存在。

## 来源

- https://github.com/rPlayAI/carcast-public
- https://github.com/rPlayAI/carcast-public/issues/12
- https://developer.apple.com/videos/play/wwdc2016/722/
- https://github.com/serein-morii/DiPlay-CN/blob/main/common/src/main/java/com/shilapi/xcertplay/CarPlayRemoteKeys.kt
- https://github.com/luka-dev/mib2q-carplay-rgi/blob/main/java_patch/com/luka/carplay/input/TouchpadController.java

- 恢复audit11后模拟遥控器播放媒体，实机日志确认MainHighAudio102 / AAC-LC 44100Hz双声道，手机请求audioLatencyMs=1000；这是媒体缓冲参数，不等于已测得端到端总延迟。Android活动音轨为CarCast进程，fCount=3776，不能将其与1000ms协议缓冲混为一谈。

- media_queue_probe已在实机建立MainHighAudio102及活动AudioTrack；手机仍请求1000ms，实验仅改变接收端初始目标，不能称为完成延迟协商。已观察音轨欠载计数从2329增至3273，原因尚未隔离；不能宣称无杂音或已同步。
- Consumer Menu方向Usage 0x42/43/44/45已由USB-IF与AOSP官方表确认；CarPlay是否接受该报告仍属假设。诊断版本仅添加F2至F5别名，不修改实体遥控器的现有映射。

- Consumer Menu实机对照：Right/Down诊断报告已发出，网格仍停在首个电话图标；旋钮wheel也未产生预期移动，但Home按钮仍能从仪表板回到应用网格。不能据此声称整套HID被拒绝；本候选仍不满足导航要求，已启动audit11回退。后续若研究附加方向字段，应保留原X/Y布局作为对照，避免移除原字段导致解释混杂。

- 原厂iapPointer的0..8模式属于比例、相对指针与点击路径；d.smali中的rel/park等入口不能直接满足用户无光标空间四向要求，不把它们当作替代验收。
- 新的additive-menu诊断保留原X/Y、wheel、Select/Home/Back/Voice字段及其位偏移、逻辑范围和标记；仅使用bit4..7空白位表达Consumer Menu方向。与此前替换X/Y的失败候选区分。报告仍32bit，描述符76字节，放入项目自有RX桥后的既有零填充并扩展该映射长度。原始指针、长度、分配及复制在两个装载基址通过；这是宿主证明，不是iPhone接受证明。

- 输入生命周期缺陷已有独立复现和修复证据：真实输入辅助类及构建onPause方法在API23隔离进程运行，修复前长按/排队输入退出后继续发送，修复后均停止。安装audit12后长按释放、长按中回Aerial均未继续非中立注入。原生结束回调只清理并排队中立释放，不在SDK回调线程直接调用原生报告发送。

- 发现另一处可定位的主动断连：已有安装版日志在TextureView累计5帧、frameAgeMs=149683时输出“Visible CarPlay video stalled”，随后screen stop和session disconnected，再约15秒后重连。该顺序证明监视器主动拆断会话，不能据此认定真实链路已经失效，也不是所有点击退出的统一根因。
- audit16将画面监视器限制为记录，不再根据帧回调静默执行teardownSession或CnReconnect.start；SDK onCarPlayEnded既有重连路径保留。静态安全边界先红后绿、完整20项测试通过；候选未安装，静止画面、真正断线及跨应用恢复仍待实机。
- 四向协议研究现阶段仍未突破：原旋钮轴/步进、Consumer Menu及Generic Desktop D-pad均未达到需求。标准字段存在不等于iPhone接受，禁止继续把更多未经证明的Usage数值当修复方案。原厂primaryInputDevice与HID设备构造已定位，尚未证明存在可用的新空间导航入口。

- CnHold原先任意方向UP都会取消当前长按，Right DOWN→Left DOWN→Right UP导致Left丢失重复；当前按keyCode匹配释放已用隔离Android实际类先红后绿验证。
- CnRender.route原先遇slot0的null绕过current/output，导致旧SurfaceView销毁清空实际TextureView的原生窗口；真实route隔离回归验证并修正。现场旧停帧是否均由该路径引发尚无对应日志，不能扩大归因。
- CnReconnect重试预算存在会话代次问题：第六次后120秒排队窗口中连接再断开，新start被旧task挡住，随后旧run因预算耗尽终止。需在主屏已连接时清除旧任务，并在服务销毁时取消；尚未实施，保留待修。

- 有结构化deviceOfferFocus/focusTransfer通道，但只证明视区焦点移交能力，未证明控件级矩形回调或当前delegate注册；Java接口未提供控件树。不能据此宣称已存在可用全应用空间导航。
- 原厂CarCastForceKeyFrame(0x14850c)接收有效CFLString UUID，使用当前会话发forceKeyFrame队列命令；空UUID/会话直接返回。已有Java setScreenSurface同窗口且codec有效时不触发此请求。不能传jstring/slot号代替UUID或忽略对象生命周期。Siri也未定位到证据充分的出站请求入口；能力声明及入站enhancedSiriParameters不能冒充发送接口。
