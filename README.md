# mtexts

A tool for extracting content from Google Drive documents and creating a comprehensive knowledge base optimized for use with AI systems like ChatGPT, Claude, and others.

## Features

- Connects to Google Drive to access your documents
- Extracts text from various file types:
  - Google Docs, Sheets, and Slides
  - PDFs
  - Microsoft Word and PowerPoint files
  - Plain text and HTML files
- Generates summaries and key concepts for each document using OpenAI
- Creates a well-structured Markdown file as a knowledge base
- Preserves metadata and document organization

## Use Cases

- Create context for AI conversations
- Build a personal knowledge base from your documents
- Prepare content for RAG (Retrieval-Augmented Generation) systems
- Make your document collection searchable and accessible

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- A Google account with documents in Google Drive
- An OpenAI API key

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mtexts.git
   cd mtexts
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up Google Drive API access:
   
   a. Go to the [Google Cloud Console](https://console.cloud.google.com/)
   b. Create a new project
   c. Enable the Google Drive API
   d. Create OAuth 2.0 credentials (Desktop application)
   e. Download the credentials JSON file and save it as `credentials.json` in the project directory
      (You can use `credentials.example.json` as a template)

4. Configure your OpenAI API key:
   
   a. Copy `config.example.json` to `config.json`
   b. Add your OpenAI API key to the config file:
   ```
   {
     "openai_api_key": "your-openai-api-key"
   }
   ```
   
   Alternatively, you can set the `OPENAI_API_KEY` environment variable.

## Usage

### Basic Usage

Run the script with default settings:

```
python main.py
```

This will:
1. Prompt you to authenticate with Google (first time only)
2. Process all accessible files in your Google Drive
3. Create a `knowledge_base.md` file in the current directory

### Command Line Options

```
python main.py --help
```

Available options:

- `--credentials`: Path to Google API credentials JSON file (default: `credentials.json`)
- `--token`: Path to Google API token file (default: `token.json`)
- `--output`: Output file path for the knowledge base (default: `knowledge_base.md`)
- `--folder-id`: Google Drive folder ID to process (default: root of Drive)
- `--config`: Path to configuration file (default: `config.json`)

### Example: Process a Specific Folder

1. Get the folder ID from the URL of your Google Drive folder:
   - Example URL: `https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j`
   - Folder ID: `1a2b3c4d5e6f7g8h9i0j`

2. Run the script with the folder ID:
   ```
   python main.py --folder-id 1a2b3c4d5e6f7g8h9i0j
   ```

## Output Format

The generated knowledge base is a Markdown file with:

- A table of contents with links to each document
- For each document:
  - Metadata (title, type, created/modified dates, path, URL)
  - AI-generated summary and key concepts
  - Full text content

## Security and Privacy

- Your documents remain private and are processed locally
- Google API authentication uses OAuth for secure access
- API keys are stored securely in configuration files
- No data is sent to third parties except when using OpenAI for summarization
- Sensitive files (`config.json`, `credentials.json`, `token.json`) are listed in `.gitignore` and should never be committed to version control

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
