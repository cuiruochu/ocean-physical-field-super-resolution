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
- 开始时间：`2026-01-01T00:00:00Z`
- 结束时间：`2026-05-01T00:00:00Z`

下载脚本中的时间参数必须使用带 `Z` 的 UTC 时间格式，例如 `2026-01-01T00:00:00Z`。

`cmd`:

```cmd
set CMEMS_USERNAME=rcui1
set CMEMS_PASSWORD=Cuiruochu1
uv run python .\scripts\download_cmems_waves.py ^
  --min-lon 105 ^
  --max-lon 135 ^
  --min-lat 0 ^
  --max-lat 45 ^
  --start 2026-01-01T00:00:00Z ^
  --end 2026-05-01T00:00:00Z ^
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
  --start 2026-01-01T00:00:00Z `
  --end 2026-05-01T00:00:00Z `
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
  --start 2026-01-01T00:00:00Z \
  --end 2026-05-01T00:00:00Z \
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
  --start 2026-01-01T00:00:00Z `
  --end 2026-05-01T00:00:00Z
```

只下载其中一个产品时：

```powershell
uv run python .\scripts\download_cmems_waves.py `
  --products GLOBAL_MULTIYEAR_WAV_001_032 `
  --min-lon 105 `
  --max-lon 135 `
  --min-lat 0 `
  --max-lat 45 `
  --start 2026-01-01T00:00:00Z `
  --end 2026-05-01T00:00:00Z
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

# ERA5 与哥白尼变量对应关系

如果从变量定义上看，ERA5 中这三个变量和哥白尼海事中心波浪产品中的三个变量是可以对应上的：

- `swh` ↔ `VHM0`
- `mwp` ↔ `VTM10`
- `mwd` ↔ `VMDR`

其中：

- `swh` 和 `VHM0` 都对应总显著波高
- `mwp` 和 `VTM10` 都对应平均波周期
- `mwd` 和 `VMDR` 都对应平均波向

所以从“变量类别和物理意义”上说，这三组是可以对应的。

最后还要注意，即使在定义上可以对应，ERA5 和哥白尼海事中心产品本身的模型、空间分辨率、时间分辨率、同化方案都不同，因此数值结果肯定不会完全相同。

# ERA5 与哥白尼数据的时空对齐

ERA5 和哥白尼海事中心数据在后续进行对比、融合或建模之前，需要先做好时空对齐。

## 空间对齐

空间对齐的第一步，是在下载数据时就指定一致的经纬度范围。

- 下载 ERA5 数据时，需要指定目标经纬度范围
- 下载哥白尼海事中心数据时，也需要指定同样的经纬度范围

这样在两套数据切分成 `npy` 之后，二者才会覆盖同一个地理区域。

### 经纬度对齐

即使下载时指定了相同的经纬度范围，ERA5 和哥白尼海事中心数据在数组中的经纬度排列顺序也不完全相同。

下面这两张图，使用的是同一个时间点下的同类型变量：

- ERA5：`swh`
- 哥白尼海事中心：`VHM0`

对应图片如下：

![CMEMS VHM0](./images/cmems_vhm0_2026-01-01T00.png)

![ERA5 swh](./images/era5_swh_2026-01-01T00.png)

从原始 `nc` 文件中的坐标可以确认：

- 哥白尼海事中心数据的数组 `[0,0]` 对应最小纬度、最小经度
- ERA5 数据的数组 `[0,0]` 对应最大纬度、最小经度

也就是说，二者在经度方向上是一致的，但在纬度方向上的排列顺序相反。

由于当前单个 `npy` 文件的 shape 是：

- `(纬度数, 经度数)`

因此，如果要让 ERA5 和哥白尼海事中心数据在同一地理朝向下进行比较，就需要对 ERA5 的数组做一次“上下翻转”。

这里的“上下翻转”指的是：

- 沿着数组的第一个维度翻转
- 也就是沿着纬度维度翻转
- 如果按二维数组记法理解，就是对 `H` 这一维翻转，而不是对 `W` 这一维翻转

这样处理之后，ERA5 数组左上角对应的经纬度方向，才能和哥白尼海事中心数据保持一致。

### 数组 shape 对齐

在完成上面的经纬度方向对齐之后，还需要继续关注三类数据的数组 shape。

当前单个 `npy` 文件的 shape 分别是：

- ERA5：`(91, 61)`
- 哥白尼再分析数据：`(225, 151)`
- 哥白尼预报数据：`(541, 361)`

它们的含义都是：

- `(纬度数, 经度数)`

从分辨率上看：

- ERA5 约为 `0.5°`
- 哥白尼预报数据约为 `1/12°`
- 哥白尼再分析数据约为 `0.2°`

因此，在经纬度方向对齐处理好 ERA5 的翻转之后，ERA5 和哥白尼在空间采样密度上还存在整数倍或接近整数倍的关系。

对于哥白尼预报数据：

- ERA5 对应 shape 是 `(91, 61)`
- 哥白尼预报数据对应 shape 是 `(541, 361)`
- 如果把最大纬度和最大经度对应的一行一列裁掉，那么：
- ERA5 会变成 `(90, 60)`
- 哥白尼预报数据会变成 `(540, 360)`
- 此时二者正好是严格的 `6` 倍关系

对于哥白尼再分析数据：

- ERA5 对应 shape 是 `(91, 61)`
- 哥白尼再分析数据对应 shape 是 `(225, 151)`
- 哥白尼再分析数据当前下载结果中的纬度范围是 `0.2°` 到 `45.0°`
- 这意味着它没有像预期那样从 `0.0°` 开始
- 目前可以确认，本项目下载数据集的脚本本身并没有问题；但为什么 CMEMS 再分析数据下载结果是从 `0.2°` 开始，这个原因暂时还不明确

在工程处理上，ERA5 和哥白尼再分析数据进行对齐时，仍然可以采用下面这种方式：

- 在纬度方向上，删除 ERA5 中 `0.0°` 对应的那一行
- 删除最大经度对应的一列

这样处理之后：

- ERA5 纬度会从 `91` 变成 `90`
- 哥白尼再分析数据纬度保持 `225`
- 此时纬度方向正好是严格的 `2.5` 倍关系

同时：

- ERA5 经度会从 `61` 变成 `60`
- 哥白尼再分析数据经度会从 `151` 变成 `150`
- 此时经度方向也正好是严格的 `2.5` 倍关系

因此，在完成经纬度方向对齐之后，这样的裁剪方式在 ERA5 和哥白尼再分析数据之间是可接受的。

### 备注

- 如果同一份 ERA5 数据分别去对齐哥白尼再分析产品和哥白尼预报产品，并且都采用“删除最大经纬度对应的行和列”的方式，那么工程上会出现一个问题：
- 同一份 ERA5 数据需要为了对齐这两个哥白尼产品而做出不同的裁剪处理
- 这会导致需要额外保存两份不同版本的 ERA5 产品

因此，也可以考虑另一种工程处理方案：

- 统一采用“删除最小经纬度对应的行和列”的方式来处理 ERA5

这样做在工程上仍然是可以接受的，并且只需要处理和保留一份 ERA5 产品，后续管理会更简单。

本项目中也提供了一个针对样本 `npy` 文件的处理脚本：

- `./scripts/align_example_npy_shapes.py`

这个脚本会对三个输入样本分别执行约定好的处理，并把结果输出到 `./tmp`，用于得到 shape 已经完成对齐的三个 `npy` 文件。

## 时间对齐

时间对齐的第一步，是在下载数据时指定一致的时间范围。

- 下载 ERA5 数据时，需要指定目标时间范围
- 下载哥白尼海事中心数据时，也需要指定同样的时间范围

但仅仅指定相同的起止时间还不够，因为两套数据的时间分辨率不同：

- 哥白尼海事中心数据当前使用的是 3 小时分辨率
- ERA5 数据当前使用的是 1 小时分辨率

因此，在下载并切分完成之后，还需要在时间维上再取一次交集。

也就是说，后续真正用于比较的时间点，应当是：

- 同时存在于 ERA5 `npy` 文件集合中的时间点
- 同时存在于哥白尼 `npy` 文件集合中的时间点

只有在完成这一步之后，二者在时间上才算真正对齐。
