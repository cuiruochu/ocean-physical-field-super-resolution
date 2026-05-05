# CMEMS Wave Download

这个项目现在已经接好了 `copernicusmarine`，可以直接下载下面两个产品里这 3 个变量：

- `GLOBAL_ANALYSISFORECAST_WAV_001_027`
- `GLOBAL_MULTIYEAR_WAV_001_032`
- 变量固定为 `VMDR`、`VTM10`、`VHM0`

哥白尼海洋产品官网下载入口：

- [Copernicus Marine Products](https://data.marine.copernicus.eu/products)

实际下载使用的 dataset id 是：

- `GLOBAL_ANALYSISFORECAST_WAV_001_027` -> `cmems_mod_glo_wav_anfc_0.083deg_PT3H-i`
- `GLOBAL_MULTIYEAR_WAV_001_032` -> `cmems_mod_glo_wav_my_0.2deg_PT3H-i`

## 用法

下面示例命令统一使用这组默认参数：

- 账号：`1211304813@qq.com`
- 密码：`cuiruochu1`
- 最小纬度：`0`
- 最大纬度：`45`
- 最小经度：`105`
- 最大经度：`135`
- 开始时间：`2026-01-01T00:00:00`
- 结束时间：`2026-05-01T00:00:00`

`cmd`:

```cmd
set CMEMS_USERNAME=1211304813@qq.com
set CMEMS_PASSWORD=cuiruochu1
uv run python .\scripts\download_cmems_waves.py ^
  --min-lon 105 ^
  --max-lon 135 ^
  --min-lat 0 ^
  --max-lat 45 ^
  --start 2026-01-01T00:00:00 ^
  --end 2026-05-01T00:00:00 ^
  --output-dir .\downloads
```

`pwsh`:

```powershell
$env:CMEMS_USERNAME="1211304813@qq.com"
$env:CMEMS_PASSWORD="cuiruochu1"
uv run python .\scripts\download_cmems_waves.py `
  --min-lon 105 `
  --max-lon 135 `
  --min-lat 0 `
  --max-lat 45 `
  --start 2026-01-01T00:00:00 `
  --end 2026-05-01T00:00:00 `
  --output-dir .\downloads
```

`bash`:

```bash
export CMEMS_USERNAME="1211304813@qq.com"
export CMEMS_PASSWORD="cuiruochu1"
uv run python ./scripts/download_cmems_waves.py \
  --min-lon 105 \
  --max-lon 135 \
  --min-lat 0 \
  --max-lat 45 \
  --start 2026-01-01T00:00:00 \
  --end 2026-05-01T00:00:00 \
  --output-dir ./downloads
```

如果你想直接把账号密码写到命令行，也支持：

```powershell
uv run python .\scripts\download_cmems_waves.py `
  --username "1211304813@qq.com" `
  --password "cuiruochu1" `
  --min-lon 105 `
  --max-lon 135 `
  --min-lat 0 `
  --max-lat 45 `
  --start 2026-01-01T00:00:00 `
  --end 2026-05-01T00:00:00
```

只下载其中一个产品时：

```powershell
uv run python .\scripts\download_cmems_waves.py `
  --products GLOBAL_MULTIYEAR_WAV_001_032 `
  --min-lon 105 `
  --max-lon 135 `
  --min-lat 0 `
  --max-lat 45 `
  --start 2026-01-01T00:00:00 `
  --end 2026-05-01T00:00:00
```

## 下载结果

- 下载文件格式是 NetCDF，扩展名为 `.nc`
- 默认下载目录是项目下的 [downloads](<E:\projects\CMEMS\downloads>)，也就是 `E:\projects\CMEMS\downloads`
- 如果传入 `--output-dir`，文件会下载到你指定的目录
- 脚本执行成功后，会在终端打印每个文件的实际完整路径

默认文件名格式如下：

```text
analysisforecast_开始时间_结束时间_lon最小经度_最大经度_lat最小纬度_最大纬度.nc
multiyear_开始时间_结束时间_lon最小经度_最大经度_lat最小纬度_最大纬度.nc
```

例如：

```text
E:\projects\CMEMS\downloads\analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45.nc
E:\projects\CMEMS\downloads\multiyear_20260101T000000_20260501T000000_lon105_135_lat0_45.nc
```

## 可选参数

- `--username`：CMEMS 用户名，也可用环境变量 `CMEMS_USERNAME`
- `--password`：CMEMS 密码，也可用环境变量 `CMEMS_PASSWORD`
- `--overwrite`：覆盖已有文件
- `--skip-existing`：目标文件已存在时跳过
- `--dry-run`：只检查请求，不实际下载
- `--no-progress`：关闭进度条
