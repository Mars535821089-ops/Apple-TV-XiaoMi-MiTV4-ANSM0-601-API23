# 研究与对比候选

本目录不进入默认构建。任何脚本成功或native仿真通过均不等于实机兼容通过。

- `fix_carcast_voice_pcm.py`：历史交互PCM限制，已撤回，不作为无线音频修复。
- `localize_carcast.py`：最初中文适配生成器，非幂等；当前通过src/carcast的固定源码与最小钩子补丁重建，不再重复运行该生成器。
- `native_xrefs.py`：只读定位诊断字符串及CFLString引用，或查看限定范围Thumb指令。使用`--apk`指定原厂/候选APK，`--strings`选择键名，`--disassemble START END`仅显示最多4096字节范围。
- `low_latency_media.py`：**未通过实机验收的音频协商实验**。保留AAC-LC压缩音频，在MainAudio100媒体路径声明已有AAC-LC格式，移除MainHigh102和缓冲103能力及mainBuffered token，用于比较手机视频与电视声音的延迟。若不能保持播放和连接，应立即覆盖回退已知可出声的audit11。它不修改认证、到期时间或手机视频时间戳，也不承诺一定降低延迟。

实验结果与失败项保留在验收记录；不要把实验候选称为修复完成版。
