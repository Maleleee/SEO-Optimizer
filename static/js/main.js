let currentUrl = '';
let currentAnalysis = null;

// Initialize Bootstrap modal for saving analyses
const saveModal = new bootstrap.Modal(document.getElementById('saveAnalysisModal'));

// Initialize all tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Format score with appropriate color class
function formatScore(score) {
    if (typeof score !== 'number') {
        console.error('Invalid score:', score);
        return `<span class="text-danger">N/A</span>`;
    }
    if (score >= 90) {
        return `<span class="text-success">${score.toFixed(1)}</span>`;
    } else if (score >= 70) {
        return `<span class="text-warning">${score.toFixed(1)}</span>`;
    } else {
        return `<span class="text-danger">${score.toFixed(1)}</span>`;
    }
}

// Format status with appropriate icon and color
function formatStatus(status) {
    if (status) {
        return '<i class="fas fa-check-circle text-success"></i>';
    } else {
        return '<i class="fas fa-times-circle text-danger"></i>';
    }
}

// Update progress bar and status message
function updateProgress(step, total) {
    const progress = (step / total) * 100;
    document.getElementById('analysisProgress').style.width = `${progress}%`;
    document.getElementById('progressStatus').textContent = `Analyzing... ${step}/${total}`;
}

// Handle form submission
document.getElementById('seoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('url').value;
    currentUrl = url;
    
    // Show loading state
    document.querySelector('.loading').style.display = 'block';
    document.querySelector('.result-section').style.display = 'none';
    document.getElementById('analysisProgress').style.width = '0%';
    document.getElementById('progressStatus').textContent = 'Starting analysis...';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        currentAnalysis = data;
        
        if (data.status === 'error') {
            throw new Error(data.message);
        }
        
        // Update UI with results
        document.getElementById('title').textContent = data.title;
        document.getElementById('metaDescription').textContent = data.meta_description;
        document.getElementById('wordCount').textContent = data.word_count;

        // Debugging statements to check values
        console.log('Readability Score:', data.readability_score);
        console.log('Page Load Time:', data.performance.page_load_time);
        console.log('Server Response Time:', data.performance.server_response_time);

        document.getElementById('readabilityScore').textContent = data.readability_score.toFixed(2);
        
        // Update performance metrics
        document.getElementById('pageLoadTime').textContent = `${data.performance.page_load_time.toFixed(2)}s`;
        document.getElementById('serverResponseTime').textContent = `${data.performance.server_response_time.toFixed(2)}s`;
        document.getElementById('resourceCount').textContent = data.performance.resource_count;
        document.getElementById('performanceScore').innerHTML = formatScore(data.performance.performance_score);
        
        // Update overall SEO score
        const overallScore = data.overall_seo_score;
        document.getElementById('overallScore').innerHTML = formatScore(overallScore);
        
        // Update score breakdown
        const scoreBreakdown = document.getElementById('scoreBreakdown');
        scoreBreakdown.innerHTML = `
            <div class="mb-2">
                <strong>Performance:</strong> ${formatScore(data.performance.performance_score)} (25% weight)
            </div>
            <div class="mb-2">
                <strong>Mobile:</strong> ${formatScore(data.mobile.mobile_score)} (20% weight)
            </div>
            <div class="mb-2">
                <strong>Content:</strong> ${formatScore(data.content_quality.score)} (20% weight)
            </div>
            <div class="mb-2">
                <strong>Technical:</strong> ${formatScore(data.technical_score)} (20% weight)
            </div>
            <div class="mb-2">
                <strong>Readability:</strong> ${formatScore(data.readability_score * 100)} (15% weight)
            </div>
        `;
        
        // Update mobile metrics
        document.getElementById('mobileFriendly').innerHTML = formatStatus(data.mobile.is_mobile_friendly);
        document.getElementById('viewportWidth').textContent = data.mobile.viewport_width;
        document.getElementById('responsiveImages').textContent = data.mobile.responsive_images;
        document.getElementById('hasMediaQueries').innerHTML = formatStatus(data.mobile.has_media_queries);
        document.getElementById('mobileScore').innerHTML = formatScore(data.mobile.mobile_score);
        
        // Update recommendations
        const recommendationsList = document.getElementById('recommendations');
        recommendationsList.innerHTML = '';
        data.mobile.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recommendationsList.appendChild(li);
        });
        
        // Update keyword density chart
        const keywordData = Object.entries(data.keyword_density).map(([keyword, density]) => ({
            keyword,
            density
        }));
        
        const trace = {
            x: keywordData.map(d => d.keyword),
            y: keywordData.map(d => d.density),
            type: 'bar',
            marker: {
                color: keywordData.map(d => d.density),
                colorscale: 'Viridis'
            }
        };
        
        const layout = {
            title: 'Keyword Density Analysis',
            xaxis: {
                title: 'Keyword'
            },
            yaxis: {
                title: 'Density (%)'
            },
            margin: {
                t: 50,
                b: 100,
                l: 50,
                r: 20
            }
        };
        
        Plotly.newPlot('keywordChart', [trace], layout);
        
        // Show results
        document.querySelector('.loading').style.display = 'none';
        document.querySelector('.result-section').style.display = 'block';
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis: ' + error.message);
        document.querySelector('.loading').style.display = 'none';
    }
});

// Handle save analysis
document.getElementById('saveAnalysisBtn').addEventListener('click', async () => {
    if (!currentAnalysis) {
        alert('No analysis to save');
        return;
    }
    
    const notes = document.getElementById('analysisNotes').value;
    
    try {
        const response = await fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: currentUrl,
                analysis: currentAnalysis,
                notes: notes
            })
        });
        
        const result = await response.json();
        if (result.status === 'success') {
            alert('Analysis saved successfully');
            saveModal.hide();
            // Refresh saved analyses list
            location.reload();
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to save analysis: ' + error.message);
    }
});

// Handle load analysis
document.querySelectorAll('.load-analysis-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        const filename = e.target.dataset.filename;
        try {
            const response = await fetch(`/load/${filename}`);
            const result = await response.json();
            
            if (result.status === 'success') {
                currentAnalysis = result.data.data;
                currentUrl = result.data.url;
                
                // Update UI with loaded data
                document.getElementById('url').value = currentUrl;
                // Trigger form submission to update UI
                document.getElementById('seoForm').dispatchEvent(new Event('submit'));
            } else {
                throw new Error(result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to load analysis: ' + error.message);
        }
    });
});

// Handle export to PDF
document.getElementById('exportBtn').addEventListener('click', async () => {
    if (!currentUrl) {
        alert('No analysis to export');
        return;
    }
    
    try {
        const response = await fetch('/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: currentUrl })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `seo_report_${new Date().toISOString().slice(0,19).replace(/[:]/g, '')}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            throw new Error('Failed to generate PDF');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to export report: ' + error.message);
    }
});