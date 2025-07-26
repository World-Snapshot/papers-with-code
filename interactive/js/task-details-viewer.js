/**
 * Task Details Viewer Module
 * Handles displaying detailed information about selected tasks
 */

class TaskDetailsViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container with ID ${containerId} not found`);
            return;
        }
        
        this.currentTask = null;
        this.dataLoader = null;
    }

    setDataLoader(loader) {
        this.dataLoader = loader;
    }

    show(task) {
        if (!task) return;
        
        this.currentTask = task;
        this.render();
        this.container.classList.add('visible');
    }

    hide() {
        this.container.classList.remove('visible');
        this.currentTask = null;
    }

    render() {
        if (!this.currentTask) return;
        
        const task = this.currentTask;
        
        // Update task name
        const nameElement = this.container.querySelector('#task-name');
        if (nameElement) {
            nameElement.textContent = task.name;
        }
        
        // Update dataset count
        const datasetCountElement = this.container.querySelector('#task-dataset-count');
        if (datasetCountElement) {
            const count = task.dataset_count || 0;
            datasetCountElement.innerHTML = `
                <strong>${count}</strong> ${count === 1 ? 'dataset' : 'datasets'}
                ${count > 0 ? this.createDatasetBar(count) : ''}
            `;
        }
        
        // Update description
        const descriptionElement = this.container.querySelector('#task-description');
        if (descriptionElement) {
            descriptionElement.textContent = task.description || 'No description available';
        }
        
        // Update benchmarks
        const benchmarksElement = this.container.querySelector('#task-benchmarks');
        if (benchmarksElement) {
            benchmarksElement.innerHTML = this.renderList(task.benchmarks, 'benchmarks');
        }
        
        // Update metrics
        const metricsElement = this.container.querySelector('#task-metrics');
        if (metricsElement) {
            metricsElement.innerHTML = this.renderList(task.metrics, 'metrics');
        }
        
        // Add additional sections if available
        this.renderAdditionalInfo(task);
    }

    createDatasetBar(count) {
        // Create a visual bar showing relative dataset count
        const maxCount = 350; // Based on the data, ~350 is the max
        const percentage = Math.min((count / maxCount) * 100, 100);
        
        return `
            <div style="margin-top: 10px;">
                <div style="background: #e0e0e0; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: #007bff; width: ${percentage}%; height: 100%; transition: width 0.3s;"></div>
                </div>
            </div>
        `;
    }

    renderList(items, type) {
        if (!items || items.length === 0) {
            return `<span style="color: #999;">No ${type} specified</span>`;
        }
        
        if (items.length <= 5) {
            return items.map(item => 
                `<span class="detail-tag">${item}</span>`
            ).join(' ');
        }
        
        // Show first 5 and indicate more
        const visible = items.slice(0, 5);
        const hidden = items.slice(5);
        
        return `
            <div>
                ${visible.map(item => `<span class="detail-tag">${item}</span>`).join(' ')}
                <span class="more-indicator" onclick="taskDetailsViewer.showAll('${type}')">
                    +${hidden.length} more
                </span>
            </div>
            <div id="${type}-all" style="display: none; margin-top: 10px;">
                ${hidden.map(item => `<span class="detail-tag">${item}</span>`).join(' ')}
            </div>
        `;
    }

    showAll(type) {
        const allSection = document.getElementById(`${type}-all`);
        const moreIndicator = event.target;
        
        if (allSection.style.display === 'none') {
            allSection.style.display = 'block';
            moreIndicator.textContent = 'Show less';
        } else {
            allSection.style.display = 'none';
            moreIndicator.textContent = `+${this.currentTask[type].length - 5} more`;
        }
    }

    renderAdditionalInfo(task) {
        // Remove any existing additional info
        const existingAdditional = this.container.querySelector('.additional-info');
        if (existingAdditional) {
            existingAdditional.remove();
        }
        
        const additionalDiv = document.createElement('div');
        additionalDiv.className = 'additional-info';
        additionalDiv.style.cssText = 'margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0;';
        
        // Task hierarchy path
        if (task.path && task.path.length > 1) {
            additionalDiv.innerHTML += `
                <div class="detail-item">
                    <div class="detail-label">Hierarchy Path</div>
                    <div class="detail-value">
                        ${task.path.map((p, i) => 
                            `<span style="color: ${i === task.path.length - 1 ? '#333' : '#666'};">${p}</span>`
                        ).join(' → ')}
                    </div>
                </div>
            `;
        }
        
        // Task type
        if (task.type) {
            additionalDiv.innerHTML += `
                <div class="detail-item">
                    <div class="detail-label">Task Type</div>
                    <div class="detail-value">
                        <span class="task-type-badge ${task.type}">
                            ${task.type.charAt(0).toUpperCase() + task.type.slice(1)}
                        </span>
                    </div>
                </div>
            `;
        }
        
        // Children information
        if (task.children && task.children.length > 0) {
            const childrenNames = task.children.map(c => c.name).slice(0, 10);
            const moreCount = task.children.length - 10;
            
            additionalDiv.innerHTML += `
                <div class="detail-item">
                    <div class="detail-label">Subtasks (${task.children.length})</div>
                    <div class="detail-value">
                        ${childrenNames.map(name => 
                            `<span class="detail-tag clickable" onclick="taskDetailsViewer.navigateToTask('${name}')">${name}</span>`
                        ).join(' ')}
                        ${moreCount > 0 ? `<span style="color: #999;">+${moreCount} more</span>` : ''}
                    </div>
                </div>
            `;
        }
        
        // Related tasks (if we have this information)
        if (this.dataLoader) {
            const relatedTasks = this.findRelatedTasks(task);
            if (relatedTasks.length > 0) {
                additionalDiv.innerHTML += `
                    <div class="detail-item">
                        <div class="detail-label">Related Tasks</div>
                        <div class="detail-value">
                            ${relatedTasks.map(t => 
                                `<span class="detail-tag clickable" onclick="taskDetailsViewer.navigateToTask('${t.name}')">${t.name}</span>`
                            ).join(' ')}
                        </div>
                    </div>
                `;
            }
        }
        
        if (additionalDiv.innerHTML) {
            this.container.querySelector('.close-btn').insertAdjacentElement('afterend', additionalDiv);
        }
    }

    findRelatedTasks(task) {
        if (!this.dataLoader || !this.dataLoader.currentData) return [];
        
        const related = [];
        const taskWords = task.name.toLowerCase().split(/\s+/);
        
        // Find tasks with similar names
        Object.values(this.dataLoader.currentData.taskIndex).forEach(t => {
            if (t.name === task.name) return;
            
            const tWords = t.name.toLowerCase().split(/\s+/);
            const commonWords = taskWords.filter(w => tWords.includes(w) && w.length > 3);
            
            if (commonWords.length >= 2 || 
                (commonWords.length === 1 && commonWords[0].length > 5)) {
                related.push({
                    name: t.name,
                    score: commonWords.length
                });
            }
        });
        
        // Sort by relevance and limit
        return related
            .sort((a, b) => b.score - a.score)
            .slice(0, 5)
            .map(r => ({ name: r.name }));
    }

    navigateToTask(taskName) {
        if (!this.dataLoader) return;
        
        const task = this.dataLoader.getTaskByName(taskName);
        if (task) {
            // Update details view
            this.show(task);
            
            // Trigger search to highlight and expand to this task
            const searchBox = document.getElementById('search-box');
            if (searchBox) {
                searchBox.value = taskName;
                searchBox.dispatchEvent(new Event('input'));
            }
        }
    }

    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .detail-tag {
                display: inline-block;
                background-color: #f0f0f0;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                margin: 2px;
                color: #333;
            }
            
            .detail-tag.clickable {
                cursor: pointer;
                transition: background-color 0.2s;
            }
            
            .detail-tag.clickable:hover {
                background-color: #e0e0e0;
            }
            
            .more-indicator {
                display: inline-block;
                color: #007bff;
                cursor: pointer;
                font-size: 12px;
                margin-left: 5px;
                text-decoration: underline;
            }
            
            .more-indicator:hover {
                color: #0056b3;
            }
            
            .task-type-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }
            
            .task-type-badge.hierarchical {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            
            .task-type-badge.standalone {
                background-color: #f3e5f5;
                color: #7b1fa2;
            }
        `;
        document.head.appendChild(style);
    }
}

// Export for use in other modules
window.TaskDetailsViewer = TaskDetailsViewer;