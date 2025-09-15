#!/usr/bin/env python3
"""
Entry point for the Secretaria El Cano application.

This script initializes and runs the Streamlit application with proper
error handling and logging.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for the application."""
    try:
        from app import SecretariaElCanoApp
        from utils.logger import get_logger
        
        logger = get_logger(__name__)
        logger.info("Starting Secretaria El Cano application")
        
        app = SecretariaElCanoApp()
        app.run()
        
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("Please make sure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()