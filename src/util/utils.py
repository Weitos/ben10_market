"""
Utility functions for the Ben 10 Market application.
"""

import logging
import asyncio
import functools

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

def retry_with_backoff(max_retries: int = 5, base_delay: int = 2):
    """
    Decorator for exponential backoff retry logic.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Max retries exceeded for {func.__name__}: {e}")
                        raise
                    
                    delay = base_delay ** retries
                    logger.warning(f"Attempt {retries} failed for {func.__name__}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
                except Exception as e:
                    logger.error(f"Non-retryable error in {func.__name__}: {e}")
                    raise
            return None
        return wrapper
    return decorator