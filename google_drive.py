"""
Google Drive API integration for mtexts.

This module handles authentication and interaction with the Google Drive API,
including listing files and downloading file content.
"""

import os
import logging
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Configure logging
logger = logging.getLogger(__name__)

# Define the scopes needed for Google Drive access
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def create_drive_client(credentials_path, token_path):
    """
    Create and return an authenticated Google Drive API client.
    
    Args:
        credentials_path: Path to the credentials.json file
        token_path: Path to store/retrieve the token.json file
    
    Returns:
        Google Drive API service object
    """
    creds = None
    
    # Check if token.json exists with stored credentials
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_info(
                json.loads(open(token_path).read()), SCOPES)
        except Exception as e:
            logger.warning(f"Error loading stored credentials: {e}")
    
    # If credentials don't exist or are invalid, prompt for authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for future runs
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    # Build and return the Drive service
    service = build('drive', 'v3', credentials=creds)
    return service


def list_all_files(drive_service, folder_id=None):
    """
    List all files in Google Drive or in a specific folder.
    
    Args:
        drive_service: Google Drive API service object
        folder_id: Optional ID of folder to list files from
    
    Returns:
        List of file metadata dictionaries
    """
    all_files = []
    page_token = None
    
    # Build the query based on folder_id
    query = "trashed = false"
    if folder_id:
        query += f" and '{folder_id}' in parents"
    
    # Fields to retrieve for each file
    fields = "nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, webViewLink, parents)"
    
    while True:
        try:
            # Get batch of files
            response = drive_service.files().list(
                q=query,
                spaces='drive',
                fields=fields,
                pageToken=page_token,
                pageSize=1000
            ).execute()
            
            # Add current batch to our list
            files = response.get('files', [])
            all_files.extend(files)
            
            # Get next page token or exit loop if done
            page_token = response.get('nextPageToken')
            if not page_token:
                break
                
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            break
    
    # For each file, get its full path in Drive for better context
    for file_info in all_files:
        try:
            file_info['path'] = get_file_path(drive_service, file_info)
        except Exception as e:
            logger.warning(f"Could not get path for file {file_info['name']}: {e}")
            file_info['path'] = "Unknown path"
    
    return all_files


def get_file_path(drive_service, file_info):
    """
    Get the full path of a file in Google Drive.
    
    Args:
        drive_service: Google Drive API service object
        file_info: File metadata dictionary with 'parents' field
    
    Returns:
        String representing the full path of the file
    """
    path_parts = [file_info['name']]
    
    # Handle case where file has no parents
    if 'parents' not in file_info or not file_info['parents']:
        return f"/{file_info['name']}"
    
    # Recursively get parent folders
    current_parent = file_info['parents'][0]
    while current_parent:
        try:
            parent_info = drive_service.files().get(
                fileId=current_parent,
                fields='name,parents'
            ).execute()
            
            path_parts.insert(0, parent_info['name'])
            
            # Move up one level in folder hierarchy
            current_parent = parent_info.get('parents', [None])[0]
            
            # Prevent infinite loops
            if len(path_parts) > 100:
                path_parts.insert(0, "...")
                break
                
        except Exception as e:
            path_parts.insert(0, "...")
            logger.warning(f"Error getting parent info: {e}")
            break
    
    # Construct path string
    return "/" + "/".join(path_parts)


def download_file(drive_service, file_id):
    """
    Download a file's content from Google Drive.
    
    Args:
        drive_service: Google Drive API service object
        file_id: ID of the file to download
    
    Returns:
        BytesIO object containing the file content
    """
    try:
        request = drive_service.files().get_media(fileId=file_id)
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        file_content.seek(0)
        return file_content
        
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {e}")
        return None


def export_google_doc(drive_service, file_id, mime_type='text/plain'):
    """
    Export a Google Doc/Sheet/Slide to the specified format.
    
    Args:
        drive_service: Google Drive API service object
        file_id: ID of the Google Doc to export
        mime_type: MIME type to export as
    
    Returns:
        BytesIO object containing the exported content
    """
    try:
        request = drive_service.files().export_media(fileId=file_id, mimeType=mime_type)
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        file_content.seek(0)
        return file_content
        
    except Exception as e:
        logger.error(f"Error exporting Google Doc {file_id}: {e}")
        return None