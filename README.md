# Carplay-XiaoMi MiTV4-ANSM0-601-API23

小米 MiTV4-ANSM0（Android 6.0.1 / API23 / ARM32）的电视 CarPlay 适配补丁、构建工具和实机验收记录。

**开发中，尚未完成全方位适配。当前候选的上下键仍可能横移，不是最终交付版本。**

已确认：中文接收页面、16:9无线主画面、Aerial桌面、一次真实重启后自动进入Aerial，及用户确认的电视出声。仍未完成：真实四向、跨应用全部按钮、Siri、杂音、iPhone视频画面与电视音频同步及长期稳定性。详见 [完整验收矩阵](docs/ACCEPTANCE.md)。

## 源码与第三方基线

- `src/carcast/`：本项目新增Smali适配代码及5个原厂类的最小钩子补丁。
- `tools/`：构建、已授权电视的部署/按键与普通实时预览工具。
- `experiments/`：未通过验收的历史实验；**不进入默认构建**。特别是交互PCM限制已撤回。
- `upstream/aerial-tv/`：Aerial官方MIT源码子模块，固定为电视现用1.74对应提交；使用`git clone --recurse-submodules`或`git submodule update --init --recursive`取得源码。用于重现已安装版本。
- `dependencies.lock.json`：原厂APK和工具的官方来源与固定SHA256。
- `local/`：仅本地保存的运行材料、上游应用解包目录和设备记录，全部被Git忽略。

CarCast是闭源第三方基线，本仓库不包含其完整反编译代码、APK或原生库。构建从[原厂公开发布](https://github.com/rPlayAI/carcast-public/releases/tag/android-0.3.25)获取基线，仅重现本项目补丁。保留原测试期限 **2027-01-19** 及认证逻辑。本项目不是原厂发行版，不表示与Apple、小米或CarCast原厂有关联。

Aerial来源为[pengchujin/aerial-tv](https://github.com/pengchujin/aerial-tv)。2026-10-31重新核对发现电视现用1.74，安装包SHA256与官方v1.74 standard资产一致；最后更新时间为当日12:02:33。此次仅将交付源码固定到现用版本，版本变化原因未确认。原1.72来源保留在依赖锁的aerial_previous_baseline字段。

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
  --apk build/outputs/CarCast-0.3.25-audit20-reconnect-lifecycle-aligned-debugSigned.apk \
  --receipt build/outputs/audit20-reconnect-lifecycle.json
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

当前默认构建标签为`audit18-surface-ownership`，保留输入清理、旧光标清理及静默观察修正，并修复交叠方向释放错误和原SurfaceView清空TextureView输出的问题。audit18已完成覆盖安装和设备字节核对；真实画面持续更新超过150秒，不能据此宣称长期稳定。audit12已完成长按相关实测，修复退到后台、失去焦点及会话结束时的长按/排队输入清理；四向空间导航仍未完成。audit11历史回退包保留，不覆盖其文件。声音与ADB最终验收按用户安排留到其他兼容项完成后。

`tests/run_input_lifecycle.py`在电视独立shell进程运行实际输入辅助类和构建产物中的onPause方法，使用真实Android Looper/Handler/Activity；只有会话标志和原生报告接收端被隔离替身替代，不安装应用，也不向手机发送按键。两个回归分别验证长按任务和排队按键在onPause之后不再产生非中立报告，修复前都失败、修复后都通过。它不代替真实应用长按、方向或跨应用验收。

## 画面静默与会话恢复

旧画面监视器在TextureView超过120秒没有新回调时主动调用`teardownSession`。
已保留的实机记录出现149683ms后主动结束会话、随后再连的完整顺序；这不是应用崩溃的证据，也不能解释所有用户报告的退出。
画面静默本身不足以判断无线传输失效。audit16只记录帧龄与帧数，不再据此拆断连接；原厂SDK真实会话结束后的重连钩子保留。
`test_render_safety.py`是禁止画面观察器主动拆断传输的静态边界检查，修复前失败、修复后通过；不冒充真实静止画面或故障恢复验收。


## 后续输入与画面回归

`tests/run_input_lifecycle.py`新增交叠方向测试：Right按下、Left按下、Right释放，Left仍应重复，只有Left释放才停止。修复前FAIL、修复后三项均PASS。排队输入夹具增加冷启动余量，避免首次类加载使“尚未产生输入”被误计为清理成功。

`tests/run_render_routing.py`提取实际route方法，在独立Android进程用真实Surface对象、隔离原生sink验证引用。原SurfaceView销毁不得清除仍有效的TextureView输出；其他slot和没有当前TextureView的正常清理仍保留。修复前FAIL、修复后PASS，真实停帧是否均由此导致尚无充分证据。

`--input-probe axis-nudge --label audit19-axis-diagnostic`只增加F2至F9的原有轴诊断，不改变原HID描述符或实体方向键。它用于在画面可更新时重新核对既有单元/满幅轴行为，不是已完成的四向修复；不进入默认版本。


## 当前候选与空间焦点探针

默认源码现为`audit20-reconnect-lifecycle`，增加新会话建立与服务停止时清理旧重试任务，以及过期回调身份保护。`tests/run_reconnect_lifecycle.py`在独立Android VM运行实际主屏回调与重连类，先FAIL后PASS；仍需真实无线反复断连验收。

`--input-probe spatial-focus --label audit23-focus-probe`是独立的焦点矩形探针，不替换实体方向映射。F2/F3只发送一次前/后wheel，再处理当前TextureView现有视频的320×180临时像素数组，输出矩形、置信度和耗时；F10保留画面重建诊断。无Select、无图片落盘。超时、缺帧、全页变化或多个近似候选会失败，不宣称已实现空间导航。

Java仅含自有几何和探针状态，ECJ/D8由依赖锁固定。Android胶水仍是自有Smali；编译期Host桩被明确排除设备DEX。默认版本不引入这些Java候选。验证纯算法及状态机：

```sh
python3 tests/run_focus_geometry.py --java /path/to/java
```

当前12项几何人工夹具及探针状态机检查通过；取消保护通过移除guard的故障注入检测验证。它们不代表真实视频识别、更不代表全应用遥控通过。


焦点候选后续增加了输入代次标记：取消后尚在队列的探针报告失效，普通用户报告不受影响；启动前拒绝积压或按住的输入。抓帧期间取消、分析内存不足和失焦有独立保护。`tests/run_probe_queue.py`在API23实际Handler队列验证这一点，修复前失败、修复后通过。真实矩形准确性与全应用导航仍需验收。
