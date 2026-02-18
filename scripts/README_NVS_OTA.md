# 在烧录时修改 NVS 中的 OTA 地址

## 概述

OTA URL 存储在 NVS (Non-Volatile Storage) 的 `wifi` 命名空间中，键名为 `ota_url`。如果 NVS 中没有存储，系统会使用编译时的 `CONFIG_OTA_URL` 作为默认值。

## 方法一：使用脚本自动生成（推荐）

### 1. 安装依赖

确保已安装 ESP-IDF 或相关工具：

```bash
# 如果使用 ESP-IDF
export IDF_PATH=/path/to/esp-idf

# 或者安装 Python 依赖
pip install pyserial esptool
```

### 2. 生成 NVS 分区镜像

```bash
# 生成包含自定义 OTA URL 的 NVS 镜像
python scripts/generate_nvs_with_ota.py \
    --ota-url "https://your-server.com/ota/" \
    --output nvs_ota.bin

# 或者直接生成并烧录
python scripts/generate_nvs_with_ota.py \
    --ota-url "https://your-server.com/ota/" \
    --flash \
    --port COM3
```

### 3. 烧录 NVS 分区

如果只生成了镜像文件，可以使用以下命令烧录：

```bash
# 使用 esptool.py
esptool.py --port COM3 write_flash 0x9000 nvs_ota.bin

# 或者使用 idf.py (需要先配置)
idf.py -p COM3 flash
```

## 方法二：手动使用 ESP-IDF NVS 工具

### 1. 创建 CSV 文件

创建 `nvs_data.csv` 文件：

```csv
key,type,encoding,value
ota_url,namespace,,
ota_url,data,string,https://your-server.com/ota/
```

### 2. 生成 NVS 分区镜像

```bash
# 使用 ESP-IDF 的 nvs_partition_gen.py
python $IDF_PATH/components/nvs_flash/nvs_partition_gen/nvs_partition_gen.py \
    generate nvs_ota.bin 16 nvs_data.csv
```

参数说明：
- `nvs_ota.bin`: 输出的 NVS 分区镜像文件名
- `16`: NVS 分区大小（KB），根据分区表配置（通常是 16KB）
- `nvs_data.csv`: 输入的 CSV 数据文件

### 3. 烧录 NVS 分区

```bash
esptool.py --port COM3 write_flash 0x9000 nvs_ota.bin
```

## 方法三：在编译时配置默认值

### 1. 使用 menuconfig

```bash
idf.py menuconfig
```

导航到：
```
Xiaozhi Assistant -> Default OTA URL
```

输入你的 OTA URL，例如：`https://your-server.com/ota/`

### 2. 编译和烧录

```bash
idf.py build flash
```

**注意**：这种方法设置的是默认值，如果 NVS 中已有 `ota_url`，会优先使用 NVS 中的值。

## 方法四：运行时修改（设备已运行）

如果设备已经在运行，可以通过代码或 API 修改：

```cpp
Settings settings("wifi", true);
settings.SetString("ota_url", "https://your-server.com/ota/");
```

## 分区信息

根据 `partitions/v2/16m.csv`，NVS 分区信息：
- **名称**: `nvs`
- **偏移地址**: `0x9000`
- **大小**: `0x4000` (16KB)

## 验证

烧录后，可以通过以下方式验证：

1. **查看日志**：设备启动时会打印 OTA URL
2. **检查 NVS**：使用 `nvs_dump.py` 工具查看 NVS 内容

```bash
python $IDF_PATH/components/nvs_flash/nvs_partition_gen/nvs_dump.py nvs_ota.bin
```

## 常见问题

### Q: 如何清除 NVS 中的 OTA URL？

A: 可以擦除整个 NVS 分区：

```bash
esptool.py --port COM3 erase_region 0x9000 0x4000
```

或者使用设备上的复位按钮（如果支持）。

### Q: NVS 分区大小不够怎么办？

A: 需要修改分区表文件（`partitions/v2/*.csv`），增加 NVS 分区大小，然后重新编译。

### Q: 如何批量烧录？

A: 可以先生成 NVS 镜像文件，然后在批量烧录时包含此文件：

```bash
# 生成 NVS 镜像
python scripts/generate_nvs_with_ota.py --ota-url "https://your-server.com/ota/" --output nvs_ota.bin

# 批量烧录脚本
for port in COM3 COM4 COM5; do
    esptool.py --port $port write_flash 0x9000 nvs_ota.bin
done
```

## 参考

- [ESP-IDF NVS 文档](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/storage/nvs_flash.html)
- [NVS 分区生成工具](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/storage/nvs_partition_gen.html)






