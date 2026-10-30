# 研究与对比候选

本目录不进入默认构建。任何脚本成功或native仿真通过均不等于实机兼容通过。

- `fix_carcast_voice_pcm.py`：历史交互PCM限制，已撤回，不作为无线音频修复。
- `localize_carcast.py`：最初中文适配生成器，非幂等；当前通过src/carcast的固定源码与最小钩子补丁重建，不再重复运行该生成器。
- `native_xrefs.py`：只读定位诊断字符串及CFLString引用，或查看限定范围Thumb指令。使用`--apk`指定原厂/候选APK，`--strings`选择键名，`--disassemble START END`仅显示最多4096字节范围。
- `low_latency_media.py`：**本机实测失败，已安排回退，不作为可用修复**。该实验在MainAudio100媒体路径声明已有AAC-LC格式，移除MainHigh102和缓冲103能力及mainBuffered token。无线画面可连接，QQ音乐显示播放且进度前进，但CarCast没有播放AudioTrack，也没有媒体音频SETUP。不能以画面或播放按钮正常判定音频可用。它不修改认证、到期时间或手机视频时间戳；仅保留失败研究源码。

实验结果与失败项保留在验收记录；不要把实验候选称为修复完成版。
