<!-- Author: Dr. Denys Dutykh (Mathematics Department, Khalifa University of Science and Technology, Abu Dhabi, UAE) -->

# web2txt: the text of a web page in a plain text file

The script `web2txt.py` downloads one web page and writes its human-readable text into a UTF-8 text file, ready to be read offline, searched, gathered into a corpus, or given to a large language model. It removes the scripts and the style sheets of the page, keeps all its other text (the title of the page included), decodes the HTML entities, and reduces the line breaks and runs of blanks to single spaces, so that the file holds the whole text of the page on one line.

The repository is at

https://github.com/dutykh/web2txt

## Quick start

```bash
git clone https://github.com/dutykh/web2txt.git
cd web2txt
python3 -m venv .venv && . .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 web2txt.py "https://www.example.com"
```

The virtual environment keeps the three packages apart from the Python of the system, which recent Ubuntu and Debian releases protect from `pip`; in a new terminal, `. .venv/bin/activate` brings it back. The last command writes the text of the page into `www_example_com_content.txt`, in the current folder. A second argument names the output file instead, and an address given without its protocol is fetched over `https://`:

```bash
python3 web2txt.py "https://news.ycombinator.com" hackernews_frontpage.txt
python3 web2txt.py "wikipedia.org/wiki/Python" python_wiki.txt
```

## Usage

```text
python3 web2txt.py URL [OUTPUT.txt]
```

Without a second argument, the name of the output file is made from the address: the protocol is removed, every character other than a letter, a digit, a hyphen or an underscore becomes an underscore, repeated underscores are merged, the result is cut at 100 characters, and `_content.txt` is appended. An existing file of the same name is overwritten.

| Command | File written |
| --- | --- |
| `python3 web2txt.py "https://www.example.com"` | `www_example_com_content.txt` |
| `python3 web2txt.py "https://stackoverflow.com/questions/tagged/python?sort=votes"` | `stackoverflow_com_questions_tagged_python_sort_votes_content.txt` |
| `python3 web2txt.py "https://news.ycombinator.com" hackernews_frontpage.txt` | `hackernews_frontpage.txt` |

The script can also be made executable (`chmod +x web2txt.py`) and run as `./web2txt.py URL`.

## How it works

The page is requested with a timeout of 15 seconds and downloaded in pieces of 8 KiB, with a progress bar drawn by `tqdm` (with the total size when the server announces it). The bytes are decoded with the character set that the `requests` library reports for the page, and with UTF-8, replacing the bytes it cannot read, when that decoding fails. Beautiful Soup parses the page with the HTML parser of the Python standard library; the `<script>` and `<style>` elements are removed, the remaining text is taken with a space between consecutive elements, and every line break and run of blanks is reduced to one space. A page without any readable text produces a warning and a file holding the sentence "No readable text content found."

Two limits follow from this design. The script reads the page that the server sends and runs none of its JavaScript, so the text of a page that builds its content in the browser is missing. A page whose server declares no character set is decoded as ISO-8859-1, the default that `requests` applies to text in that case, so that the accented letters of such a page written in UTF-8 come out garbled.

## Messages and exit status

The script prints what it is doing (the address, the parsing, the saving) and ends with "Successfully saved text from URL to FILE." and the exit status 0. When something fails it prints one line and exits with the status 1; with the wrong number of arguments it prints its usage.

| Situation | Message |
| --- | --- |
| The page does not exist | `Error: Could not retrieve content from URL. Reason: Not Found (404): URL` |
| Another refusal of the server | `Error: Could not retrieve content from URL. Reason: Client Error (403): URL`, with the status received |
| An error of the server | `Error: Could not retrieve content from URL. Reason: Server Error (500): URL`, with the status received |
| No answer within 15 seconds | `Error: Could not retrieve content from URL. Reason: Timeout: Could not connect to URL` |
| No connection | `Error: Could not retrieve content from URL. Reason: Connection Error: Could not connect to URL` |
| The file cannot be written | `Error: Could not write to file FILE. Reason: Permission denied: Cannot write to FILE` |
| An address without a host | `Error: Invalid URL. Invalid URL format: URL` |

## Requirements

Python 3.7 or newer, with the three packages listed in `requirements.txt`: `requests` (version 2.25.1 or newer) for the download, `beautifulsoup4` (version 4.9.3 or newer) for the parsing, and `tqdm` (version 4.62.0 or newer) for the progress bar. The script itself is the single file `web2txt.py`.

## How to cite

The file [`CITATION.cff`](CITATION.cff) describes the script for citation, and GitHub turns it into a reference, in APA or BibTeX, through the "Cite this repository" button of the repository page.

## Licence

The script is free software under the GNU Lesser General Public License, version 3 (`LGPL-3.0-only`), as its header states. The file [LICENSE](LICENSE) holds the text of that licence, and the file [COPYING](COPYING) the text of the GNU General Public License, version 3, on which the Lesser General Public License builds.

## Author

Dr. Denys Dutykh, Mathematics Department, Khalifa University of Science and Technology, Abu Dhabi, United Arab Emirates (https://www.denys-dutykh.com/). Bug reports and suggestions are welcome through the issues of the repository.
