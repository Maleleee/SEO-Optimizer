from flask import Flask, render_template, request, jsonify, send_file, make_response
from bs4 import BeautifulSoup
import requests
import pandas as pd
import plotly.express as px
import plotly.utils
import json
from urllib.parse import urlparse, urljoin
import nltk
from textblob import TextBlob
import re
from collections import Counter
import os
from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime
import time
from src.analyzers.performance_analyzer import PerformanceAnalyzer
from src.analyzers.mobile_analyzer import MobileAnalyzer
from src.utils.helpers import save_analysis, load_analysis, list_saved_analyses, format_score, format_status

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

app = Flask(__name__)
load_dotenv()

def analyze_images(soup, base_url):
    images = soup.find_all('img')
    image_analysis = {
        'total_images': len(images),
        'images_with_alt': 0,
        'images_without_alt': 0,
        'image_sizes': [],
        'missing_alt_texts': []
    }
    
    for img in images:
        if img.get('alt'):
            image_analysis['images_with_alt'] += 1
        else:
            image_analysis['images_without_alt'] += 1
            if img.get('src'):
                image_analysis['missing_alt_texts'].append(img.get('src'))
        
        # Get image dimensions if available
        if img.get('width') and img.get('height'):
            image_analysis['image_sizes'].append({
                'width': img.get('width'),
                'height': img.get('height'),
                'src': img.get('src')
            })
    
    return image_analysis

def analyze_links(soup, base_url):
    links = soup.find_all('a')
    link_analysis = {
        'total_links': len(links),
        'internal_links': 0,
        'external_links': 0,
        'broken_links': [],
        'link_texts': []
    }
    
    for link in links:
        href = link.get('href')
        if href:
            absolute_url = urljoin(base_url, href)
            if base_url in absolute_url:
                link_analysis['internal_links'] += 1
            else:
                link_analysis['external_links'] += 1
            
            link_text = link.get_text().strip()
            if link_text:
                link_analysis['link_texts'].append({
                    'text': link_text,
                    'url': absolute_url
                })
    
    return link_analysis

def analyze_headings(soup):
    headings = {
        'h1': len(soup.find_all('h1')),
        'h2': len(soup.find_all('h2')),
        'h3': len(soup.find_all('h3')),
        'h4': len(soup.find_all('h4')),
        'h5': len(soup.find_all('h5')),
        'h6': len(soup.find_all('h6'))
    }
    return headings

def analyze_content_quality(text_content):
    sentences = nltk.sent_tokenize(text_content)
    words = nltk.word_tokenize(text_content)
    
    # Calculate average sentence length
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    
    # Calculate unique word ratio
    unique_words = set(words)
    unique_word_ratio = len(unique_words) / len(words)
    
    # Analyze sentence complexity
    complex_sentences = sum(1 for s in sentences if len(nltk.word_tokenize(s)) > 20)
    
    return {
        'avg_sentence_length': round(avg_sentence_length, 2),
        'unique_word_ratio': round(unique_word_ratio * 100, 2),
        'complex_sentences': complex_sentences,
        'total_sentences': len(sentences)
    }

def analyze_social_media(soup):
    social_platforms = {
        'facebook': ['facebook.com', 'fb.com'],
        'twitter': ['twitter.com', 'x.com'],
        'linkedin': ['linkedin.com'],
        'instagram': ['instagram.com'],
        'youtube': ['youtube.com']
    }
    
    social_links = {platform: [] for platform in social_platforms}
    
    for link in soup.find_all('a'):
        href = link.get('href', '')
        for platform, domains in social_platforms.items():
            if any(domain in href.lower() for domain in domains):
                social_links[platform].append(href)
    
    return social_links

def analyze_url(url):
    try:
        print(f"Starting analysis for URL: {url}")
        start_time = time.time()
        response = requests.get(url)
        server_response_time = time.time() - start_time
        print(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            return {
                'status': 'error',
                'message': f'Failed to fetch URL. Status code: {response.status_code}'
            }
            
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Successfully parsed HTML")
        
        # Performance analysis
        print("Starting performance analysis...")
        performance_analyzer = PerformanceAnalyzer(soup, response, server_response_time)
        performance = performance_analyzer.analyze()
        
        # Mobile responsiveness analysis
        print("Starting mobile analysis...")
        mobile_analyzer = MobileAnalyzer(soup)
        mobile = mobile_analyzer.analyze()
        
        # Basic SEO analysis
        title = soup.title.string if soup.title else "No title found"
        title_length = len(title) if title else 0
        print(f"Title length: {title_length}")
        
        meta_description = soup.find('meta', {'name': 'description'})
        meta_description = meta_description['content'] if meta_description else "No meta description found"
        meta_length = len(meta_description) if meta_description else 0
        print(f"Meta description length: {meta_length}")
        
        # Get all text content
        text_content = soup.get_text()
        words = text_content.lower().split()
        word_count = len(words)
        print(f"Word count: {word_count}")
        
        # Keyword density analysis
        word_freq = Counter(words)
        keyword_density = {word: (count/word_count)*100 for word, count in word_freq.most_common(10)}
        print(f"Top keywords: {list(keyword_density.keys())[:5]}")
        
        # Readability analysis
        blob = TextBlob(text_content)
        readability_score = blob.sentiment.polarity
        print(f"Readability score: {readability_score}")
        
        # URL structure analysis
        parsed_url = urlparse(url)
        url_structure = {
            'scheme': parsed_url.scheme,
            'netloc': parsed_url.netloc,
            'path': parsed_url.path,
            'params': parsed_url.params,
            'query': parsed_url.query,
            'fragment': parsed_url.fragment
        }
        print(f"URL structure analyzed")
        
        # Enhanced analysis
        print("Starting image analysis...")
        image_analysis = analyze_images(soup, url)
        
        print("Starting link analysis...")
        link_analysis = analyze_links(soup, url)
        
        print("Starting heading analysis...")
        heading_analysis = analyze_headings(soup)
        
        print("Starting content quality analysis...")
        content_quality = analyze_content_quality(text_content)
        
        print("Starting social media analysis...")
        social_media = analyze_social_media(soup)
        
        print("All analysis completed successfully")
        
        return {
            'title': title,
            'title_length': title_length,
            'meta_description': meta_description,
            'meta_length': meta_length,
            'word_count': word_count,
            'keyword_density': keyword_density,
            'readability_score': readability_score,
            'url': url,
            'url_length': len(url),
            'url_structure': url_structure,
            'image_analysis': image_analysis,
            'link_analysis': link_analysis,
            'heading_analysis': heading_analysis,
            'content_quality': content_quality,
            'social_media': social_media,
            'performance': performance,
            'mobile': mobile,
            'status': 'success'
        }
    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return {
            'status': 'error',
            'message': f'Failed to fetch URL: {str(e)}'
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'status': 'error',
            'message': f'An unexpected error occurred: {str(e)}'
        }

def generate_pdf_report(data, url):
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        title = f"SEO Analysis Report for {url}"
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 20))
        
        # Basic Information
        elements.append(Paragraph("Basic Information", styles['Heading1']))
        elements.append(Paragraph(f"URL: {url}", styles['Normal']))
        elements.append(Paragraph(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Title Analysis
        elements.append(Paragraph("Title Analysis", styles['Heading1']))
        elements.append(Paragraph(f"Title: {data['title']}", styles['Normal']))
        elements.append(Paragraph(f"Length: {data['title_length']} characters", styles['Normal']))
        elements.append(Paragraph(f"Status: {'Optimal' if 50 <= data['title_length'] <= 60 else 'Could be improved'}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Meta Description
        elements.append(Paragraph("Meta Description", styles['Heading1']))
        elements.append(Paragraph(f"Description: {data['meta_description']}", styles['Normal']))
        elements.append(Paragraph(f"Length: {data['meta_length']} characters", styles['Normal']))
        elements.append(Paragraph(f"Status: {'Optimal' if 150 <= data['meta_length'] <= 160 else 'Could be improved'}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Content Statistics
        elements.append(Paragraph("Content Statistics", styles['Heading1']))
        elements.append(Paragraph(f"Word Count: {data['word_count']}", styles['Normal']))
        elements.append(Paragraph(f"Average Sentence Length: {data['content_quality']['avg_sentence_length']:.1f} words", styles['Normal']))
        elements.append(Paragraph(f"Unique Word Ratio: {data['content_quality']['unique_word_ratio']*100:.1f}%", styles['Normal']))
        elements.append(Paragraph(f"Complex Sentences: {data['content_quality']['complex_sentences']} ({data['content_quality']['complex_sentences']/data['content_quality']['total_sentences']*100:.1f}%)", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Readability Score
        elements.append(Paragraph("Readability Score", styles['Heading1']))
        elements.append(Paragraph(f"Score: {data['readability_score']:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Status: {'Very Readable' if data['readability_score'] > 0.6 else 'Moderately Readable' if data['readability_score'] > 0.3 else 'Difficult to Read'}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Image Analysis
        elements.append(Paragraph("Image Analysis", styles['Heading1']))
        image_data = data['image_analysis']
        elements.append(Paragraph(f"Total Images: {image_data['total_images']}", styles['Normal']))
        elements.append(Paragraph(f"Images with Alt Text: {image_data['images_with_alt']}", styles['Normal']))
        elements.append(Paragraph(f"Images without Alt Text: {image_data['images_without_alt']}", styles['Normal']))
        elements.append(Paragraph(f"Status: {'Good' if image_data['images_with_alt']/image_data['total_images'] > 0.8 else 'Needs Improvement'}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Link Analysis
        elements.append(Paragraph("Link Analysis", styles['Heading1']))
        link_data = data['link_analysis']
        elements.append(Paragraph(f"Total Links: {link_data['total_links']}", styles['Normal']))
        elements.append(Paragraph(f"Internal Links: {link_data['internal_links']}", styles['Normal']))
        elements.append(Paragraph(f"External Links: {link_data['external_links']}", styles['Normal']))
        elements.append(Paragraph(f"Status: {'Good Internal Linking' if link_data['internal_links'] > link_data['external_links'] else 'Consider Adding More Internal Links'}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Heading Structure
        elements.append(Paragraph("Heading Structure", styles['Heading1']))
        heading_data = data['heading_analysis']
        for level, count in heading_data.items():
            elements.append(Paragraph(f"{level.upper()}: {count}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Keyword Analysis
        elements.append(Paragraph("Top Keywords", styles['Heading1']))
        for keyword, density in data['keyword_density'].items():
            elements.append(Paragraph(f"{keyword}: {density:.2f}%", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Social Media Presence
        elements.append(Paragraph("Social Media Presence", styles['Heading1']))
        social_data = data['social_media']
        for platform, links in social_data.items():
            elements.append(Paragraph(f"{platform}: {'Present' if links else 'Not Found'}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # URL Structure
        elements.append(Paragraph("URL Structure", styles['Heading1']))
        url_data = data['url_structure']
        elements.append(Paragraph(f"URL Length: {data['url_length']} characters", styles['Normal']))
        elements.append(Paragraph(f"Status: {'Good' if data['url_length'] <= 100 else 'Consider Shortening'}", styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        return buffer
        
    except Exception as e:
        print(f"Error in generate_pdf_report: {str(e)}")
        raise

@app.route('/')
def index():
    saved_analyses = list_saved_analyses()
    return render_template('index.html', saved_analyses=saved_analyses)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'})
        
        results = analyze_url(url)
        return jsonify(results)
    except Exception as e:
        print(f"Error in analyze route: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        })

@app.route('/save', methods=['POST'])
def save():
    try:
        data = request.get_json()
        url = data.get('url')
        analysis_data = data.get('analysis')
        notes = data.get('notes', '')
        
        if not url or not analysis_data:
            return jsonify({'status': 'error', 'message': 'URL and analysis data are required'})
        
        result = save_analysis(url, analysis_data, notes)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to save analysis: {str(e)}'
        })

@app.route('/load/<filename>')
def load(filename):
    try:
        result = load_analysis(filename)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to load analysis: {str(e)}'
        })

@app.route('/export', methods=['POST'])
def export_report():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'})
        
        results = analyze_url(url)
        if results.get('status') == 'error':
            return jsonify(results)
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(results, url)
        pdf_buffer.seek(0)  # Reset buffer position to start
        
        # Create response
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=seo_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        return response
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to generate PDF: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True) 