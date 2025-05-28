import logging
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_RETRY_ATTEMPTS = 3
MIN_WAIT_SECONDS = 2
MAX_WAIT_SECONDS = 10
MULTIPLIER = 1

def is_wsl():
    """Detect if running in WSL environment"""
    try:
        return open('/proc/sys/fs/binfmt_misc/WSLInterop', 'r').close() or True
    except:
        return False

def with_retry(max_attempts=MAX_RETRY_ATTEMPTS):
    """
    Decorator to add retry logic to connection handlers.
    
    Args:
        max_attempts: Maximum number of connection attempts
    """
    def decorator(func):
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=MULTIPLIER, min=MIN_WAIT_SECONDS, max=MAX_WAIT_SECONDS),
            retry_error_callback=lambda retry_state: logger.error(
                f"All {max_attempts} connection attempts failed: {retry_state.outcome._exception}"
            ),
            before_sleep=lambda retry_state: logger.info(
                f"Connection attempt {retry_state.attempt_number}/{max_attempts} failed. "
                f"Retrying in {retry_state.next_action.sleep} seconds..."
            ),
        )
        async def wrapper(*args, **kwargs):
            logger.info(f"Connection attempt {1}/{max_attempts}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
