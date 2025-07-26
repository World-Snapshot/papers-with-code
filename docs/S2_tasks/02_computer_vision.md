# Computer Vision Tasks

Computer Vision encompasses 2,275 tasks in the Papers With Code archive, making it the largest research area. These tasks focus on enabling machines to interpret and understand visual information from the world.

## Interactive Task Explorer

Explore all 2,275 Computer Vision tasks in our interactive hierarchical viewer:

<iframe src="../../interactive/task_viewer.html?domain=cv" width="100%" height="800" style="border: 1px solid #ddd; border-radius: 8px;"></iframe>

## Key Statistics

- **Total Tasks**: 2,275
- **Hierarchical Tasks**: 1,562 (organized in parent-child relationships)
- **Standalone Tasks**: 1,476
- **Maximum Hierarchy Depth**: 6 levels
- **Root Categories**: 210

## Top Tasks by Dataset Count

1. **Semantic Segmentation** - 348 datasets
2. **Object Detection** - 333 datasets  
3. **Image Classification** - 283 datasets
4. **Visual Question Answering** - 145 datasets
5. **Pose Estimation** - 124 datasets
6. **Anomaly Detection** - 120 datasets
7. **Action Recognition** - 115 datasets
8. **Instance Segmentation** - 111 datasets
9. **Face Recognition** - 68 datasets
10. **Language Modeling** - 88 datasets

## Major Task Categories

Computer Vision tasks are organized into several major categories:

- **Detection & Localization**: Object detection, face detection, keypoint detection
- **Segmentation**: Semantic, instance, panoptic segmentation
- **Classification**: Image classification, fine-grained recognition
- **3D Vision**: 3D reconstruction, depth estimation, pose estimation
- **Video Understanding**: Action recognition, video classification, tracking
- **Generation**: Image generation, style transfer, image-to-image translation
- **Low-Level Vision**: Super-resolution, denoising, enhancement
- **Medical Imaging**: Medical segmentation, disease classification

## Common Evaluation Metrics

- **Detection**: mAP, IoU, FPS
- **Segmentation**: mIoU, Dice Score, Pixel Accuracy
- **Classification**: Accuracy, F1 Score, AUC-ROC
- **Generation**: FID, IS, LPIPS

## Data Access

### Hierarchical Data
- **JSON Format**: `results/hierarchical/cv_hierarchy.json`
- **CSV Format**: `results/hierarchical/cv_hierarchy.csv`

### Traditional Lists
- **Simple Task List**: `results/cv/cv_tasks.csv`
- **Detailed Task Info**: `results/cv/cv_tasks_detailed.csv`

### Analysis Scripts
- `scripts/create_hierarchical_tasks.py` - Generate hierarchical structures
- `scripts/classify_tasks.py` - Original task classification
- `scripts/extract_detailed_tasks.py` - Extract task details

## Usage Tips

1. **Search**: Use the search box to find specific tasks
2. **Navigation**: Click on task names to see details
3. **Expansion**: Use "Expand All" to see the complete hierarchy
4. **Filtering**: Tasks are organized by parent-child relationships

## Related Resources

- [All Tasks Overview](01_all_tasks.md)
- [NLP Tasks](03_nlp.md)
- [Audio Tasks](04_audio.md)
- [Medical Tasks](05_medical.md)