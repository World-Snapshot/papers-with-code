/**
 * Task Data Loader Module
 * Handles loading and caching task hierarchy data
 */

class TaskDataLoader {
    constructor() {
        this.cache = {};
        this.currentData = null;
        this.currentDomain = '';
    }

    async loadDomain(domain) {
        if (!domain) {
            throw new Error('Domain is required');
        }

        // Check cache first
        if (this.cache[domain]) {
            this.currentData = this.cache[domain];
            this.currentDomain = domain;
            return this.currentData;
        }

        try {
            const response = await fetch(`../results/hierarchical/${domain}_hierarchy.json`);
            if (!response.ok) {
                throw new Error(`Failed to load data: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Process and enhance data
            this.processData(data);
            
            // Cache the data
            this.cache[domain] = data;
            this.currentData = data;
            this.currentDomain = domain;
            
            return data;
        } catch (error) {
            console.error('Error loading task data:', error);
            throw error;
        }
    }

    processData(data) {
        // Add computed properties
        data.hierarchicalTaskCount = this.countHierarchicalTasks(data.hierarchical_tasks);
        data.maxDepth = this.findMaxDepth(data.hierarchical_tasks);
        data.tasksByDatasetCount = this.sortTasksByDatasetCount(data);
        
        // Index tasks for quick lookup
        data.taskIndex = this.createTaskIndex(data);
    }

    countHierarchicalTasks(trees) {
        let count = 0;
        
        const countNode = (node) => {
            count++;
            if (node.children) {
                node.children.forEach(child => countNode(child));
            }
        };
        
        trees.forEach(tree => countNode(tree));
        return count;
    }

    findMaxDepth(trees) {
        let maxDepth = 0;
        
        const findDepth = (node, depth = 0) => {
            maxDepth = Math.max(maxDepth, depth);
            if (node.children) {
                node.children.forEach(child => findDepth(child, depth + 1));
            }
        };
        
        trees.forEach(tree => findDepth(tree));
        return maxDepth;
    }

    sortTasksByDatasetCount(data) {
        const allTasks = [];
        
        const collectTasks = (node) => {
            allTasks.push({
                name: node.name,
                dataset_count: node.dataset_count || 0,
                description: node.description || '',
                type: 'hierarchical'
            });
            if (node.children) {
                node.children.forEach(child => collectTasks(child));
            }
        };
        
        data.hierarchical_tasks.forEach(tree => collectTasks(tree));
        
        data.standalone_tasks.forEach(task => {
            allTasks.push({
                ...task,
                type: 'standalone'
            });
        });
        
        return allTasks.sort((a, b) => (b.dataset_count || 0) - (a.dataset_count || 0));
    }

    createTaskIndex(data) {
        const index = {};
        
        const indexNode = (node, path = []) => {
            const fullPath = [...path, node.name];
            index[node.name.toLowerCase()] = {
                ...node,
                path: fullPath,
                type: 'hierarchical'
            };
            
            if (node.children) {
                node.children.forEach(child => indexNode(child, fullPath));
            }
        };
        
        data.hierarchical_tasks.forEach(tree => indexNode(tree));
        
        data.standalone_tasks.forEach(task => {
            index[task.name.toLowerCase()] = {
                ...task,
                path: [task.name],
                type: 'standalone'
            };
        });
        
        return index;
    }

    searchTasks(query) {
        if (!this.currentData || !query) {
            return [];
        }
        
        const lowerQuery = query.toLowerCase();
        const results = [];
        
        // Search in task index
        Object.entries(this.currentData.taskIndex).forEach(([key, task]) => {
            if (key.includes(lowerQuery) || 
                (task.description && task.description.toLowerCase().includes(lowerQuery))) {
                results.push({
                    ...task,
                    relevance: key.startsWith(lowerQuery) ? 2 : 1
                });
            }
        });
        
        // Sort by relevance and dataset count
        return results.sort((a, b) => {
            if (a.relevance !== b.relevance) {
                return b.relevance - a.relevance;
            }
            return (b.dataset_count || 0) - (a.dataset_count || 0);
        });
    }

    getTaskByName(name) {
        if (!this.currentData) return null;
        return this.currentData.taskIndex[name.toLowerCase()] || null;
    }

    getTopTasksByDatasetCount(limit = 10) {
        if (!this.currentData) return [];
        return this.currentData.tasksByDatasetCount.slice(0, limit);
    }

    getDomainStats() {
        if (!this.currentData) return null;
        
        return {
            domain: this.currentDomain,
            totalTasks: this.currentData.total_tasks,
            hierarchicalTasks: this.currentData.hierarchicalTaskCount,
            standaloneTasks: this.currentData.standalone_tasks.length,
            maxDepth: this.currentData.maxDepth,
            rootTasks: this.currentData.hierarchical_tasks.length
        };
    }
}

// Export for use in other modules
window.TaskDataLoader = TaskDataLoader;