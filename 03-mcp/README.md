# Doc-MCP: Documentation Search MCP Server

A Context7-inspired MCP (Model Context Protocol) server that provides intelligent documentation search capabilities using Jina Reader and minsearch.

## Features

- **Web Scraping**: Convert any web page to clean markdown using Jina Reader
- **Word Counting**: Count word occurrences in web pages
- **Documentation Search**: Full-text search across FastMCP documentation (266+ files)
- **MCP Integration**: Seamlessly integrates with Claude Code, Claude Desktop, and other MCP clients

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that enables AI assistants to securely access data and tools. This server exposes documentation search capabilities as MCP tools that can be used by any MCP-compatible client.

## Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager

### Install uv

```bash
pip install uv
```

### Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd doc-mcp

# Install dependencies
uv sync
```

## Available MCP Tools

### 1. `scrape_web`

Scrapes any web page and returns its content as markdown.

**Parameters:**
- `url` (string): The URL of the web page to scrape

**Example:**
```python
scrape_web("https://example.com")
```

**How it works:**
Uses Jina Reader API (`r.jina.ai`) to convert HTML to clean, readable markdown.

### 2. `count_word_in_url`

Counts how many times a specific word appears in a web page.

**Parameters:**
- `url` (string): The URL of the web page to analyze
- `word` (string): The word to count (case-insensitive)

**Returns:**
```json
{
  "url": "https://datatalks.club/",
  "word": "data",
  "count": 42,
  "content_length": 31361
}
```

**Example:**
```python
count_word_in_url("https://datatalks.club/", "data")
```

### 3. `add` (Demo Tool)

A simple demo tool that adds two numbers.

**Parameters:**
- `a` (int): First number
- `b` (int): Second number

**Returns:** Sum of a and b

## Testing the Server

### Method 1: MCP Inspector (Recommended)

Test your MCP tools interactively with a web UI:

```bash
uv run fastmcp dev main.py
```

This will:
1. Install the MCP Inspector (first time only)
2. Start the server
3. Open a web interface where you can test all tools

**In the Inspector UI:**
- Navigate to the "Tools" tab
- Select a tool (e.g., `scrape_web`, `count_word_in_url`)
- Fill in the parameters
- Click "Run" to see results

### Method 2: Command Line Testing

Test individual functions directly:

```bash
# Test web scraping
uv run python test.py

# Test documentation search
uv run python search.py "demo"
uv run python search.py "authentication"
uv run python search.py "your query here"
```

## Integrating with MCP Clients

### Claude Code

1. **Configuration file is already created** (`.mcp.json`)

2. **Restart Claude Code** to load the server

3. **Verify the server is loaded:**
   ```bash
   /mcp
   ```
   You should see `doc-mcp` listed.

4. **Use the tools:**
   ```
   Count how many times "data" appears on https://datatalks.club/
   ```

### Claude Desktop

Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "doc-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/doc-mcp",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

### Other MCP Clients

The server uses **stdio transport**, making it compatible with any MCP client. Use the command:

```bash
uv --directory /path/to/doc-mcp run python main.py
```

## Documentation Search

The server indexes 266+ documentation files from the FastMCP repository, including:
- Getting started guides
- API reference
- Integration guides
- Code examples
- Authentication docs

### How it Works

1. **Download**: Fetches FastMCP repository as a zip file
2. **Extract**: Reads all `.md` and `.mdx` files
3. **Process**: Removes repository prefix from filenames
4. **Index**: Uses minsearch for full-text search with TF-IDF
5. **Search**: Returns top 5 most relevant documents

### Search Examples

```bash
# Search for "demo" examples
uv run python search.py "demo"
# Result: examples/testing_demo/README.md

# Search for authentication docs
uv run python search.py "authentication"
# Result: docs/servers/auth/authentication.mdx

# Search for tools documentation
uv run python search.py "tools"
```

## Project Structure

```
doc-mcp/
├── main.py              # MCP server with tool definitions
├── indexer.py           # Documentation indexing and search
├── search.py            # CLI search interface
├── test.py              # Web scraping test script
├── .mcp.json            # MCP server configuration
├── pyproject.toml       # Python dependencies
├── fastmcp-main.zip     # FastMCP documentation archive
└── README.md            # This file
```

## Architecture

```
┌─────────────────────┐
│   MCP Client        │
│ (Claude Code, etc)  │
└──────────┬──────────┘
           │ stdio
           │
┌──────────▼──────────┐
│   FastMCP Server    │
│   (main.py)         │
├─────────────────────┤
│ Tools:              │
│ • scrape_web        │
│ • count_word_in_url │
│ • add               │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼────┐   ┌───▼────┐
│ Jina   │   │ Min-   │
│ Reader │   │ search │
└────────┘   └────────┘
```

## Dependencies

- **fastmcp** (2.14.2+): MCP server framework
- **requests**: HTTP client for web scraping
- **minsearch** (0.0.7): Lightweight search engine
- **numpy**, **pandas**, **scikit-learn**: Search dependencies

## Development

### Adding New Tools

1. Open `main.py`
2. Define your tool function with type hints
3. Decorate with `@mcp.tool`
4. Add comprehensive docstring

Example:
```python
@mcp.tool
def your_tool(param: str) -> dict:
    """
    Description of what your tool does.

    Args:
        param: Description of parameter

    Returns:
        Description of return value
    """
    # Your implementation
    return {"result": "success"}
```

### Testing New Tools

```bash
# Restart the inspector
uv run fastmcp dev main.py

# Your new tool will appear in the Tools list
```

## Use Cases

- **Documentation Assistant**: Search through technical docs instantly
- **Content Analysis**: Analyze word frequency in web content
- **Research Tool**: Extract and search information from websites
- **AI Integration**: Provide context-aware documentation to AI assistants

## Performance

- **Indexing**: ~2-3 seconds for 266 documents
- **Search**: <100ms per query
- **Web Scraping**: ~1-2 seconds per page (depends on Jina Reader)

## Limitations

- Web scraping depends on Jina Reader service availability
- Search is limited to indexed FastMCP documentation
- Case-insensitive word counting only

## Future Enhancements

- [ ] Index custom documentation repositories
- [ ] Cache indexed documents to disk
- [ ] Add semantic search with embeddings
- [ ] Support for multiple documentation sources
- [ ] Advanced search filters and ranking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own documentation search needs!

## Acknowledgments

- **FastMCP**: For the excellent MCP server framework
- **Jina Reader**: For clean web page to markdown conversion
- **Minsearch**: For lightweight, effective text search
- **Context7**: For the inspiration

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Built with ❤️ using FastMCP and the Model Context Protocol
