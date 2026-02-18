# ESP-IDF 环境检查脚本
# 使用方法: .\scripts\check_idf_env.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ESP-IDF 环境检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$all_ok = $true

# 1. 检查 Python
Write-Host "[1] 检查 Python..." -ForegroundColor Yellow
$python_cmd = Get-Command python -ErrorAction SilentlyContinue
if ($python_cmd) {
    $python_version = python --version 2>&1
    Write-Host "  [OK] Python: $python_version" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Python 未找到" -ForegroundColor Red
    Write-Host "    请从 https://www.python.org/downloads/ 下载安装" -ForegroundColor Yellow
    $all_ok = $false
}

# 2. 检查 Git
Write-Host "[2] 检查 Git..." -ForegroundColor Yellow
$git_cmd = Get-Command git -ErrorAction SilentlyContinue
if ($git_cmd) {
    $git_version = git --version 2>&1
    Write-Host "  [OK] Git: $git_version" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Git 未找到" -ForegroundColor Red
    Write-Host "    请从 https://git-scm.com/download/win 下载安装" -ForegroundColor Yellow
    $all_ok = $false
}

# 3. 检查 IDF_PATH
Write-Host "[3] 检查 IDF_PATH 环境变量..." -ForegroundColor Yellow
if ($env:IDF_PATH) {
    Write-Host "  [OK] IDF_PATH: $env:IDF_PATH" -ForegroundColor Green
    if (Test-Path $env:IDF_PATH) {
        Write-Host "  [OK] ESP-IDF 目录存在" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] ESP-IDF 目录不存在: $env:IDF_PATH" -ForegroundColor Red
        $all_ok = $false
    }
} else {
    Write-Host "  [FAIL] IDF_PATH 未设置" -ForegroundColor Red
    Write-Host "    需要先运行 ESP-IDF 的 export.ps1 脚本" -ForegroundColor Yellow
    $all_ok = $false
}

# 4. 检查 idf.py
Write-Host "[4] 检查 idf.py..." -ForegroundColor Yellow
$idf_cmd = Get-Command idf.py -ErrorAction SilentlyContinue
if ($idf_cmd) {
    $idf_version = idf.py --version 2>&1
    Write-Host "  [OK] idf.py 可用" -ForegroundColor Green
    Write-Host "    版本信息: $idf_version" -ForegroundColor Gray
} else {
    Write-Host "  [FAIL] idf.py 未找到" -ForegroundColor Red
    Write-Host "    需要先运行 ESP-IDF 的 export.ps1 脚本" -ForegroundColor Yellow
    $all_ok = $false
}

# 5. 检查工具链
Write-Host "[5] 检查编译工具链..." -ForegroundColor Yellow
$tools = @(
    "xtensa-esp32-elf-gcc",
    "xtensa-esp32s3-elf-gcc",
    "riscv32-esp-elf-gcc"
)

$tools_found = 0
foreach ($tool in $tools) {
    try {
        $result = & $tool --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $tools_found++
        }
    } catch {
        # 工具未找到，继续
    }
}

if ($tools_found -gt 0) {
    Write-Host "  [OK] 找到 $tools_found 个工具链" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] 未找到编译工具链" -ForegroundColor Red
    Write-Host "    需要运行: cd `$IDF_PATH && .\install.bat esp32,esp32s3,esp32c3" -ForegroundColor Yellow
    $all_ok = $false
}

# 6. 检查常见 ESP-IDF 安装路径
Write-Host "[6] 检查常见 ESP-IDF 安装路径..." -ForegroundColor Yellow
$common_paths = @(
    "$env:USERPROFILE\.espressif\frameworks\esp-idf-v*",
    "C:\Espressif\frameworks\esp-idf*",
    "C:\esp\esp-idf*"
)

$found_paths = @()
foreach ($path_pattern in $common_paths) {
    $paths = Get-ChildItem -Path $path_pattern -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($paths) {
        $found_paths += $paths.FullName
    }
}

if ($found_paths.Count -gt 0) {
    Write-Host "  [OK] 找到可能的 ESP-IDF 安装:" -ForegroundColor Green
    foreach ($path in $found_paths) {
        Write-Host "    - $path" -ForegroundColor Gray
    }
} else {
    Write-Host "  [WARN] 未在常见路径找到 ESP-IDF" -ForegroundColor Yellow
    Write-Host "    如果已安装，请手动设置 IDF_PATH 环境变量" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($all_ok) {
    Write-Host "[OK] 环境检查通过！可以运行 idf.py menuconfig" -ForegroundColor Green
    Write-Host ""
    Write-Host "下一步:" -ForegroundColor Cyan
    Write-Host "  1. idf.py set-target esp32s3  # 设置目标芯片" -ForegroundColor White
    Write-Host "  2. idf.py menuconfig           # 打开配置菜单" -ForegroundColor White
} else {
    Write-Host "[FAIL] 环境检查未通过，请解决上述问题" -ForegroundColor Red
    Write-Host ""
    Write-Host "解决方案:" -ForegroundColor Cyan
    Write-Host "  1. 查看文档: docs\setup_idf_windows.md" -ForegroundColor White
    Write-Host "  2. 或使用 ESP-IDF 安装器: https://www.espressif.com/en/support/download/other-tools" -ForegroundColor White
    Write-Host "  3. 或使用 VSCode/Cursor 的 ESP-IDF 插件（最简单）" -ForegroundColor White
}

Write-Host "========================================" -ForegroundColor Cyan

