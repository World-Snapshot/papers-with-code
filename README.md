# Papers with Code Data Analysis Project

## Note:

[https://web.archive.org/web/20250616051252/https://paperswithcode.com/](https://web.archive.org/web/20250616051252/https://paperswithcode.com/)

I hope someone can help to deploy all the snapshots of this webpage to Github. It can be this repository or any other repository. In short, paperwithcode must not disappear!

## Project Background

In July 2025, the Papers with Code website ceased operations. This project urgently preserved and analyzed the website's core data, including task information across domains such as computer vision, natural language processing, and audio.

This template is a commonly used template of the World Snapshot Organization. It is derived from [this link](https://github.com/World-Snapshot/doc):

> This is a website template that needs to be rendered by the server, so if you want to modify and view it in real time, you can't do it like html, but use one of vscode's plug-ins: Live Server (by Ritwick Dey). Similar local server plug-in should also work.
>
> CC BY-SA 4.0: Feel free to use this template, but please keep the Powered by [World Snapshot Doc](https://github.com/World-Snapshot/doc).

## Data Sources

### Original Data Files (located in `data/` directory)

1. **datasets.json.gz** (Source: Papers with Code official data export)
   - Contains detailed information for all datasets
   - Task lists associated with each dataset
   - Dataset descriptions, paper links, and other metadata

2. **evaluation-tables.json.gz** (Source: Papers with Code official data export)
   - Contains task evaluation tables
   - Task hierarchical relationships (parent-child tasks)
   - Benchmark information
   - SOTA (State of the Art) metrics

3. **methods.json.gz** (Source: Papers with Code official data export)
   - Contains information about various methods/algorithms

4. **papers-with-abstracts.json.gz** (537.7 MB)
   - Contains 576,261 papers with abstracts
   - Full paper metadata: title, abstract, authors, date

5. **links-between-papers-and-code.json.gz** (25.0 MB)
   - Contains 300,161 links between papers and code
   - Maps papers to their code implementations

### Third-party Repositories (located in `repositories/` directory)

1. **paperswithcode-client-develop**
   - Official Python client for Papers with Code
   - Used to access PWC data via API
   - Contains data model definitions

2. **paperswithcode-data-master**
   - PWC data repository documentation
   - Contains data download links

3. **sota-extractor-master**
   - Tool for extracting SOTA results
   - Contains data for specific tasks

## Data Processing Scripts (located in `scripts/` directory)

1. **classify_tasks.py**
   - Classifies tasks by domain (CV, NLP, Audio, Other)
   - Counts datasets per task
   - Generates basic task classification CSV files

2. **extract_detailed_tasks.py**
   - Extracts detailed task information
   - Includes: datasets, benchmarks, SOTA metrics, subtasks, descriptions, etc.
   - Generates detailed task information CSV files

3. **analyze_pwc_client.py**
   - Analyzes task hierarchical relationships
   - Generates research area statistics
   - Creates task hierarchy and research area CSV files

4. **create_hierarchical_tasks.py**
   - Creates hierarchical task structures for each domain
   - Combines task hierarchy with detailed task information
   - Outputs both JSON and CSV formats for interactive visualization

## Interactive Task Viewer

The project includes an interactive web-based task viewer that allows you to:
- Browse all 4,451 tasks in a hierarchical tree structure
- Search and filter tasks by name
- View detailed information for each task including datasets, benchmarks, and metrics
- Navigate tasks by domain (Computer Vision, NLP, Audio, Other)

### Usage
1. Open `index.html` in a web browser
2. Navigate to the "Tasks" section
3. Click on any task category to launch the interactive viewer
4. Or directly open `interactive/task_viewer.html?domain=cv` (replace `cv` with `nlp`, `audio`, or `other`)

## Output Results (located in `results/` directory)

### Simple Task Lists (sorted by dataset count)
- **cv_tasks.csv** - 1,947 computer vision tasks
- **nlp_tasks.csv** - 999 natural language processing tasks
- **audio_tasks.csv** - 31 audio processing tasks
- **other_tasks.csv** - 744 other domain tasks

### Detailed Task Information (including datasets, benchmarks, metrics, etc.)
- **cv_tasks_detailed.csv** - Detailed information for 2,275 CV tasks
- **nlp_tasks_detailed.csv** - Detailed information for 1,093 NLP tasks
- **audio_tasks_detailed.csv** - Detailed information for 40 audio tasks
- **other_tasks_detailed.csv** - Detailed information for 1,043 other tasks
- **all_tasks_detailed.csv** - Combined information for all tasks

### Task Relationships and Classifications
- **task_hierarchy.csv** - Parent-child relationships and hierarchy depth for 766 tasks
- **research_areas.csv** - Task classifications across 17 research areas

### Hierarchical Task Data (located in `results/hierarchical/` directory)
- **cv_hierarchy.json/csv** - Hierarchical structure for Computer Vision tasks
- **nlp_hierarchy.json/csv** - Hierarchical structure for NLP tasks
- **audio_hierarchy.json/csv** - Hierarchical structure for Audio tasks
- **other_hierarchy.json/csv** - Hierarchical structure for other domains

## Key Findings

1. **Total Tasks**: 4,451 unique tasks (from evaluation-tables)

2. **Task Distribution by Research Area** (from PWC client analysis):
   - Computer Vision: 865 tasks
   - Natural Language Processing: 436 tasks
   - Miscellaneous: 219 tasks
   - Medical: 190 tasks
   - Methodology: 157 tasks
   - Time Series: 98 tasks
   - Graphs: 87 tasks
   - Audio: 69 tasks
   - Computer Code: 61 tasks
   - Robots: 56 tasks
   - Knowledge Base: 50 tasks
   - Reasoning: 50 tasks
   - Speech: 48 tasks
   - Playing Games: 40 tasks
   - Music: 32 tasks
   - Adversarial: 31 tasks

3. **Task Hierarchy**:
   - Maximum depth of 6 levels (e.g., 3D-related tasks)
   - Object Detection has the most subtasks (39)

4. **Evaluation Metrics**:
   - 3,468 different evaluation metrics
   - Accuracy is the most commonly used metric (9,307 occurrences)

## About Client Persistence

**paperswithcode-client** is an open-source Python package:
- Code has been downloaded locally and can continue to be used even if official maintenance stops
- However, the client depends on PWC's API service
- If PWC's API servers shut down, the client cannot retrieve online data
- Recommendation: Regularly backup downloaded data files, do not rely on online services

## Usage Recommendations

1. **Find specific tasks**: Search in the corresponding domain CSV files
2. **Understand task relationships**: View task_hierarchy.csv
3. **Explore research areas**: View research_areas.csv
4. **Get benchmark information**: View the Benchmarks column in detailed CSV files

## Data Updates

Since Papers with Code has ceased operations, this data represents the final state before the website closure. It is recommended to properly preserve this data as historical records.

---
*Data collection date: July 2025*  
*Data processing: Automated processing using Python scripts*
