import json
import logging
from typing import Any, Dict, List
from pathlib import Path
from pydantic import BaseModel, ValidationError
from ..util.aliexpress_api import AliExpressAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Product(BaseModel):
    id: int
    name: str
    price: float
    cost_price: float
    commission_pct: float
    barcode: str

class DataProvider:
    def __init__(self, mock_data_path: str = "data/mock_data.json"):
        self.mock_data_path = mock_data_path
        self.aliexpress_api = AliExpressAPI()
    
    async def load_data(self, use_api: bool = True) -> List[Dict[str, Any]]:
        """
        Load data from AliExpress API with fallback to local JSON.
        
        Args:
            use_api: Whether to attempt loading from API first (default: True)
            
        Returns:
            List of product dictionaries
        """
        if use_api:
            try:
                # Try to load data from AliExpress API
                api_data = await self.aliexpress_api.search_products("Ben 10")
                
                if api_data:
                    # Validate API data
                    validated_data = []
                    for item in api_data:
                        try:
                            product = Product(**item)
                            validated_data.append(product.dict())
                        except ValidationError as e:
                            logger.error(f"Validation error for API product {item.get('id', 'unknown')}: {e}")
                            continue
                    
                    logger.info(f"Successfully loaded {len(validated_data)} products from AliExpress API")
                    return validated_data
                    
                # If API returns no data, fall back to local data
                logger.info("AliExpress API returned no data, falling back to local data")
                
            except Exception as e:
                # Log API error and fall back to local data
                logger.error(f"Error loading data from AliExpress API: {e}. Falling back to local data.")
        
        # Load from local data as fallback
        return self.load_local_data()
    
    def load_local_data(self) -> List[Dict[str, Any]]:
        """Load data from local JSON file with validation."""
        try:
            with open(self.mock_data_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            validated_data = []
            for item in raw_data:
                try:
                    product = Product(**item)
                    validated_data.append(product.dict())
                except ValidationError as e:
                    logger.error(f"Validation error for product {item.get('id', 'unknown')}: {e}")
                    continue
            
            logger.info(f"Successfully loaded {len(validated_data)} products from local data")
            return validated_data
        
        except FileNotFoundError:
            logger.error(f"Mock data file not found at {self.mock_data_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {self.mock_data_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error loading local data: {e}")
            return []



# Example usage of the data provider
if __name__ == "__main__":
    async def main():
        provider = DataProvider()
        data = await provider.load_data()
        print(f"Loaded {len(data)} products")
    
    asyncio.run(main())