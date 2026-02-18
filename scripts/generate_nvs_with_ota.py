#!/usr/bin/env python3
"""
生成包含 OTA URL 的 NVS 分区镜像

使用方法:
    python scripts/generate_nvs_with_ota.py --ota-url "https://your-server.com/ota/" --output nvs.bin

或者直接烧录:
    python scripts/generate_nvs_with_ota.py --ota-url "https://your-server.com/ota/" --flash
"""

import argparse
import os
import sys
import subprocess
import tempfile
import csv

def find_nvs_partition_gen():
    """查找 nvs_partition_gen.py 工具"""
    # 尝试从环境变量获取
    idf_path = os.environ.get('IDF_PATH')
    if idf_path:
        nvs_tool = os.path.join(idf_path, 'components', 'nvs_flash', 'nvs_partition_gen', 'nvs_partition_gen.py')
        if os.path.exists(nvs_tool):
            return nvs_tool
    
    # 尝试从当前 Python 环境查找
    try:
        import esptool
        # 如果安装了 esptool，尝试查找 nvs_partition_gen
        esptool_path = os.path.dirname(esptool.__file__)
        nvs_tool = os.path.join(os.path.dirname(esptool_path), 'nvs_partition_gen', 'nvs_partition_gen.py')
        if os.path.exists(nvs_tool):
            return nvs_tool
    except ImportError:
        pass
    
    # 尝试使用 idf.py 查找
    try:
        result = subprocess.run(['idf.py', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            # 尝试从常见路径查找
            common_paths = [
                os.path.expanduser('~/.espressif/esp-idf/components/nvs_flash/nvs_partition_gen/nvs_partition_gen.py'),
                '/opt/esp/idf/components/nvs_flash/nvs_partition_gen/nvs_partition_gen.py',
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
    except:
        pass
    
    return None

def create_nvs_csv(ota_url, output_csv):
    """创建 NVS CSV 文件"""
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        # 写入 CSV 头部
        writer.writerow(['key', 'type', 'encoding', 'value'])
        # 写入命名空间
        writer.writerow(['wifi', 'namespace', '', ''])
        # 写入 OTA URL
        writer.writerow(['ota_url', 'data', 'string', ota_url])
    
    print(f"✓ 创建 NVS CSV 文件: {output_csv}")
    print(f"  - OTA URL: {ota_url}")

def generate_nvs_bin(nvs_tool, csv_file, output_bin, size_kb=16):
    """生成 NVS 分区镜像"""
    cmd = [
        sys.executable,
        nvs_tool,
        'generate',
        output_bin,
        str(size_kb),
        csv_file
    ]
    
    print(f"\n生成 NVS 分区镜像...")
    print(f"命令: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"✗ 生成失败:")
        print(result.stderr)
        return False
    
    print(f"✓ 成功生成 NVS 分区镜像: {output_bin}")
    print(f"  大小: {size_kb}KB")
    return True

def flash_nvs_bin(port, nvs_bin, offset=0x9000):
    """烧录 NVS 分区到设备"""
    esptool_cmd = [
        'esptool.py',
        '--port', port,
        '--baud', '921600',
        'write_flash',
        hex(offset),
        nvs_bin
    ]
    
    print(f"\n烧录 NVS 分区到设备...")
    print(f"端口: {port}")
    print(f"偏移: {hex(offset)}")
    print(f"文件: {nvs_bin}")
    
    result = subprocess.run(esptool_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"✗ 烧录失败:")
        print(result.stderr)
        return False
    
    print(f"✓ 成功烧录 NVS 分区")
    return True

def main():
    parser = argparse.ArgumentParser(
        description='生成包含 OTA URL 的 NVS 分区镜像',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 仅生成 NVS 镜像文件
  python scripts/generate_nvs_with_ota.py --ota-url "https://api.example.com/ota/" --output nvs.bin
  
  # 生成并烧录到设备
  python scripts/generate_nvs_with_ota.py --ota-url "https://api.example.com/ota/" --flash --port COM3
  
  # 使用默认 OTA URL (从 CONFIG_OTA_URL)
  python scripts/generate_nvs_with_ota.py --output nvs.bin
        """
    )
    
    parser.add_argument(
        '--ota-url',
        type=str,
        default='',
        help='OTA 服务器 URL (例如: https://api.example.com/ota/)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='nvs_ota.bin',
        help='输出的 NVS 分区镜像文件名 (默认: nvs_ota.bin)'
    )
    
    parser.add_argument(
        '--size',
        type=int,
        default=16,
        help='NVS 分区大小 (KB, 默认: 16)'
    )
    
    parser.add_argument(
        '--flash',
        action='store_true',
        help='生成后直接烧录到设备'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=str,
        default='',
        help='串口端口 (例如 COM3 或 /dev/ttyUSB0)'
    )
    
    parser.add_argument(
        '--offset',
        type=str,
        default='0x9000',
        help='NVS 分区在 Flash 中的偏移地址 (默认: 0x9000)'
    )
    
    args = parser.parse_args()
    
    # 如果没有提供 OTA URL，尝试从环境变量或配置读取
    ota_url = args.ota_url
    if not ota_url:
        # 尝试从环境变量读取
        ota_url = os.environ.get('OTA_URL', '')
        if not ota_url:
            # 使用默认值
            ota_url = 'https://api.tenclass.net/xiaozhi/ota/'
            print(f"⚠ 未指定 OTA URL，使用默认值: {ota_url}")
    
    # 查找 nvs_partition_gen.py 工具
    nvs_tool = find_nvs_partition_gen()
    if not nvs_tool:
        print("✗ 错误: 找不到 nvs_partition_gen.py 工具")
        print("\n请确保:")
        print("1. 已安装 ESP-IDF 并设置了 IDF_PATH 环境变量")
        print("2. 或者已安装 esptool 和相关工具")
        print("\n也可以手动安装:")
        print("  pip install nvs-partition-gen")
        return 1
    
    print(f"✓ 找到 NVS 工具: {nvs_tool}")
    
    # 创建临时 CSV 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_csv:
        csv_file = tmp_csv.name
        create_nvs_csv(ota_url, csv_file)
    
    try:
        # 生成 NVS 分区镜像
        if not generate_nvs_bin(nvs_tool, csv_file, args.output, args.size):
            return 1
        
        # 如果需要烧录
        if args.flash:
            port = args.port
            if not port:
                # 尝试自动检测端口
                try:
                    import serial.tools.list_ports
                    ports = list(serial.tools.list_ports.comports())
                    if ports:
                        port = ports[0].device
                        print(f"✓ 自动检测到端口: {port}")
                    else:
                        print("✗ 错误: 未找到串口设备")
                        return 1
                except ImportError:
                    print("✗ 错误: 需要指定 --port 参数")
                    print("  安装 pyserial 可以自动检测: pip install pyserial")
                    return 1
            
            offset = int(args.offset, 16)
            if not flash_nvs_bin(port, args.output, offset):
                return 1
        
        print("\n" + "="*50)
        print("✓ 完成!")
        print(f"  NVS 镜像文件: {args.output}")
        if args.flash:
            print(f"  已烧录到设备: {port}")
        else:
            print(f"\n要烧录此文件，可以使用:")
            print(f"  esptool.py --port <PORT> write_flash {args.offset} {args.output}")
            print(f"\n或者使用 idf.py:")
            print(f"  idf.py -p <PORT> flash")
            print(f"  然后在 menuconfig 中配置 NVS 分区文件")
        print("="*50)
        
        return 0
        
    finally:
        # 清理临时文件
        if os.path.exists(csv_file):
            os.unlink(csv_file)

if __name__ == '__main__':
    sys.exit(main())

