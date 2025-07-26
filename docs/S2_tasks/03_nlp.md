# Natural Language Processing Tasks

Natural Language Processing encompasses 1,093 tasks in the Papers With Code archive, representing the second-largest research area. These tasks focus on enabling machines to understand, interpret, and generate human language.

## Interactive Task Explorer

Explore all 1,093 NLP tasks in our interactive hierarchical viewer:

<iframe src="../../interactive/task_viewer.html?domain=nlp" width="100%" height="800" style="border: 1px solid #ddd; border-radius: 8px;"></iframe>

## Key Statistics

- **Total Tasks**: 1,093
- **Hierarchical Tasks**: 707 (organized in parent-child relationships)
- **Standalone Tasks**: 896
- **Maximum Hierarchy Depth**: 5 levels
- **Root Categories**: 128

## Top Tasks by Dataset Count

1. **Named Entity Recognition** - 130 datasets
2. **Machine Translation** - 85 datasets
3. **Language Modeling** - 88 datasets
4. **Question Answering** - 74 datasets
5. **Sentiment Analysis** - 63 datasets
6. **Text Classification** - 61 datasets
7. **Text Summarization** - 82 datasets
8. **Reading Comprehension** - 20 subtasks
9. **Dialogue Systems** - 21 subtasks
10. **Text Generation** - 25 subtasks

## Major Task Categories

NLP tasks are organized into several major categories:

- **Text Understanding**: Classification, sentiment analysis, NER
- **Text Generation**: Summarization, translation, dialogue
- **Question Answering**: Reading comprehension, open-domain QA
- **Information Extraction**: Relation extraction, event extraction
- **Language Modeling**: Masked LM, causal LM, multilingual LM
- **Semantic Analysis**: Parsing, semantic similarity, entailment
- **Speech & Text**: ASR integration, TTS, multimodal tasks

## Common Evaluation Metrics

- **Generation**: BLEU, ROUGE, METEOR, BERTScore
- **Classification**: Accuracy, F1 Score, Precision/Recall
- **QA**: Exact Match, F1 Score
- **Language Modeling**: Perplexity, Bits per character

## Data Access

### Hierarchical Data
- **JSON Format**: `results/hierarchical/nlp_hierarchy.json`
- **CSV Format**: `results/hierarchical/nlp_hierarchy.csv`

### Traditional Lists
- **Simple Task List**: `results/nlp/nlp_tasks.csv`
- **Detailed Task Info**: `results/nlp/nlp_tasks_detailed.csv`

### Analysis Scripts
- `scripts/create_hierarchical_tasks.py` - Generate hierarchical structures
- `scripts/classify_tasks.py` - Original task classification
- `scripts/extract_detailed_tasks.py` - Extract task details

## Usage Tips

1. **Search**: Use the search box to find specific tasks
2. **Navigation**: Click on task names to see details
3. **Tabs**: Switch between hierarchical and standalone tasks
4. **Expansion**: Explore subtasks by expanding parent nodes

## Popular Frameworks

- Transformers (Hugging Face)
- spaCy
- NLTK
- Stanford NLP
- AllenNLP

## Related Resources

- [All Tasks Overview](01_all_tasks.md)
- [Computer Vision Tasks](02_computer_vision.md)
- [Audio Tasks](04_audio.md)
- [Medical Tasks](05_medical.md)