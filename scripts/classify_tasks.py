import json
import gzip
import csv
from collections import defaultdict

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

# 读取数据并分类
tasks_by_category = defaultdict(list)
task_counts = defaultdict(int)

with gzip.open('datasets.json.gz', 'rt', encoding='utf-8') as f:
    data = json.load(f)
    
for dataset in data:
    if 'tasks' in dataset:
        for task_info in dataset['tasks']:
            task_name = task_info.get('task', '')
            if task_name:
                category = classify_task(task_name)
                if task_name not in tasks_by_category[category]:
                    tasks_by_category[category].append(task_name)
                task_counts[task_name] += 1

# 创建CV任务CSV
with open('cv_tasks.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Task Name', 'Dataset Count'])
    cv_tasks_sorted = sorted([(task, task_counts[task]) for task in tasks_by_category['CV']], 
                           key=lambda x: x[1], reverse=True)
    for task, count in cv_tasks_sorted:
        writer.writerow([task, count])

# 创建NLP任务CSV
with open('nlp_tasks.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Task Name', 'Dataset Count'])
    nlp_tasks_sorted = sorted([(task, task_counts[task]) for task in tasks_by_category['NLP']], 
                            key=lambda x: x[1], reverse=True)
    for task, count in nlp_tasks_sorted:
        writer.writerow([task, count])

# 创建音频任务CSV
with open('audio_tasks.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Task Name', 'Dataset Count'])
    audio_tasks_sorted = sorted([(task, task_counts[task]) for task in tasks_by_category['Audio']], 
                              key=lambda x: x[1], reverse=True)
    for task, count in audio_tasks_sorted:
        writer.writerow([task, count])

# 创建其他任务CSV
with open('other_tasks.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Task Name', 'Dataset Count'])
    other_tasks_sorted = sorted([(task, task_counts[task]) for task in tasks_by_category['Other']], 
                              key=lambda x: x[1], reverse=True)
    for task, count in other_tasks_sorted:
        writer.writerow([task, count])

# 打印统计信息
print(f"计算机视觉(CV)任务数: {len(tasks_by_category['CV'])}")
print(f"自然语言处理(NLP)任务数: {len(tasks_by_category['NLP'])}")
print(f"音频处理任务数: {len(tasks_by_category['Audio'])}")
print(f"其他领域任务数: {len(tasks_by_category['Other'])}")
print(f"总任务数: {sum(len(tasks) for tasks in tasks_by_category.values())}")