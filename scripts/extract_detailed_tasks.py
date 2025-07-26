import json
import gzip
import csv
from collections import defaultdict
import re

# CV任务关键词
cv_keywords = [
    'image', 'visual', 'video', 'object', 'detection', 'segmentation', 'recognition',
    'tracking', 'pose', 'depth', 'reconstruction', '3d', '2d', 'face', 'optical',
    'medical image', 'scene', 'action', 'gesture', 'sketch', 'photo', 'instance',
    'panoptic', 'semantic', 'keypoint', 'landmark', 'shape', 'stereo', 'camera',
    'view', 'synthesis', 'rendering', 'enhancement', 'restoration', 'super-resolution',
    'denoising', 'deblurring', 'colorization', 'inpainting', 'matting', 'saliency',
    'aesthetic', 'quality', 'compression', 'forensics', 'biometric', 'gaze', 'emotion',
    'attribute', 'retrieval', 'matching', 'alignment', 'registration', 'stitching',
    'motion', 'flow', 'activity', 'event', 'anomaly detection', 'crowd', 'pedestrian',
    'vehicle', 'autonomous driving', 'slam', 'localization', 'mapping', 'navigation',
    'medical', 'x-ray', 'ct', 'mri', 'ultrasound', 'microscopy', 'histopathology',
    'radiology', 'retinal', 'skin', 'lesion', 'tumor', 'cell', 'nuclei'
]

# NLP任务关键词
nlp_keywords = [
    'text', 'language', 'nlp', 'natural language', 'word', 'sentence', 'document',
    'translation', 'summarization', 'classification', 'generation', 'understanding',
    'question answering', 'qa', 'reading comprehension', 'named entity', 'ner',
    'relation extraction', 'sentiment', 'emotion', 'opinion', 'aspect', 'dependency',
    'parsing', 'tagging', 'tokenization', 'lemmatization', 'stemming', 'morphology',
    'syntax', 'semantic', 'pragmatic', 'discourse', 'dialogue', 'conversation',
    'chatbot', 'intent', 'slot filling', 'coreference', 'anaphora', 'ellipsis',
    'information extraction', 'information retrieval', 'search', 'ranking', 'recommendation',
    'knowledge', 'reasoning', 'inference', 'entailment', 'contradiction', 'paraphrase',
    'similarity', 'analogy', 'commonsense', 'logic', 'argumentation', 'fact checking',
    'fake news', 'stance', 'claim', 'evidence', 'abstractive', 'extractive', 'multi-document',
    'cross-lingual', 'multilingual', 'low-resource', 'zero-shot', 'few-shot', 'transfer',
    'domain adaptation', 'style transfer', 'text simplification', 'readability', 'coherence',
    'grammatical error', 'spell checking', 'punctuation', 'capitalization', 'diacritization',
    'transliteration', 'code-switching', 'code generation', 'code completion', 'code search',
    'code summarization', 'code translation', 'bug detection', 'vulnerability', 'documentation'
]

# 语音/音频任务关键词
audio_keywords = [
    'speech', 'audio', 'sound', 'voice', 'speaker', 'acoustic', 'phoneme', 'prosody',
    'pitch', 'tone', 'music', 'singing', 'instrument', 'beat', 'rhythm', 'melody',
    'harmony', 'timbre', 'noise', 'echo', 'reverberation', 'source separation',
    'enhancement', 'denoising', 'dereverberation', 'beamforming', 'localization',
    'asr', 'tts', 'speech recognition', 'speech synthesis', 'voice conversion',
    'voice cloning', 'speaker recognition', 'speaker verification', 'speaker diarization',
    'emotion recognition', 'language identification', 'accent', 'dialect', 'keyword spotting',
    'wake word', 'command recognition', 'music transcription', 'music generation',
    'music information retrieval', 'genre classification', 'mood detection', 'audio tagging',
    'sound event detection', 'acoustic scene classification', 'environmental sound'
]

def classify_task(task_name):
    task_lower = task_name.lower()
    
    # 检查是否为CV任务
    for keyword in cv_keywords:
        if keyword in task_lower:
            return 'CV'
    
    # 检查是否为NLP任务
    for keyword in nlp_keywords:
        if keyword in task_lower:
            return 'NLP'
    
    # 检查是否为音频任务
    for keyword in audio_keywords:
        if keyword in task_lower:
            return 'Audio'
    
    # 其他任务
    return 'Other'

# 存储任务详细信息
task_details = defaultdict(lambda: {
    'datasets': set(),
    'dataset_count': 0,
    'benchmarks': set(),
    'description': '',
    'subtasks': set(),
    'categories': set(),
    'synonyms': set(),
    'papers': set(),
    'sota_metrics': set()
})

print("正在读取datasets.json.gz...")
# 从datasets.json提取信息
with gzip.open('datasets.json.gz', 'rt', encoding='utf-8') as f:
    datasets = json.load(f)
    
for dataset in datasets:
    if 'tasks' in dataset:
        for task_info in dataset['tasks']:
            task_name = task_info.get('task', '')
            if task_name:
                # 添加数据集信息
                task_details[task_name]['datasets'].add(dataset['name'])
                task_details[task_name]['dataset_count'] += 1

print("正在读取evaluation-tables.json.gz...")
# 从evaluation-tables.json提取更多信息
with gzip.open('evaluation-tables.json.gz', 'rt', encoding='utf-8') as f:
    eval_tables = json.load(f)
    
for table in eval_tables:
    task_name = table.get('task', '')
    if task_name:
        # 添加描述
        if 'description' in table and table['description']:
            task_details[task_name]['description'] = table['description']
        
        # 添加分类
        if 'categories' in table:
            task_details[task_name]['categories'].update(table['categories'])
        
        # 添加子任务
        if 'subtasks' in table:
            for subtask in table['subtasks']:
                if 'task' in subtask:
                    task_details[task_name]['subtasks'].add(subtask['task'])
        
        # 添加同义词
        if 'synonyms' in table:
            task_details[task_name]['synonyms'].update(table['synonyms'])
        
        # 添加基准数据集
        if 'datasets' in table:
            for dataset_info in table['datasets']:
                if 'dataset' in dataset_info:
                    # dataset字段可能是字符串或对象
                    if isinstance(dataset_info['dataset'], str):
                        benchmark_name = dataset_info['dataset']
                    else:
                        benchmark_name = dataset_info['dataset'].get('name', 'Unknown')
                    task_details[task_name]['benchmarks'].add(benchmark_name)
                    
                    # 提取SOTA指标
                    if 'sota' in dataset_info and 'rows' in dataset_info['sota']:
                        for row in dataset_info['sota']['rows']:
                            if 'metrics' in row:
                                for metric, value in row['metrics'].items():
                                    task_details[task_name]['sota_metrics'].add(metric)

print("正在生成详细的CSV文件...")

def create_detailed_csv(category, tasks_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Task Name', 
            'Dataset Count', 
            'Common Datasets (Top 10)', 
            'Benchmarks',
            'SOTA Metrics',
            'Subtasks',
            'Categories',
            'Description (First 200 chars)'
        ])
        
        for task_name in tasks_list:
            details = task_details[task_name]
            
            # 获取前10个数据集
            datasets_list = list(details['datasets'])[:10]
            datasets_str = '; '.join(datasets_list) if datasets_list else 'N/A'
            
            # 获取基准
            benchmarks_str = '; '.join(list(details['benchmarks'])[:10]) if details['benchmarks'] else 'N/A'
            
            # 获取SOTA指标
            metrics_str = '; '.join(list(details['sota_metrics'])[:10]) if details['sota_metrics'] else 'N/A'
            
            # 获取子任务
            subtasks_str = '; '.join(list(details['subtasks'])[:5]) if details['subtasks'] else 'N/A'
            
            # 获取分类
            categories_str = '; '.join(details['categories']) if details['categories'] else 'N/A'
            
            # 截取描述
            description = details['description'][:200] + '...' if len(details['description']) > 200 else details['description']
            description = description.replace('\n', ' ').replace('\r', ' ')
            
            writer.writerow([
                task_name,
                details['dataset_count'],
                datasets_str,
                benchmarks_str,
                metrics_str,
                subtasks_str,
                categories_str,
                description if description else 'N/A'
            ])

# 分类任务
tasks_by_category = defaultdict(list)
for task_name in task_details.keys():
    category = classify_task(task_name)
    tasks_by_category[category].append(task_name)

# 为每个类别创建详细的CSV
for category in ['CV', 'NLP', 'Audio', 'Other']:
    # 按数据集数量排序
    sorted_tasks = sorted(
        tasks_by_category[category], 
        key=lambda x: task_details[x]['dataset_count'], 
        reverse=True
    )
    
    filename = f'{category.lower()}_tasks_detailed.csv'
    create_detailed_csv(category, sorted_tasks, filename)
    print(f"已创建 {filename}，包含 {len(sorted_tasks)} 个任务")

# 创建一个包含所有任务的主CSV文件
print("\n正在创建主任务列表...")
with open('all_tasks_detailed.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Category',
        'Task Name', 
        'Dataset Count', 
        'Common Datasets (Top 10)', 
        'Benchmarks',
        'SOTA Metrics',
        'Subtasks Count',
        'Has Description'
    ])
    
    for category in ['CV', 'NLP', 'Audio', 'Other']:
        sorted_tasks = sorted(
            tasks_by_category[category], 
            key=lambda x: task_details[x]['dataset_count'], 
            reverse=True
        )
        
        for task_name in sorted_tasks[:50]:  # 每个类别前50个
            details = task_details[task_name]
            
            datasets_list = list(details['datasets'])[:10]
            datasets_str = '; '.join(datasets_list) if datasets_list else 'N/A'
            
            benchmarks_str = '; '.join(list(details['benchmarks'])[:10]) if details['benchmarks'] else 'N/A'
            
            metrics_str = '; '.join(list(details['sota_metrics'])[:10]) if details['sota_metrics'] else 'N/A'
            
            writer.writerow([
                category,
                task_name,
                details['dataset_count'],
                datasets_str,
                benchmarks_str,
                metrics_str,
                len(details['subtasks']),
                'Yes' if details['description'] else 'No'
            ])

print("\n任务统计：")
print(f"计算机视觉(CV)任务数: {len(tasks_by_category['CV'])}")
print(f"自然语言处理(NLP)任务数: {len(tasks_by_category['NLP'])}")
print(f"音频处理任务数: {len(tasks_by_category['Audio'])}")
print(f"其他领域任务数: {len(tasks_by_category['Other'])}")
print(f"总任务数: {len(task_details)}")