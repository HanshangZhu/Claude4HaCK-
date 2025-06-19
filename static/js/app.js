// Drug Repositioning Agent - Frontend JavaScript
class DrugRepositioningApp {
    constructor() {
        this.socket = null;
        this.currentAnalysis = null;
        this.analysisInProgress = false;
        
        this.init();
    }
    
    init() {
        this.initializeSocket();
        this.bindEvents();
        this.checkApiStatus();
    }
    
    initializeSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to server');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });
        
        this.socket.on('analysis_progress', (data) => {
            this.updateProgress(data);
        });
        
        this.socket.on('analysis_complete', (data) => {
            this.displayResults(data.result);
            this.analysisInProgress = false;
            this.updateAnalyzeButton(false);
        });
        
        this.socket.on('analysis_error', (data) => {
            this.showError(data.error);
            this.analysisInProgress = false;
            this.updateAnalyzeButton(false);
        });
    }
    
    bindEvents() {
        // Form submission
        document.getElementById('analysis-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startAnalysis();
        });
        
        // Clear form button
        window.clearForm = () => {
            document.getElementById('user-input').value = '';
            document.getElementById('dry-run-mode').checked = false;
            this.hideAllSections();
        };
        
        // Modal functions
        window.showHistory = () => {
            this.loadHistory();
        };
        
        window.showHelp = () => {
            const helpModal = new bootstrap.Modal(document.getElementById('helpModal'));
            helpModal.show();
        };
        
        // Export functions
        window.exportResults = (format) => {
            this.exportResults(format);
        };
        
        window.printResults = () => {
            this.printResults();
        };
    }
    
    async checkApiStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            
            const statusElement = document.getElementById('api-status');
            if (status.api_key_configured) {
                statusElement.innerHTML = '<i class="bi bi-circle-fill text-success me-1"></i>API Ready';
            } else {
                statusElement.innerHTML = '<i class="bi bi-circle-fill text-warning me-1"></i>Demo Mode Only';
            }
        } catch (error) {
            document.getElementById('api-status').innerHTML = '<i class="bi bi-circle-fill text-danger me-1"></i>Connection Error';
        }
    }
    
    async startAnalysis() {
        if (this.analysisInProgress) return;
        
        const userInput = document.getElementById('user-input').value.trim();
        const dryRun = document.getElementById('dry-run-mode').checked;
        
        if (!userInput) {
            alert('Please enter a disease name or molecular pathology description.');
            return;
        }
        
        this.analysisInProgress = true;
        this.updateAnalyzeButton(true);
        this.hideAllSections();
        this.showProgressSection();
        this.resetProgress();
        
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_input: userInput,
                    dry_run: dryRun
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Join the analysis session
                this.socket.emit('join_analysis', { session_id: data.session_id });
            } else {
                throw new Error(data.error || 'Failed to start analysis');
            }
        } catch (error) {
            this.showError(error.message);
            this.analysisInProgress = false;
            this.updateAnalyzeButton(false);
        }
    }
    
    updateProgress(data) {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        const stepMessage = document.getElementById('step-message');
        
        // Update progress bar
        progressBar.style.width = `${data.progress}%`;
        progressText.textContent = `${data.progress}%`;
        
        // Update step message
        stepMessage.textContent = data.message;
        
        // Update step indicators
        this.updateStepIndicators(data.step);
        
        // Add fade-in animation to progress section
        document.getElementById('progress-section').classList.add('fade-in');
    }
    
    updateStepIndicators(currentStep) {
        for (let i = 1; i <= 3; i++) {
            const stepElement = document.getElementById(`step-${i}`);
            stepElement.classList.remove('active', 'current');
            
            if (i < currentStep) {
                stepElement.classList.add('active');
            } else if (i === currentStep) {
                stepElement.classList.add('current');
            }
        }
    }
    
    displayResults(result) {
        this.currentAnalysis = result;
        
        // Hide progress section
        document.getElementById('progress-section').style.display = 'none';
        
        // Show results section
        document.getElementById('results-section').style.display = 'block';
        document.getElementById('results-section').classList.add('fade-in');
        
        // Update disease information
        document.getElementById('disease-name').textContent = result.molecular_analysis.disease_name;
        document.getElementById('analysis-timestamp').textContent = 
            new Date(result.timestamp).toLocaleString();
        
        // Display molecular markers
        this.displayMolecularMarkers(result.molecular_analysis.molecular_markers);
        
        // Display drug candidates
        this.displayDrugCandidates(result.drug_candidates);
        
        // Display filtering analysis
        this.displayFilterAnalysis(result.filter_analysis);
        
        // Display sources
        this.displaySources(result.molecular_analysis.sources);
        
        // Scroll to results
        document.getElementById('results-section').scrollIntoView({ 
            behavior: 'smooth' 
        });
    }
    
    displayMolecularMarkers(markers) {
        const container = document.getElementById('molecular-markers');
        container.innerHTML = '';
        
        Object.entries(markers).forEach(([category, markerList]) => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'molecular-marker-category bounce-in';
            
            const categoryTitle = document.createElement('h6');
            categoryTitle.textContent = category.replace(/_/g, ' ').toUpperCase();
            categoryDiv.appendChild(categoryTitle);
            
            const markerTags = document.createElement('div');
            markerList.forEach(marker => {
                const tag = document.createElement('span');
                tag.className = 'marker-tag';
                tag.textContent = marker;
                markerTags.appendChild(tag);
            });
            
            categoryDiv.appendChild(markerTags);
            container.appendChild(categoryDiv);
        });
    }
    
    displayDrugCandidates(candidates) {
        const container = document.getElementById('drug-candidates');
        container.innerHTML = '';
        
        candidates.forEach((candidate, index) => {
            const candidateDiv = document.createElement('div');
            candidateDiv.className = 'drug-candidate slide-in-left';
            candidateDiv.style.animationDelay = `${index * 0.1}s`;
            
            const statusClass = candidate.approval_status.toLowerCase().includes('approved') ? '' : 
                              candidate.approval_status.toLowerCase().includes('investigational') ? 'investigational' : 
                              'experimental';
            
            candidateDiv.innerHTML = `
                <div class="drug-name">${candidate.drug_name}</div>
                <div class="drug-status ${statusClass}">${candidate.approval_status}</div>
                <div class="mb-2">
                    <strong>Current Applications:</strong> ${candidate.current_applications.join(', ')}
                </div>
                <div class="mb-2">
                    <strong>Molecular Rationale:</strong> ${candidate.molecular_rationale}
                </div>
                <div>
                    <strong>Shared Pathology:</strong> ${candidate.shared_pathology}
                </div>
            `;
            
            container.appendChild(candidateDiv);
        });
    }
    
    displayFilterAnalysis(analysis) {
        const container = document.getElementById('filter-analysis');
        container.innerHTML = `<div class="fade-in">${analysis.replace(/\n/g, '<br>')}</div>`;
    }
    
    displaySources(sources) {
        const container = document.getElementById('sources');
        container.innerHTML = '';
        
        const sourcesList = document.createElement('ul');
        sourcesList.className = 'list-unstyled fade-in';
        
        sources.forEach(source => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<i class="bi bi-book me-2 text-primary"></i>${source}`;
            listItem.className = 'mb-2';
            sourcesList.appendChild(listItem);
        });
        
        container.appendChild(sourcesList);
    }
    
    showError(message) {
        document.getElementById('progress-section').style.display = 'none';
        document.getElementById('results-section').style.display = 'none';
        
        document.getElementById('error-message').querySelector('span').textContent = message;
        document.getElementById('error-section').style.display = 'block';
        document.getElementById('error-section').classList.add('fade-in');
    }
    
    hideAllSections() {
        document.getElementById('progress-section').style.display = 'none';
        document.getElementById('results-section').style.display = 'none';
        document.getElementById('error-section').style.display = 'none';
    }
    
    showProgressSection() {
        document.getElementById('progress-section').style.display = 'block';
    }
    
    resetProgress() {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        const stepMessage = document.getElementById('step-message');
        
        progressBar.style.width = '0%';
        progressText.textContent = 'Starting...';
        stepMessage.textContent = 'Initializing analysis...';
        
        // Reset step indicators
        for (let i = 1; i <= 3; i++) {
            const stepElement = document.getElementById(`step-${i}`);
            stepElement.classList.remove('active', 'current');
        }
    }
    
    updateAnalyzeButton(loading) {
        const button = document.getElementById('analyze-btn');
        if (loading) {
            button.innerHTML = '<div class="loading-spinner me-2"></div>Analyzing...';
            button.disabled = true;
        } else {
            button.innerHTML = '<i class="bi bi-play-circle me-2"></i>Start Analysis';
            button.disabled = false;
        }
    }
    
    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            const history = await response.json();
            
            const historyContent = document.getElementById('history-content');
            historyContent.innerHTML = '';
            
            if (history.length === 0) {
                historyContent.innerHTML = '<p class="text-muted text-center">No analysis history available.</p>';
            } else {
                history.reverse().forEach((analysis, index) => {
                    const analysisCard = document.createElement('div');
                    analysisCard.className = 'card mb-3';
                    analysisCard.innerHTML = `
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h6 class="mb-0">${analysis.molecular_analysis.disease_name}</h6>
                            <small class="text-muted">${new Date(analysis.timestamp).toLocaleString()}</small>
                        </div>
                        <div class="card-body">
                            <p class="mb-2"><strong>Input:</strong> ${analysis.user_input}</p>
                            <p class="mb-0"><strong>Candidates Found:</strong> ${analysis.drug_candidates.length}</p>
                        </div>
                    `;
                    historyContent.appendChild(analysisCard);
                });
            }
            
            const historyModal = new bootstrap.Modal(document.getElementById('historyModal'));
            historyModal.show();
        } catch (error) {
            alert('Failed to load history: ' + error.message);
        }
    }
    
    exportResults(format) {
        if (!this.currentAnalysis) {
            alert('No analysis results to export.');
            return;
        }
        
        let content, filename, mimeType;
        
        if (format === 'json') {
            content = JSON.stringify(this.currentAnalysis, null, 2);
            filename = `drug_analysis_${Date.now()}.json`;
            mimeType = 'application/json';
        } else if (format === 'txt') {
            content = this.formatResultsAsText(this.currentAnalysis);
            filename = `drug_analysis_${Date.now()}.txt`;
            mimeType = 'text/plain';
        }
        
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    formatResultsAsText(analysis) {
        let text = `DRUG REPOSITIONING ANALYSIS RESULTS\n`;
        text += `${'='.repeat(50)}\n\n`;
        text += `Disease/Condition: ${analysis.molecular_analysis.disease_name}\n`;
        text += `Analysis Date: ${new Date(analysis.timestamp).toLocaleString()}\n`;
        text += `User Input: ${analysis.user_input}\n\n`;
        
        text += `MOLECULAR MARKERS:\n`;
        text += `${'-'.repeat(20)}\n`;
        Object.entries(analysis.molecular_analysis.molecular_markers).forEach(([category, markers]) => {
            text += `${category.replace(/_/g, ' ').toUpperCase()}:\n`;
            markers.forEach(marker => text += `  • ${marker}\n`);
            text += '\n';
        });
        
        text += `DRUG REPOSITIONING CANDIDATES:\n`;
        text += `${'-'.repeat(30)}\n`;
        analysis.drug_candidates.forEach((candidate, index) => {
            text += `${index + 1}. ${candidate.drug_name}\n`;
            text += `   Status: ${candidate.approval_status}\n`;
            text += `   Current Uses: ${candidate.current_applications.join(', ')}\n`;
            text += `   Molecular Rationale: ${candidate.molecular_rationale}\n`;
            text += `   Shared Pathology: ${candidate.shared_pathology}\n\n`;
        });
        
        text += `FILTERING ANALYSIS:\n`;
        text += `${'-'.repeat(20)}\n`;
        text += `${analysis.filter_analysis}\n\n`;
        
        text += `SOURCES:\n`;
        text += `${'-'.repeat(10)}\n`;
        analysis.molecular_analysis.sources.forEach(source => {
            text += `• ${source}\n`;
        });
        
        return text;
    }
    
    printResults() {
        if (!this.currentAnalysis) {
            alert('No analysis results to print.');
            return;
        }
        
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
            <head>
                <title>Drug Repositioning Analysis Results</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1, h2 { color: #0d6efd; }
                    .header { border-bottom: 2px solid #0d6efd; padding-bottom: 10px; }
                    .section { margin: 20px 0; }
                    .candidate { border: 1px solid #ddd; padding: 10px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🧬 Drug Repositioning Analysis Results</h1>
                    <p><strong>Disease/Condition:</strong> ${this.currentAnalysis.molecular_analysis.disease_name}</p>
                    <p><strong>Analysis Date:</strong> ${new Date(this.currentAnalysis.timestamp).toLocaleString()}</p>
                </div>
                
                <div class="section">
                    <h2>Molecular Markers</h2>
                    ${Object.entries(this.currentAnalysis.molecular_analysis.molecular_markers).map(([category, markers]) => `
                        <h3>${category.replace(/_/g, ' ').toUpperCase()}</h3>
                        <ul>${markers.map(marker => `<li>${marker}</li>`).join('')}</ul>
                    `).join('')}
                </div>
                
                <div class="section">
                    <h2>Drug Repositioning Candidates</h2>
                    ${this.currentAnalysis.drug_candidates.map(candidate => `
                        <div class="candidate">
                            <h4>${candidate.drug_name}</h4>
                            <p><strong>Status:</strong> ${candidate.approval_status}</p>
                            <p><strong>Current Uses:</strong> ${candidate.current_applications.join(', ')}</p>
                            <p><strong>Molecular Rationale:</strong> ${candidate.molecular_rationale}</p>
                            <p><strong>Shared Pathology:</strong> ${candidate.shared_pathology}</p>
                        </div>
                    `).join('')}
                </div>
                
                <div class="section">
                    <h2>Filtering Analysis</h2>
                    <p>${this.currentAnalysis.filter_analysis}</p>
                </div>
                
                <div class="section">
                    <h2>Sources</h2>
                    <ul>${this.currentAnalysis.molecular_analysis.sources.map(source => `<li>${source}</li>`).join('')}</ul>
                </div>
            </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DrugRepositioningApp();
}); 