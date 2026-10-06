import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
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

class TeleBot:
    def __init__(self):
        """Initialize the Telegram bot."""
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
            raise ValueError("Telegram bot token not configured")
        
        # Initialize bot and dispatcher
        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher(storage=MemoryStorage())
        
        logger.info("Telegram bot initialized successfully")
    
    async def start_polling(self):
        """Start polling for updates."""
        try:
            logger.info("Starting bot polling...")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Error during bot polling: {e}")
            raise

# Example usage
if __name__ == "__main__":
    # This would typically be called from main.py
    pass