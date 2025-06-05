# Web2TXT - Webpage Text Extraction Tool

**Author:** Dr. Denys Dutykh (Khalifa University of Science and Technology, Abu Dhabi, UAE)  
**Repository:** [https://github.com/dutykh/web2txt](https://github.com/dutykh/web2txt)  
**License:** GNU Lesser General Public License v3.0 (LGPL3)

A robust Python 3 script that fetches textual content from any webpage and saves it to a clean text file. This tool is designed for researchers, developers, and data analysts who need to extract readable content from web pages for further processing, analysis, or feeding to Large Language Models (LLMs).

## 🚀 Features

### Core Functionality
- **URL-to-Text Conversion**: Extracts all human-readable text from any webpage
- **Smart HTML Parsing**: Removes scripts, styles, and HTML tags while preserving logical text structure
- **Intelligent Text Cleaning**: Handles whitespace normalization and HTML entity decoding
- **Flexible Output**: Supports custom output filenames or auto-generates meaningful names from URLs

### User Experience
- **Progress Indication**: Real-time download progress bars using `tqdm`
- **Comprehensive Error Handling**: Clear error messages for network issues, file I/O problems, and invalid URLs
- **Automatic URL Validation**: Adds missing protocols and validates URL structure
- **UTF-8 Encoding Support**: Handles various character encodings with fallback mechanisms

### Robustness
- **Network Resilience**: 15-second timeout with detailed error reporting for various HTTP status codes
- **File Safety**: Secure filename generation from URLs with character sanitization
- **Cross-Platform**: Works on Linux, macOS, and Windows with Python 3.7+

## 📋 Requirements

### System Requirements
- Python 3.7 or higher
- Internet connection for webpage fetching

### Python Dependencies
The script requires the following packages (automatically installable via `requirements.txt`):
- `requests` (≥2.25.1) - For HTTP requests and webpage fetching
- `beautifulsoup4` (≥4.9.3) - For HTML parsing and text extraction
- `tqdm` (≥4.62.0) - For progress bars and user feedback

## 🛠️ Installation

1. **Clone or download the script:**
   ```bash
   # If using git
   git clone https://github.com/dutykh/web2txt.git
   cd web2txt
   
   # Or download web2txt.py directly from https://github.com/dutykh/web2txt
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make the script executable (optional):**
   ```bash
   chmod +x web2txt.py
   ```

## 📖 Usage

### Basic Syntax
```bash
python3 web2txt.py <URL> [output_filename.txt]
```

### Parameters
- `<URL>`: **Required** - The webpage URL to extract text from
- `[output_filename.txt]`: **Optional** - Custom output filename

### Usage Examples

#### 1. Basic Usage with Auto-Generated Filename
```bash
python3 web2txt.py "https://www.example.com"
```
**Output:** Creates `www_example_com_content.txt`

#### 2. Custom Output Filename
```bash
python3 web2txt.py "https://news.ycombinator.com" "hackernews_frontpage.txt"
```
**Output:** Creates `hackernews_frontpage.txt`

#### 3. URL Without Protocol (Automatically Adds HTTPS)
```bash
python3 web2txt.py "wikipedia.org/wiki/Python" "python_wiki.txt"
```
**Output:** Fetches from `https://wikipedia.org/wiki/Python` and saves to `python_wiki.txt`

#### 4. Complex URL with Parameters
```bash
python3 web2txt.py "https://stackoverflow.com/questions/tagged/python?sort=votes"
```
**Output:** Creates `stackoverflow_com_questions_tagged_python_sort_votes_content.txt`

## 🔧 How It Works

### 1. URL Validation and Normalization
- Validates URL format and structure
- Automatically adds `https://` protocol if missing
- Handles various URL edge cases

### 2. Content Fetching
- Makes HTTP request with 15-second timeout
- Streams content with real-time progress indication
- Handles various HTTP status codes (404, 500, etc.)
- Manages encoding detection and Unicode decoding

### 3. HTML Processing
- Parses HTML using BeautifulSoup4
- Removes `<script>` and `<style>` elements
- Extracts text while preserving logical spacing
- Decodes HTML entities to readable characters

### 4. Text Cleaning
- Normalizes whitespace and line breaks
- Removes excessive spacing while preserving structure
- Ensures clean, readable output

### 5. File Output
- Saves content in UTF-8 encoding
- Handles file permission and I/O errors gracefully
- Provides confirmation of successful saves

## 📄 Output Format

The extracted text files contain:
- **Clean, readable text** with logical spacing preserved
- **No HTML tags, scripts, or styling information**
- **Properly decoded special characters** and Unicode
- **UTF-8 encoding** for universal compatibility

## ⚠️ Error Handling

The script provides detailed error messages for common issues:

### Network Errors
- **404 Not Found**: "Error: Could not retrieve content from [URL]. Reason: Not Found (404)"
- **Server Errors**: "Error: Could not retrieve content from [URL]. Reason: Server Error (500)"
- **Timeout**: "Error: Could not retrieve content from [URL]. Reason: Timeout"
- **Connection Issues**: "Error: Could not retrieve content from [URL]. Reason: Connection Error"

### File I/O Errors
- **Permission Denied**: "Error: Could not write to file [filename]. Reason: Permission denied"
- **Invalid Path**: "Error: Could not write to file [filename]. Reason: File system error"

### URL Errors
- **Invalid Format**: "Error: Invalid URL. Invalid URL format: [URL]"
- **Empty URL**: "Error: Invalid URL. URL cannot be empty"

## 🎯 Use Cases

### Academic Research
- Extracting content from research papers and articles
- Gathering text data for linguistic analysis
- Creating datasets from web sources

### Data Science & AI
- Preparing web content for LLM training or fine-tuning
- Creating text corpora from online sources
- Web scraping for sentiment analysis or NLP tasks

### Content Analysis
- Archiving webpage content in readable format
- Preparing web articles for offline reading
- Converting web content for accessibility tools

### Development & Testing
- Creating test datasets from web sources
- Extracting documentation from web pages
- Preparing content for text processing algorithms

## 🔒 Technical Specifications

- **Language**: Python 3.7+
- **Architecture**: Modular design with separate functions for each major task
- **Error Handling**: Comprehensive exception handling with graceful degradation
- **Performance**: Efficient streaming download with progress indication
- **Encoding**: Robust UTF-8 handling with fallback mechanisms
- **Code Style**: PEP 8 compliant with comprehensive documentation

## 👨‍💼 About the Author

**Dr. Denys Dutykh** is affiliated with Khalifa University of Science and Technology in Abu Dhabi, UAE. This tool was developed to facilitate web content extraction for research and data analysis purposes, providing a reliable and user-friendly solution for converting web pages into clean, processable text format.

## 📝 License

This project is licensed under the GNU Lesser General Public License v3.0 (LGPL3). See the LICENSE file for full license terms.

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome. Please ensure any modifications maintain the robust error handling and user-friendly interface that characterize this tool.
