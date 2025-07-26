/**
 * Task Tree Renderer Module
 * Handles rendering hierarchical task structures
 */

class TaskTreeRenderer {
    constructor(options = {}) {
        this.options = {
            showDatasetCount: true,
            collapsible: true,
            searchHighlight: true,
            onTaskClick: null,
            maxInitialDepth: 2,
            ...options
        };
        
        this.expandedNodes = new Set();
        this.selectedNode = null;
    }

    renderHierarchicalTasks(container, tasks) {
        container.innerHTML = '';
        
        if (!tasks || tasks.length === 0) {
            container.innerHTML = '<p style="color: #666;">No hierarchical tasks found.</p>';
            return;
        }
        
        tasks.forEach(tree => {
            container.appendChild(this.createTreeNode(tree, 0));
        });
    }

    renderStandaloneTasks(container, tasks) {
        container.innerHTML = '';
        
        if (!tasks || tasks.length === 0) {
            container.innerHTML = '<p style="color: #666;">No standalone tasks found.</p>';
            return;
        }
        
        // Group standalone tasks by first letter for easier navigation
        const grouped = this.groupTasksByFirstLetter(tasks);
        
        Object.entries(grouped).forEach(([letter, taskGroup]) => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'task-group';
            
            const header = document.createElement('h4');
            header.textContent = letter;
            header.style.cssText = 'margin: 20px 0 10px 0; color: #666; border-bottom: 1px solid #e0e0e0; padding-bottom: 5px;';
            groupDiv.appendChild(header);
            
            taskGroup.forEach(task => {
                groupDiv.appendChild(this.createTreeNode(task, 0, false));
            });
            
            container.appendChild(groupDiv);
        });
    }

    groupTasksByFirstLetter(tasks) {
        const grouped = {};
        
        tasks.forEach(task => {
            const firstLetter = task.name[0].toUpperCase();
            if (!grouped[firstLetter]) {
                grouped[firstLetter] = [];
            }
            grouped[firstLetter].push(task);
        });
        
        // Sort each group by dataset count
        Object.keys(grouped).forEach(letter => {
            grouped[letter].sort((a, b) => (b.dataset_count || 0) - (a.dataset_count || 0));
        });
        
        return grouped;
    }

    createTreeNode(node, depth = 0, isHierarchical = true) {
        const div = document.createElement('div');
        div.className = 'tree-node';
        div.dataset.taskName = node.name;
        div.dataset.depth = depth;
        
        const content = document.createElement('div');
        content.className = 'tree-node-content';
        if (this.selectedNode === node.name) {
            content.classList.add('selected');
        }
        
        // Click handler
        content.onclick = () => {
            this.selectNode(node);
            if (this.options.onTaskClick) {
                this.options.onTaskClick(node);
            }
        };
        
        const info = document.createElement('div');
        info.className = 'tree-node-info';
        
        // Toggle button for hierarchical nodes with children
        if (isHierarchical && this.options.collapsible) {
            const toggle = document.createElement('span');
            toggle.className = 'tree-toggle';
            
            if (node.children && node.children.length > 0) {
                const isExpanded = this.expandedNodes.has(node.name) || depth < this.options.maxInitialDepth;
                toggle.textContent = isExpanded ? '▼' : '▶';
                toggle.onclick = (e) => {
                    e.stopPropagation();
                    this.toggleNode(div, node);
                };
            } else {
                toggle.textContent = ' ';
            }
            info.appendChild(toggle);
        }
        
        // Task name
        const name = document.createElement('span');
        name.className = 'task-name';
        name.textContent = node.name;
        info.appendChild(name);
        
        // Children count badge
        if (node.children && node.children.length > 0) {
            const childCount = document.createElement('span');
            childCount.className = 'child-count';
            childCount.textContent = `(${node.children.length})`;
            childCount.style.cssText = 'color: #999; font-size: 12px; margin-left: 5px;';
            info.appendChild(childCount);
        }
        
        content.appendChild(info);
        
        // Dataset count
        if (this.options.showDatasetCount && node.dataset_count > 0) {
            const count = document.createElement('span');
            count.className = 'dataset-count';
            count.textContent = `${node.dataset_count} datasets`;
            content.appendChild(count);
        }
        
        div.appendChild(content);
        
        // Children container
        if (isHierarchical && node.children && node.children.length > 0) {
            const children = document.createElement('div');
            children.className = 'tree-children';
            
            const isExpanded = this.expandedNodes.has(node.name) || depth < this.options.maxInitialDepth;
            if (isExpanded) {
                children.classList.add('expanded');
                if (depth < this.options.maxInitialDepth) {
                    this.expandedNodes.add(node.name);
                }
            }
            
            node.children.forEach(child => {
                children.appendChild(this.createTreeNode(child, depth + 1, true));
            });
            
            div.appendChild(children);
        }
        
        return div;
    }

    toggleNode(nodeElement, nodeData) {
        const toggle = nodeElement.querySelector('.tree-toggle');
        const children = nodeElement.querySelector('.tree-children');
        
        if (children) {
            if (children.classList.contains('expanded')) {
                children.classList.remove('expanded');
                toggle.textContent = '▶';
                this.expandedNodes.delete(nodeData.name);
            } else {
                children.classList.add('expanded');
                toggle.textContent = '▼';
                this.expandedNodes.add(nodeData.name);
            }
        }
    }

    selectNode(node) {
        // Remove previous selection
        document.querySelectorAll('.tree-node-content.selected').forEach(el => {
            el.classList.remove('selected');
        });
        
        // Add new selection
        const nodeElement = document.querySelector(`[data-task-name="${node.name}"] .tree-node-content`);
        if (nodeElement) {
            nodeElement.classList.add('selected');
        }
        
        this.selectedNode = node.name;
    }

    expandAll() {
        document.querySelectorAll('.tree-children').forEach(el => {
            el.classList.add('expanded');
            const nodeElement = el.parentElement;
            const taskName = nodeElement.dataset.taskName;
            if (taskName) {
                this.expandedNodes.add(taskName);
            }
        });
        document.querySelectorAll('.tree-toggle').forEach(el => {
            if (el.textContent !== ' ') el.textContent = '▼';
        });
    }

    collapseAll() {
        document.querySelectorAll('.tree-children').forEach(el => {
            el.classList.remove('expanded');
        });
        document.querySelectorAll('.tree-toggle').forEach(el => {
            if (el.textContent !== ' ') el.textContent = '▶';
        });
        this.expandedNodes.clear();
    }

    expandToDepth(depth) {
        document.querySelectorAll('.tree-node').forEach(nodeElement => {
            const nodeDepth = parseInt(nodeElement.dataset.depth);
            const children = nodeElement.querySelector('.tree-children');
            const toggle = nodeElement.querySelector('.tree-toggle');
            
            if (children) {
                if (nodeDepth < depth) {
                    children.classList.add('expanded');
                    if (toggle) toggle.textContent = '▼';
                    this.expandedNodes.add(nodeElement.dataset.taskName);
                } else {
                    children.classList.remove('expanded');
                    if (toggle) toggle.textContent = '▶';
                    this.expandedNodes.delete(nodeElement.dataset.taskName);
                }
            }
        });
    }

    highlightSearchResults(query) {
        const allNodes = document.querySelectorAll('.tree-node');
        
        if (!query || query.trim() === '') {
            // Clear all highlights
            allNodes.forEach(node => {
                node.style.display = '';
                const nameSpan = node.querySelector('.task-name');
                if (nameSpan) {
                    nameSpan.innerHTML = nameSpan.textContent;
                }
            });
            return;
        }
        
        const lowerQuery = query.toLowerCase();
        const matchedNodes = new Set();
        
        allNodes.forEach(node => {
            const nameSpan = node.querySelector('.task-name');
            if (nameSpan) {
                const name = nameSpan.textContent.toLowerCase();
                if (name.includes(lowerQuery)) {
                    // Show matching node
                    node.style.display = '';
                    matchedNodes.add(node);
                    
                    // Highlight matching text
                    if (this.options.searchHighlight) {
                        const regex = new RegExp(`(${query})`, 'gi');
                        nameSpan.innerHTML = nameSpan.textContent.replace(regex, '<span class="highlight">$1</span>');
                    }
                    
                    // Expand parent nodes
                    this.expandParents(node);
                } else {
                    node.style.display = 'none';
                }
            }
        });
        
        // Show parents of matched nodes
        matchedNodes.forEach(node => {
            let parent = node.parentElement;
            while (parent) {
                if (parent.classList.contains('tree-node')) {
                    parent.style.display = '';
                }
                parent = parent.parentElement;
            }
        });
    }

    expandParents(node) {
        let parent = node.parentElement;
        while (parent) {
            if (parent.classList.contains('tree-children')) {
                parent.classList.add('expanded');
                const parentNode = parent.parentElement;
                if (parentNode) {
                    const taskName = parentNode.dataset.taskName;
                    if (taskName) {
                        this.expandedNodes.add(taskName);
                    }
                    const toggle = parentNode.querySelector('.tree-toggle');
                    if (toggle && toggle.textContent !== ' ') {
                        toggle.textContent = '▼';
                    }
                }
            }
            parent = parent.parentElement;
        }
    }

    getSelectedNode() {
        return this.selectedNode;
    }

    clearSelection() {
        document.querySelectorAll('.tree-node-content.selected').forEach(el => {
            el.classList.remove('selected');
        });
        this.selectedNode = null;
    }
}

// Export for use in other modules
window.TaskTreeRenderer = TaskTreeRenderer;