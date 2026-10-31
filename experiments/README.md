# 研究与对比候选

本目录不进入默认构建。任何脚本成功或native仿真通过均不等于实机兼容通过。

- `fix_carcast_voice_pcm.py`：历史交互PCM限制，已撤回，不作为无线音频修复。
- `localize_carcast.py`：最初中文适配生成器，非幂等；当前通过src/carcast的固定源码与最小钩子补丁重建，不再重复运行该生成器。
- `native_xrefs.py`：只读定位诊断字符串及CFLString引用，或查看限定范围Thumb指令。使用`--apk`指定原厂/候选APK，`--strings`选择键名，`--disassemble START END`仅显示最多4096字节范围。
- `low_latency_media.py`：**本机实测失败，已安排回退，不作为可用修复**。该实验在MainAudio100媒体路径声明已有AAC-LC格式，移除MainHigh102和缓冲103能力及mainBuffered token。无线画面可连接，QQ音乐显示播放且进度前进，但CarCast没有播放AudioTrack，也没有媒体音频SETUP。不能以画面或播放按钮正常判定音频可用。它不修改认证、到期时间或手机视频时间戳；仅保留失败研究源码。

实验结果与失败项保留在验收记录；不要把实验候选称为修复完成版。

`media_queue_probe.py`是独立的接收媒体队列实验，保留原有全部格式和通道，将type102/103初始化目标改为200ms；手机仍请求原延迟，不能称为已协商低延迟或同步修复。8项原始Thumb换算仿真通过，默认构建不使用。需观察实际音频、断音、延迟与恢复后决定保留或回退。

`consumer_menu_probe.py`以F2/F3/F4/F5发送Consumer Menu上/下/左/右；仅诊断iPhone是否接受这种输入，未证实兼容，不替代完整遥控器适配。可通过正常构建命令附加`--input-probe consumer-menu --label consumer-menu-probe`重建；必须使用独立标签以保留基线。对应标准来源：https://www.usb.org/sites/default/files/hut1_21_0.pdf 和 https://source.android.com/docs/core/interaction/input/keyboard-devices 。

实机结果：Consumer Menu候选无线画面及媒体音轨可建立，但独立方向指令和原旋钮对照均未产生预期焦点变化；不作为可用输入方案。media_queue_probe出现新增音轨欠载，未获得同步改善确认，已撤回其缓冲改动。

`additive_menu_probe.py`是后续隔离诊断：保留所有既有按钮、X/Y及wheel的位置，仅把原报告bit4..7的空白位改为Consumer Menu四方向。描述符放在本项目原生桥的既有文件填充中，RX映射从104扩为180字节；报告仍为32bit，不新增可写可执行映射。固定偏移、原始字节、完整字段对照、两个ASLR基址的分配复制检查通过。`--input-probe additive-menu --label additive-menu-probe`可构建。F2/F3/F4/F5依次为上/下/左/右，实体遥控器映射尚未修改。手机是否接受该字段仍未实测，不能称为修复。

additive-menu的实机对照仍未通过，原wheel可用但Consumer Menu方向没有正确移动。后续`--input-probe additive-dpad --label audit14-additive-dpad`仅切换为USB-IF Generic Desktop的D-pad Up/Down/Right/Left（0x90..0x93），同样保留原字段，报告32bit、描述符78字节；F2/F3/F4/F5仍按上/下/左/右排列。构建及4项分配复制验证通过，尚待实机。标准来源：https://www.usb.org/sites/default/files/hut1_12.pdf 。

实机结论：additive-dpad同样未通过，普通wheel有效时，新增方向未产生预期空间移动。与Consumer Menu路线一并拒绝作为最终四向方案。有效的输入生命周期修复保留在默认audit12中。


`axis_nudge_probe.py`只使用既有X/Y，不改HID描述符。真实画面确认：网格满幅Y可上下同列，设置列表却首项跳末项，单位轴不动，因此仍失败。F10只作Activity.recreate诊断，不能把它当长期停帧修复。

`spatial_focus_probe.py`与`spatial-focus/`是新的可否定焦点几何探针。自有Java只处理数组/异步状态，自有Smali读取接收器现有视频纹理，所有像素只在内存，日志仅矩形与计数。F2/F3一次wheel、不发送Select；F10只重建画面。audit23真实图标确实移动，但前/后探针都未稳定输出矩形，判失败；audit24增加计数指标以定位原因。人工图形夹具通过不等于真实识别通过。默认构建仍不采用该方案。
