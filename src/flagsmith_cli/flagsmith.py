from typing import Dict, List
import requests

class Flagsmith:
    def __init__(self, api_key: str):
        self.api_url = "https://edge.api.flagsmith.com/api/v1"
        self.headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }
        
    def get_feature_flags(self, page: int = 1, page_size: int = 50) -> Dict:
        """Get paginated feature flags."""
        params = {
            "page": page,
            "page_size": page_size
        }
        response = requests.get(
            f"{self.api_url}/flags/",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
        
    def update_flag(self, flag_id: int, data: Dict) -> Dict:
        """Update a feature flag."""
        response = requests.patch(
            f"{self.api_url}/features/{flag_id}/",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()