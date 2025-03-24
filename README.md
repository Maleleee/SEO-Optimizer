# SEO-Sensei: Smart Content Optimization

A comprehensive SEO analysis tool built with Python Flask that provides detailed insights into website performance, mobile responsiveness, and SEO metrics. SEO-Sensei helps you optimize your content with AI-powered analysis and smart recommendations.

## ⚠️ Technical Requirements

This tool is built using Python Flask and requires technical knowledge to set up and run. It is not suitable for deployment on static hosting services like GitHub Pages due to its server-side processing requirements.

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Technical knowledge of Python and web development

## Features

### 1. Performance Analysis
- Page load time estimation
- Server response time measurement
- Resource count analysis (scripts, stylesheets, images)
- Performance scoring system
- Detailed recommendations for optimization

### 2. Mobile Responsiveness Analysis
- Mobile-friendly detection
- Viewport configuration check
- Responsive images analysis
- Media queries detection
- Mobile optimization scoring
- Specific recommendations for mobile improvements

### 3. SEO Analysis
- Title tag analysis (length and optimization)
- Meta description evaluation
- Content length and quality assessment
- Readability scoring
- Keyword density analysis
- URL structure evaluation

### 4. User Interface
- Interactive progress bar during analysis
- Detailed tooltips explaining each metric
- Visual keyword density chart
- Color-coded status indicators
- Mobile-responsive design

### 5. Additional Features
- Save analysis results locally
- Load previous analyses
- Export detailed PDF reports
- Comprehensive recommendations section

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Maleleee/SEO-Sensei.git
cd SEO-Sensei
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage Examples

### Basic Analysis
1. Enter a URL in the input field (e.g., `https://example.com`)
2. Click "Analyze" to start the process
3. Watch the progress bar for real-time updates
4. Review the comprehensive analysis results

### Saving Analysis Results
1. After analysis is complete, click "Save Analysis"
2. Add optional notes about the analysis
3. Click "Save" to store the results locally
4. Access saved analyses from the "Saved Analyses" section

### Loading Previous Analyses
1. Go to the "Saved Analyses" section
2. Click "Load" next to any saved analysis
3. The results will be displayed as if it was a new analysis
4. You can compare different analyses or track changes over time

### Exporting Reports
1. After analysis is complete, click "Export Report"
2. Choose the format (PDF)
3. The report will be downloaded automatically
4. Share the report with team members or clients

### Example Analysis Results
```
Performance Score: 85/100
- Page Load Time: 2.3s
- Server Response Time: 150ms
- Resource Count: 12

Mobile Score: 90/100
- Mobile-Friendly: Yes
- Responsive Images: 8/10
- Media Queries: Present

SEO Score: 75/100
- Title Length: 55 characters
- Meta Description: 155 characters
- Readability Score: 0.8
```

## Troubleshooting Guide

### Common Issues and Solutions

1. **Installation Problems**
   - **Error**: "ModuleNotFoundError: No module named 'flask'"
   - **Solution**: Run `pip install -r requirements.txt` again
   - **Alternative**: Install packages individually: `pip install flask beautifulsoup4 requests pandas nltk reportlab`

2. **URL Analysis Issues**
   - **Error**: "Failed to fetch URL"
   - **Solutions**:
     - Check if the URL is accessible
     - Ensure the URL starts with http:// or https://
     - Try removing trailing slashes
     - Check if the website blocks web scraping

3. **Performance Issues**
   - **Problem**: Analysis takes too long
   - **Solutions**:
     - Check your internet connection
     - Try analyzing smaller pages first
     - Close other resource-intensive applications
     - Check if the website is experiencing high traffic

4. **PDF Export Problems**
   - **Error**: "Failed to generate PDF"
   - **Solutions**:
     - Ensure you have write permissions in the download folder
     - Try a different browser
     - Check if the PDF viewer is up to date
     - Try saving the analysis first, then export

5. **Browser Compatibility**
   - **Problem**: UI elements not displaying correctly
   - **Solutions**:
     - Update your browser to the latest version
     - Clear browser cache and cookies
     - Try a different browser (Chrome recommended)
     - Disable browser extensions temporarily

### Getting Help

If you encounter issues not covered in this guide:
1. Check the [GitHub Issues](https://github.com/Maleleee/SEO-Sensei/issues) page
2. Create a new issue with:
   - Detailed error message
   - Steps to reproduce
   - Screenshots if applicable
   - Your system information

## Understanding the Analysis Results

### Performance Metrics
- **Page Load Time**: Estimated time for complete page loading (optimal: < 3 seconds)
- **Server Response Time**: Time taken by server to respond (optimal: < 200ms)
- **Resource Count**: Total number of page resources (scripts, stylesheets, images)
- **Performance Score**: Overall performance rating (90-100: Excellent, 70-89: Good, <70: Needs improvement)

### Mobile Responsiveness
- **Mobile-Friendly Status**: Indicates if the site is optimized for mobile devices
- **Viewport Configuration**: Checks for proper mobile viewport settings
- **Responsive Images**: Counts images that adapt to different screen sizes
- **Media Queries**: Detects responsive design implementation
- **Mobile Score**: Overall mobile optimization rating

### SEO Metrics
- **Title Length**: Optimal range: 50-60 characters
- **Meta Description**: Optimal range: 150-160 characters
- **Word Count**: Content length analysis
- **Readability Score**: Range from -1 to 1 (higher is better)
- **Keyword Density**: Optimal range: 1-3% per keyword

## Technical Limitations

1. **Server-Side Processing**: The tool requires Python Flask to run and cannot be deployed on static hosting services.
2. **Local Storage**: Analysis results are saved locally on the user's machine.
3. **URL Access**: The tool can only analyze publicly accessible URLs.
4. **Resource Usage**: Analysis of large websites may take longer to complete.

## Development

The project structure is organized as follows:
```
SEO-Sensei/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css  # Custom styles
│   └── js/
│       └── main.js    # Frontend functionality
└── templates/
    └── index.html     # Main application template
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask web framework
- BeautifulSoup4 for HTML parsing
- NLTK for natural language processing
- Plotly for data visualization
- Bootstrap for UI components

## Author

Allen Takahashi - [Maleleee](https://github.com/Maleleee)
 
