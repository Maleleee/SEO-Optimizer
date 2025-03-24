from typing import Dict, Any, List
from datetime import datetime
import json
import os
from pathlib import Path

def save_analysis(url: str, data: Dict[str, Any], notes: str = "") -> Dict[str, Any]:
    """Save analysis results to local storage."""
    try:
        # Create storage directory if it doesn't exist
        storage_dir = Path("storage/analyses")
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename from URL and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_url = "".join(c for c in url if c.isalnum() or c in ('-', '_')).rstrip()
        filename = f"{safe_url}_{timestamp}.json"
        
        # Prepare data for storage
        storage_data = {
            'url': url,
            'timestamp': timestamp,
            'notes': notes,
            'data': data
        }
        
        # Save to file
        filepath = storage_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(storage_data, f, indent=2)
            
        return {
            'status': 'success',
            'message': 'Analysis saved successfully',
            'filename': filename
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to save analysis: {str(e)}'
        }

def load_analysis(filename: str) -> Dict[str, Any]:
    """Load analysis results from local storage."""
    try:
        filepath = Path("storage/analyses") / filename
        if not filepath.exists():
            return {
                'status': 'error',
                'message': 'Analysis file not found'
            }
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return {
            'status': 'success',
            'data': data
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Failed to load analysis: {str(e)}'
        }

def list_saved_analyses() -> List[Dict[str, Any]]:
    """List all saved analyses."""
    try:
        storage_dir = Path("storage/analyses")
        if not storage_dir.exists():
            return []
            
        analyses = []
        for filepath in storage_dir.glob("*.json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                analyses.append({
                    'filename': filepath.name,
                    'url': data['url'],
                    'timestamp': data['timestamp'],
                    'notes': data.get('notes', '')
                })
                
        return sorted(analyses, key=lambda x: x['timestamp'], reverse=True)
        
    except Exception as e:
        print(f"Error listing analyses: {str(e)}")
        return []

def format_score(score: float) -> str:
    """Format a score with appropriate color class."""
    if score >= 90:
        return f'<span class="text-success">{score:.1f}</span>'
    elif score >= 70:
        return f'<span class="text-warning">{score:.1f}</span>'
    else:
        return f'<span class="text-danger">{score:.1f}</span>'

def format_status(status: bool) -> str:
    """Format a status with appropriate icon and color."""
    if status:
        return '<i class="fas fa-check-circle text-success"></i>'
    else:
        return '<i class="fas fa-times-circle text-danger"></i>' 