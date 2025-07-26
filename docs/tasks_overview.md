# Tasks Overview

Papers With Code organized machine learning research into 4,451 unique tasks across various domains. Each task represents a specific problem that researchers aim to solve.

## Task Distribution

```
Computer Vision         2,275 tasks (51%)
Natural Language        1,093 tasks (25%)
Other Domains          1,043 tasks (23%)
Audio Processing          40 tasks (1%)
```

## Top Tasks by Dataset Count

### Computer Vision
1. **Image Classification** - 346 datasets
2. **Object Detection** - 194 datasets
3. **Semantic Segmentation** - 150 datasets
4. **Image Generation** - 64 datasets
5. **Face Recognition** - 46 datasets

### Natural Language Processing
1. **Language Modelling** - 88 datasets
2. **Machine Translation** - 85 datasets
3. **Question Answering** - 74 datasets
4. **Sentiment Analysis** - 63 datasets
5. **Text Classification** - 61 datasets

### Audio Processing
1. **Speech Recognition** - 39 datasets
2. **Music Generation** - 15 datasets
3. **Speech Synthesis** - 14 datasets
4. **Sound Event Detection** - 12 datasets
5. **Speaker Recognition** - 11 datasets

## Task Hierarchy

Tasks are organized in a hierarchical structure with parent-child relationships. For example:

```
Object Detection
├── 3D Object Detection
├── Face Detection
├── Real-Time Object Detection
├── Weakly Supervised Object Detection
└── 35 more subtasks...
```

## Interactive Data Viewer

To explore the tasks interactively, we provide a web-based viewer that allows you to:

- Search tasks by name or keyword
- Filter by domain (CV, NLP, Audio, etc.)
- View associated datasets and benchmarks
- See SOTA results and progress over time
- Browse task hierarchies

[View Interactive Data Viewer →](../interactive/data_viewer.html)

## CSV Files

For offline analysis, all task data is available in CSV format:

- `results/all_tasks_detailed.csv` - Complete task information
- `results/task_hierarchy.csv` - Parent-child relationships
- `results/research_areas.csv` - Tasks grouped by research area

## Using the Data

### Python Example
```python
import pandas as pd
import gzip
import json

# Load evaluation tables
with gzip.open('data/evaluation-tables.json.gz', 'rt') as f:
    eval_tables = json.load(f)

# Find tasks with most SOTA results
task_sota_counts = {}
for table in eval_tables:
    task = table.get('task', 'Unknown')
    sota_count = 0
    for dataset in table.get('datasets', []):
        if 'sota' in dataset and 'rows' in dataset['sota']:
            sota_count += len(dataset['sota']['rows'])
    task_sota_counts[task] = sota_count

# Top 10 tasks by SOTA entries
top_tasks = sorted(task_sota_counts.items(), key=lambda x: x[1], reverse=True)[:10]
```

## Task Categories

Tasks are grouped into 16 research areas:

1. **Computer Vision** - 2,399 tasks
2. **Natural Language Processing** - 1,149 tasks  
3. **Medical** - 238 tasks
4. **Methodology** - 169 tasks
5. **Audio** - 101 tasks
6. **Miscellaneous** - 96 tasks
7. **Graphs** - 68 tasks
8. **Time Series** - 49 tasks
9. **Speech** - 49 tasks
10. **Adversarial** - 38 tasks
11. **Reinforcement Learning** - 31 tasks
12. **Robots** - 21 tasks
13. **Music** - 20 tasks
14. **Computer Code** - 16 tasks
15. **Knowledge Base** - 5 tasks
16. **Reasoning** - 2 tasks