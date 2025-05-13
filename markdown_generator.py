"""
Markdown generator for creating the knowledge base output file.

This module formats the processed document results into a comprehensive 
Markdown file optimized for AI consumption.
"""

import logging
from datetime import datetime
import re

# Configure logging
logger = logging.getLogger(__name__)


def create_knowledge_base(document_results, output_path):
    """
    Generate a Markdown file from the processed documents.
    
    Args:
        document_results: List of document entries (each with metadata, summary, content)
        output_path: Path to save the output Markdown file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# Google Drive Knowledge Base\n\n")
            f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write("*This file contains text extracted from documents in Google Drive, along with AI-generated summaries.*\n\n")
            
            # Write table of contents
            f.write("## Table of Contents\n\n")
            for i, doc in enumerate(document_results, 1):
                name = doc['metadata'].get('name', 'Unnamed Document')
                # Create safe anchor link (remove special chars)
                anchor = create_anchor_link(name)
                f.write(f"{i}. [{name}](#{anchor})\n")
            
            f.write("\n---\n\n")
            
            # Write each document
            for doc in document_results:
                write_document_section(f, doc)
                f.write("\n\n---\n\n")  # Separator between documents
                
            logger.info(f"Knowledge base written to {output_path}")
            
    except Exception as e:
        logger.error(f"Error creating knowledge base file: {e}")
        raise


def create_anchor_link(text):
    """
    Create a GitHub-compatible anchor link from text.
    
    Args:
        text: The text to convert to an anchor
        
    Returns:
        String suitable for use as a Markdown anchor
    """
    # Convert to lowercase
    anchor = text.lower()
    
    # Replace spaces with hyphens
    anchor = anchor.replace(' ', '-')
    
    # Remove non-alphanumeric characters (except hyphens)
    anchor = re.sub(r'[^\w-]', '', anchor)
    
    # Ensure it starts with a letter or number
    if anchor and not anchor[0].isalnum():
        anchor = 'doc-' + anchor
        
    return anchor


def write_document_section(file, doc):
    """
    Write a document section to the Markdown file.
    
    Args:
        file: File object to write to
        doc: Document entry (metadata, summary, content)
    """
    metadata = doc['metadata']
    summary = doc.get('summary', {})
    content = doc.get('content', '')
    
    # Document title
    name = metadata.get('name', 'Unnamed Document')
    file.write(f"## {name}\n\n")
    
    # Metadata section
    file.write("### Metadata\n\n")
    file.write("```yaml\n")
    
    # Format basic metadata
    file.write(f"title: {name}\n")
    
    # File type/MIME type
    mime_type = metadata.get('mimeType', 'Unknown')
    file.write(f"type: {mime_type}\n")
    
    # Dates
    created_time = metadata.get('createdTime', 'Unknown')
    modified_time = metadata.get('modifiedTime', 'Unknown')
    file.write(f"created: {created_time}\n")
    file.write(f"modified: {modified_time}\n")
    
    # Path
    path = metadata.get('path', 'Unknown path')
    file.write(f"path: {path}\n")
    
    # File ID
    file_id = metadata.get('id', 'Unknown ID')
    file.write(f"id: {file_id}\n")
    
    # URL
    url = metadata.get('webViewLink', '')
    if url:
        file.write(f"url: {url}\n")
    
    file.write("```\n\n")
    
    # Summary and key concepts
    file.write("### Summary & Key Concepts\n\n")
    
    # Write summary
    if isinstance(summary, dict):
        summary_text = summary.get('summary', '')
        key_concepts = summary.get('key_concepts', [])
    else:
        summary_text = str(summary)
        key_concepts = []
        
    if summary_text:
        file.write(f"{summary_text}\n\n")
    else:
        file.write("*No summary available*\n\n")
    
    # Write key concepts as a bullet list
    if key_concepts:
        file.write("**Key Concepts:**\n\n")
        for concept in key_concepts:
            file.write(f"- {concept}\n")
        file.write("\n")
    
    # Content section
    file.write("### Full Content\n\n")
    if content and content.strip():
        # Clean up content for Markdown
        content = format_content_for_markdown(content)
        file.write(f"{content}\n")
    else:
        file.write("*No content available*\n")


def format_content_for_markdown(content):
    """
    Format document content to display well in Markdown.
    
    Args:
        content: The text content to format
        
    Returns:
        Formatted content string
    """
    # Add code block fencing for content that might contain Markdown syntax
    # This prevents the document's own formatting from interfering with the output
    
    # If content appears to be code or has markdown syntax, wrap in code block
    if ('```' in content or '#' in content or 
        '**' in content or '*' in content or
        '[' in content and '](' in content):
        
        # But first, escape any existing backtick blocks
        if '```' in content:
            content = content.replace('```', '\\`\\`\\`')
            
        return f"```\n{content}\n```"
    
    # Otherwise return as regular text
    return content