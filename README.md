# Papers with Code 数据分析项目

## 项目背景

2025年7月，Papers with Code 网站停止服务。本项目紧急保存并分析了该网站的核心数据，包括计算机视觉、自然语言处理、音频等领域的任务的信息。

This template is a commonly used template of the World Snapshot Organization. It is derived from [this link](https://github.com/World-Snapshot/doc):

> This is a website template that needs to be rendered by the server, so if you want to modify and view it in real time, you can't do it like html, but use one of vscode's plug-ins: Live Server (by Ritwick Dey). Similar local server plug-in should also work.
>
> CC BY-SA 4.0: Feel free to use this template, but please keep the Powered by [World Snapshot Doc](https://github.com/World-Snapshot/doc).

## 数据来源

### 原始数据文件（位于 `data/` 目录）

1. **datasets.json.gz** (来源：Papers with Code 官方数据导出)
   - 包含所有数据集的详细信息
   - 每个数据集关联的任务列表
   - 数据集的描述、论文链接等元数据

2. **evaluation-tables.json.gz** (来源：Papers with Code 官方数据导出)
   - 包含任务的评估表格
   - 任务的层级关系（父任务-子任务）
   - 基准测试信息
   - SOTA（State of the Art）指标

3. **methods.json.gz** (来源：Papers with Code 官方数据导出)
   - 包含各种方法/算法的信息

4. **all_tasks.txt**
   - 从datasets.json提取的所有任务名称列表
   - 共3,722个独特任务

### 第三方仓库（位于 `repositories/` 目录）

1. **paperswithcode-client-develop**
   - Papers with Code 的官方 Python 客户端
   - 用于通过 API 访问 PWC 数据
   - 包含数据模型定义

2. **paperswithcode-data-master**
   - PWC 数据仓库的说明文档
   - 包含数据下载链接

3. **sota-extractor-master**
   - 用于提取 SOTA 结果的工具
   - 包含一些特定任务的数据

## 数据处理脚本（位于 `scripts/` 目录）

1. **classify_tasks.py**
   - 将任务按领域分类（CV、NLP、Audio、Other）
   - 统计每个任务的数据集数量
   - 生成基础的任务分类CSV文件

2. **extract_detailed_tasks.py**
   - 提取任务的详细信息
   - 包括：数据集、基准、SOTA指标、子任务、描述等
   - 生成详细的任务信息CSV文件

3. **analyze_pwc_client.py**
   - 分析任务的层级关系
   - 统计研究领域分布
   - 生成任务层级和研究领域CSV文件

## 输出结果（位于 `results/` 目录）

### 简单任务列表（按数据集数量排序）
- **cv_tasks.csv** - 1,947个计算机视觉任务
- **nlp_tasks.csv** - 999个自然语言处理任务
- **audio_tasks.csv** - 31个音频处理任务
- **other_tasks.csv** - 744个其他领域任务

### 详细任务信息（包含数据集、基准、指标等）
- **cv_tasks_detailed.csv** - 2,275个CV任务的详细信息
- **nlp_tasks_detailed.csv** - 1,093个NLP任务的详细信息
- **audio_tasks_detailed.csv** - 40个音频任务的详细信息
- **other_tasks_detailed.csv** - 1,043个其他任务的详细信息
- **all_tasks_detailed.csv** - 所有任务的汇总信息

### 任务关系和分类
- **task_hierarchy.csv** - 766个任务的父子关系和层级深度
- **research_areas.csv** - 16个研究领域的任务分类

## 主要发现

1. **任务总数**：4,451个独特任务（从evaluation-tables统计）

2. **任务分布**：
   - 计算机视觉占主导地位（约51%）
   - 自然语言处理次之（约25%）
   - 其余为医疗、方法论、时间序列等领域

3. **任务层级**：
   - 最深达6层（如3D相关任务）
   - Object Detection拥有最多子任务（39个）

4. **评估指标**：
   - 共3,468种不同的评估指标
   - Accuracy是最常用的指标（9,307次）

## 关于客户端的持久性

**paperswithcode-client** 是一个开源的Python包：
- 代码已经下载到本地，即使官方停止维护也能继续使用
- 但是客户端依赖于PWC的API服务
- 如果PWC的API服务器关闭，客户端将无法获取在线数据
- 建议：定期备份已下载的数据文件，不要依赖在线服务

## 使用建议

1. **查找特定任务**：在对应领域的CSV文件中搜索
2. **了解任务关系**：查看task_hierarchy.csv
3. **探索研究领域**：查看research_areas.csv
4. **获取基准信息**：在detailed CSV文件中查看Benchmarks列

## 数据更新

由于Papers with Code已停止服务，这些数据代表了网站关闭前的最后状态。建议妥善保存这些数据作为历史记录。

---
*数据收集日期：2025年7月*  
*数据处理：使用Python脚本自动化处理*