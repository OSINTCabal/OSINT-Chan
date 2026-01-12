# OSINTChan

A 4chan/8kun OSINT collection and archival tool for investigators and researchers.

## Description

OSINTChan is designed for collecting and archiving threads, posts, and images from imageboards like 4chan and 8kun. It's built for OSINT investigators who need to document and preserve imageboard content for investigations, threat analysis, and research purposes.

## Features

- Thread archival and retrieval
- Board catalog browsing
- Keyword search across threads
- Archived thread listing
- Post and image metadata collection
- JSON export for analysis
- No API keys required (uses public APIs)
- Rate limiting friendly

## Sources/APIs

This tool uses the following public imageboard APIs:

1. **4chan API** - Official 4chan read-only JSON API
   - API Documentation: https://github.com/4chan/4chan-API
   - No authentication required
   - Public and free to use
   - Rate limits apply

2. **8kun API** (planned)
   - Similar API structure to 4chan
   - Public API endpoints

**Note**: No API keys or authentication are required. These are public, read-only APIs.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/osintchan.git
cd osintchan
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the tool:
```bash
python osintchan.py --help
```

## Usage

### List All Boards

```bash
python osintchan.py -o boards
```

### Get Board Catalog

View all active threads on a board:
```bash
python osintchan.py pol -o catalog
```

### Get Specific Thread

Retrieve a full thread with all posts:
```bash
python osintchan.py pol -o thread -t 123456789
```

### Search for Keywords

Search thread subjects and comments:
```bash
python osintchan.py pol -o search -k "election"
```

### Get Archived Threads

List archived thread IDs:
```bash
python osintchan.py pol -o archive
```

### Save Results

Output to JSON file:
```bash
python osintchan.py pol -o catalog -f results.json
```

### Command-Line Options

```
usage: osintchan.py [-h] [-o {catalog,thread,search,archive,boards}] 
                    [-t THREAD] [-k KEYWORD] [-s {4chan,8kun}] [-f OUTPUT]
                    [board]

positional arguments:
  board                 Board name (e.g., pol, b, int)

optional arguments:
  -h, --help            show this help message and exit
  -o, --operation       Operation to perform (required)
  -t, --thread THREAD   Thread number (for thread operation)
  -k, --keyword KEYWORD Keyword to search for
  -s, --site {4chan,8kun} Imageboard site (default: 4chan)
  -f, --output OUTPUT   Output file for JSON results
```

## Examples

### Basic Thread Investigation

```bash
# Get the catalog for /pol/
python osintchan.py pol -o catalog

# Search for specific topics
python osintchan.py pol -o search -k "Ukraine"

# Archive a specific thread
python osintchan.py pol -o thread -t 456789123 -f thread_archive.json
```

### Monitoring Boards

```bash
# Get current threads on multiple boards
python osintchan.py pol -o catalog -f pol_catalog.json
python osintchan.py int -o catalog -f int_catalog.json
python osintchan.py biz -o catalog -f biz_catalog.json
```

### Keyword Tracking

```bash
# Search for keywords across different boards
python osintchan.py pol -o search -k "cybersecurity" -f results.json
python osintchan.py g -o search -k "data breach"
```

## Common Boards

Here are some commonly monitored boards:

- **/pol/** - Politically Incorrect (political discussions)
- **/b/** - Random (general/random content)
- **/int/** - International (country discussions)
- **/biz/** - Business & Finance
- **/g/** - Technology
- **/k/** - Weapons
- **/x/** - Paranormal
- **/his/** - History & Humanities
- **/sci/** - Science & Math

Use `-o boards` to see all available boards.

## Output Format

Results are provided in JSON format:

```json
{
  "board": "pol",
  "operation": "thread",
  "site": "4chan",
  "timestamp": "2025-01-11T12:00:00",
  "data": {
    "board": "pol",
    "thread_no": 123456789,
    "posts_found": 250,
    "thread_url": "https://boards.4chan.org/pol/thread/123456789",
    "posts": [
      {
        "no": 123456789,
        "time": 1704988800,
        "name": "Anonymous",
        "subject": "Thread Subject",
        "comment": "Thread content...",
        "image": {
          "filename": "image",
          "ext": ".jpg",
          "image_url": "https://i.4cdn.org/pol/1234567890.jpg"
        }
      }
    ]
  }
}
```

## Use Cases

### Investigation Scenarios

1. **Threat Monitoring**: Track discussions related to potential threats
2. **Disinformation Research**: Monitor coordinated campaigns or narratives
3. **Evidence Preservation**: Archive threads before deletion
4. **Trend Analysis**: Track emerging topics or coordinated activity
5. **Person of Interest**: Search for posts by specific tripcodes or IDs
6. **Image Collection**: Gather images shared in relevant threads
7. **Timeline Construction**: Build chronological records of discussions

## Rate Limiting and Best Practices

### 4chan API Guidelines

- Be respectful with request frequency
- Implement delays between requests (1-2 seconds recommended)
- Cache results when possible
- Don't hammer the API with rapid requests
- The API is provided as a courtesy - abuse may result in blocks

### Recommended Usage

```python
# Add delays between requests
import time

# Get multiple threads with delays
for thread_id in thread_ids:
    result = get_thread("pol", thread_id)
    time.sleep(2)  # 2 second delay
```

## Legal and Ethical Use

**IMPORTANT**: This tool is intended for legitimate research and investigations only. Users must:

- Have proper authorization before conducting investigations
- Comply with all applicable laws and regulations
- Respect 4chan's Terms of Service and API guidelines
- Not use for harassment, doxxing, or illegal activities
- Be aware of content warnings (4chan contains NSFW content)
- Only investigate targets you have legal authority to investigate
- Preserve evidence in accordance with legal standards

**Content Warning**: Imageboards contain adult content, offensive material, and explicit discussions. Use appropriate judgment and caution.

The author is not responsible for misuse of this tool.

## Understanding 4chan Structure

### Threads and Posts
- Each thread has a unique number (thread_no)
- Original post (OP) starts the thread
- Replies are numbered sequentially
- Threads 404 (disappear) when they fall off the board

### Archival
- Some boards have built-in archives
- Threads are archived when they 404
- Archived threads are read-only

### Tripcodes
- Secure tripcodes identify repeat posters
- Format: `Name!!tripcode`
- Useful for tracking specific individuals

### Post IDs
- Temporary IDs assigned per thread
- Changes between threads
- Helps identify samefagging (self-replies)

## Troubleshooting

### Thread Not Found (404)
- Thread may have been deleted or archived
- Try checking the archive: `-o archive`
- Very old threads may no longer be available

### API Rate Limiting
- Reduce request frequency
- Add delays between requests
- Avoid rapid sequential calls

### Invalid Board
- Check board name spelling
- Use `-o boards` to see valid boards
- Board may have been removed

## Limitations

- Read-only access (cannot post)
- No authentication or user tracking
- Limited to public boards
- Archived threads may have incomplete data
- Images must be downloaded separately
- No access to deleted/removed content

## Advanced Usage

### Automated Monitoring

Create a monitoring script:

```python
import time
from osintchan import OSINTChan

osint = OSINTChan()

while True:
    # Search for keyword every 5 minutes
    results = osint.search_catalog("pol", "keyword")
    osint.save_results(results, f"monitor_{int(time.time())}.json")
    time.sleep(300)  # 5 minutes
```

### Bulk Thread Archival

```bash
# Archive multiple threads
for thread in 123456 234567 345678; do
    python osintchan.py pol -o thread -t $thread -f "thread_${thread}.json"
    sleep 2
done
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

## Related Tools

- [4chan-API](https://github.com/4chan/4chan-API) - Official API documentation
- [4chan-x](https://github.com/ccd0/4chan-x) - Browser extension for 4chan
- [gallery-dl](https://github.com/mikf/gallery-dl) - Image downloader

## Disclaimer

This tool is provided "as-is" without warranty. Use at your own risk. Always ensure you have proper authorization before conducting investigations. The tool accesses public APIs only and does not bypass any security measures.

## Author

Created for professional OSINT investigators and researchers.

## Changelog

### Version 1.0.0
- Initial release
- 4chan API integration
- Thread and catalog retrieval
- Keyword search functionality
- Archive listing
- JSON export support
- Board listing
