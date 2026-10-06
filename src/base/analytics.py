import pandas as pd
import logging
from typing import List, Dict

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

def process_market_data(data: List[Dict]) -> pd.DataFrame:
    """
    Process market data and calculate margins.
    
    Args:
        data: List of product dictionaries
        
    Returns:
        DataFrame with calculated margins and sorted by profitability
    """
    try:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Validate required columns
        required_columns = ['price', 'cost_price', 'commission_pct']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Calculate net margin (rubles)
        # Net Margin = Price - Cost Price - (Price * Commission Percentage)
        df['net_margin_rub'] = df['price'] - df['cost_price'] - (df['price'] * df['commission_pct'])
        
        # Calculate margin percentage
        df['margin_pct'] = (df['net_margin_rub'] / df['price']) * 100
        
        # Sort by net margin (descending for best performers)
        df_sorted = df.sort_values('net_margin_rub', ascending=False)
        
        # Add rank column
        df_sorted['rank'] = range(1, len(df_sorted) + 1)
        
        logger.info(f"Processed {len(df_sorted)} products successfully")
        return df_sorted
    
    except Exception as e:
        logger.error(f"Error processing market data: {e}")
        raise

def get_top_products(df: pd.DataFrame, n: int = 3) -> Dict[str, pd.DataFrame]:
    """
    Get top N best and worst performing products.
    
    Args:
        df: DataFrame with processed market data
        n: Number of top products to return
        
    Returns:
        Dictionary with 'best' and 'worst' DataFrames
    """
    try:
        # Top N best performing (highest margin)
        top_best = df.head(n)
        
        # Top N worst performing (lowest margin)
        top_worst = df.tail(n)
        
        logger.info(f"Identified top {n} best and worst performing products")
        return {
            'best': top_best,
            'worst': top_worst
        }
    
    except Exception as e:
        logger.error(f"Error getting top products: {e}")
        raise

# Example usage
if __name__ == "__main__":
    # This would typically be called from another module
    pass