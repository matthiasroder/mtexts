#!/usr/bin/env python3
"""
mtexts - Extract and consolidate texts from Google Drive into a comprehensive knowledge base.

This script connects to Google Drive, extracts text from various file types,
generates summaries using OpenAI, and compiles everything into a structured Markdown file.
"""

import os
import logging
from pathlib import Path
import json
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract text from Google Drive and create a knowledge base."
    )
    parser.add_argument(
        "--credentials", 
        type=str, 
        default="credentials.json",
        help="Path to Google API credentials JSON file"
    )
    parser.add_argument(
        "--token", 
        type=str, 
        default="token.json",
        help="Path to Google API token file"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="knowledge_base.md",
        help="Output file path for the knowledge base"
    )
    parser.add_argument(
        "--folder-id", 
        type=str,
        help="Google Drive folder ID to process (default: root of Drive)"
    )
    parser.add_argument(
        "--config", 
        type=str, 
        default="config.json",
        help="Path to configuration file"
    )
    return parser.parse_args()


def main():
    """Main entry point for the script."""
    args = parse_arguments()
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize Google Drive client
    drive_client = initialize_drive_client(args.credentials, args.token)
    
    # Get list of files
    files = list_files(drive_client, args.folder_id)
    logger.info(f"Found {len(files)} files to process")
    
    # Process each file
    results = []
    for file_info in files:
        try:
            # Extract text based on file type
            content = extract_content(drive_client, file_info)
            
            if content and content.strip():
                # Generate summary with OpenAI
                summary = generate_summary(content, config['openai_api_key'])
                
                # Prepare document entry
                doc_entry = {
                    'metadata': file_info,
                    'summary': summary,
                    'content': content
                }
                
                results.append(doc_entry)
                logger.info(f"Processed: {file_info['name']}")
            else:
                logger.warning(f"No content extracted from: {file_info['name']}")
        
        except Exception as e:
            logger.error(f"Error processing {file_info['name']}: {str(e)}")
    
    # Generate final markdown
    generate_markdown(results, args.output)
    logger.info(f"Knowledge base created at: {args.output}")


def load_config(config_path):
    """Load configuration from file or environment variables."""
    config = {
        'openai_api_key': os.environ.get('OPENAI_API_KEY', '')
    }
    
    # Try to load from file if it exists
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)
    
    # Validate required config
    if not config['openai_api_key']:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or add to config.json")
    
    return config


def initialize_drive_client(credentials_path, token_path):
    """Initialize and return Google Drive API client."""
    # This function will be implemented in google_drive.py
    from google_drive import create_drive_client
    return create_drive_client(credentials_path, token_path)


def list_files(drive_client, folder_id=None):
    """List all files in Google Drive (or in specific folder if folder_id provided)."""
    # This function will be implemented in google_drive.py
    from google_drive import list_all_files
    return list_all_files(drive_client, folder_id)


def extract_content(drive_client, file_info):
    """Extract content from a file based on its MIME type."""
    # This function will dispatch to appropriate extractors
    from extractors import extract_file_content
    return extract_file_content(drive_client, file_info)


def generate_summary(content, api_key):
    """Generate summary and extract key concepts using OpenAI."""
    # This function will be implemented in ai_summary.py
    from ai_summary import generate_content_summary
    return generate_content_summary(content, api_key)


def generate_markdown(results, output_path):
    """Generate final markdown file from all processed documents."""
    # This function will be implemented in markdown_generator.py
    from markdown_generator import create_knowledge_base
    create_knowledge_base(results, output_path)


if __name__ == "__main__":
    main()