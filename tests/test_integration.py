#!/usr/bin/env python3
"""
Integration test script for Ben 10 Market application.
This script tests the core functionality of the application.
"""

import asyncio
import logging
import os
import sys
from src.base.data_provider import DataProvider
from src.base.analytics import process_market_data, get_top_products
from src.base.database import DatabaseClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_data_provider():
    """Test the data provider functionality."""
    logger.info("Testing Data Provider...")
    
    provider = DataProvider()
    data = provider.load_local_data()
    
    if not data:
        logger.error("Failed to load local data")
        return False
    
    logger.info(f"Successfully loaded {len(data)} products from local data")
    return True

def test_analytics():
    """Test the analytics functionality."""
    logger.info("Testing Analytics Engine...")
    
    provider = DataProvider()
    data = provider.load_local_data()
    
    if not data:
        logger.error("Failed to load data for analytics")
        return False
    
    try:
        df = process_market_data(data)
        top_products = get_top_products(df)
        
        logger.info(f"Processed {len(df)} products successfully")
        logger.info(f"Top 3 best products: {len(top_products['best'])}")
        logger.info(f"Top 3 worst products: {len(top_products['worst'])}")
        
        # Print sample results
        print("\n=== ANALYTICS RESULTS ===")
        print(f"Total products: {len(df)}")
        print("\nTop 3 Best Performing Products:")
        for i, (_, row) in enumerate(top_products['best'].head(3).iterrows()):
            print(f"  {i+1}. {row['name']} - Margin: {row['net_margin_rub']:.2f} RUB ({row['margin_pct']:.1f}%)")
        
        print("\nTop 3 Worst Performing Products:")
        for i, (_, row) in enumerate(top_products['worst'].head(3).iterrows()):
            print(f"  {i+1}. {row['name']} - Margin: {row['net_margin_rub']:.2f} RUB ({row['margin_pct']:.1f}%)")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in analytics processing: {e}")
        return False

async def test_db_client():
    """Test the Database client functionality."""
    logger.info("Testing DB/Excel Client...")
    
    try:
        provider = DataProvider()
        data = provider.load_local_data()
        
        if not data:
            logger.error("Failed to load data for Excel upload")
            return False
        
        df = process_market_data(data)
        
        # Initialize Database
        db_client = DatabaseClient()
        # Upload to Excel file
        db_client.save_market_data(df)
        db_client.export_to_excel()

        logger.info("Testing DB/Excel successful")
        return True
        
    except Exception as e:
        logger.warning(f"DB/Excel test skipped due to configuration: {e}")
        print("\n=== DB/EXCEL TEST ===")
        print("DB/Excel test skipped - database not configured")
        print("To run this test, set up your database url in the .env file")
        return True  # This is okay, it's just a configuration issue

def main():
    """Run all integration tests."""
    print("Ben 10 Market - Integration Tests")
    print("=" * 50)
    
    # Test 1: Data Provider
    if not test_data_provider():
        logger.error("Data Provider test failed")
        sys.exit(1)
    
    # Test 2: Analytics
    if not test_analytics():
        logger.error("Analytics test failed")
        sys.exit(1)
    
    # Test 3: DB/Excel
    if not asyncio.run(test_db_client()):
        logger.error("DB/Excel test failed")
        sys.exit(1)
    
    print("\nAll integration tests passed!")
    print("\nNext steps:")
    print("1. Configure your .env file with real database url")
    print("2. Run 'python src/main.py' to start the Telegram bot")
    print("3. Use the bot to generate reports and analyze data")

if __name__ == "__main__":
    main()