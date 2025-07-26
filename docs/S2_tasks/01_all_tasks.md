# Tasks Overview

Papers With Code organized machine learning research into 4,451 unique tasks across 17 research areas. This comprehensive taxonomy represents the state of AI/ML research as of July 2025.

## Interactive Task Explorers

Explore tasks by domain using our interactive viewers:

- 📊 [**Computer Vision Tasks**](02_computer_vision.md) - 2,275 tasks with hierarchical organization
- 💬 [**Natural Language Processing**](03_nlp.md) - 1,093 tasks across text understanding and generation
- 🎵 [**Audio Processing**](04_audio.md) - 195 tasks including speech, music, and sound
- 🏥 [**Medical & Other Domains**](05_medical.md) - 1,043 specialized tasks

## 1. Overview

### 1.1 Total Statistics
- **Total Tasks**: 4,451 unique tasks
- **Research Areas**: 17 major categories
- **Task Hierarchies**: Up to 6 levels deep
- **Datasets**: 15,008 associated datasets
- **Evaluation Metrics**: 3,468 different metrics

### 1.2 Task Organization
Tasks are organized in a hierarchical structure:
1. **Research Areas** (17 top-level categories)
2. **Parent Tasks** (e.g., Object Detection, Text Generation)
3. **Child Tasks** (e.g., 3D Object Detection, Dialogue Generation)
4. **Sub-tasks** (up to 6 levels of depth)

## 2. Research Area Distribution

### 2.1 By Task Count (PWC Client Analysis)
1. **Computer Vision** - 865 tasks
2. **Natural Language Processing** - 436 tasks
3. **Miscellaneous** - 219 tasks
4. **Medical** - 190 tasks
5. **Methodology** - 157 tasks
6. **Time Series** - 98 tasks
7. **Graphs** - 87 tasks
8. **Audio** - 69 tasks
9. **Computer Code** - 61 tasks
10. **Robots** - 56 tasks
11. **Knowledge Base** - 50 tasks
12. **Reasoning** - 50 tasks
13. **Speech** - 48 tasks
14. **Playing Games** - 40 tasks
15. **Music** - 32 tasks
16. **Adversarial** - 31 tasks

### 2.2 By Domain Classification
- **Computer Vision** - 2,275 tasks (51%)
- **Natural Language Processing** - 1,093 tasks (25%)
- **Other Domains** - 1,043 tasks (23%)
- **Audio Processing** - 40 tasks (1%)

## 3. Task Hierarchies

### 3.1 Deepest Hierarchies
The deepest task hierarchies reach 6 levels, particularly in:
- **3D Tasks** - Spanning multiple research areas
- **Video Understanding** - Complex temporal tasks
- **Medical Imaging** - Specialized clinical applications

### 3.2 Parent Tasks with Most Children
1. **Object Detection** - 39 subtasks
2. **3D** - 38 subtasks (cross-domain)
3. **Video** - 34 subtasks
4. **Image Classification** - 33 subtasks
5. **Medical Image Segmentation** - 31 subtasks

### 3.3 Cross-Domain Parent Tasks
Some parent tasks span multiple research areas:
- **3D** - Present in 7 areas (Computer Vision, Methodology, Time Series, Music, Miscellaneous, Playing Games, Knowledge Base)
- **Classification** - Present in 11 areas
- **Anomaly Detection** - Present in 4 areas (Methodology, Graphs, Miscellaneous, Computer Vision)

## 4. Task Categories by Research Area

### 4.1 Computer Vision Tasks
[Detailed in cv_tasks.md]
- Object Detection (333 datasets)
- Semantic Segmentation (348 datasets)
- Image Classification (283 datasets)
- Visual Question Answering (145 datasets)
- Instance Segmentation (111 datasets)
- Pose Estimation (124 datasets)
- [View all CV tasks →](cv_tasks.md)

### 4.2 Natural Language Processing Tasks
[Detailed in nlp_tasks.md]
- Machine Translation (85 datasets)
- Named Entity Recognition (130 datasets)
- Text Generation (25 subtasks)
- Question Answering (74 datasets)
- Sentiment Analysis (63 datasets)
- Language Modeling (88 datasets)
- [View all NLP tasks →](nlp_tasks.md)

### 4.3 Audio Processing Tasks
[Detailed in audio_tasks.md]
- Speech Recognition (39 datasets)
- Music Generation (15 datasets)
- Speech Synthesis (14 datasets)
- Sound Event Detection (12 datasets)
- Audio Classification
- [View all Audio tasks →](audio_tasks.md)

### 4.4 Medical Tasks
- Medical Image Segmentation (31 subtasks)
- Disease Prediction
- Medical Code Prediction
- Drug Discovery
- Clinical NLP
- [View all Medical tasks →](medical_tasks.md)

### 4.5 Other Domain Tasks
[Detailed in other_tasks.md]
- Methodology (157 tasks)
- Time Series (98 tasks)
- Graphs (87 tasks)
- Computer Code (61 tasks)
- Robotics (56 tasks)
- [View all Other tasks →](other_tasks.md)

## 5. Most Popular Tasks by Dataset Count

### 5.1 Top 20 Tasks
1. **Semantic Segmentation** - 348 datasets
2. **Object Detection** - 333 datasets
3. **Image Classification** - 283 datasets
4. **Visual Question Answering** - 145 datasets
5. **Named Entity Recognition** - 130 datasets
6. **Pose Estimation** - 124 datasets
7. **Anomaly Detection** - 120 datasets
8. **Action Recognition** - 115 datasets
9. **Instance Segmentation** - 111 datasets
10. **Machine Translation** - 85 datasets
11. **Text Summarization** - 82 datasets
12. **Question Answering** - 74 datasets
13. **Face Recognition** - 68 datasets
14. **Language Modeling** - 88 datasets
15. **Sentiment Analysis** - 63 datasets
16. **Text Classification** - 61 datasets
17. **Image Generation** - 58 datasets
18. **Speech Recognition** - 39 datasets
19. **Object Tracking** - 45 datasets
20. **Super-Resolution** - 42 datasets

## 6. Evaluation Metrics

### 6.1 Most Common Metrics
1. **Accuracy** - 9,307 occurrences
2. **F1 Score** - Various forms
3. **mAP (mean Average Precision)** - Detection tasks
4. **IoU (Intersection over Union)** - Segmentation
5. **BLEU Score** - Translation/Generation
6. **Perplexity** - Language modeling

### 6.2 Domain-Specific Metrics
- **Computer Vision**: mAP, IoU, FPS, PCK
- **NLP**: BLEU, ROUGE, METEOR, BERTScore
- **Audio**: WER, MOS, SDR
- **Medical**: Dice Score, Sensitivity, Specificity

## 7. Data Access

### 7.1 Raw Data Files
Located in `data/` directory:
- `evaluation-tables.json.gz` - Task definitions and SOTA results
- `datasets.json.gz` - Dataset information
- `methods.json.gz` - Algorithm descriptions
- `papers-with-abstracts.json.gz` - 576K papers
- `links-between-papers-and-code.json.gz` - Implementation links

### 7.2 Processed CSV Files
Located in `results/` directory:
- `all_tasks_detailed.csv` - Complete task information
- `task_hierarchy.csv` - Parent-child relationships
- `research_areas.csv` - Research area classification
- Domain-specific task lists (cv_tasks.csv, nlp_tasks.csv, etc.)

### 7.3 Interactive Tools
- [Interactive Data Viewer](../interactive/data_viewer.html) - Browse and search tasks
- Python scripts in `scripts/` for custom analysis

## 8. Task Trends and Insights

### 8.1 Emerging Areas
- **Vision-Language Tasks** - Multimodal understanding
- **3D Understanding** - Growing rapidly across domains
- **Few-Shot Learning** - Limited data scenarios
- **Adversarial Robustness** - Security considerations

### 8.2 Interdisciplinary Tasks
Many tasks span multiple research areas:
- Medical + Computer Vision
- NLP + Knowledge Graphs
- Audio + Computer Vision
- Robotics + 3D Vision

### 8.3 Application Domains
- **Autonomous Vehicles** - Multiple CV tasks
- **Healthcare** - Medical imaging and NLP
- **Content Creation** - Generation tasks
- **Security** - Adversarial and privacy tasks

## 9. Using This Data

### 9.1 Finding Specific Tasks
1. Use the search function in the [Interactive Viewer](../interactive/data_viewer.html)
2. Browse domain-specific markdown files
3. Search CSV files with grep or pandas

### 9.2 Understanding Task Relationships
1. Consult `task_hierarchy.csv` for parent-child relationships
2. Check task descriptions in detailed CSV files
3. Review benchmark associations

### 9.3 Accessing SOTA Results
1. Load `evaluation-tables.json.gz` for complete SOTA history
2. Filter by task name and dataset
3. Track progress over time with paper dates

## 10. Preservation Note

This data represents the final state of Papers With Code before its closure in July 2025. It serves as a valuable historical record of:
- The organization of AI/ML research tasks
- Benchmark and evaluation standards
- The relationships between different research areas
- The evolution of task definitions over time

**Please preserve and share this data responsibly to support continued AI/ML research.**