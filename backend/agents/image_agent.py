"""
Image Agent - Uses Unsplash API for contextual image selection
"""

import httpx
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class ImageAgent:
    """Agent responsible for selecting and optimizing images"""
    
    def __init__(self):
        self.unsplash_access_key = settings.UNSPLASH_ACCESS_KEY
        self.base_url = "https://api.unsplash.com"
    
    async def generate_images(self, business_info: dict, content_data: dict) -> dict:
        """
        Select contextual images from Unsplash
        
        Args:
            business_info: Business information
            content_data: Generated content from content agent
            
        Returns:
            Dictionary containing selected images with metadata
        """
        try:
            if not self.unsplash_access_key or self.unsplash_access_key == "your_unsplash_access_key":
                logger.warning("Unsplash API key not configured, using placeholder images")
                return self._get_placeholder_images()
            
            # Search for relevant images
            hero_image = await self._search_image(f"{business_info['business_category']} professional")
            about_image = await self._search_image(f"{business_info['business_category']} team office")
            service_images = []
            
            # Get service-related images
            for i in range(3):
                service_image = await self._search_image(f"{business_info['business_category']} service")
                service_images.append(service_image)
            
            return {
                "hero_image": hero_image,
                "about_image": about_image,
                "service_images": service_images,
                "background_images": await self._search_image(f"{business_info['business_category']} background"),
            }
            
        except Exception as e:
            logger.error(f"Image selection failed: {e}")
            return self._get_placeholder_images()
    async def _search_image(self, query: str) -> dict:
        """Search for an image on Unsplash"""
        headers = {"Authorization": f"Client-ID {self.unsplash_access_key}"}
        
        # Set a reasonable timeout for image API calls
        timeout = httpx.Timeout(30.0, connect=10.0)  # 30 seconds total, 10 seconds connect
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                f"{self.base_url}/search/photos",
                headers=headers,
                params={
                    "query": query,
                    "per_page": 1,
                    "orientation": "landscape"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data["results"]:
                    photo = data["results"][0]
                    return {
                        "url": photo["urls"]["regular"],
                        "url_small": photo["urls"]["small"],
                        "url_thumb": photo["urls"]["thumb"],
                        "alt_description": photo.get("alt_description", query),
                        "photographer": photo["user"]["name"],
                        "photographer_url": photo["user"]["links"]["html"],
                        "download_url": photo["links"]["download_location"]
                    }
            
            return self._get_placeholder_image()
    
    def _get_placeholder_images(self) -> dict:
        """Return placeholder images when Unsplash is not available"""
        return {
            "hero_image": self._get_placeholder_image(),
            "about_image": self._get_placeholder_image(),
            "service_images": [self._get_placeholder_image() for _ in range(3)],
            "background_images": self._get_placeholder_image()
        }
    
    def _get_placeholder_image(self) -> dict:
        """Return a placeholder image"""
        return {
            "url": "https://via.placeholder.com/1200x600/2563eb/ffffff?text=Professional+Image",
            "url_small": "https://via.placeholder.com/600x300/2563eb/ffffff?text=Professional+Image",
            "url_thumb": "https://via.placeholder.com/300x150/2563eb/ffffff?text=Professional+Image",
            "alt_description": "Professional business image",
            "photographer": "Placeholder",
            "photographer_url": "#",
            "download_url": "#"
        }
