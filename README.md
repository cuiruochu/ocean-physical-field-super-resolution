# CMEMS Wave Download

这个项目现在已经接好了 `copernicusmarine`，可以直接下载下面两个产品里这 3 个变量：

- `GLOBAL_ANALYSISFORECAST_WAV_001_027`
- `GLOBAL_MULTIYEAR_WAV_001_032`
- 变量固定为 `VMDR`、`VTM10`、`VHM0`

哥白尼海洋产品官网下载入口：

- [Copernicus Marine Products](https://data.marine.copernicus.eu/products)

实际下载使用的 dataset id 是：

- `GLOBAL_ANALYSISFORECAST_WAV_001_027`
- `GLOBAL_MULTIYEAR_WAV_001_032`

默认的下载路径：
- .\downloads
- 确保不要携带中文路径，否则可能会失败

## 用法

下面示例命令统一使用这组默认参数：

- 账号：`rcui1`
- 密码：`Cuiruochu1`
- 最小纬度：`0`
- 最大纬度：`45`
- 最小经度：`105`
- 最大经度：`135`
- 开始时间：`2026-01-01T00:00:00`
- 结束时间：`2026-05-01T00:00:00`

`cmd`:

```cmd
set CMEMS_USERNAME=rcui1
set CMEMS_PASSWORD=Cuiruochu1
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
$env:CMEMS_USERNAME="rcui1"
$env:CMEMS_PASSWORD="Cuiruochu1"
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
export CMEMS_USERNAME="rcui1"
export CMEMS_PASSWORD="Cuiruochu1"
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
  --username "rcui1" `
  --password "Cuiruochu1" `
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
- 默认下载目录是项目下的 `./downloads`
- 如果传入 `--output-dir`，文件会下载到你指定的目录
- 脚本执行成功后，会在终端打印每个文件的实际完整路径

默认文件名格式如下：

```text
analysisforecast_开始时间_结束时间_lon最小经度_最大经度_lat最小纬度_最大纬度.nc
multiyear_开始时间_结束时间_lon最小经度_最大经度_lat最小纬度_最大纬度.nc
```

例如：

```text
./downloads/analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45.nc
./downloads/multiyear_20260101T000000_20260501T000000_lon105_135_lat0_45.nc
```

## 可选参数

- `--username`：CMEMS 用户名，也可用环境变量 `CMEMS_USERNAME`
- `--password`：CMEMS 密码，也可用环境变量 `CMEMS_PASSWORD`
- `--overwrite`：覆盖已有文件
- `--skip-existing`：目标文件已存在时跳过
- `--dry-run`：只检查请求，不实际下载
- `--no-progress`：关闭进度条

## NC 转 NPY

脚本 `./scripts/split_nc_to_npy.py`，用于把某个 `.nc` 文件按时间维切分成一批 `.npy` 文件。

- 每个 `.npy` 文件对应一个时间点和一个变量
- 文件名格式是 `2026-01-01T00.npy`
- 数据统一转换为 `float32`
- 原始缺失值会继续保留为 `NaN`
- 默认输出目录是项目下的 `./data`，最终会自动拼接成 `./data/nc文件名/变量名/`
- 每个 `.npy` 文件的 shape 是 `(纬度数, 经度数)`
- 当前变量目录会按 `VMDR`、`VTM10`、`VHM0` 分开保存

例如输入文件：

```text
./downloads/analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45.nc
```

默认会输出到：

```text
./data/analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45/
```

其中目录结构类似：

```text
./data/analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45/
  VMDR/
    2025-12-31T18.npy
    2025-12-31T21.npy
  VTM10/
    2025-12-31T18.npy
    2025-12-31T21.npy
  VHM0/
    2025-12-31T18.npy
    2025-12-31T21.npy
```

`pwsh` 示例：

```powershell
uv run python .\scripts\split_nc_to_npy.py `
  .\downloads\analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45.nc
```

指定输出根目录时，仍然会自动拼接 `nc` 文件名：

```powershell
uv run python .\scripts\split_nc_to_npy.py `
  .\downloads\analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45.nc `
  --output-dir .\my_npy_data
```

上面这条命令最终会输出到：

```text
./my_npy_data/analysisforecast_20260101T000000_20260501T000000_lon105_135_lat0_45/
```

# ERA5

## 下载 ERA5 数据
ERA5 数据集下载地址：

- [ERA5 single levels dataset](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=download)

这里不使用欧洲中期天气预报中心提供的 SDK 下载。原因是 ERA5 这类数据集通常涉及排队、审核等流程，使用 SDK 下载不够直接，因此这里采用“在官网手动下载 `.nc` 文件，再用本项目脚本切分”的方式。

## NC 转 NPY
ERA5 的 `nc` 文件和哥白尼海事中心下载的 `nc` 文件结构不同，主要区别是时间维名字是 `valid_time`，不是 `time`。因此这里单独提供一个 ERA5 专用切分脚本：

- `./scripts/split_era5_nc_to_npy.py`

这个脚本的输出路径结构和哥白尼脚本保持一致：

```text
./data/ERA5的nc文件名/变量名/时间.npy
```

例如当前下载文件：

```text
./downloads/df44a36af69b40d1e1fa386759c08acc.nc
```

ERA5 文件中的变量是：

- `mwd`
- `mwp`
- `swh`

默认输出会类似：

```text
./data/df44a36af69b40d1e1fa386759c08acc/
  mwd/
    2026-01-01T00.npy
    2026-01-01T01.npy
  mwp/
    2026-01-01T00.npy
    2026-01-01T01.npy
  swh/
    2026-01-01T00.npy
    2026-01-01T01.npy
```

每个 `.npy` 文件的特点：

- 对应一个时间点和一个变量
- shape 是 `(纬度数, 经度数)`
- dtype 是 `float32`
- 缺失值仍然保留为 `NaN`

`pwsh` 示例：

```powershell
uv run python .\scripts\split_era5_nc_to_npy.py `
  .\downloads\df44a36af69b40d1e1fa386759c08acc.nc
```

指定输出根目录时，仍然会自动拼接 `nc` 文件名：

```powershell
uv run python .\scripts\split_era5_nc_to_npy.py `
  .\downloads\df44a36af69b40d1e1fa386759c08acc.nc `
  --output-dir .\my_era5_data
```
