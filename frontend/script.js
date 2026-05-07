// API Base URL
const API_BASE = 'http://localhost:5000';

// Global State
let state = {
    dataUploaded: false,
    modelTrained: false,
    currentK: 3,
    optimalK: 3,
    lastData: null,
    charts: {}
};

// DOM Elements
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const navBtns = document.querySelectorAll('.nav-btn');
const pages = document.querySelectorAll('.page');
const darkModeBtn = document.getElementById('dark-mode-btn');
const modal = document.getElementById('modal');
const closeModal = document.querySelector('.close');

// Event Listeners
document.addEventListener('DOMContentLoaded', initApp);
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', (e) => e.preventDefault());
uploadArea.addEventListener('drop', handleFileDrop);
fileInput.addEventListener('change', handleFileSelect);
uploadBtn.addEventListener('click', uploadFile);
navBtns.forEach(btn => btn.addEventListener('click', handleNavigation));
darkModeBtn.addEventListener('click', toggleDarkMode);
closeModal.addEventListener('click', closeModalDialog);
document.getElementById('preprocess-btn')?.addEventListener('click', preprocessData);
document.getElementById('elbow-btn')?.addEventListener('click', computeElbow);
document.getElementById('train-btn')?.addEventListener('click', trainModel);
document.getElementById('predict-form')?.addEventListener('submit', predictCustomer);
document.getElementById('export-csv-btn')?.addEventListener('click', exportCSV);
document.getElementById('export-report-btn')?.addEventListener('click', exportReport);
document.getElementById('generate-report-btn')?.addEventListener('click', generateReport);

// Initialize App
function initApp() {
    console.log('App initialized');
    checkModelStatus();
    setInterval(checkModelStatus, 5000);
}

// Navigation
function handleNavigation(e) {
    const page = e.currentTarget.dataset.page;
    navBtns.forEach(btn => btn.classList.remove('active'));
    pages.forEach(p => p.classList.remove('active'));
    e.currentTarget.classList.add('active');
    document.getElementById(page).classList.add('active');
}

// File Upload
function handleFileDrop(e) {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        showModal('File Selected', 'File ready to upload. Click "Upload File" to proceed.');
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        uploadBtn.textContent = `📁 ${file.name}`;
        uploadBtn.disabled = false;
    }
}

async function uploadFile() {
    const file = fileInput.files[0];
    if (!file) {
        showModal('Error', 'Please select a file first.');
        return;
    }

    uploadBtn.disabled = true;
    uploadBtn.textContent = '⏳ Uploading...';

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();
        state.dataUploaded = true;
        state.lastData = data;

        // Show preview
        showDataPreview(data);
        showModal('Success', `Dataset uploaded successfully!\n${data.rows} customers, ${data.columns.length} features`);

    } catch (error) {
        showModal('Error', `Upload failed: ${error.message}`);
        console.error(error);
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = '📂 Upload File';
    }
}

function showDataPreview(data) {
    const preview = document.getElementById('preview-section');
    const stats = document.getElementById('data-stats');
    const table = document.getElementById('data-preview');

    let statsHTML = '';
    for (const [key, value] of Object.entries(data.missing_values)) {
        statsHTML += `<div class="stat-item"><strong>${value}</strong><small>${key}</small></div>`;
    }

    stats.innerHTML = `
        <div class="stat-item"><strong>${data.rows}</strong><small>Total Rows</small></div>
        <div class="stat-item"><strong>${data.columns.length}</strong><small>Columns</small></div>
        ${statsHTML}
    `;

    let tableHTML = '<table><thead><tr>';
    data.columns.forEach(col => tableHTML += `<th>${col}</th>`);
    tableHTML += '</tr></thead><tbody>';

    data.preview.forEach(row => {
        tableHTML += '<tr>';
        data.columns.forEach(col => {
            const val = row[col];
            tableHTML += `<td>${typeof val === 'number' ? val.toFixed(2) : val}</td>`;
        });
        tableHTML += '</tr>';
    });

    tableHTML += '</tbody></table>';
    table.innerHTML = tableHTML;
    preview.style.display = 'block';
}

async function preprocessData() {
    if (!state.dataUploaded) {
        showModal('Error', 'Please upload data first.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/preprocess`);
        if (!response.ok) throw new Error('Preprocessing failed');

        const data = await response.json();

        const summary = document.getElementById('preprocessing-summary');
        const details = document.getElementById('preprocessing-details');

        let detailsHTML = '<strong>Preprocessing Steps:</strong><ul>';
        data.preprocessing_summary.steps_completed.forEach(step => {
            detailsHTML += `<li>${step}</li>`;
        });
        detailsHTML += '</ul>';

        detailsHTML += `<p><strong>Final Dataset:</strong> ${data.processed_shape[0]} samples × ${data.processed_shape[1]} features</p>`;

        details.innerHTML = detailsHTML;
        summary.style.display = 'block';

        showModal('Success', 'Data preprocessing completed successfully!');

    } catch (error) {
        showModal('Error', `Preprocessing failed: ${error.message}`);
        console.error(error);
    }
}

async function computeElbow() {
    if (!state.dataUploaded) {
        showModal('Error', 'Please upload data first.');
        return;
    }

    document.getElementById('elbow-btn').disabled = true;
    document.getElementById('elbow-btn').textContent = '⏳ Computing...';

    try {
        const response = await fetch(`${API_BASE}/elbow-method`);
        if (!response.ok) throw new Error('Elbow method failed');

        const data = await response.json();
        state.optimalK = data.optimal_k;
        document.getElementById('k-value').value = data.optimal_k;
        document.getElementById('k-suggestion').textContent = `Suggested: ${data.optimal_k}`;

        // Draw charts
        drawElbowChart(data);
        drawSilhouetteChart(data);

        // Show info
        const info = document.getElementById('elbow-info');
        info.innerHTML = `
            <strong>Analysis Results:</strong>
            <p>Optimal K detected: <span style="color: var(--primary); font-weight: bold;">${data.optimal_k}</span></p>
            <p>Silhouette Score at K=${data.optimal_k}: ${(data.silhouette_scores[data.optimal_k-2]).toFixed(3)}</p>
        `;

        document.getElementById('elbow-chart-container').style.display = 'block';

    } catch (error) {
        showModal('Error', `Elbow method failed: ${error.message}`);
        console.error(error);
    } finally {
        document.getElementById('elbow-btn').disabled = false;
        document.getElementById('elbow-btn').textContent = '📊 Calculate Elbow';
    }
}

function drawElbowChart(data) {
    const ctx = document.getElementById('elbow-chart').getContext('2d');
    
    if (state.charts.elbow) {
        state.charts.elbow.destroy();
    }

    state.charts.elbow = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.k_range,
            datasets: [{
                label: 'Inertia',
                data: data.inertias,
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointBackgroundColor: '#6366f1',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: 'rgba(0,0,0,0.7)' }
                },
                title: {
                    display: true,
                    text: 'Elbow Method - Inertia vs K'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: { color: 'rgba(0,0,0,0.7)' }
                },
                x: {
                    ticks: { color: 'rgba(0,0,0,0.7)' }
                }
            }
        }
    });
}

function drawSilhouetteChart(data) {
    const ctx = document.getElementById('silhouette-chart').getContext('2d');
    
    if (state.charts.silhouette) {
        state.charts.silhouette.destroy();
    }

    state.charts.silhouette = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.k_range,
            datasets: [{
                label: 'Silhouette Score',
                data: data.silhouette_scores,
                backgroundColor: '#8b5cf6',
                borderColor: '#7c3aed',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: 'rgba(0,0,0,0.7)' }
                },
                title: {
                    display: true,
                    text: 'Silhouette Score by K'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: { color: 'rgba(0,0,0,0.7)' }
                },
                x: {
                    ticks: { color: 'rgba(0,0,0,0.7)' }
                }
            }
        }
    });
}

async function trainModel() {
    const k = parseInt(document.getElementById('k-value').value);
    
    if (isNaN(k) || k < 2 || k > 10) {
        showModal('Error', 'K must be between 2 and 10');
        return;
    }

    if (!state.dataUploaded) {
        showModal('Error', 'Please upload and preprocess data first.');
        return;
    }

    document.getElementById('training-status').style.display = 'block';
    document.getElementById('train-btn').disabled = true;

    try {
        const response = await fetch(`${API_BASE}/train?k=${k}`, {
            method: 'POST'
        });

        if (!response.ok) throw new Error('Training failed');

        const data = await response.json();
        state.modelTrained = true;
        state.currentK = k;

        // Show results
        const results = document.getElementById('training-results');
        const summary = document.getElementById('training-summary');

        let clusterHTML = '<strong>Cluster Distribution:</strong><ul>';
        for (const [cluster, info] of Object.entries(data.cluster_statistics)) {
            clusterHTML += `<li>${cluster}: ${info.size} customers (${info.percentage.toFixed(1)}%)</li>`;
        }
        clusterHTML += '</ul>';

        summary.innerHTML = `
            <p><strong>K-Means Model Trained Successfully!</strong></p>
            <p>Number of Clusters: <strong>${data.k}</strong></p>
            <p>Silhouette Score: <strong>${(data.silhouette_score).toFixed(3)}</strong></p>
            <p>Inertia: <strong>${(data.inertia).toFixed(2)}</strong></p>
            ${clusterHTML}
        `;

        results.style.display = 'block';
        showModal('Success', `Model trained successfully with K=${k}!`);

    } catch (error) {
        showModal('Error', `Training failed: ${error.message}`);
        console.error(error);
    } finally {
        document.getElementById('training-status').style.display = 'none';
        document.getElementById('train-btn').disabled = false;
    }
}

async function loadAnalysis() {
    if (!state.modelTrained) {
        showModal('Error', 'Please train a model first.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/clusters`);
        if (!response.ok) throw new Error('Failed to load clusters');

        const data = await response.json();

        // Fetch report for accuracy metrics
        const reportResponse = await fetch(`${API_BASE}/report`);
        const reportData = await reportResponse.json();

        // Display accuracy metrics
        displayAccuracyMetrics(reportData, data.k, data.total_customers);

        // Display insights
        displayKeyInsights(data.cluster_profiles, data.recommendations);

        // Draw PCA chart
        drawPCAChart(data.visualization);

        // Display profiles
        displayProfiles(data.cluster_profiles);

        // Display recommendations
        displayRecommendations(data.recommendations);

        // Draw distribution chart
        drawDistributionChart(data.cluster_profiles);

        // Update stats
        document.getElementById('stat-customers').textContent = data.total_customers;
        document.getElementById('stat-clusters').textContent = data.k;

    } catch (error) {
        console.error(error);
        showModal('Error', `Failed to load analysis: ${error.message}`);
    }
}

function displayAccuracyMetrics(reportData, k, totalCustomers) {
    const silhouette = reportData.summary.silhouette_score || 0;
    const inertia = reportData.summary.inertia || 0;

    // Update silhouette score with interpretation
    document.getElementById('metric-silhouette').textContent = (silhouette).toFixed(3);
    let silhouetteInterpretation = '';
    if (silhouette > 0.7) {
        silhouetteInterpretation = '✅ Excellent cluster separation';
    } else if (silhouette > 0.5) {
        silhouetteInterpretation = '✅ Good cluster separation';
    } else if (silhouette > 0.3) {
        silhouetteInterpretation = '⚠️ Fair cluster separation';
    } else {
        silhouetteInterpretation = '⚠️ Weak cluster separation - consider different K';
    }
    document.getElementById('metric-silhouette-desc').textContent = silhouetteInterpretation;

    // Update inertia (within-cluster sum of squares)
    const inertiaFormatted = inertia > 1000000 ? (inertia / 1000000).toFixed(2) + 'M' : inertia.toFixed(0);
    document.getElementById('metric-inertia').textContent = inertiaFormatted;
    
    document.getElementById('metric-k').textContent = k;
    document.getElementById('metric-total').textContent = totalCustomers.toLocaleString();

    // Update dashboard stats
    document.getElementById('stat-silhouette').textContent = (silhouette * 100).toFixed(1) + '%';
}

function displayKeyInsights(clusterProfiles, recommendations) {
    const container = document.getElementById('insights-container');
    let html = '';

    // Cluster size insights
    const sizes = Object.values(clusterProfiles).map(p => p.size);
    const avgSize = sizes.reduce((a, b) => a + b, 0) / sizes.length;
    const largestCluster = Math.max(...sizes);
    const smallestCluster = Math.min(...sizes);

    html += `
        <div class="insight-card">
            <h4>📈 Cluster Distribution</h4>
            <p>Largest Segment: ${largestCluster.toLocaleString()} customers</p>
            <p>Smallest Segment: ${smallestCluster.toLocaleString()} customers</p>
            <p>Average Segment: ${Math.round(avgSize).toLocaleString()} customers</p>
        </div>
    `;

    // Get top recommendation insights
    const topInsights = Object.entries(recommendations).slice(0, 2);
    topInsights.forEach(([cluster, rec]) => {
        const recommendations_list = rec.recommendations || [];
        html += `
            <div class="insight-card">
                <h4>🎯 ${rec.label || cluster}</h4>
                <p><strong>Size:</strong> ${rec.percentage}</p>
                <p><strong>Strategy:</strong> ${rec.marketing_strategy?.primary_channel || 'Multi-channel'}</p>
                <ul>
                    ${recommendations_list.slice(0, 2).map(r => `<li>${r}</li>`).join('')}
                </ul>
            </div>
        `;
    });

    // Value analysis
    let totalValue = 0;
    let topValueCluster = '';
    let maxValue = 0;

    Object.entries(clusterProfiles).forEach(([cluster, profile]) => {
        const avgSpending = profile.avg_spending || profile.avg_mntwines || 0;
        totalValue += avgSpending * profile.size;
        if (avgSpending > maxValue) {
            maxValue = avgSpending;
            topValueCluster = cluster;
        }
    });

    if (topValueCluster) {
        const topProfile = clusterProfiles[topValueCluster];
        html += `
            <div class="insight-card">
                <h4>💰 Value Analysis</h4>
                <p><strong>Highest Value Segment:</strong> ${topValueCluster}</p>
                <p><strong>Average Spending:</strong> $${(maxValue).toFixed(2)}</p>
                <p><strong>Segment Size:</strong> ${topProfile.size.toLocaleString()} customers</p>
            </div>
        `;
    }

    // Growth opportunities
    const lowestSize = Math.min(...sizes);
    const lowestCluster = Object.entries(clusterProfiles).find(([_, p]) => p.size === lowestSize);
    
    if (lowestCluster) {
        html += `
            <div class="insight-card">
                <h4>🚀 Growth Opportunities</h4>
                <p><strong>Underrepresented Segment:</strong> ${lowestCluster[0]}</p>
                <p><strong>Current Size:</strong> ${lowestSize.toLocaleString()} customers</p>
                <p>Focus acquisition efforts on this segment to balance portfolio</p>
            </div>
        `;
    }

    container.innerHTML = html;
}

function drawPCAChart(visualization) {
    const container = document.getElementById('pca-chart-container');
    const colors = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];

    const traces = [];
    const uniqueClusters = [...new Set(visualization.clusters)];

    uniqueClusters.forEach(cluster => {
        const indices = visualization.clusters
            .map((c, i) => c === cluster ? i : -1)
            .filter(i => i !== -1);

        traces.push({
            x: indices.map(i => visualization.x[i]),
            y: indices.map(i => visualization.y[i]),
            mode: 'markers',
            name: `Cluster ${cluster}`,
            marker: {
                size: 8,
                color: colors[cluster % colors.length],
                opacity: 0.7,
                line: {
                    color: 'white',
                    width: 1
                }
            },
            type: 'scatter'
        });
    });

    const layout = {
        title: 'Customer Segments - PCA Projection',
        xaxis: { title: 'Principal Component 1' },
        yaxis: { title: 'Principal Component 2' },
        hovermode: 'closest',
        showlegend: true,
        height: 400
    };

    Plotly.newPlot(container, traces, layout, { responsive: true });
}

function displayProfiles(profiles) {
    const container = document.getElementById('profiles-container');
    let html = '';

    for (const [cluster, profile] of Object.entries(profiles)) {
        const clusterLabel = profile.cluster_id !== undefined ? `Cluster ${profile.cluster_id}` : cluster;
        
        // Extract key metrics
        const avgSpending = profile.avg_spending || profile.avg_mntwines || profile.avg_mntmeatproducts || 0;
        const avgIncome = profile.avg_income || 0;
        const avgAge = profile.avg_age || (2026 - profile.avg_year_birth) || 0;
        
        html += `
            <div class="info-box">
                <strong style="font-size: 15px; color: var(--primary);">📊 ${clusterLabel}</strong>
                <p style="margin-top: 10px;"><strong>👥 Size:</strong> ${profile.size.toLocaleString()} customers (${profile.percentage.toFixed(1)}%)</p>
                <p><strong>💵 Avg Income:</strong> $${avgIncome.toFixed(0)}</p>
                <p><strong>💳 Avg Spending:</strong> $${avgSpending.toFixed(0)}</p>
        `;

        if (avgAge > 0) {
            html += `<p><strong>📅 Avg Age:</strong> ${Math.round(avgAge)} years</p>`;
        }

        // Add detailed metrics
        const metrics = Object.entries(profile)
            .filter(([k, v]) => (k.startsWith('avg_') || k.startsWith('median_')) && typeof v === 'number')
            .filter(([k, v]) => !k.includes('year_birth'));

        if (metrics.length > 5) {
            html += `<p style="font-size: 12px; color: var(--text-light); margin-top: 10px;"><em>✓ Additional ${metrics.length} metrics available</em></p>`;
        }

        html += '</div>';
    }

    container.innerHTML = html;
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations-container');
    let html = '';

    for (const [cluster, rec] of Object.entries(recommendations)) {
        const strategy = rec.marketing_strategy || {};
        const recommendations_list = rec.recommendations || [];
        
        html += `
            <div class="info-box">
                <strong style="color: var(--primary); font-size: 16px;">🎯 ${rec.label || cluster}</strong>
                <p style="margin-top: 10px;"><strong>📊 Segment Size:</strong> ${rec.percentage}</p>
                <p><strong>📱 Primary Channel:</strong> ${strategy.primary_channel || 'Multi-channel'}</p>
                <p><strong>⏱️ Campaign Frequency:</strong> ${strategy.frequency || 'Regular'}</p>
                <p><strong>💰 Investment Priority:</strong> ${strategy.investment_priority || 'Medium'}</p>
                <strong style="display: block; margin-top: 10px;">💡 Recommendations:</strong>
                <ul style="margin-left: 20px; margin-top: 8px;">
                    ${recommendations_list.slice(0, 3).map(r => `<li style="font-size: 13px; margin-bottom: 5px;">${r}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    container.innerHTML = html;
}

function drawDistributionChart(profiles) {
    const ctx = document.getElementById('distribution-chart').getContext('2d');
    
    if (state.charts.distribution) {
        state.charts.distribution.destroy();
    }

    const clusters = Object.keys(profiles);
    const sizes = clusters.map(c => profiles[c].size);
    const colors = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];

    state.charts.distribution = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: clusters,
            datasets: [{
                data: sizes,
                backgroundColor: colors.slice(0, clusters.length),
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: { color: 'rgba(0,0,0,0.7)' }
                }
            }
        }
    });
}

async function predictCustomer(e) {
    e.preventDefault();

    const age = parseInt(document.getElementById('pred-age').value);
    const income = parseFloat(document.getElementById('pred-income').value);
    const spending = parseFloat(document.getElementById('pred-spending').value);

    try {
        const response = await fetch(`${API_BASE}/predict?age=${age}&income=${income}&spending=${spending}`, {
            method: 'POST'
        });

        if (!response.ok) throw new Error('Prediction failed');

        const data = await response.json();

        const result = document.getElementById('prediction-result');
        const details = document.getElementById('prediction-details');

        details.innerHTML = `
            <p><strong>Cluster:</strong> ${data.cluster_name}</p>
            <p><strong>Segment ID:</strong> ${data.cluster}</p>
            <p><strong>Distance to Center:</strong> ${data.distance_to_center.toFixed(3)}</p>
            <p><strong>Input:</strong> Age: ${data.input.age}, Income: $${data.input.income}, Spending: $${data.input.spending}</p>
            <p><strong>Recommendation:</strong> ${typeof data.recommendation === 'string' ? data.recommendation : 'See cluster analysis'}</p>
        `;

        result.style.display = 'block';

    } catch (error) {
        showModal('Error', `Prediction failed: ${error.message}`);
        console.error(error);
    }
}

async function generateReport() {
    try {
        const response = await fetch(`${API_BASE}/report`);
        if (!response.ok) throw new Error('Report generation failed');

        const data = await response.json();
        const container = document.getElementById('report-content');

        let html = `
            <h4>Summary</h4>
            <p>Total Customers: ${data.summary.total_customers}</p>
            <p>Clusters: ${data.summary.clusters}</p>
            <p>Silhouette Score: ${(data.summary.silhouette_score).toFixed(3)}</p>
            <h4>Cluster Profiles</h4>
        `;

        for (const [cluster, profile] of Object.entries(data.cluster_profiles)) {
            html += `
                <div class="info-box">
                    <strong>${cluster}</strong>
                    <p>Size: ${profile.size} (${profile.percentage.toFixed(1)}%)</p>
                </div>
            `;
        }

        container.innerHTML = html;
        document.getElementById('report-container').style.display = 'block';

    } catch (error) {
        showModal('Error', `Report generation failed: ${error.message}`);
        console.error(error);
    }
}

async function exportCSV() {
    try {
        window.location.href = `${API_BASE}/export`;
        showModal('Success', 'Download started');
    } catch (error) {
        showModal('Error', `Export failed: ${error.message}`);
    }
}

async function exportReport() {
    try {
        const response = await fetch(`${API_BASE}/report`);
        if (!response.ok) throw new Error('Export failed');

        const data = await response.json();
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data, null, 2)));
        element.setAttribute('download', 'clustering_report.json');
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);

        showModal('Success', 'Report downloaded');
    } catch (error) {
        showModal('Error', `Export failed: ${error.message}`);
    }
}

async function checkModelStatus() {
    try {
        const response = await fetch(`${API_BASE}/model-status`);
        if (!response.ok) return;

        const data = await response.json();
        const indicator = document.getElementById('status-indicator');
        const info = document.getElementById('status-info');

        if (data.model_trained) {
            indicator.className = 'status-indicator status-green';
            indicator.textContent = '🟢 Ready';
            info.textContent = `K=${data.k} | ${data.customers} customers`;
            state.modelTrained = true;
        } else {
            indicator.className = 'status-indicator status-red';
            indicator.textContent = '🔴 Not Ready';
            info.textContent = data.data_uploaded ? 'Data uploaded' : 'No data';
            state.modelTrained = false;
        }
    } catch (error) {
        console.log('Model status check failed');
    }
}

// Navigation to Analysis tab when model loads
document.addEventListener('DOMContentLoaded', () => {
    // Listen for model training
    const originalTrain = trainModel;
    trainModel = async function() {
        await originalTrain.call(this);
        if (state.modelTrained) {
            setTimeout(() => {
                document.querySelector('[data-page="analysis"]').click();
                loadAnalysis();
            }, 1000);
        }
    };
});

// Dark Mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Modal Functions
function showModal(title, message) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-message').textContent = message;
    modal.classList.add('show');
}

function closeModalDialog() {
    modal.classList.remove('show');
}

document.getElementById('modal-btn')?.addEventListener('click', closeModalDialog);

// Load analysis when navigating to analysis page
document.querySelector('[data-page="analysis"]')?.addEventListener('click', () => {
    setTimeout(loadAnalysis, 100);
});

// Auto-refresh analysis every 5 seconds if on analysis page
setInterval(() => {
    if (document.getElementById('analysis').classList.contains('active') && state.modelTrained) {
        loadAnalysis();
    }
}, 5000);
