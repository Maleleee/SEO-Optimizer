from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import Dict, Any

class BaseAnalyzer(ABC):
    """Base class for all analyzers in the SEO Optimizer."""
    
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
    
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Perform the analysis and return results."""
        pass
    
    def _validate_input(self) -> bool:
        """Validate input data before analysis."""
        return True
    
    def _format_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format the analysis results."""
        return results 