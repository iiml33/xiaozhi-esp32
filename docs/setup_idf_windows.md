# Windows 上配置 ESP-IDF 开发环境

## 前提条件

1. **Python 3.8 或更高版本**
2. **Git**
3. **ESP-IDF 5.4 或更高版本**

## 方法一：使用 ESP-IDF 安装器（推荐）

### 1. 下载 ESP-IDF 安装器

访问 [ESP-IDF 官方下载页面](https://www.espressif.com/en/support/download/other-tools)

下载 Windows 安装器：`esp-idf-tools-setup-online.exe`

### 2. 运行安装器

1. 运行安装程序
2. 选择安装路径（例如：`C:\Espressif`）
3. 选择 ESP-IDF 版本：**v5.4** 或更高
4. 选择安装组件：
   - ESP-IDF
   - Python
   - Git
   - 其他工具
5. 等待安装完成

### 3. 配置环境

安装完成后，会创建一个 ESP-IDF 命令提示符快捷方式。使用该快捷方式打开终端。

或者手动配置：

```powershell
# 在 PowerShell 中运行（替换为你的安装路径）
C:\Espressif\frameworks\esp-idf-v5.4\export.ps1
```

## 方法二：手动安装 ESP-IDF

### 1. 安装 Python

从 [Python 官网](https://www.python.org/downloads/) 下载并安装 Python 3.8+

**重要**：安装时勾选 "Add Python to PATH"

验证安装：
```powershell
python --version
# 应该显示 Python 3.x.x
```

### 2. 安装 Git

从 [Git 官网](https://git-scm.com/download/win) 下载并安装 Git

### 3. 克隆 ESP-IDF

```powershell
# 创建目录
mkdir C:\Espressif
cd C:\Espressif

# 克隆 ESP-IDF（选择 v5.4 分支）
git clone --recursive https://github.com/espressif/esp-idf.git -b v5.4

# 或者使用最新版本
git clone --recursive https://github.com/espressif/esp-idf.git
```

### 4. 安装 ESP-IDF 工具

```powershell
cd C:\Espressif\esp-idf
.\install.bat esp32,esp32s3,esp32c3,esp32p4
```

这会安装：
- 交叉编译工具链
- OpenOCD
- CMake
- Ninja
- 其他必需工具

### 5. 设置环境变量

每次使用 ESP-IDF 前，需要运行：

```powershell
# 在项目目录中
cd D:\AIprojects\xiaozhi-esp32

# 运行 ESP-IDF 环境脚本
C:\Espressif\esp-idf\export.ps1
```

**注意**：如果使用 CMD，使用 `export.bat` 而不是 `export.ps1`

## 验证安装

运行以下命令验证：

```powershell
# 检查 idf.py
idf.py --version

# 检查工具链
xtensa-esp32-elf-gcc --version
xtensa-esp32s3-elf-gcc --version

# 检查 Python 包
pip list | findstr esp-idf
```

## 使用 menuconfig

### 1. 设置目标芯片

```powershell
# 对于 ESP32-S3
idf.py set-target esp32s3

# 对于 ESP32-C3
idf.py set-target esp32c3

# 对于 ESP32-P4
idf.py set-target esp32p4
```

### 2. 打开配置菜单

```powershell
idf.py menuconfig
```

这会打开一个基于 ncurses 的文本界面菜单。

### 3. 导航菜单

- **方向键**：上下左右移动
- **Enter**：进入子菜单或选择选项
- **Esc**：返回上一级菜单
- **/ 或 ?**：搜索配置项
- **S**：保存配置
- **Q**：退出（会提示保存）

### 4. 配置 OTA URL

在 menuconfig 中：

1. 导航到：`Xiaozhi Assistant` → `Default OTA URL`
2. 按 Enter 编辑
3. 输入你的 OTA URL，例如：`https://your-server.com/ota/`
4. 保存并退出

### 5. 编译和烧录

```powershell
# 编译
idf.py build

# 烧录（替换 COM3 为你的串口）
idf.py -p COM3 flash

# 编译并烧录
idf.py -p COM3 build flash
```

## 方法三：使用 VSCode/Cursor ESP-IDF 插件（最简单）

### 1. 安装插件

在 VSCode 或 Cursor 中：

1. 打开扩展市场
2. 搜索 "ESP-IDF"
3. 安装 "Espressif IDF" 插件

### 2. 配置插件

1. 按 `F1` 打开命令面板
2. 输入 "ESP-IDF: Configure ESP-IDF extension"
3. 选择 ESP-IDF 安装路径（如果已安装）
4. 或者让插件自动下载和安装

### 3. 使用插件

插件会自动：
- 设置环境变量
- 提供 `idf.py menuconfig` 的图形界面
- 提供编译、烧录按钮
- 提供串口监视器

## 常见问题

### Q: 提示 "idf.py 不是内部或外部命令"

**A**: 需要先运行 ESP-IDF 环境脚本：

```powershell
# 找到你的 ESP-IDF 安装路径，然后运行
C:\Espressif\esp-idf\export.ps1
```

### Q: PowerShell 执行策略错误

**A**: 以管理员身份运行 PowerShell，然后：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: Python 找不到

**A**: 
1. 确保安装 Python 时勾选了 "Add Python to PATH"
2. 或者手动添加到 PATH 环境变量
3. 重启终端

### Q: menuconfig 界面显示乱码

**A**: 
1. 确保终端支持 UTF-8
2. 使用 Windows Terminal 而不是 CMD
3. 或者使用 VSCode/Cursor 的 ESP-IDF 插件（图形界面）

### Q: 如何永久设置环境变量？

**A**: 可以创建一个批处理文件：

**`setup_idf.bat`**:
```batch
@echo off
call C:\Espressif\esp-idf\export.bat
cd /d D:\AIprojects\xiaozhi-esp32
```

每次打开新的终端时运行：
```cmd
setup_idf.bat
```

## 快速检查清单

- [ ] Python 3.8+ 已安装
- [ ] Git 已安装
- [ ] ESP-IDF 已下载/安装
- [ ] ESP-IDF 工具已安装（运行 install.bat）
- [ ] 已运行 export.ps1/export.bat
- [ ] `idf.py --version` 可以运行
- [ ] 已设置目标芯片（`idf.py set-target esp32s3`）

## 下一步

配置完成后，你可以：

1. 运行 `idf.py menuconfig` 配置项目
2. 运行 `idf.py build` 编译项目
3. 运行 `idf.py -p COM3 flash` 烧录固件

## 参考链接

- [ESP-IDF 官方文档](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/)
- [Windows 安装指南](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/windows-setup.html)
- [VSCode ESP-IDF 插件](https://github.com/espressif/vscode-esp-idf-extension)






