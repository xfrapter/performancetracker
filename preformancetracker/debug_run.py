import sys
import traceback
import os
import logging
import inspect

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_with_debug():
    try:
        logger.info("Starting app initialization...")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Python path: {sys.path}")
        
        from .app import main
        logger.info("Successfully imported main from app")
        
        app = main()
        logger.info("App initialized successfully")
        
        # Print all methods of the app class
        logger.info("Available methods in app class:")
        for name, method in inspect.getmembers(app, predicate=inspect.ismethod):
            logger.info(f"  - {name}")
        
        logger.info("Starting main loop...")
        app.main_loop()
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        logger.error("Full traceback:")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        logger.error(f"ERROR: App failed to start!")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Exception message: {str(e)}")
        logger.error("Full traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    run_with_debug() 