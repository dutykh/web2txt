#!/usr/bin/env python3
"""
Web2TXT - Webpage Text Extraction Tool

This script fetches textual content from a given URL and saves it to a text file.
It provides robust error handling, progress indication, and user-friendly interface.

Author: Dr. Denys Dutykh (Khalifa University of Science and Technology, Abu Dhabi, UAE)
Repository: https://github.com/dutykh/web2txt
License: GNU Lesser General Public License v3.0 (LGPL3)
"""

import codecs
import sys
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse

# The charset parameter of a Content-Type header, and the character set that a
# page declares in a <meta charset="..."> or <meta http-equiv="Content-Type"
# content="text/html; charset=..."> element.
CHARSET_IN_HEADER = re.compile(r'charset\s*=\s*["\']?([^"\';,\s]+)', re.IGNORECASE)
CHARSET_IN_META = re.compile(rb'<meta\b[^>]*?charset\s*=\s*["\']?\s*([A-Za-z0-9._:-]+)', re.IGNORECASE)
META_SEARCH_BYTES = 16384

def print_usage():
    """Print usage information and exit."""
    print("Usage: python3 web2txt.py <URL> [output_filename.txt]")
    print("  URL: The full URL of the webpage to scrape")
    print("  output_filename.txt: Optional output filename")
    sys.exit(1)


def sanitize_filename(url):
    """
    Generate a safe filename from URL.
    
    Args:
        url (str): The input URL
        
    Returns:
        str: Sanitized filename with _content.txt suffix
    """
    # Remove protocol
    clean_url = re.sub(r'^https?://', '', url)
    
    # Replace non-alphanumeric characters (except hyphens and underscores) with underscores
    clean_url = re.sub(r'[^a-zA-Z0-9\-_]', '_', clean_url)
    
    # Remove multiple consecutive underscores
    clean_url = re.sub(r'_+', '_', clean_url)
    
    # Remove leading/trailing underscores
    clean_url = clean_url.strip('_')
    
    # Truncate to reasonable length (100 chars before suffix)
    max_length = 100
    if len(clean_url) > max_length:
        clean_url = clean_url[:max_length]
    
    return f"{clean_url}_content.txt"


def decode_page(content, content_type):
    """
    Decode the bytes of a webpage into text.

    The character set is the one that the server declares in its Content-Type
    header; without one, the one that the page declares in a <meta> element of
    its first 16 KiB; without either, UTF-8 when the bytes are valid UTF-8.
    A declared character set that is unknown or does not decode the bytes is
    passed over for the next choice, and Windows-1252 decodes what remains.

    Args:
        content (bytes): The bytes of the page
        content_type (str): The Content-Type header of the response, or ''

    Returns:
        tuple: The text of the page and a description of the character set used
    """
    candidates = []
    match = CHARSET_IN_HEADER.search(content_type or '')
    if match:
        candidates.append((match.group(1), 'declared by the server'))
    match = CHARSET_IN_META.search(content[:META_SEARCH_BYTES])
    if match:
        name = match.group(1).decode('ascii')
        # A <meta> element readable as ASCII cannot be written in UTF-16, so a
        # page that declares UTF-16 there is read as UTF-8, as browsers do.
        if name.lower().replace('_', '-') in ('utf-16', 'utf-16le', 'utf-16be'):
            name = 'utf-8'
        candidates.append((name, 'declared by the page'))
    candidates.append(('utf-8', 'detected'))

    for name, origin in candidates:
        try:
            codec = codecs.lookup(name).name
        except LookupError:
            continue
        try:
            # utf-8-sig also removes a byte-order mark at the start of the page
            text = content.decode('utf-8-sig' if codec == 'utf-8' else codec)
        except UnicodeDecodeError:
            continue
        return text, f"{name.lower()} ({origin})"

    return content.decode('cp1252', errors='replace'), "windows-1252 (assumed: not UTF-8, no usable declaration)"


def fetch_webpage(url, timeout=15):
    """
    Fetch webpage content with progress indication.
    
    Args:
        url (str): URL to fetch
        timeout (int): Request timeout in seconds
        
    Returns:
        str: HTML content of the webpage
        
    Raises:
        requests.RequestException: For various network errors
    """
    print(f"Fetching URL: {url}...")
    
    try:
        # Make initial request to get headers
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # Get content length for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        content = b''
        
        # Download with progress bar
        if total_size > 0:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        content += chunk
                        pbar.update(len(chunk))
        else:
            # If content-length not available, show progress without percentage
            with tqdm(unit='B', unit_scale=True, desc="Downloading") as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        content += chunk
                        pbar.update(len(chunk))
        
        # Decode content: the charset of the HTTP header, else that of the
        # page's <meta> element, else UTF-8 detection (see decode_page)
        html_content, charset = decode_page(content, response.headers.get('Content-Type', ''))
        print(f"Decoding as {charset}")

        return html_content
        
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            status_code = e.response.status_code
            if status_code == 404:
                raise requests.RequestException(f"Not Found (404): {url}")
            elif 400 <= status_code < 500:
                raise requests.RequestException(f"Client Error ({status_code}): {url}")
            elif 500 <= status_code < 600:
                raise requests.RequestException(f"Server Error ({status_code}): {url}")
        
        if "timeout" in str(e).lower():
            raise requests.RequestException(f"Timeout: Could not connect to {url}")
        elif "connection" in str(e).lower():
            raise requests.RequestException(f"Connection Error: Could not connect to {url}")
        else:
            raise requests.RequestException(f"Network Error: {str(e)}")


def extract_text_from_html(html_content):
    """
    Extract human-readable text from HTML content.
    
    Args:
        html_content (str): Raw HTML content
        
    Returns:
        str: Extracted and cleaned text
    """
    print("Parsing HTML content...")
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text with spacing
        text = soup.get_text(separator=' ')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        raise Exception(f"Error parsing HTML: {str(e)}")


def save_text_to_file(text, filename):
    """
    Save text content to file.
    
    Args:
        text (str): Text content to save
        filename (str): Output filename
        
    Raises:
        IOError: For file I/O errors
    """
    print(f"Saving text to {filename}...")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
    except PermissionError:
        raise IOError(f"Permission denied: Cannot write to {filename}")
    except OSError as e:
        raise IOError(f"File system error: {str(e)}")
    except Exception as e:
        raise IOError(f"Unexpected error writing to {filename}: {str(e)}")


def validate_url(url):
    """
    Basic URL validation.
    
    Args:
        url (str): URL to validate
        
    Returns:
        str: Validated URL (with protocol if missing)
        
    Raises:
        ValueError: If URL is invalid
    """
    if not url:
        raise ValueError("URL cannot be empty")
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Basic URL structure validation
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Invalid URL format: {url}")
    
    return url


def main():
    """Main function to orchestrate the webpage text extraction process."""
    # Check command-line arguments
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print_usage()
    
    # Parse arguments
    url = sys.argv[1]
    
    if len(sys.argv) == 3:
        output_filename = sys.argv[2]
    else:
        output_filename = None
    
    try:
        # Validate and normalize URL
        url = validate_url(url)
        
        # Generate default filename if not provided
        if output_filename is None:
            output_filename = sanitize_filename(url)
            print(f"Using default output filename: {output_filename}")
        
        # Fetch webpage content
        html_content = fetch_webpage(url)
        
        # Extract text from HTML
        text_content = extract_text_from_html(html_content)
        
        # Check if we got any meaningful content
        if not text_content.strip():
            print("Warning: No readable text content found on the webpage.")
            text_content = "No readable text content found."
        
        # Save to file
        save_text_to_file(text_content, output_filename)
        
        # Success message
        print(f"Successfully saved text from {url} to {output_filename}.")
        
    except ValueError as e:
        print(f"Error: Invalid URL. {str(e)}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Error: Could not retrieve content from {url}. Reason: {str(e)}")
        sys.exit(1)
    except IOError as e:
        print(f"Error: Could not write to file {output_filename}. Reason: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 