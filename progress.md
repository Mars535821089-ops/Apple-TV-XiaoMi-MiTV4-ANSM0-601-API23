# 执行记录

## 2026-10-31

- 用户将范围明确为全方位适配，并要求本地源码集中、公开GitHub仓库、方便重部署。
- 现有结果只作为分项证据：声音输出与开机Aerial已确认，四向导航明确失败。
- 已建立完整计划与研究结论。进度按全方位验收重新估为50%，不再沿用局部任务的90%。
- 公开仓库准备中；没有宣称仓库已经创建。
- ADB持久开启与重启后原电脑授权保留，安排为最终验收项。
- 所有既有本地运行材料已移动到 local/runtime/，旧工作路径改为指向该目录的符号链接；未复制大体积工具或删除用户资料。
- 已提取9个自有适配类与5个原厂类的388行钩子补丁。原厂完整解包源码和二进制不进入公开仓库。
- 从干净原厂基线重建audit11，签名APK SHA256与设备安装版完全一致；原始资源与资产568项保留，ARM32对齐32例、桥接30例、HID分配复制4例通过。
- 构建环境发现系统python3为3.9、与pyelftools要求不符；已固定uv使用现有Python3.12.4，哈希读取改为兼容的分块实现。构建和6项边界测试已通过。
- 单实例预览显式指定 OMX.amlogic.video.encoder.avc 后，普通800×450窗口再次获得当前CarPlay画面；默认按类型创建AVC编码器曾初始化失败。
- 公开仓库已创建并推送： https://github.com/Mars535821089-ops/Carplay-XiaoMi-MiTV4-ANSM0-601-API23 。默认分支 codex/tv-carplay-adaptation，初始提交2ef6a23；GitHub REST确认公开。
- 用户新增实机失败：iPhone画面、电视声音的视频播放明显不同步。保持该项失败，研究MainHighAudio102缓冲协商；不能把此前“出声”确认升级为音频全通过。
- 定位原厂CFLString常量头，原先只按裸字符串定位无法发现属性引用的问题已修正；找到audioLatencies、audioLatencyMs、mainBuffered等引用点。
- 低延迟媒体协商实验候选已生成并通过原厂函数仿真：100媒体AAC-LC，省略102/103媒体能力；其他交互/语音格式保留。签名候选SHA256 887397bab38683d17424d7cce4ed100ef7b5e1401949b5ac6a5404fdf6149695。此为待验收候选，不进入默认构建，不宣称降低延迟。
- 媒体实验覆盖安装进行中；保留已知可出声audit11用于必要时覆盖回退。
- 媒体实验安装已通过设备字节核对，PID9900无线画面建立；QQ音乐播放页显示暂停图标和前进进度，但电视CarCast没有播放AudioTrack，日志也无媒体音频SETUP。实验判定失败，已启动audit11覆盖回退。
- 安装客户端等待电视单次确认时超过180秒，但设备端随后实际完成安装；已依据设备字节结果确认，不因客户端超时重复安装候选。部署工具需要补充超时后的状态核对与独立verify-install能力。
- audit11覆盖回退已返回Success，设备安装包MD5与8a21cc7d签名基线再次一致，接收服务启动后无线会话已恢复。未把75ms屏幕流参数当作音频延迟证据。
- Aerial官方MIT源码来源已确认；v1.72发布资产SHA256与电视安装包完全一致，源码提交为b8e12bcf0175c8e8f6ede546d92210ff8ce5841f。上游已有v1.73，但不升级当前电视。

- 安装超时状态核对回归先复现失败后修复；新增verify-install只读核对入口。14项测试通过。
- Aerial1.72官方源码已以固定提交子模块纳入；后续clone需带--recurse-submodules。
- 恢复基线后播放媒体，实机MainHighAudio102请求audioLatencyMs=1000；确认仍走原厂AAC-LC通道，继续研究接收端延迟，尚未宣称同步修复。

- media_queue_probe签名SHA256 7c319a474f61cfaa1315a165d1b2e657f4b8d2c7cd34db49066835b41ab88203 已覆盖安装并核对字节，数据和配对保留；遥控选择原配对手机后无线画面与AAC-LC音轨建立。8项队列换算仿真通过；没有实际手机声画同步确认。
- Consumer Menu独立方向诊断候选构建完成，SHA256 c3b78145b59decfc7bf5ef82322c9cd6f6aa14c8498167e9aa4bcabe2d5b8583，原资源568项保留，分配复制4例通过；准备实测，默认构建继续保持audit11。

- Consumer Menu候选已核对安装包字节并恢复无线会话，媒体音轨建立，音频已回到原缓冲设置；独立Right/Down及原wheel对照均未出现预期焦点变化。该候选判定失败，准备恢复audit11。默认版本在新增诊断开关后再次构建，SHA256仍为8a21cc7d，16项边界测试通过。

- Consumer Menu额外对照：Home按钮可以回到应用网格，网格中的独立Right仍不动；不是全部HID都失效。此前仪表板一次wheel无响应不能推断整体描述被拒绝。已启动audit11覆盖回退，保留数据与原配对。

- 回退安装客户端超过等待时限后，电视确认窗口进入无响应；ADB身份、getprop、shell与dumpsys仍可用，InputDispatcher显示android系统窗口保留超过120秒的未处理按键队列，非CarCast窗口队列。核验仍是Consumer Menu候选。普通遥控、普通预览按键和点击均未完成确认，未重复发起安装。已执行电视故障恢复重启，后续再核对安装状态；不是ADB最终持久验收。
- 历史交付目录已物理集中到local/legacy-delivery，原路径改为兼容符号链接；修正旧状态文件中“还未出声”的过时结论，保留旧文本供追溯。

- 故障恢复重启命令已结束，但尚未观察到新的boot_id；设备调试TCP可达而ADB离线，新握手关闭且无有效头。不能宣称电视已重启。已请用户方便时进行物理断电恢复；源码工作继续。
- 部署工具增加回归：安装命令不因固定180秒期限主动关闭等待电视确认的通道；先复现该限制测试失败，再修改，16项测试通过。旧客户端或外部中断后的verify-install仍保留，不重复安装未知状态。该流程改动尚待设备恢复后的实机回归。

- 后续目标轮已重新核验：ADB仍offline，未取得新boot_id；用户物理恢复请求仍待回应。没有重发安装或重启。
- 完成保留原字段的additive-menu隔离诊断候选，SHA256 1fc244a58b3d50785d2e0629286b329430a8291de76059905a8a9e3bfe745192，构建回执build/outputs/additive-menu-probe.json。原资源568项保留、签名v1/v2/v3通过，字段检查与4例ASLR分配复制通过，19项边界测试通过。未安装到电视，默认版本不采用该方案。
- 恢复后顺序：先核对实际APK并完成audit11回退、验证无线与输入基线；再决定是否安装additive-menu进行F2..F5诊断。只有手机接受且符合空间方向后才能调整实体遥控器映射，随后逐应用验收。

- 用户确认已断电再通电后，新boot_id已核对为df676007-4490-4651-9e8f-36f652bdb698，sys.boot_completed=1，原电脑授权ADB恢复；未手动启动桌面时Aerial前台。原失败候选仍在，随后audit11覆盖安装返回成功并核对SHA256一致，数据保留。此恢复不作为最终ADB持久验收。

- 用户已静置遥控器，并安排先独立完成声音与ADB以外的兼容修复；声音和ADB留待最后配合验收。
- 发现并隔离复现：onPause之后CnHold长按任务和CnInput排队报告继续发送。实际输入类及onPause运行在电视独立进程，原生传输使用隔离计数替身，不向手机发送输入；修复前hold/queue两项均FAIL。
- 已增加onPause、窗口失焦及会话结束的取消钩子，清除重复任务、排队按键、待释放语音状态；中立报告在主线程排队释放，避免在原生结束回调内直接调用传输。修复后hold/queue均PASS，宿主19项测试通过。测试初次因隔离Activity缺少Application而异常，已修正夹具；该异常发生在测试进程，不是CarCast进程崩溃。
- audit12-input-lifecycle签名SHA256 719838c527568133f16775531954175fc988e2d954eced60dea15b11613ed157，原资源568项保留；正在保留数据覆盖安装，待真实应用回归。

- audit12-input-lifecycle已完成覆盖安装，设备安装包与719838c5候选字节一致。普通预览出现旧帧滞留，停止并重开唯一预览客户端后恢复当前接收首页；不以旧帧作为验收证据。

- 软件预览恢复当前画面后，安装版audit12完成约1.2秒方向长按，设备记录600ms起、约250ms间隔重复，释放后无新增非中立报告，网格焦点停止。首次“长按中回主页”调度实际先于长按，不计该复合场景通过；改用观察到按下后再触发主页的顺序避免时序误判。

- 第二次复合测试通过设备事件观察保证Right按下在前、Home在后、Right释放在最后。安装版26518于12:52:03开始重复，12:52:06失焦后只发中立报告，后续超过20秒无非中立注入，前台核对Aerial。该场景通过；不把预览瞬间的旧帧作为应用身份依据。
- 启动audit13-additive-menu覆盖安装；该候选包含audit12输入清理修复及保留原字段的方向诊断，SHA256 b86626124a763b98e7aac6c9eec4387df515de16f6da0beb997b57526fec90e7。实体方向键暂沿用旋钮映射，仅F2至F5发送诊断方向。

- audit13附加Consumer Menu候选实机未通过：原wheel可逐项从音乐到LEXUS，F2/3/4/5报告分别输出buttons16/32/64/128，但音乐位置的左、右、下，以及LEXUS位置的上未产生正确方向移动。先前瞬间落点不能排除预览旧帧，不作为有效输入证据。保留原字段仍无效，后续仅验证一次标准Generic Desktop D-pad字段，停止继续猜Consumer数值。
- Aerial屏保预览黑背景仅为观察：源码采用SurfaceView独立图层，设备日志出现AVC解码器工作，无当前匹配播放错误证据；不能据此称实体屏保黑屏，未改变画质或播放设置。

- audit14-additive-dpad构建与分配复制通过，SHA256 c8d14474fdda374440003f9cc274be0eb5130206ae389641c53f388cbcdcbbc8，原资源568项保留；开始覆盖安装作一次标准D-pad对照。不是默认构建，也不将宿主验证当作方向兼容通过。

- audit14 Generic Desktop D-pad实机未通过：右方向未移动，普通wheel三步可从电话到信息；在信息图标处D-pad下未进入同列设置，D-pad左未到地图，仍停在信息。已启动保留数据回退audit12。向上正向对照期间普通预览获取连续两次超时，不将该未观察场景算通过或失败；现有左右下反例已足以拒绝该方案。

- audit14回退在设备身份核验阶段因ADB离线退出，未发出重复安装；当前最后已核对安装版仍是audit14，不能称为已回退。
- 原有小米6095局域网服务可探活，Home接口返回status0，但未恢复ADB；Aerial8790管理接口需要已有随机凭据，未绕过保护。随后通过原有power接口作一次待机唤醒检查，首个请求status0，第二个请求超时；不能据此确认已唤醒，未重复发送状态不明的电源切换。现有邻居缓存和设备基线未找到可验证的唤醒地址，未猜测目标或改变网络配置。
- 删除默认源码中的未使用旧光标handle/click及Activity的cnCursor/cnX/cnY字段，保留configure与已验证输入修复。新默认audit15-no-legacy-cursor构建成功，SHA256 eb941e07a0037dc84fcf0939f9eafc0ce294676897b81a1720608175bd92fbef，DEX中旧光标字段与提示均已消失。尚未安装；audit12原回退包继续保留。19项测试通过。

- 待机唤醒请求超时后，未重复切换电源。定向接口探测未改变网络：既有en0/en1连接分别探测，未找到可验证的TV邻居唤醒地址；精确检索当前会话的既有TV ARP记录同样未找到唯一地址，因此未向猜测MAC发送唤醒。已请用户方便时仅确认亮屏，若黑屏按一次电源，声音及ADB设置不需现在配合。

- 用户确认电视始终亮屏，因此旧power接口status0不代表实际进入待机，待机唤醒验收仍未完成。
- 之后短暂恢复调试并核对另一个新boot_id，开机43秒时Aerial在前台；用户也确认本次开机ADB默认开启。随后再次离线，已发出的audit12保留数据覆盖请求未取得完成结果，不能把“最后核对audit14”写成当前安装版已确定，也不能重复安装。现无存活安装客户端；恢复后先verify-install。
- 旧日志定位到画面监视器在149683ms无新TextureView回调后主动拆断会话，接着触发重连。撤除仅凭画面静默结束会话的规则，保留真实SDK会话结束重连。静态边界回归修复前FAIL、修复后PASS，完整20项测试通过。
- audit16-observe-frame-silence构建完成，SHA256 eecbe2e5ecf97aa5d4a1d26afa2caea3531c4414828739f53cc89f764417debb；568项原资源、581项非DEX原始条目保留，ARM32对齐32例、桥接30例、HID复制4例、v1/v2/v3签名通过。未安装，仍须真实会话验收。空间四向继续保留失败状态，整体进度仍57%。

- 用户重新开启ADB后，短暂读取到新启动及Aerial前台；audit12只读核对明确不匹配，所以此前回退未能确认。随后发起一次audit16覆盖请求，普通预览仅见Aerial，无本次安装确认框。安装过程中调试再次离线；没有字节核对结果，audit16也不能称已安装。专用连接重建仍无响应；已仅停止失联的本机安装客户端，不重复安装，当前设备版本未知。

- 用户进一步确认ADB开机“允许”稍后变“拒绝”，该项明确失败，不把此前默认开启反馈视为持久性通过。恢复后已用桌面现有ConfigReceiver启用keep_adb，回执keep_adb=true、adb_enabled=1；这是保持施工连接，最终重启验收仍最后。
- 只读核对证实此前audit16实际上已安装，SHA256与eecbe2e5回执一致，无须重复安装。新增实际Android交叠方向回归先FAIL；修复CnHold仅匹配当前方向键释放后，hold/queue/overlap三项PASS。排队夹具首次因类加载未产生输入报ERROR，已增加冷启动余量，再运行原实现得到正确overlap FAIL后修复。
- 发现Surface所有权缺陷：原SurfaceView销毁经route(0,null)错误清除活跃TextureView输出。提取实际route、用真实Android Surface与隔离native sink先FAIL后PASS；保留其他slot与真正TextureView销毁的原行为。日志过滤同步保留脱敏surface证据，新增边界先FAIL再PASS，完整21项通过。
- audit18-surface-ownership SHA256 ba390c3c9c39b8c166b32f0390f578a08f3168aabe73ef9583ee07ada3786c51已覆盖安装并核对设备字节。无线会话恢复后frames从111增至564、持续超过150秒更新；这只证明本轮画面有更新，不能把先前所有停帧都归因于已修路由，也不代表长期稳定通过。
- 用户要求再次实测上下：audit18网格电话处按Down实际横移到音乐，按Up横移回电话，报告分别wheel+1/-1。四向仍失败。为排除旧帧对先前原轴观察的干扰，仅用原HID既有X/Y做一次单元/满幅对照，不更换Usage或描述符；audit19-axis-diagnostic已安装核对，SHA256 e4a059f906b958583b31e2f554a4454bd9e145131c52d4e27d25df127a5a99e1。当前测试结果待记录，默认仍audit18。
- 实机Aerial来源发生漂移：发现当前版本1.74/code94、最后更新时间2026-10-31 12:02:33；安装包SHA256 6faea5a357b5036f3d0bab2454df795f433bd54c0a754a7e9d4569648ed2306a与官方v1.74 standard发布资产一致。变化原因未确认；本轮没有执行Aerial升级。为对应现用版本，源码子模块固定到官方v1.74提交3094d55c7ba17818974a4e51cb793e3cf4ddb486，依赖锁保留旧1.72元数据。
- 当前整体估算58%，仅因真实画面更新与输入边界回归推进；空间四向、全部应用、Siri、完整重连、声音、最终ADB仍未完成。

- 19原轴对照已有可靠真实画面证据：网格满幅Y可上下同列，但设置首项驾驶专注模式一按满幅Down直达末项无障碍，单位Up仍不动。再次拒绝原轴作为全应用方案，不继续盲调幅度。
- audit20-reconnect-lifecycle已构建，SHA256 0955f6a6c99b73e1f518bd423e3d21f268f1b6a3628b36e4a49f515101dcc5d5。真实main-screen回调取消旧task、服务销毁取消、run身份保护，实际类和回调在Android隔离VM先FAIL后PASS。21项宿主及3项输入隔离回归保持通过。未单独部署20。
- audit21视频重建诊断包含20修复并已安装核对，SHA256 38addfbbf54ca62a6ce5746d21d667dbd64d9cc9e9b2c35e7daf8ac3e9670c30。F10 Activity.recreate保持PID9215，窗口和TextureView重建；受监控的这一段未出现session disconnected，随后出现新帧。长时仍有停帧/后来自行恢复记录，不能称停帧根因全修，也未将重建自动加入观察器。
- 用户要求继续并指出卡住：后续继续自主推进，不将状态回答作为停止点。原生轴路线不够，启动按现有视频流焦点几何的可否定探针设计；用户已明确全权处理并退出反复问答，按技能例外自主选择实现路线。新设计经独立builder check无关键缺口，结论仅覆盖探针。
- 纯Java几何算法10项人工夹具由空实现FAIL到PASS；异步探针fresh-frame、重复请求、超时、取消及缺帧合同通过，并注入移除guard的变异证明取消回归会FAIL。ECJ3.37.0/R8 8.3.37固定官方来源和SHA256，编译期自有Host桩严格排除设备DEX，不下载整套Android SDK。
- audit23-focus-probe构建完成，SHA256 7070765b389a4a4b7400228b3e79e55d4aa95b2b5677ffbf3283b44399c8bb06，正进行一次保留数据部署，尚未核对完成。仅F2/F3执行一次wheel前后内存取样并输出矩形，无Select、无截图文件、默认实体方向暂不改。不得将探针安装或人工测试当成方向适配通过。

- audit23已安装并核对7070765b候选，API23无类验证崩溃。真实网格F2焦点电话→音乐，F3反向回电话，但两次均输出no stable focus，按失败处理。继续用计数/矩形文本区分取样、帧稳定性和检测阈值，不保存像素或图片。
- audit24-focus-metrics构建通过，SHA256 d67ef0f2b3b94bcb6b015b7c458039fd504af8d5ce594d72cee50fff23caa05a；正发起一次覆盖安装，结果待核对。source当前geometry统计增加changed/best/second/bounds/fill，仅日志数字；所有像素仍临时内存。独立Android重连和Surface回归再次通过。

- audit24已安装核对，真实网格changed=1015但best=0；设置相邻行changed=14828，超过原28%整页门槛，错误被拒绝。增加真实尺寸的大列表行夹具先FAIL后修正45%门槛，人工几何11项通过，整页变化仍拒绝。
- audit25已安装核对，SHA256 6eb25f0dc89a81a598863153f42c7a541670e698b73f8523121b77e825875c40。真实图标候选raw=360像素、bounds57,20,97,74、fill166/1000，说明细边框和标签组合被填充率误排除。新增彩色图标细边框夹具先FAIL，再采用边框覆盖判据后12项通过；audit26构建与覆盖安装核对9288d86b通过，尚未将真实识别算通过。
- 独立代码审查发现Probe.cancel跨线程双读/取帧后发布、取消未撤销CnInput延迟探针报告、几何分析OOM逃逸。已用LOCK/epoch及输入代次标记修正，锁内仅入队、不调用native，启动时拒绝积压或仍按住的按钮。API23真实Input Handler隔离先FAIL后PASS，证实取消探针报告被丢弃且普通用户报告保留；Java取帧中取消、积压、取消代次及OOM合同也先FAIL后PASS。尚在native中的已发送报告无法撤回，不把它称为排队取消保证。
- audit27-probe-cancellation候选构建通过，SHA256 992fd4e9f71a330dfb7f48d589495eafd8c4b8e860c16ae56bf98113c925d65d；正进行一次保留数据覆盖，结果待核对。仍为独立探针，默认20不采用，方向映射未完成。

- audit27已安装核对992fd4e9，独立复核未发现限定范围内新的确定严重取消/死锁/异常逃逸问题。真实图标探针现找到best465、bounds122,20,163,74、edge451/1000，但仍被“必须再来一张不同视频帧”的稳定条件挡住。实际CarPlay新焦点静止后可停止发帧，该条件错误。
- 新增“操作后已有新帧、同一帧重复采样稳定也应完成”的状态回归，旧条件FAIL；改为新帧门槛加150ms矩形稳定后PASS，操作前旧帧仍不能确认。人工几何12项及Probe合同保持通过。audit28-focus-settling构建完成并发起一次保留数据覆盖，设备结果待核对，真实矩形识别尚待这一版复测。

- audit28已覆盖安装并核对1188652d。真实网格F2首个成功输出rect122,20,163,74（音乐），elapsed500ms；随后反向电话rect57,20,97,74（731ms），再向前音乐610ms、地图1319–1444ms、第二行LEXUS/日历/设置也输出对应矩形496–1785ms。仍有部分动作changed=0未确认，不能把整页或方向通过。需继续列表、标签和未确认输入诊断，不能盲补发。
# 2026-10-31 空间执行继续

audit28在设置列表实测：正向38,55,313,83（743ms）、反向38,27,313,55（629/1439ms），一次正向虽实际移动但2200ms未确认，保留超时。网易云播客121,5,148,22、我的93,5,120,22、精选64,5,91,22识别，与普通实时预览一致；不是四向完成。网格存在一次changed=0和跨过高德的路径，必须保留跳项风险。

Ruling: 已有三类控件几何证据，开始有界空间路径候选；先验证纯状态机和旧焦点识别，再接入实体键。用户已全权委托直接执行，不为实现选择再次等待。整体仍58%。


## audit32空间方向首轮实机

已安装核对audit32-spatial-lifecycle，SHA256 a66ae25fc3493fb1d50f855c6f27c18724b4e47d2de3ea6634f7eaac5ced087d，PID21056。真实DPAD_DOWN从电话穿过同排焦点到同列播放中（3518ms）；DPAD_UP回电话（2581ms），普通预览逐终点确认。Right电话到音乐2198ms。之后Down音乐第一步Maps964ms，下一步changed=0超时，实际预览已在信息，安全门禁停止，未盲回滚/Select。方向可靠性与响应速度仍不通过，不能宣称完整四向。新候选真实普通窗口，无图片/录像文件。

审查修正：OOM不能留下永久busy；前向同坐标循环unknown；焦点外页面变化保守检测；音量/失焦stop保持unknown；明确Back/Menu与新的主屏连接cancel重置。API23实际CnKeys+KeyEvent隔离验证门禁/UP释放/音量/Home/方向单路由先红后绿，实际队列取消/用户报告保留通过。

## audit33–37继续：取帧、圆形焦点与显示所有权

audit33摘要排除本次空白取帧：51840不透明像素且亮像素/均值正常。一次会话Texture帧停10，F10重建后同PID恢复，独立停帧尚未统一归因。audit34实机音乐Down到LEXUS正确3559ms、Up回音乐4674ms；连续其他列仍超时。audit35把观察诊断延至7秒仍失败，未当作修复；一次Up在中途PlayingNow后图像摘要7秒不变，随后预览已Messages，继续查显示/观察时序。不得继续盲加等待。

源码查到观察器每100ms重复getBitmap，即使没有新Texture帧；已先红后绿改为只对新版本读回一次，缓存同一新帧用于稳定确认，未实机验证改善。新增圆形按钮闭合环与残缺环拒绝两项几何（共14项），与方框/列表分开，未夸大应用覆盖。

独立确定缺陷：旧CnRender迟到Available可覆盖新实例output，之后旧Destroyed不清理但释放旧纹理。API23真实SurfaceTexture/Surface、实际Available与route、隔离native sink先FAIL后PASS；修复阻止不同活动实例抢输出，current为空时保留重新进入，旧实例不绑定/不安排watch。默认源码audit36已构建47e88f82b736232a2c5fa8b98a1e7b6830339af6245740ac62ca5b71a86c5f91，未单独安装。不把此所有权缺陷宣称为所有停帧根因。

目前安装audit35 d996f5a54591a113ee456082afe67a80ab8232b5535acabdaa042cb210764493 PID23591。audit37（含36所有权及新帧缓存）正在构建。已有自动重连，启动接收器前必须确认会话状态，禁止无脑Down+OK，否则已连接卡会变成断开。监控包含CarCast-screen与OMX组件名，拒绝色彩格式17=软件解码的无证据判断。

## audit38 baseline and audit39 render-generation candidate

Default audit38 built f1a7cc7e6c75bced995e81914effe32a88a15653152b9bde3b6e68becac57e45 (not separately installed). Latest-owner weak reference prevents obsolete A from reclaiming current while B is temporarily destroyed; real API23 SurfaceTexture/Surface regression failed before, passed after, including B re-entry and zero obsolete binds/watch scheduling. Probe cache now checks render generation: repeated frame numbers across replacement cannot confirm old focus, and replacement during baseline capture sends no input. Both new cases failed before and passed after.

Installed audit37 cached fresh-frame candidate still froze at 5 initial frames; F10 restored the same process. Afterwards Music DOWN reached same-column LEXUS in3278ms, bottom-row RIGHT reached Calendar1301ms and Settings924ms. Settings DOWN again timed out after7s: list navigation remains FAILED. Extending observation or reducing repeated GPU reads is not a demonstrated freeze fix. Native in/out count attempts, not checked-success values. Active component is OMX.amlogic.avc.decoder.awesome; color-format17 alone was not evidence. A zero-wait drain-after-input tail-frame window is under investigation; no native decoder patch applied yet. Candidate39 f58fec7a41979a9b4a971809ec8977a72f0962b83201aebe4e7212abace533df install in progress, do not repeat before receipt.

## audit40 live decoder status and audit41 controlled first-poll wait

audit40 installed/verified8d9c64a788fe937f1351a7e4cced345da37d663658081b7124e2013e043d8af8, PID25566. Real settings DOWN/DOWN/UP/UP reached adjacent rows, but timings5324/585/2628/591ms remain poor. Native telemetry recorded648 successful queue and642 successful release returns, no nonzero status in that bounded segment. At21:15:03 DOWN there were4 queue/3 release, no calls04-07, then08 had8 queue/9 release. This supports the tail-frame window but does not prove all freezes share it.

Controlled audit41 built73b300ba63ef119efcbe784b03420bf61f2a197bd710489a050e0b2caa9449a8, not installed yet. It changes only the first output poll of initial drain to5000us at the exact original header boundary; subsequent polls stay0. Actual original Thumb first poll failed the5000 expectation, wrapper passed6 ASLR/status cases with unchanged SP/callee registers/fallback/result/LR. Return telemetry remains enabled for the contrast, defaults unchanged. Await independent read-only review before install.

## Decoder probe source delivery

Return telemetry and first-poll wait are separate opt-in build modes with baseline-label protection. Both were independently reviewed; no definite ABI/stack/tail-branch defect found. Return telemetry12 emulation cases, first-wait6 cases including original-loop secondpoll0 passed. The first-wait hook affects initial drain entry only, including error-drain entry, not every output-loop iteration. It is not an independent asynchronous pump and cannot guarantee outputs completing after5ms.

Controlled audit41 one-time installation now pending; verify receipt before any retry. No live41 performance or reliability acceptance yet. Default38 and no-wait spatial39 remain available. Full project stays incomplete58%, audio/finalADB deferred.

## audit41 first-poll contrast: not accepted

Installed/verified73b300ba63ef119efcbe784b03420bf61f2a197bd710489a050e0b2caa9449a8, PID27280. Initial Home changed dashboard to grid, but DOWN Phone->Music1460ms then next forward observation failed after7s (total8621ms). Native queue/release3311/3300 returns all0 in this captured period. At21:39:49 there were9 queue/10 release, then50-57 no calls;58 had1/1,59 had17/17. Thus the bounded5ms first-poll experiment has NOT established a complete tail-frame/stall fix. Keep it out of defaults. Continue investigating report transport and native frame arrival; do not simply keep raising timeouts or mark spatial navigation complete.

## audit42 delta-only and separate telephony failure

Added light-appearance polarity handling: original geometry selected the old row in a synthetic light UI; now17 geometry fixtures and all probe/path/generation contracts pass. This is not light-theme hardware acceptance. Relative Wheel descriptor is Data/Variable/Relative; known sender copies bytes and visible queues do not deduplicate. Delta-only opt-in removed only its redundant zero report. Actual API23 Host.send/CnInput isolated test failed with2 reports before, passes with1 plus preserved normal cancellation neutral afterward.

audit42 installed/verified8e2b960dbc08298284a69a92164029ef36d465c8b37bfe50f40d8d9a932ee31c, PID28307. Initial Right still timed out (baseline38 frames unchanged), so delta-only is not a demonstrated initial-freeze fix. F10 recreated output, then a separate new MainAudio(100) telephony request negotiated0x40000000/Opus48k at80ms and failed38/0x26; SDK tore down the session. No real phone call was initiated by our tests. This connection-breaking audio-format path is now being traced, preserving media AAC102 and all required user functions. Audio subjective acceptance remains deferred.
