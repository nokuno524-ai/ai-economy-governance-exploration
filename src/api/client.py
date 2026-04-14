"""
Mock API client for external data.
"""
from typing import Dict, Any

class PricingAPIClient:
    """Mock client for fetching live pricing data."""

    def __init__(self, api_key: str = "mock_key"):
        """Initialize with API key."""
        self.api_key = api_key

    def fetch_live_hardware_pricing(self) -> Dict[str, float]:
        """
        Mock method to simulate fetching live cloud pricing.
        Returns:
            Dict mapping hardware names to current hourly costs.
        """
        return {
            "A100_80GB": 3.65,
            "H100_80GB": 8.80,
            "B200": 15.50
        }
