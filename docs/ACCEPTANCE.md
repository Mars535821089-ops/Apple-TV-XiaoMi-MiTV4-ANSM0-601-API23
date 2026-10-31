# 全方位验收清单

> **CarPlay adaptation is shelved at the user's request (2026-11-01). Do not resume development, device testing or deployment without a new user request. This is not a completed compatibility release.**
> See [current delivery status](DELIVERY_STATUS.md) for the separate desktop, Hongguo and ADB results.


状态：通过 / 失败 / 部分通过 / 待测 / 需手机权限。代码或仿真通过不代表实机通过。每项记录触发、预期、实际、接收进程是否存活、会话是否保留，以及证据来源；不保存截图或录像。

## 验收矩阵

| 范围 | 具体要求 | 当前状态 |
|---|---|---|
| 桌面 | Aerial主页、中文名称、应用打开、主页返回 | 部分通过：主页与名称用户已确认 |
| 开机 | 真正重启后自动Aerial，无手动拉起 | 通过：已多次观察新启动后Aerial前台，仍保留最终整体验收 |
| 显示 | 16:9、无额外仪表盘、文字可读、无裁切和黑层 | 部分通过：主画面与单画面已确认 |
| 四向 | 上下左右符合屏幕空间方向；每次短按一步；边缘不误跳 | 失败：audit18现场Down电话→音乐向右，Up音乐→电话向左 |
| 空间焦点候选 | 内存视频焦点识别、方向邻居、取消与回滚 | 进行中：12项人工几何及队列安全通过；真实识别尚未通过，未实现方向搜索 |
| 按钮覆盖 | 同组标签、列表、弹窗、分页、滚动、返回、确定、菜单 | 部分通过：仍有重大缺口 |
| 长按 | 重复间隔合理、释放即停、断连后不继续注入 | 部分通过：长按释放/回主页实测停止；audit18包含交叠键释放修复，隔离三项通过，完整安装版组合与断连待回归 |
| 系统按键 | 主页、电源、音量和语音键的实际行为 | 部分通过：主页用户已确认 |
| 音乐输出 | 电视扬声器出声、暂停/继续/上下一曲、音量与静音 | 部分通过：用户已确认出声 |
| 音质 | 无杂音、欠载、丢包；连续播放；前后台和锁屏不劣化 | 待测 |
| 视频音频延迟 | iPhone显示视频时电视声音与画面匹配，延迟不妨碍观看 | **失败：用户确认明显声音滞后** |
| 音频混合 | 导航与音乐混音、语音打断、结束恢复 | 待测 |
| 语音 | 实体语音键、Siri界面、收音、响应，不退出连接 | 未通过：此前实验没有成功唤起 |
| 应用 | 当前手机所有可见CarPlay应用的启动、主区域和安全按钮 | 部分通过：网易云部分区域、地图/电话/信息入口 |
| 连接 | 首次已授权无线连接、重新进入、后台返回、停止后不乱连 | 部分通过 |
| 恢复 | 会话结束自动恢复、真正失活恢复、退桌面不误触发恢复 | 部分通过：有重连记录；查明画面静默触发主动断连，audit16撤除该规则但未实机验收 |
| 待机 | 休眠/唤醒、蓝牙遥控器恢复、桌面与音频恢复 | 待测 |
| 稳定性 | 连续使用、应用切换、重复进出、内存与热负载、无崩溃 | 部分通过：audit18本轮连续帧更新超过150秒；完整长时、跨应用与恢复仍待测，旧停帧未统一归因 |
| 部署 | 干净基线构建、资源保留、覆盖安装保数据、回退路径 | 进行中 |
| 公开源码 | 指定本地目录、公开仓库、源码完整、无设备资料或第三方二进制 | 进行中 |
| ADB最终关卡 | 持续开启；重启后接受原电脑；多次自动连接不需电视确认 | **用户确认完成**：2026-11-01用户补充“ADB重启已完成”；按用户验收记录，不再执行新的重启测试 |

## 应用内部覆盖

- 网格：逐页收集当前可见应用名称；不把未打开的图标当兼容通过。
- 设置：每一行相邻上下、二级页面、开关、返回和滚动；不能首项一键跳末项。
- 网易云/QQ音乐：顶部全部标签、列表、播放页全部安全按钮、暂停继续、上下一曲与返回。
- 地图：搜索入口、已有结果列表、缩放和返回；涉及实际路线或位置分享时不提交无关操作。
- 电话/信息：只验收安全浏览与控件覆盖；不拨打、不发送。不把未做的真实提交写成已通过。
- 第三方或手机权限提示：记录“需手机权限”，不能通过隐藏功能或关闭保护来获得通过结果。

## 交付判定

完整交付需要以上所有必需项目有对应实机证据。若存在系统、手机或闭源协议边界，必须明确到具体功能，保留失败项并继续工作，不能用旋钮遍历、光标或少数成功页面替代用户要求的真实四向与完整体验。

## audit32空间候选补充

电话→同列播放中（Down3518ms）、播放中→电话（Up2581ms）已在实际会话按键及普通预览验证；Right电话→音乐也可到达。其他列连续Down曾在中间项超时，即使预览可见新焦点也未被该步骤确认。方向可靠性、速度、长按和翻页仍未通过，不提升完整交付结论。屏蔽未知焦点的确定键是保护措施，不是兼容成功。

## 2026-11-01 memory compatibility checkpoint

- Actual television syscall385 returned ENOSYS38; the ring initializer's positive38 path is confirmed before codec creation.
- Actual patched audit44 APK library passed independent on-TV initialization, aligned and power-of-two double mappings, wrap aliases and the original destructor. Twenty ASLR/error/cleanup cases also passed, including valid address0 failure cleanup.
- audit44 deployed and installed bytes verified. No actual telephony request has yet been accepted on this version; call quality, Siri, media mixing and delay remain unaccepted. The allocator result is not a substitute for these requirements.
- Hongguo MPV0.2.136 installation and launch are complete as a separate user request. Playback and full remote acceptance remain untested and do not advance CarPlay completion.
