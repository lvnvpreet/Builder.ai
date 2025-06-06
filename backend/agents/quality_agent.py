"""
Quality Agent - Validates and optimizes generated content
"""

import re
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class QualityAgent:
    """Agent responsible for quality validation and optimization"""
    
    def __init__(self):
        self.quality_score = 0
        self.issues = []
    
    async def validate_generation(self, content_data: dict, design_data: dict, structure_data: dict, images_data: dict) -> dict:
        """
        Validate and optimize the generated website components
        
        Args:
            content_data: Generated content
            design_data: Generated design/CSS
            structure_data: Generated HTML structure
            images_data: Selected images
            
        Returns:
            Dictionary containing validation results and optimizations
        """
        try:
            validation_results = {
                "overall_score": 0,
                "content_validation": self._validate_content(content_data),
                "design_validation": self._validate_design(design_data),
                "structure_validation": self._validate_structure(structure_data),
                "images_validation": self._validate_images(images_data),
                "recommendations": [],
                "issues": []
            }
            
            # Calculate overall score
            scores = [
                validation_results["content_validation"]["score"],
                validation_results["design_validation"]["score"],
                validation_results["structure_validation"]["score"],
                validation_results["images_validation"]["score"]
            ]
            validation_results["overall_score"] = sum(scores) / len(scores)
            
            # Collect all recommendations and issues
            for section in ["content_validation", "design_validation", "structure_validation", "images_validation"]:
                validation_results["recommendations"].extend(validation_results[section].get("recommendations", []))
                validation_results["issues"].extend(validation_results[section].get("issues", []))
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Quality validation failed: {e}")
            return {
                "overall_score": 0,
                "error": str(e),
                "recommendations": ["Manual review required"],
                "issues": ["Validation process failed"]
            }
    
    def _validate_content(self, content_data: dict) -> dict:
        """Validate content quality"""
        score = 85  # Base score
        recommendations = []
        issues = []
        
        # Check for required content sections
        required_sections = ["hero_headline", "hero_subtitle", "about_content", "services"]
        for section in required_sections:
            if not content_data.get(section):
                score -= 10
                issues.append(f"Missing {section}")
        
        # Check content length
        if content_data.get("hero_headline"):
            if len(content_data["hero_headline"]) > 60:
                recommendations.append("Consider shortening hero headline for better impact")
        
        # Check SEO elements
        if not content_data.get("meta_title"):
            score -= 5
            issues.append("Missing SEO meta title")
        
        if not content_data.get("meta_description"):
            score -= 5
            issues.append("Missing SEO meta description")
        
        return {
            "score": max(0, score),
            "recommendations": recommendations,
            "issues": issues
        }
    
    def _validate_design(self, design_data: dict) -> dict:
        """Validate design quality"""
        score = 90  # Base score
        recommendations = []
        issues = []
        
        # Check for required CSS sections
        required_css = ["global_css", "header_css", "hero_css"]
        for css_section in required_css:
            if not design_data.get(css_section):
                score -= 15
                issues.append(f"Missing {css_section}")
        
        # Check color scheme
        if not design_data.get("color_scheme"):
            score -= 10
            issues.append("Missing color scheme definition")
        
        return {
            "score": max(0, score),
            "recommendations": recommendations,
            "issues": issues
        }
    
    def _validate_structure(self, structure_data: dict) -> dict:
        """Validate HTML structure quality"""
        score = 88  # Base score
        recommendations = []
        issues = []
        
        # Check for required HTML sections
        required_sections = ["html_structure", "navigation", "header"]
        for section in required_sections:
            if not structure_data.get(section):
                score -= 12
                issues.append(f"Missing {section}")
        
        # Check for semantic elements (placeholder validation)
        html_content = structure_data.get("html_structure", "")
        if "nav" not in html_content.lower():
            recommendations.append("Consider adding semantic navigation elements")
        
        return {
            "score": max(0, score),
            "recommendations": recommendations,
            "issues": issues
        }
    
    def _validate_images(self, images_data: dict) -> dict:
        """Validate image selection quality"""
        score = 92  # Base score
        recommendations = []
        issues = []
        
        # Check for required images
        if not images_data.get("hero_image"):
            score -= 20
            issues.append("Missing hero image")
        
        # Check image alt descriptions
        for image_key, image_data in images_data.items():
            if isinstance(image_data, dict):
                if not image_data.get("alt_description"):
                    score -= 5
                    issues.append(f"Missing alt description for {image_key}")
        
        return {
            "score": max(0, score),
            "recommendations": recommendations,
            "issues": issues
        }
