# Data Overview

## Raw Data Files (JSON.GZ)

Located in the `data/` directory:

| File | Size | Records | Description |
|------|------|---------|-------------|
| `datasets.json.gz` | 8.0 MB | 15,008 | Dataset metadata including names, descriptions, tasks, modalities |
| `evaluation-tables.json.gz` | 20.8 MB | 2,254 | Evaluation tables with SOTA results, metrics, and benchmarks |
| `methods.json.gz` | 5.2 MB | 8,725 | Methods and algorithms with descriptions |
| `papers-with-abstracts.json.gz` | 537.7 MB | 576,261 | Full paper details with abstracts, authors, dates |
| `links-between-papers-and-code.json.gz` | 25.0 MB | 300,161 | Paper-to-code repository mappings |

## Processed Data Files (CSV)

Located in the `results/` directory:

### Task Lists by Domain
| File | Records | Description |
|------|---------|-------------|
| `cv_tasks.csv` | 1,947 | Computer Vision tasks with dataset counts |
| `nlp_tasks.csv` | 999 | Natural Language Processing tasks |
| `audio_tasks.csv` | 31 | Audio Processing tasks |
| `other_tasks.csv` | 744 | Other domain tasks |

### Detailed Task Information
| File | Records | Description |
|------|---------|-------------|
| `cv_tasks_detailed.csv` | 2,275 | CV tasks with benchmarks, metrics, descriptions |
| `nlp_tasks_detailed.csv` | 1,093 | NLP tasks with full details |
| `audio_tasks_detailed.csv` | 40 | Audio tasks with benchmarks |
| `other_tasks_detailed.csv` | 1,043 | Other tasks with details |
| `all_tasks_detailed.csv` | 4,451 | Combined detailed task information |

### Task Organization
| File | Records | Description |
|------|---------|-------------|
| `task_hierarchy.csv` | 766 | Parent-child task relationships |
| `research_areas.csv` | 16 | Research area categorization |

## Data Structure Examples

### Dataset Entry
```json
{
  "name": "imagenet-1k",
  "full_name": "ImageNet (ILSVRC2012)",
  "description": "The ImageNet dataset contains...",
  "homepage": "http://www.image-net.org/",
  "tasks": ["Image Classification"],
  "modalities": ["Images"],
  "languages": []
}
```

### Evaluation Table Entry
```json
{
  "task": "Image Classification",
  "datasets": [{
    "dataset": "ImageNet",
    "sota": {
      "rows": [{
        "model_name": "ViT-22B",
        "paper_title": "Scaling Vision Transformers to 22 Billion Parameters",
        "paper_date": "2023-02-10",
        "metrics": {
          "Top 1 Accuracy": 91.3,
          "Top 5 Accuracy": 98.5
        }
      }]
    }
  }]
}
```

### Paper Entry
```json
{
  "paper_url": "https://arxiv.org/abs/2302.05442",
  "arxiv_id": "2302.05442",
  "title": "Scaling Vision Transformers to 22 Billion Parameters",
  "abstract": "We present a recipe for scaling vision transformers...",
  "url_abs": "https://arxiv.org/abs/2302.05442",
  "date": "2023-02-10"
}
```

## Key Statistics

- **Total Tasks**: 4,451 unique AI/ML tasks
- **Computer Vision**: 2,275 tasks (51%)
- **NLP**: 1,093 tasks (25%)
- **Audio**: 40 tasks (1%)
- **Other Domains**: 1,043 tasks (23%)
- **Task Hierarchy Depth**: Up to 6 levels
- **Most Common Metric**: Accuracy (used 9,307 times)
- **Date Range**: Papers from 2015 to 2024