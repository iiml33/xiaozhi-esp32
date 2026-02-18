# An MCP-based Chatbot

（中文 | [English](README.md) | [日本語](README_ja.md)）

## 介绍

👉 [人类：给 AI 装摄像头 vs AI：当场发现主人三天没洗头【bilibili】](https://www.bilibili.com/video/BV1bpjgzKEhd/)

👉 [手工打造你的 AI 女友，新手入门教程【bilibili】](https://www.bilibili.com/video/BV1XnmFYLEJN/)

小智 AI 聊天机器人作为一个语音交互入口，利用 Qwen / DeepSeek 等大模型的 AI 能力，通过 MCP 协议实现多端控制。

<img src="docs/mcp-based-graph.jpg" alt="通过MCP控制万物" width="320">

### 版本说明

当前 v2 版本与 v1 版本分区表不兼容，所以无法从 v1 版本通过 OTA 升级到 v2 版本。分区表说明参见 [partitions/v2/README.md](partitions/v2/README.md)。

使用 v1 版本的所有硬件，可以通过手动烧录固件来升级到 v2 版本。

v1 的稳定版本为 1.9.2，可以通过 `git checkout v1` 来切换到 v1 版本，该分支会持续维护到 2026 年 2 月。

### 已实现功能

- Wi-Fi / ML307 Cat.1 4G
- 离线语音唤醒 [ESP-SR](https://github.com/espressif/esp-sr)
- 支持两种通信协议（[Websocket](docs/websocket.md) 或 MQTT+UDP）
- 采用 OPUS 音频编解码
- 基于流式 ASR + LLM + TTS 架构的语音交互
- 声纹识别，识别当前说话人的身份 [3D Speaker](https://github.com/modelscope/3D-Speaker)
- OLED / LCD 显示屏，支持表情显示
- 电量显示与电源管理
- 支持多语言（中文、英文、日文）
- 支持 ESP32-C3、ESP32-S3、ESP32-P4 芯片平台
- 通过设备端 MCP 实现设备控制（音量、灯光、电机、GPIO 等）
- 通过云端 MCP 扩展大模型能力（智能家居控制、PC桌面操作、知识搜索、邮件收发等）
- 自定义唤醒词、字体、表情与聊天背景，支持网页端在线修改 ([自定义Assets生成器](https://github.com/78/xiaozhi-assets-generator))

## 硬件

### 面包板手工制作实践

详见飞书文档教程：

👉 [《小智 AI 聊天机器人百科全书》](https://ccnphfhqs21z.feishu.cn/wiki/F5krwD16viZoF0kKkvDcrZNYnhb?from=from_copylink)

面包板效果图如下：

![面包板效果图](docs/v1/wiring2.jpg)

### 支持 70 多个开源硬件（仅展示部分）

- <a href="https://oshwhub.com/li-chuang-kai-fa-ban/li-chuang-shi-zhan-pai-esp32-s3-kai-fa-ban" target="_blank" title="立创·实战派 ESP32-S3 开发板">立创·实战派 ESP32-S3 开发板</a>
- <a href="https://github.com/espressif/esp-box" target="_blank" title="乐鑫 ESP32-S3-BOX3">乐鑫 ESP32-S3-BOX3</a>
- <a href="https://docs.m5stack.com/zh_CN/core/CoreS3" target="_blank" title="M5Stack CoreS3">M5Stack CoreS3</a>
- <a href="https://docs.m5stack.com/en/atom/Atomic%20Echo%20Base" target="_blank" title="AtomS3R + Echo Base">M5Stack AtomS3R + Echo Base</a>
- <a href="https://gf.bilibili.com/item/detail/1108782064" target="_blank" title="神奇按钮 2.4">神奇按钮 2.4</a>
- <a href="https://www.waveshare.net/shop/ESP32-S3-Touch-AMOLED-1.8.htm" target="_blank" title="微雪电子 ESP32-S3-Touch-AMOLED-1.8">微雪电子 ESP32-S3-Touch-AMOLED-1.8</a>
- <a href="https://github.com/Xinyuan-LilyGO/T-Circle-S3" target="_blank" title="LILYGO T-Circle-S3">LILYGO T-Circle-S3</a>
- <a href="https://oshwhub.com/tenclass01/xmini_c3" target="_blank" title="虾哥 Mini C3">虾哥 Mini C3</a>
- <a href="https://oshwhub.com/movecall/cuican-ai-pendant-lights-up-y" target="_blank" title="Movecall CuiCan ESP32S3">璀璨·AI 吊坠</a>
- <a href="https://github.com/WMnologo/xingzhi-ai" target="_blank" title="无名科技Nologo-星智-1.54">无名科技 Nologo-星智-1.54TFT</a>
- <a href="https://www.seeedstudio.com/SenseCAP-Watcher-W1-A-p-5979.html" target="_blank" title="SenseCAP Watcher">SenseCAP Watcher</a>
- <a href="https://www.bilibili.com/video/BV1BHJtz6E2S/" target="_blank" title="ESP-HI 超低成本机器狗">ESP-HI 超低成本机器狗</a>

<div style="display: flex; justify-content: space-between;">
  <a href="docs/v1/lichuang-s3.jpg" target="_blank" title="立创·实战派 ESP32-S3 开发板">
    <img src="docs/v1/lichuang-s3.jpg" width="240" />
  </a>
  <a href="docs/v1/espbox3.jpg" target="_blank" title="乐鑫 ESP32-S3-BOX3">
    <img src="docs/v1/espbox3.jpg" width="240" />
  </a>
  <a href="docs/v1/m5cores3.jpg" target="_blank" title="M5Stack CoreS3">
    <img src="docs/v1/m5cores3.jpg" width="240" />
  </a>
  <a href="docs/v1/atoms3r.jpg" target="_blank" title="AtomS3R + Echo Base">
    <img src="docs/v1/atoms3r.jpg" width="240" />
  </a>
  <a href="docs/v1/magiclick.jpg" target="_blank" title="神奇按钮 2.4">
    <img src="docs/v1/magiclick.jpg" width="240" />
  </a>
  <a href="docs/v1/waveshare.jpg" target="_blank" title="微雪电子 ESP32-S3-Touch-AMOLED-1.8">
    <img src="docs/v1/waveshare.jpg" width="240" />
  </a>
  <a href="docs/v1/lilygo-t-circle-s3.jpg" target="_blank" title="LILYGO T-Circle-S3">
    <img src="docs/v1/lilygo-t-circle-s3.jpg" width="240" />
  </a>
  <a href="docs/v1/xmini-c3.jpg" target="_blank" title="虾哥 Mini C3">
    <img src="docs/v1/xmini-c3.jpg" width="240" />
  </a>
  <a href="docs/v1/movecall-cuican-esp32s3.jpg" target="_blank" title="CuiCan">
    <img src="docs/v1/movecall-cuican-esp32s3.jpg" width="240" />
  </a>
  <a href="docs/v1/wmnologo_xingzhi_1.54.jpg" target="_blank" title="无名科技Nologo-星智-1.54">
    <img src="docs/v1/wmnologo_xingzhi_1.54.jpg" width="240" />
  </a>
  <a href="docs/v1/sensecap_watcher.jpg" target="_blank" title="SenseCAP Watcher">
    <img src="docs/v1/sensecap_watcher.jpg" width="240" />
  </a>
  <a href="docs/v1/esp-hi.jpg" target="_blank" title="ESP-HI 超低成本机器狗">
    <img src="docs/v1/esp-hi.jpg" width="240" />
  </a>
</div>

## 软件

### 固件烧录

新手第一次操作建议先不要搭建开发环境，直接使用免开发环境烧录的固件。

固件默认接入 [xiaozhi.me](https://xiaozhi.me) 官方服务器，个人用户注册账号可以免费使用 Qwen 实时模型。

👉 [新手烧录固件教程](https://ccnphfhqs21z.feishu.cn/wiki/Zpz4wXBtdimBrLk25WdcXzxcnNS)

### ESP-IDF 环境下烧录 ESP32-S3 完整流程

#### 一、环境准备

**方法一：使用 ESP-IDF 插件（推荐，最简单）**

1. **安装 ESP-IDF 插件**
   - 在 Cursor/VSCode 中打开扩展市场（`Ctrl+Shift+X`）
   - 搜索并安装 "Espressif IDF" 插件

2. **配置插件**
   - 按 `F1`，输入 `ESP-IDF: Configure ESP-IDF extension`
   - 选择 "Express" 自动安装，或选择 "Use existing setup" 使用已有安装
   - 选择芯片支持：ESP32, ESP32-S3, ESP32-C3, ESP32-P4
   - 等待安装完成（约 10-30 分钟）

**方法二：使用 ESP-IDF 安装器**

1. 下载 [ESP-IDF 安装器](https://www.espressif.com/en/support/download/other-tools)
2. 运行 `esp-idf-tools-setup-online.exe`
3. 选择安装路径，选择 ESP-IDF 版本 **v5.4 或更高**
4. 安装完成后使用 ESP-IDF 命令提示符快捷方式

**方法三：手动安装**

1. 安装 Python 3.8+（勾选 "Add Python to PATH"）
2. 安装 Git
3. 克隆 ESP-IDF：
   ```powershell
   git clone --recursive https://github.com/espressif/esp-idf.git -b v5.4
   ```
4. 安装工具链：
   ```powershell
   cd esp-idf
   .\install.bat esp32,esp32s3,esp32c3,esp32p4
   ```
5. 每次使用前运行环境脚本：
   ```powershell
   .\export.ps1  # PowerShell
   # 或
   .\export.bat  # CMD
   ```

#### 二、项目配置

1. **设置目标芯片**
   ```powershell
   cd D:\AIprojects\xiaozhi-esp32
   idf.py set-target esp32s3
   ```

2. **打开配置菜单**
   - 使用插件：按 `F1` → `ESP-IDF: SDK Configuration editor (menuconfig)`
   - 或使用终端：`idf.py menuconfig`

3. **配置项目参数**
   - 导航到 `Xiaozhi Assistant` → `Board Type`，选择你的开发板
   - 配置 `Partition Table` → `Custom partition CSV file`（如 `partitions/v2/8m.csv`）
   - 配置 `Serial flasher config` → `Flash size`（根据你的 Flash 大小选择）
   - 如需配置 OTA URL：`Xiaozhi Assistant` → `Default OTA URL`
   - 按 `S` 保存，按 `Q` 退出

#### 三、编译项目

```powershell
idf.py build
```

或使用插件：按 `F1` → `ESP-IDF: Build your project`

#### 四、烧录固件

1. **连接设备**
   - 将 ESP32-S3 通过 USB 连接到电脑
   - 安装 USB 转串口驱动（如 CH340、CP2102 等）
   - 查看设备管理器确认串口号（如 COM3）

2. **进入下载模式**
   - 不同开发板进入下载模式的方法不同：
     - 部分开发板：按住 BOOT 键，再按一下 RESET 键，松开 RESET，再松开 BOOT
     - M5Stack CoreS3：长按复位按键约 3 秒，直至内部指示灯亮绿色
     - AtomEchoS3R：按住侧面 RESET 按键，直到 RESET 按键下方绿灯闪烁

3. **执行烧录**
   ```powershell
   idf.py -p COM3 flash
   ```
   （将 `COM3` 替换为你的实际串口号）

   或使用插件：按 `F1` → `ESP-IDF: Flash your project`

4. **查看串口输出**
   ```powershell
   idf.py -p COM3 monitor
   ```
   或使用插件：按 `F1` → `ESP-IDF: Monitor your device`

#### 五、一键编译烧录（部分开发板支持）

某些开发板支持一键编译烧录：

```powershell
# 例如：M5Stack CoreS3
python scripts/release.py m5stack-core-s3

# 然后烧录
idf.py flash
```

#### 六、常见问题

- **找不到串口**：检查设备管理器，安装 USB 转串口驱动
- **烧录失败**：确保设备已进入下载模式，检查串口号是否正确
- **编译失败**：运行 `idf.py doctor` 检查环境，确保已设置目标芯片
- **PowerShell 执行策略错误**：以管理员身份运行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **menuconfig 编码错误（UnicodeDecodeError: 'gbk' codec can't decode）**：
  
  这是 Windows 系统上常见的编码问题。解决方法：
  
  **方法一：删除 sdkconfig 文件重新生成（推荐）**
  ```powershell
  # 删除损坏的配置文件
  del sdkconfig
  # 重新设置目标芯片，会自动生成新的 sdkconfig
  idf.py set-target esp32s3
  # 再次打开 menuconfig
  idf.py menuconfig
  ```
  
  **方法二：设置环境变量强制使用 UTF-8**
  ```powershell
  # 在运行 menuconfig 前设置环境变量
  $env:PYTHONIOENCODING="utf-8"
  idf.py menuconfig
  ```
  
  **方法三：将 sdkconfig 转换为 UTF-8 编码**
  ```powershell
  # 使用 PowerShell 读取并重新保存为 UTF-8
  $content = Get-Content sdkconfig -Raw -Encoding Default
  [System.IO.File]::WriteAllText("$PWD\sdkconfig", $content, [System.Text.Encoding]::UTF8)
  ```
  
  如果问题仍然存在，建议删除 `sdkconfig` 和 `build` 目录，然后重新配置：
  ```powershell
  del sdkconfig
  rmdir /s /q build
  idf.py set-target esp32s3
  idf.py menuconfig
  ```

#### 七、参考文档

- [Windows 上配置 ESP-IDF 开发环境](docs/setup_idf_windows.md)
- [在 Cursor 中使用 ESP-IDF 插件](docs/setup_cursor_esp_idf.md)
- [ESP-IDF 官方文档](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)

### 开发环境

- Cursor 或 VSCode
- 安装 ESP-IDF 插件，选择 SDK 版本 5.4 或以上
- Linux 比 Windows 更好，编译速度快，也免去驱动问题的困扰
- 本项目使用 Google C++ 代码风格，提交代码时请确保符合规范

### 开发者文档

- [自定义开发板指南](docs/custom-board.md) - 学习如何为小智 AI 创建自定义开发板
- [MCP 协议物联网控制用法说明](docs/mcp-usage.md) - 了解如何通过 MCP 协议控制物联网设备
- [MCP 协议交互流程](docs/mcp-protocol.md) - 设备端 MCP 协议的实现方式
- [MQTT + UDP 混合通信协议文档](docs/mqtt-udp.md)
- [一份详细的 WebSocket 通信协议文档](docs/websocket.md)

## 大模型配置

如果你已经拥有一个小智 AI 聊天机器人设备，并且已接入官方服务器，可以登录 [xiaozhi.me](https://xiaozhi.me) 控制台进行配置。

👉 [后台操作视频教程（旧版界面）](https://www.bilibili.com/video/BV1jUCUY2EKM/)

## 相关开源项目

在个人电脑上部署服务器，可以参考以下第三方开源的项目：

- [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) Python 服务器
- [joey-zhou/xiaozhi-esp32-server-java](https://github.com/joey-zhou/xiaozhi-esp32-server-java) Java 服务器
- [AnimeAIChat/xiaozhi-server-go](https://github.com/AnimeAIChat/xiaozhi-server-go) Golang 服务器
- [hackers365/xiaozhi-esp32-server-golang](https://github.com/hackers365/xiaozhi-esp32-server-golang) Golang 服务器

使用小智通信协议的第三方客户端项目：

- [huangjunsen0406/py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) Python 客户端
- [TOM88812/xiaozhi-android-client](https://github.com/TOM88812/xiaozhi-android-client) Android 客户端
- [100askTeam/xiaozhi-linux](http://github.com/100askTeam/xiaozhi-linux) 百问科技提供的 Linux 客户端
- [78/xiaozhi-sf32](https://github.com/78/xiaozhi-sf32) 思澈科技的蓝牙芯片固件
- [QuecPython/solution-xiaozhiAI](https://github.com/QuecPython/solution-xiaozhiAI) 移远提供的 QuecPython 固件

## 关于项目

这是一个由虾哥开源的 ESP32 项目，以 MIT 许可证发布，允许任何人免费使用，修改或用于商业用途。

我们希望通过这个项目，能够帮助大家了解 AI 硬件开发，将当下飞速发展的大语言模型应用到实际的硬件设备中。

如果你有任何想法或建议，请随时提出 Issues 或加入 [Discord](https://discord.gg/bXqgAfRm) 或 QQ 群：1011329060

## Star History

<a href="https://star-history.com/#78/xiaozhi-esp32&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=78/xiaozhi-esp32&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=78/xiaozhi-esp32&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=78/xiaozhi-esp32&type=Date" />
 </picture>
</a>
