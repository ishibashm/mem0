import gc
import os
import logging
import asyncio

logger = logging.getLogger(__name__)

MAX_MEMORY_PERCENT = 80
MEMORY_CHECK_INTERVAL = 60  # seconds
WSL_DETECTED = os.path.exists('/proc/sys/fs/binfmt_misc/WSLInterop')

async def memory_monitor():
    """
    Monitor memory usage and take action if memory usage exceeds threshold.
    Particularly useful in WSL environments with limited memory.
    """
    if not WSL_DETECTED:
        return
        
    logger.info("WSL2 environment detected. Starting memory monitor.")
    
    while True:
        try:
            with open('/proc/meminfo', 'r') as f:
                mem_info = f.readlines()
            
            mem_total = 0
            mem_available = 0
            
            for line in mem_info:
                if line.startswith('MemTotal'):
                    mem_total = int(line.split()[1])
                elif line.startswith('MemAvailable'):
                    mem_available = int(line.split()[1])
            
            if mem_total > 0:
                memory_percent = 100 - (mem_available * 100 / mem_total)
                
                logger.debug(f"Current memory usage: {memory_percent:.2f}%")
                
                if memory_percent > MAX_MEMORY_PERCENT:
                    logger.warning(f"Memory usage high ({memory_percent:.2f}%). Triggering garbage collection.")
                    gc.collect()
                    
        except Exception as e:
            logger.error(f"Error in memory monitor: {e}")
            
        await asyncio.sleep(MEMORY_CHECK_INTERVAL)

def setup_wsl_optimizations(app):
    """
    Set up WSL-specific optimizations.
    """
    if not WSL_DETECTED:
        return
        
    logger.info("Setting up WSL2 optimizations")
    
    asyncio.create_task(memory_monitor())
    
    os.environ["MCP_MAX_CONCURRENT_CONNECTIONS"] = "5"
    
    app.state.wsl_mode = True
    
    logger.info("WSL2 optimizations configured")
