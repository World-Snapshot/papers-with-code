/**
 * Task Viewer Application
 * Main application logic that ties all modules together
 */

class TaskViewerApp {
    constructor() {
        this.dataLoader = new TaskDataLoader();
        this.treeRenderer = new TaskTreeRenderer({
            onTaskClick: (task) => this.onTaskSelected(task),
            maxInitialDepth: 1
        });
        this.detailsViewer = new TaskDetailsViewer('task-details');
        
        // Set up cross-module references
        this.detailsViewer.setDataLoader(this.dataLoader);
        
        // Make details viewer globally accessible for onclick handlers
        window.taskDetailsViewer = this.detailsViewer;
        
        this.currentDomain = '';
        this.init();
    }

    init() {
        // Add custom styles
        this.detailsViewer.addStyles();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Get domain from URL parameter
        const urlParams = new URLSearchParams(window.location.search);
        const domainParam = urlParams.get('domain');
        
        if (domainParam) {
            this.loadDomain(domainParam);
        } else {
            this.showWelcomeMessage();
        }
    }

    setupEventListeners() {
        // Domain selector
        const domainSelector = document.getElementById('domain-selector');
        if (domainSelector) {
            domainSelector.addEventListener('change', (e) => {
                const domain = e.target.value;
                if (domain) {
                    window.location.search = `?domain=${domain}`;
                }
            });
        }

        // Search box
        const searchBox = document.getElementById('search-box');
        if (searchBox) {
            searchBox.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });
        }

        // Control buttons
        const expandAllBtn = document.getElementById('expand-all-btn');
        if (expandAllBtn) {
            expandAllBtn.addEventListener('click', () => this.treeRenderer.expandAll());
        }

        const collapseAllBtn = document.getElementById('collapse-all-btn');
        if (collapseAllBtn) {
            collapseAllBtn.addEventListener('click', () => this.treeRenderer.collapseAll());
        }

        // Tab switching
        document.querySelectorAll('.tab').forEach((tab, index) => {
            tab.addEventListener('click', () => {
                this.switchTab(index === 0 ? 'hierarchical' : 'standalone');
            });
        });

        // Close details button
        const closeBtn = document.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.detailsViewer.hide());
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Escape to close details
            if (e.key === 'Escape') {
                this.detailsViewer.hide();
            }
            // Ctrl/Cmd + F to focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
                e.preventDefault();
                searchBox?.focus();
            }
        });
    }

    async loadDomain(domain) {
        this.currentDomain = domain;
        document.getElementById('domain-selector').value = domain;
        
        // Show loading state
        this.showLoadingState();
        
        try {
            const data = await this.dataLoader.loadDomain(domain);
            this.updateUI(data);
            this.hideLoadingState();
        } catch (error) {
            console.error('Error loading domain:', error);
            this.showError('Failed to load task data. Please check if the data files exist.');
            this.hideLoadingState();
        }
    }

    updateUI(data) {
        if (!data) return;
        
        // Update title
        const domainNames = {
            'cv': 'Computer Vision',
            'nlp': 'Natural Language Processing', 
            'audio': 'Audio Processing',
            'other': 'Other Domains'
        };
        document.getElementById('page-title').textContent = `${domainNames[this.currentDomain]} Tasks`;
        
        // Update stats
        const stats = this.dataLoader.getDomainStats();
        document.getElementById('total-tasks').textContent = stats.totalTasks.toLocaleString();
        document.getElementById('hierarchical-tasks').textContent = stats.hierarchicalTasks.toLocaleString();
        document.getElementById('standalone-tasks').textContent = stats.standaloneTasks.toLocaleString();
        
        // Add additional stats
        this.addAdditionalStats(stats);
        
        // Render trees
        this.renderTrees(data);
        
        // Show top tasks
        this.showTopTasks();
    }

    addAdditionalStats(stats) {
        const statsContainer = document.getElementById('stats');
        
        // Check if additional stats already exist
        if (!document.getElementById('root-tasks')) {
            const additionalStats = `
                <div class="stat-item">
                    <div class="stat-value" id="root-tasks">${stats.rootTasks}</div>
                    <div class="stat-label">Root Tasks</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="max-depth">${stats.maxDepth}</div>
                    <div class="stat-label">Max Depth</div>
                </div>
            `;
            statsContainer.insertAdjacentHTML('beforeend', additionalStats);
        } else {
            document.getElementById('root-tasks').textContent = stats.rootTasks;
            document.getElementById('max-depth').textContent = stats.maxDepth;
        }
    }

    renderTrees(data) {
        const hierarchicalContainer = document.getElementById('hierarchical-tree');
        const standaloneContainer = document.getElementById('standalone-tree');
        
        this.treeRenderer.renderHierarchicalTasks(hierarchicalContainer, data.hierarchical_tasks);
        this.treeRenderer.renderStandaloneTasks(standaloneContainer, data.standalone_tasks);
    }

    showTopTasks() {
        const topTasks = this.dataLoader.getTopTasksByDatasetCount(10);
        
        // Check if top tasks section exists
        let topTasksSection = document.getElementById('top-tasks-section');
        if (!topTasksSection) {
            // Create it
            const container = document.querySelector('.container');
            const controlsDiv = document.querySelector('.controls');
            
            topTasksSection = document.createElement('div');
            topTasksSection.id = 'top-tasks-section';
            topTasksSection.className = 'top-tasks-section';
            topTasksSection.style.cssText = 'margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;';
            
            controlsDiv.insertAdjacentElement('afterend', topTasksSection);
        }
        
        topTasksSection.innerHTML = `
            <h3 style="margin-top: 0; color: #333;">Top Tasks by Dataset Count</h3>
            <div class="top-tasks-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 10px;">
                ${topTasks.map((task, index) => `
                    <div class="top-task-item" style="background: white; padding: 12px; border-radius: 4px; cursor: pointer; transition: box-shadow 0.2s;"
                         onclick="taskViewerApp.selectTaskByName('${task.name}')">
                        <span style="color: #666; font-size: 12px;">#${index + 1}</span>
                        <strong style="display: block; margin: 4px 0;">${task.name}</strong>
                        <span style="color: #007bff; font-size: 14px;">${task.dataset_count} datasets</span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    selectTaskByName(taskName) {
        const task = this.dataLoader.getTaskByName(taskName);
        if (task) {
            // Show details
            this.onTaskSelected(task);
            
            // Highlight in tree
            const searchBox = document.getElementById('search-box');
            if (searchBox) {
                searchBox.value = taskName;
                this.handleSearch(taskName);
            }
            
            // Switch to appropriate tab
            if (task.type === 'standalone') {
                this.switchTab('standalone');
            } else {
                this.switchTab('hierarchical');
            }
        }
    }

    handleSearch(query) {
        this.treeRenderer.highlightSearchResults(query);
        
        // Show search results count
        if (query) {
            const results = this.dataLoader.searchTasks(query);
            this.showSearchResultsCount(results.length);
        } else {
            this.hideSearchResultsCount();
        }
    }

    showSearchResultsCount(count) {
        let countDiv = document.getElementById('search-results-count');
        if (!countDiv) {
            countDiv = document.createElement('div');
            countDiv.id = 'search-results-count';
            countDiv.style.cssText = 'margin-top: 10px; color: #666; font-size: 14px;';
            document.querySelector('.controls').appendChild(countDiv);
        }
        countDiv.textContent = `Found ${count} matching tasks`;
    }

    hideSearchResultsCount() {
        const countDiv = document.getElementById('search-results-count');
        if (countDiv) {
            countDiv.remove();
        }
    }

    onTaskSelected(task) {
        this.detailsViewer.show(task);
    }

    switchTab(tab) {
        document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        
        if (tab === 'hierarchical') {
            document.querySelectorAll('.tab')[0].classList.add('active');
            document.getElementById('hierarchical-content').classList.add('active');
        } else {
            document.querySelectorAll('.tab')[1].classList.add('active');
            document.getElementById('standalone-content').classList.add('active');
        }
    }

    showLoadingState() {
        const container = document.querySelector('.container');
        if (!document.getElementById('loading-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255,255,255,0.9);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            `;
            overlay.innerHTML = '<div style="text-align: center;"><h2>Loading task data...</h2></div>';
            document.body.appendChild(overlay);
        }
    }

    hideLoadingState() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    }

    showError(message) {
        alert(message);
    }

    showWelcomeMessage() {
        document.getElementById('page-title').textContent = 'Task Hierarchy Viewer';
        const container = document.querySelector('.tabs');
        const welcome = document.createElement('div');
        welcome.style.cssText = 'text-align: center; padding: 40px; color: #666;';
        welcome.innerHTML = `
            <h2>Welcome to the Task Hierarchy Viewer</h2>
            <p>Please select a domain from the dropdown above to explore AI/ML tasks.</p>
            <div style="margin-top: 30px;">
                <button class="button button-primary" onclick="document.getElementById('domain-selector').value='cv'; window.location.search='?domain=cv'">
                    Explore Computer Vision
                </button>
                <button class="button button-primary" style="margin-left: 10px;" onclick="document.getElementById('domain-selector').value='nlp'; window.location.search='?domain=nlp'">
                    Explore NLP
                </button>
            </div>
        `;
        container.parentElement.insertBefore(welcome, container);
        container.style.display = 'none';
        document.querySelector('.controls').style.display = 'none';
        document.getElementById('stats').style.display = 'none';
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.taskViewerApp = new TaskViewerApp();
});