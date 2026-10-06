import asyncio
import logging
from tele.bot import TeleBot
from tele.handlers import router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

async def main():
    """Main entry point for the application."""
    try:
        # Initialize the bot
        bot = TeleBot()
        
        # Register handlers
        bot.dp.include_router(router)
        
        # Start polling
        logger.info("Starting Ben 10 Market Bot...")
        await bot.start_polling()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())