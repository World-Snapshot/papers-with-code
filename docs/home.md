# Papers With Code Archive

Welcome to the Papers With Code Archive. This is a complete data backup of the Papers With Code website before it stopped service in 24 July 2025.

## About This Archive

Papers With Code was one of the most important resource websites in the machine learning research field, collecting papers, code implementations, datasets, and benchmark results. Unfortunately, the website ceased operation in 24 July 2025.

This project preserves the website's core data, including:

- **4,451 unique AI/ML tasks**
- **15,008 datasets**
- **576,261 papers with abstracts**
- **300,161 code repository links**
- **59,860 SOTA result records**
- **8,725 methods and algorithms**

## Update Policy

Although the Papers With Code website has closed, we will update this archive as appropriate:

- Regularly organize and optimize data formats
- Fix known data issues
- Add data visualization features
- Improve documentation and usage guides

## Available Datasets

We have the following compressed JSON files in the `data/` directory:

### 1. **datasets.json.gz** (8.0 MB)
- Contains 15,008 datasets with detailed information
- Each dataset includes associated tasks, descriptions, and paper links
- Structure: name, full_name, description, homepage, tasks, modalities, languages

### 2. **evaluation-tables.json.gz** (20.8 MB)
- Contains 2,254 evaluation tables with SOTA results
- Task hierarchies (parent-child relationships)
- Benchmark information with metrics
- SOTA (State of the Art) leaderboards with model performance

### 3. **methods.json.gz** (5.2 MB)
- Contains 8,725 methods/algorithms
- Includes method names, descriptions, and paper references
- Categories and implementation details

### 4. **papers-with-abstracts.json.gz** (537.7 MB)
- Contains 576,261 papers with abstracts
- Full paper metadata: title, abstract, authors, date
- ArXiv IDs and URLs

### 5. **links-between-papers-and-code.json.gz** (25.0 MB)
- Contains 300,161 links between papers and code
- Maps papers to their code implementations
- GitHub repositories and other code sources

## Quick Start

### Browse Task Categories

- [Computer Vision Tasks](cv_tasks.md) - 1,947 tasks
- [Natural Language Processing Tasks](nlp_tasks.md) - 999 tasks
- [Audio Processing Tasks](audio_tasks.md) - 31 tasks
- [Other Domain Tasks](other_tasks.md) - 744 tasks

### Explore Datasets and Benchmarks

- [Datasets Overview](datasets_overview.md) - 15,008 datasets
- [Benchmarks](benchmarks.md) - 2,254 evaluation tables
- [SOTA Results](sota_results.md) - 59,860 records

### Find Papers and Code

- [Papers Library](papers_overview.md) - 576,261 papers
- [Methods & Algorithms](methods.md) - 8,725 methods
- [Code Repositories](code_links.md) - 300,161 links

## Data Processing Scripts

We provide several Python scripts in the `scripts/` directory:

- `classify_tasks.py` - Categorize tasks by domain
- `extract_detailed_tasks.py` - Extract detailed task information
- `analyze_sota_results.py` - Extract and analyze SOTA results
- `visualize_sota_example.py` - Example visualization of SOTA progress

## Contributing

If you find data issues or have suggestions for improvement, please provide feedback through [GitHub Issues](https://github.com/world-snapshot/papers-with-code/issues).

---

*Data collected: 25 July 2025*