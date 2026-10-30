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
