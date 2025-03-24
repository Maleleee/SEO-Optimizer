from typing import Dict, Any
from .base_analyzer import BaseAnalyzer
import time

class PerformanceAnalyzer(BaseAnalyzer):
    """Analyzes website performance metrics."""
    
    def __init__(self, soup, response, server_response_time):
        super().__init__(soup)
        self.response = response
        self.server_response_time = server_response_time
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze performance metrics."""
        if not self._validate_input():
            return {'error': 'Invalid input data'}
            
        results = {
            'page_load_time': self._calculate_page_load_time(),
            'server_response_time': self.server_response_time,
            'resource_count': self._count_resources(),
            'content_length': len(self.response.content),
            'performance_score': self._calculate_performance_score()
        }
        
        return self._format_results(results)
    
    def _calculate_page_load_time(self) -> float:
        """Calculate estimated page load time."""
        content_length = len(self.response.content)
        # Rough estimate based on content size and resource count
        resource_count = self._count_resources()
        estimated_load_time = (content_length / (1024 * 1024)) + (resource_count * 0.1)
        return round(estimated_load_time, 2)
    
    def _count_resources(self) -> int:
        """Count total number of resources."""
        scripts = len(self.soup.find_all('script'))
        stylesheets = len(self.soup.find_all('link', {'rel': 'stylesheet'}))
        images = len(self.soup.find_all('img'))
        return scripts + stylesheets + images
    
    def _calculate_performance_score(self) -> float:
        """Calculate overall performance score (0-100)."""
        # Base score starts at 100
        score = 100
        
        # Deduct points based on various factors
        if self.server_response_time > 1.0:  # More than 1 second
            score -= 20
            
        if self._count_resources() > 50:  # Too many resources
            score -= 15
            
        if len(self.response.content) > 5000000:  # Content too large
            score -= 25
            
        return max(0, min(100, score))  # Ensure score is between 0 and 100 