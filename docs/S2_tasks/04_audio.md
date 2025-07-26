# Audio Processing Tasks

Audio Processing encompasses 40 tasks in the Papers With Code archive, focusing on understanding and generating audio signals including speech, music, and environmental sounds.

## Interactive Task Explorer

Explore all Audio Processing tasks in our interactive hierarchical viewer:

<iframe src="../../interactive/task_viewer.html?domain=audio" width="100%" height="800" style="border: 1px solid #ddd; border-radius: 8px;"></iframe>

## Key Statistics

- **Total Tasks**: 195 (including subtasks)
- **Hierarchical Tasks**: 164 (organized in parent-child relationships)
- **Standalone Tasks**: 31
- **Maximum Hierarchy Depth**: 3 levels
- **Root Categories**: 25

## Top Tasks by Dataset Count

1. **Speech Recognition** - 39 datasets
2. **Text-to-Speech Synthesis** - 14 datasets
3. **Music Generation** - 15 datasets
4. **Sound Event Detection** - 12 datasets
5. **Speaker Recognition** - 11 datasets
6. **Speech Enhancement** - Various datasets
7. **Music Information Retrieval** - Various datasets
8. **Audio Classification** - Various datasets

## Major Task Categories

Audio tasks are organized into several major categories:

- **Speech Processing**: ASR, TTS, speaker recognition, emotion recognition
- **Music Processing**: Generation, transcription, source separation
- **Audio Analysis**: Classification, event detection, scene analysis
- **Audio Enhancement**: Noise reduction, dereverberation, restoration
- **Audio Generation**: Sound synthesis, style transfer
- **Multimodal Audio**: Audio-visual tasks, audio captioning

## Common Evaluation Metrics

- **Speech Recognition**: WER (Word Error Rate), CER
- **Audio Quality**: MOS, PESQ, STOI
- **Source Separation**: SDR, SIR, SAR
- **Classification**: Accuracy, F-measure
- **Generation**: Human evaluation, diversity metrics

## Data Access

### Hierarchical Data
- **JSON Format**: `results/hierarchical/audio_hierarchy.json`
- **CSV Format**: `results/hierarchical/audio_hierarchy.csv`

### Traditional Lists
- **Simple Task List**: `results/audio/audio_tasks.csv`
- **Detailed Task Info**: `results/audio/audio_tasks_detailed.csv`

### Analysis Scripts
- `scripts/create_hierarchical_tasks.py` - Generate hierarchical structures
- `scripts/classify_tasks.py` - Original task classification
- `scripts/extract_detailed_tasks.py` - Extract task details

## Popular Datasets

### Speech
- LibriSpeech - Read English speech
- Common Voice - Multilingual crowdsourced
- VoxCeleb - Speaker recognition
- VCTK - Multi-speaker British English

### Music
- MAESTRO - Classical piano
- MusicNet - Classical music
- NSynth - Musical notes
- Lakh MIDI - Symbolic music

### Environmental Sound
- ESC-50 - Environmental sounds
- UrbanSound8K - Urban acoustics
- AudioSet - Large-scale audio events
- FSD50K - Freesound annotations

## Common Frameworks

- librosa - Audio analysis
- SpeechBrain - Speech processing
- ESPnet - End-to-end speech
- PyTorch Audio - Deep learning for audio

## Usage Tips

1. **Search**: Use the search box to find specific audio tasks
2. **Navigation**: Click on task names to see details
3. **Hierarchy**: Explore parent-child relationships
4. **Datasets**: Check dataset counts for task popularity

## Related Resources

- [All Tasks Overview](01_all_tasks.md)
- [Computer Vision Tasks](02_computer_vision.md)
- [NLP Tasks](03_nlp.md)
- [Medical Tasks](05_medical.md)