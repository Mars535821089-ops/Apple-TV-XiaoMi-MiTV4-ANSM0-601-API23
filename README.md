# Carplay-XiaoMi MiTV4-ANSM0-601-API23

小米 MiTV4-ANSM0（Android 6.0.1 / API23 / ARM32）的电视 CarPlay 适配补丁、构建工具和实机验收记录。

**开发中，尚未完成全方位适配。当前候选的上下键仍可能横移，不是最终交付版本。**

已确认：中文接收页面、16:9无线主画面、Aerial桌面、一次真实重启后自动进入Aerial，及用户确认的电视出声。仍未完成：真实四向、跨应用全部按钮、Siri、杂音、iPhone视频画面与电视音频同步及长期稳定性。详见 [完整验收矩阵](docs/ACCEPTANCE.md)。

## 源码与第三方基线

- `src/carcast/`：本项目新增Smali适配代码及5个原厂类的最小钩子补丁。
- `tools/`：构建、已授权电视的部署/按键与普通实时预览工具。
- `experiments/`：未通过验收的历史实验；**不进入默认构建**。特别是交互PCM限制已撤回。
- `upstream/aerial-tv/`：Aerial官方MIT源码子模块，固定为电视当前1.72对应提交；使用`git clone --recurse-submodules`或`git submodule update --init --recursive`取得源码。不会自动升级电视上的Aerial。
- `dependencies.lock.json`：原厂APK和工具的官方来源与固定SHA256。
- `local/`：仅本地保存的运行材料、上游应用解包目录和设备记录，全部被Git忽略。

CarCast是闭源第三方基线，本仓库不包含其完整反编译代码、APK或原生库。构建从[原厂公开发布](https://github.com/rPlayAI/carcast-public/releases/tag/android-0.3.25)获取基线，仅重现本项目补丁。保留原测试期限 **2027-01-19** 及认证逻辑。本项目不是原厂发行版，不表示与Apple、小米或CarCast原厂有关联。

Aerial来源为[pengchujin/aerial-tv](https://github.com/pengchujin/aerial-tv)。已核对官方v1.72发布资产SHA256与电视安装包一致，固定来源见依赖锁文件。最新上游版本可能更高，本项目保留已验收的1.72基线。

## 构建

已验证的构建环境：macOS、Python 3.12.4、Java 21、Xcode命令行工具中的clang。安装 `uv` 后：

```sh
uv run --no-project --python 3.12.4 \
  --with capstone==5.0.9 --with pyelftools==0.33 --with unicorn==2.1.4 \
  python tools/build.py
```

Java需要在PATH中，或传 `--java /path/to/java`。原生桥接汇编使用 `xcrun clang`；其他平台尚未验收。输出在 `build/outputs/`，包含签名候选和SHA256构建回执。签名使用uber-apk-signer自带的测试签名，不在源码中存放私钥。

`--offline` 禁止下载；可用 `--upstream-apk`、`--apktool`、`--signer` 指定已有文件，仍会核对固定SHA256。大小写仅不同的原厂资源直接从原始ZIP保留，避免macOS文件系统碰撞。

2026-10-31 已用本仓库源码从干净原厂基线完成重建；当时重建的签名APK SHA256与已安装audit11字节完全一致：`8a21cc7db6ea0499862385fab03d49b45d43654e3f7d0c172d983ab2ff068518`。这证明构建可重现，不代表audit11的方向问题已经解决。

## 已授权电视部署

首次连接需在电视上开启ADB调试并允许该电脑；Wi-Fi密码只在电视上输入。地址由本地环境提供，不写入公开源码：

```sh
export TV_SERIAL='电视IP:5555'
adb -P 5040 connect "$TV_SERIAL"
python3 tools/device.py status
python3 tools/device.py install \
  --apk build/outputs/CarCast-0.3.25-audit12-input-lifecycle-aligned-debugSigned.apk \
  --receipt build/outputs/audit12-input-lifecycle.json
python3 tools/device.py launch carcast
```

工具先核对设备型号、API和ABI；覆盖安装使用`install -r`保留数据，并核对设备安装包字节一致。不自动卸载，不清除配对，不修改Wi-Fi、代理或路由。第一次配对和手机端权限仍应在设备正常界面完成。安装通过不等于功能验收通过。

电视可能要求对本次安装单独确认；保留“应用到全部”未勾选。安装命令保持前台等待电视确认，不会因固定180秒期限主动关闭安装通道。若外部工具中断或旧工具等待超时，电视仍可能稍后完成安装，不应立即重复安装。确认后可把上述命令的`install`改为`verify-install`，仅核对当前设备安装包，不发起安装。

```sh
python3 tools/device.py remote right ok back
python3 tools/device.py launch aerial
python3 tools/preview.py
```

实时预览使用普通800×450窗口，不全屏，不生成截图或录像，不捕获电视音频。当前本机采用软件解码和软件渲染，以排除硬件解码预览旧帧滞留；这不改变电视CarPlay的视频解码或音频输出。`SCRCPY_BINARY` / `ADB_BINARY` 可指向已有工具；本机验证使用scrcpy5.0.1。不要同时打开多个预览实例。

## 回退与验收

保留已知可用的本地同签名候选，以相同部署方式覆盖回退；不要通过卸载来回退。原厂签名与本地测试签名不同，不能直接互相覆盖，涉及卸载清数据时须另行处理。

完整状态见 [计划](task_plan.md)、[研究证据](findings.md)、[执行记录](progress.md) 和 [验收矩阵](docs/ACCEPTANCE.md)。ADB持续开启、重启后保留已有电脑授权由用户指定为**最终验收关卡**，目前不宣称通过。

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_public_sources.py
```

边界测试与原生指令仿真不能代替真实电视、手机和实体遥控器验收。

## 输入生命周期回归

当前默认构建标签为`audit12-input-lifecycle`，修复退到后台、失去焦点及会话结束时的长按/排队输入清理；四向空间导航仍未完成。audit11历史回退包保留，不覆盖其文件。声音与ADB最终验收按用户安排留到其他兼容项完成后。

`tests/run_input_lifecycle.py`在电视独立shell进程运行实际输入辅助类和构建产物中的onPause方法，使用真实Android Looper/Handler/Activity；只有会话标志和原生报告接收端被隔离替身替代，不安装应用，也不向手机发送按键。两个回归分别验证长按任务和排队按键在onPause之后不再产生非中立报告，修复前都失败、修复后都通过。它不代替真实应用长按、方向或跨应用验收。
