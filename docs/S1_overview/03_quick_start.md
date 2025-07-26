# Quick Start Guide

This guide helps you quickly navigate and use the Papers With Code archive.

## 1. Finding What You Need

### 1.1 Browse by Research Area
Navigate through 17 research areas in the left sidebar:
- **Computer Vision** (865 tasks)
- **Natural Language Processing** (436 tasks)
- **Medical** (190 tasks)
- **And 14 more areas...**

### 1.2 Search for Specific Tasks
1. Open the [Interactive Data Viewer](../../interactive/data_viewer.html)
2. Use the search box to find tasks
3. Filter by domain (CV, NLP, Audio, etc.)

### 1.3 Explore Datasets
- Browse 15,008 datasets in `data/datasets.json.gz`
- View popular datasets by task
- Check dataset metadata and associated papers

## 2. Understanding the Data Structure

### 2.1 Raw Data Files
```
data/
├── datasets.json.gz          # 15,008 datasets
├── evaluation-tables.json.gz  # SOTA results & benchmarks
├── methods.json.gz           # 8,725 algorithms
├── papers-with-abstracts.json.gz  # 576,261 papers
└── links-between-papers-and-code.json.gz  # 300,161 code links
```

### 2.2 Processed CSV Files
```
results/
├── all_tasks_detailed.csv    # All 4,451 tasks
├── task_hierarchy.csv        # Parent-child relationships
├── research_areas.csv        # 17 research areas
└── [domain]_tasks.csv        # Domain-specific lists
```

## 3. Common Use Cases

### 3.1 Find SOTA Results for a Task
```python
import json
import gzip

# Load evaluation tables
with gzip.open('data/evaluation-tables.json.gz', 'rt') as f:
    tables = json.load(f)

# Find specific task
task_name = "Image Classification"
for table in tables:
    if table.get('task') == task_name:
        print(f"Found {len(table['datasets'])} benchmarks")
```

### 3.2 Browse Tasks by Domain
```python
import pandas as pd

# Load computer vision tasks
cv_tasks = pd.read_csv('results/cv_tasks_detailed.csv')
print(f"Total CV tasks: {len(cv_tasks)}")

# Top tasks by dataset count
top_tasks = cv_tasks.nlargest(10, 'Dataset Count')
```

### 3.3 Find Papers with Code
```python
# Load paper-code links
with gzip.open('data/links-between-papers-and-code.json.gz', 'rt') as f:
    links = json.load(f)

# Count repositories by language
from collections import Counter
languages = Counter(link.get('language') for link in links)
```

## 4. Interactive Exploration

### 4.1 Web Interface
1. Open `index.html` in a web browser
2. Use Live Server extension in VS Code for best experience
3. Navigate through organized sections

### 4.2 Data Viewer
1. Open `interactive/data_viewer.html`
2. Features:
   - Search tasks by name
   - Filter by research area
   - View task distribution charts
   - Click tasks for details

## 5. Python Scripts

### 5.1 Classification Scripts
- `scripts/classify_tasks.py` - Categorize tasks by domain
- `scripts/extract_detailed_tasks.py` - Extract task details
- `scripts/analyze_pwc_client.py` - Analyze research areas

### 5.2 Running Scripts
```bash
cd scripts
python classify_tasks.py
python extract_detailed_tasks.py
```

## 6. Key Statistics

### 6.1 Quick Numbers
- **4,451** unique AI/ML tasks
- **15,008** datasets
- **576,261** papers with abstracts
- **300,161** paper-code links
- **8,725** methods/algorithms
- **3,468** evaluation metrics

### 6.2 Top Tasks by Popularity
1. Semantic Segmentation (348 datasets)
2. Object Detection (333 datasets)
3. Image Classification (283 datasets)
4. Visual Question Answering (145 datasets)
5. Named Entity Recognition (130 datasets)

## 7. Tips for Researchers

### 7.1 Finding Benchmarks
1. Check `evaluation-tables.json.gz` for SOTA results
2. Look for dataset-specific leaderboards
3. Review metrics used for evaluation

### 7.2 Understanding Task Relationships
1. Use `task_hierarchy.csv` to see parent-child relationships
2. Some tasks have up to 6 levels of hierarchy
3. Cross-domain tasks appear in multiple areas

### 7.3 Tracking Progress
1. SOTA results include dates
2. Filter by year to see progress over time
3. Compare different approaches on same benchmarks

## 8. Next Steps

### 8.1 Detailed Exploration
- [Browse all tasks](../S2_tasks/01_all_tasks.md)
- [Explore datasets](../S3_datasets/01_datasets_overview.md)
- [View SOTA results](../S4_benchmarks/01_sota_overview.md)

### 8.2 Domain-Specific Guides
- [Computer Vision Guide](../S2_tasks/02_computer_vision.md)
- [NLP Guide](../S2_tasks/03_nlp.md)
- [Audio Processing Guide](../S2_tasks/04_audio.md)

### 8.3 Advanced Usage
- [Data Processing Scripts](../S7_about/03_usage_guide.md)
- [API Documentation](../S7_about/02_data_sources.md)
- [Contributing Guidelines](../S7_about/04_preservation.md)