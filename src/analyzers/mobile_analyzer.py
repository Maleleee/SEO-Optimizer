from typing import Dict, Any
from .base_analyzer import BaseAnalyzer
import re

class MobileAnalyzer(BaseAnalyzer):
    """Analyzes mobile responsiveness of the website."""
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze mobile responsiveness metrics."""
        if not self._validate_input():
            return {'error': 'Invalid input data'}
            
        results = {
            'is_mobile_friendly': self._check_mobile_friendliness(),
            'viewport_width': self._check_viewport(),
            'responsive_images': self._check_responsive_images(),
            'has_media_queries': self._check_media_queries(),
            'mobile_score': self._calculate_mobile_score(),
            'recommendations': self._generate_recommendations()
        }
        
        return self._format_results(results)
    
    def _check_mobile_friendliness(self) -> bool:
        """Check if the website is mobile-friendly."""
        has_viewport = bool(self._check_viewport() == 'device-width')
        has_responsive_images = self._check_responsive_images() > 0
        has_media_queries = self._check_media_queries()
        
        return all([has_viewport, has_responsive_images, has_media_queries])
    
    def _check_viewport(self) -> str:
        """Check viewport meta tag configuration."""
        viewport = self.soup.find('meta', {'name': 'viewport'})
        if not viewport:
            return 'not set'
            
        content = viewport.get('content', '')
        if 'width=device-width' in content:
            return 'device-width'
        return 'custom'
    
    def _check_responsive_images(self) -> int:
        """Count responsive images."""
        images = self.soup.find_all('img')
        responsive_count = 0
        
        for img in images:
            if img.get('srcset') or img.get('sizes'):
                responsive_count += 1
            # Check for responsive classes
            if img.get('class'):
                classes = ' '.join(img.get('class'))
                if any(term in classes.lower() for term in ['responsive', 'fluid', 'img-fluid']):
                    responsive_count += 1
                    
        return responsive_count
    
    def _check_media_queries(self) -> bool:
        """Check for media queries in stylesheets."""
        stylesheets = self.soup.find_all('link', {'rel': 'stylesheet'})
        for stylesheet in stylesheets:
            if stylesheet.get('media'):
                return True
        return False
    
    def _calculate_mobile_score(self) -> float:
        """Calculate mobile responsiveness score (0-100)."""
        score = 100
        
        # Deduct points based on various factors
        if self._check_viewport() != 'device-width':
            score -= 30
            
        if self._check_responsive_images() == 0:
            score -= 25
            
        if not self._check_media_queries():
            score -= 25
            
        return max(0, min(100, score))
    
    def _generate_recommendations(self) -> list:
        """Generate recommendations for mobile optimization."""
        recommendations = []
        
        if self._check_viewport() != 'device-width':
            recommendations.append("Add a proper viewport meta tag with width=device-width")
            
        if self._check_responsive_images() == 0:
            recommendations.append("Implement responsive images using srcset and sizes attributes")
            
        if not self._check_media_queries():
            recommendations.append("Add media queries to handle different screen sizes")
            
        return recommendations 