# FeliX 原生分视图 PySD 模型

已使用 PySD **原生 `split_views=True`** 生成 30 个视图模块，修复草图解析问题，并保留显式 SMOOTH 广播兼容处理。未修改主目录下已有的单文件 MDL/Python，也未改动科学方程或 Total Labor Force 定义。

## 为什么只加 split_views=True 会失败

1. **新增的图形解析失败。** 普通单文件翻译不需要按草图识别视图；开启拆分后，PySD 3.14.3 会解析 sketch。原模型 3 条箭头记录包含多个折点，但当前 `sketch.peg` 的 arrow 规则只接受一个点，实际报错为 `IncompleteParseError`，余下文本包含 `(-295,883)|`。这不是 `warnings.catch_warnings()` 导致的；该上下文也不会捕获解析异常。
2. **另外需要调整后处理的执行顺序。** `read_vensim()` 默认 `initialize=True`，会在函数返回前初始化；原工具却在其返回后才修补生成代码。现改为先翻译不初始化、修补后再加载，保证后处理真正发生在初始化之前。这是流程稳健性调整，不是本次已复现的首个错误。
3. **分视图后兼容修补位置改变。** 原工具只处理入口 `.py`；拆分后两处 dimensioned SMOOTH 代码位于 `modules_FeliX3_ISE_v26_final_fixed/extreme_events.py`，因此扫描模块目录一起处理。**本次 xarray 2026.7.0 能自动广播，恢复未修补模块后加载也通过，未复现 SMOOTH 维度错误。** 显式广播与此环境原行为一致，不应将它写成当前环境必然报错的原因；其他环境仍需实测。

因此，**本次实际失败的直接原因是第 1 项**，不是 `split_views=True` 不受支持。单独改成 `initialize=False` 仍不能绕过草图解析错误；如果要保留原工具的生成代码兼容修补，就应一起调整第 2、3 项。

## 当前工具的处理流程

`felix_mdl_tool_split_view_version.py` 默认输出位置已改为本文件夹，原脚本备份为同目录的 `felix_mdl_tool_split_view_version.py.before_native_split.bak`。

1. 执行原有方程修复，或用 `--already-repaired` 读取现有已修复 MDL。
2. 仅在输出副本中规范 3 条多折点箭头，保留第一个点；保留变量名及视图归属，并逐字符确认草图处理不改方程区。具体修改保存为 `*.sketch_changes.json`。该副本用于 PySD 翻译，不承诺 Vensim 图形布局往返保真。
3. 调用 `pysd.read_vensim(..., split_views=True, initialize=False)` 原生生成模块。
4. 扫描入口和所有模块，修补两处 SMOOTH 标量广播，然后重新 `pysd.load()` 验证初始化。
5. 保存转换警告、构建元信息和短程数值对照结果。

官方说明：[原生视图拆分](https://pysd.readthedocs.io/en/master/advanced_usage.html#splitting-vensim-views-in-separate-python-files-modules)、[initialize 与 split_views 参数](https://pysd.readthedocs.io/en/v3.13.4/python_api/model_loading.html)。

## 文件结构

```text
native_split_views/
  FeliX3_ISE_v26_final_fixed.py              # 加载入口
  FeliX3_ISE_v26_final_fixed.mdl             # 翻译用 MDL 副本
  _subscripts_FeliX3_ISE_v26_final_fixed.json
  modules_FeliX3_ISE_v26_final_fixed/
    _modules.json
    population.py
    economy_gdp.py
    extreme_events.py
    ...                                    # 共 30 个 .py 模块
  run_model.py                             # 可直接运行的示例
  validate_native_split_views.py           # 失败复现和数值对照
  validation_results.json
```

**入口、JSON、整个模块目录必须一起保留。** 视图模块由 PySD 在共享模型上下文中加载，不适合单独执行 `population.py` 等文件。

## 如何重建

在 `1_felix-pysd` 目录下使用模型所需环境执行：

```powershell
$python = (Get-Command python).Source
# 从原始待修复输入执行完整流程，默认输出到本文件夹：
& $python .\felix_mdl_tool_split_view_version.py
# 或直接使用已有已修复 MDL：
& $python .\felix_mdl_tool_split_view_version.py --src .\output\FeliX3_ISE_v26_final_fixed.mdl --already-repaired
```

`--already-repaired` 会跳过不适合重复应用的方程替换规则。不要把已修复文件当成未修复输入反复套用原规则。

## 如何运行

```powershell
python .\output\native_split_views\run_model.py
# 完整运行到 2100 年：
python .\output\native_split_views\run_model.py --final-time 2100
```

默认只测试 1900–1902；`--final-time 2100` 会保留 dt=0.125 执行完整运行。示例结果写入本文件夹的 `example_results.csv`。

Notebook 使用方式（在 `1_felix-pysd` 目录）：

```python
from pathlib import Path
import pysd
model = pysd.load(Path('output/native_split_views/FeliX3_ISE_v26_final_fixed.py'))
result = model.run(return_columns=['Population','Gross World Product'],
                   final_time=1902, time_step=0.125,
                   return_timestamps=[1900,1901,1902], cache_output=False)
```

## 验证及限制

在 PySD 3.14.3 下验证加载、初始化，以及 1900–1902、dt=0.125 的 8 项核心变量（含人口年龄张量，共展开为 49 列）与原单文件模型逐项一致。详细结果见 `validation_results.json`。

验证程序复现了原草图解析失败，并在独立临时副本中检查未修补 SMOOTH 的加载行为；当前环境该项成功，结果记录在 `checks.unpatched_smooth_initialization.returned=true`。`*.py.before_smooth.txt` 保留生成模块修补前的原文，仅用于兼容性复核，不参与模型加载。短程两版均为有限值，最大绝对差为 0；原始文件哈希保持不变。

**这解决的是拆分、加载及初始化兼容问题，不会修复此前报告的 6 个 YoGL/生命表递归函数。** 请显式指定已验证输出，避免默认请求全部变量。拆分本身不会自动加速仿真。此次未重跑全程和所有情景，也未改变 Total Labor Force 的原始 skill-only 定义。
