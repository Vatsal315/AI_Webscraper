# 🤖 AI Web Scraper with Natural Language Parsing

A powerful, intelligent web scraper that lets you extract specific information from any website using plain English descriptions. No more complex CSS selectors or XPath - just describe what you want and let AI do the work!

## ✨ Features

### 🔍 **Smart Web Scraping**
- **Multi-method approach**: Tries simple HTTP requests first, falls back to full browser automation
- **Anti-detection**: Random user agents, stealth mode, realistic browser headers
- **Automatic fallbacks**: If one method fails, automatically tries another
- **DOM content parsing**: Extracts structured data from HTML

### 🤖 **AI-Powered Information Extraction**
- **Natural language parsing**: Just describe what you want to extract
- **Intelligent suggestions**: AI analyzes the page and suggests what you can extract
- **Multiple LLM models**: Support for Llama, Mistral, and other Ollama models
- **Context-aware**: Understands the content and extracts relevant information

### 🎯 **Quick Templates**
Pre-built extraction templates for common use cases:
- 📞 **Contact Information** - emails, phones, addresses
- 🔗 **Links & URLs** - all links with anchor text
- 📰 **Content** - headlines, articles, summaries
- 💼 **Business Data** - products, prices, services
- 🏢 **Company Info** - about pages, team members
- 📱 **Social Media** - profiles, handles, links

### 🛡️ **Robust & Reliable**
- **Error handling**: Graceful failures with helpful error messages
- **Progress tracking**: Visual feedback during long operations
- **Content validation**: Checks and cleans extracted data
- **Token optimization**: Smart content chunking for LLM processing

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running ([Download here](https://ollama.ai))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv ai-scraper-env
   source ai-scraper-env/bin/activate  # On Windows: ai-scraper-env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Install and setup Ollama**
   ```bash
   # Install Ollama from https://ollama.ai
   # Then pull the default model
   ollama pull llama3.2
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and go to `http://localhost:8501`

## 🎮 How to Use

### Basic Usage

1. **Enter a website URL** in the input field
2. **Click "Scrape Site"** to extract the content
3. **View the scraped content** in the DOM viewer
4. **Describe what you want to extract** in plain English
5. **Click "Parse Content"** and watch AI work its magic!

## 🔧 Technical Workflow

### Web Scraping and Content Extraction
The first step is to extract content from websites using our multi-method approach. This is done using both HTTP requests for fast scraping and Selenium browser automation for JavaScript-heavy sites. The system automatically selects the best method and falls back to alternatives if needed.

### AI-Powered Content Parsing  
After extracting the raw HTML, the next step is to parse and clean the content using BeautifulSoup and custom algorithms. The cleaned content is then processed by local LLM models through Ollama, allowing for intelligent extraction based on natural language descriptions.

### Smart Content Analysis and Suggestions
This section outlines how the system analyzes webpage structure to provide intelligent suggestions. Using pattern recognition and HTML analysis, the scraper identifies extractable elements like emails, phone numbers, prices, dates, and structured data, then suggests relevant extraction opportunities to users.

### Natural Language Processing Pipeline
The core of our system uses LangChain's text processing capabilities combined with local Ollama models. Text is intelligently chunked using RecursiveCharacterTextSplitter, then processed through carefully crafted prompts that instruct the AI to extract specific information based on user descriptions in plain English.

### Optional: Advanced DOM Content Analysis
An advanced feature explains how to leverage the structured DOM parsing capabilities to extract complex data relationships, nested content structures, and metadata from websites, providing comprehensive content analysis beyond simple text extraction.

## 🌐 Great Test URLs

Try these websites to see the scraper in action:

### 📰 **News & Articles**
- `https://news.ycombinator.com` - Tech news and discussions
- `https://techcrunch.com` - Technology news and startups
- `https://dev.to` - Developer articles and tutorials

### 🛒 **E-commerce & Products**
- `https://quotes.toscrape.com` - Great for testing quote extraction
- `https://books.toscrape.com` - Book titles, prices, and ratings
- `https://httpbin.org/html` - Simple HTML structure for testing

### 🏢 **Business & Services**
- `https://github.com` - Developer profiles and repositories
- `https://stackoverflow.com` - Q&A content and user profiles
- `https://example.com` - Simple page for basic testing

### 🎓 **Educational & Tutorials**
- `https://w3schools.com` - Tutorials and code examples
- `https://mdn.mozilla.org` - Web development documentation
- `https://freecodecamp.org` - Coding courses and articles

## 🛠️ Technical Details

### Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   Web Scraper    │    │   AI Parser     │
│                 │───▶│                  │───▶│                 │
│ • User Input    │    │ • HTTP Requests  │    │ • LLM Analysis  │
│ • Results       │    │ • Selenium       │    │ • NL Processing │
│ • Progress      │    │ • DOM Parsing    │    │ • Data Extract  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Key Components

#### `scrape.py` - Web Scraping Engine
- **Multi-method scraping**: HTTP requests + Selenium fallback
- **Anti-detection features**: User agents, stealth mode
- **Content cleaning**: Removes unnecessary elements
- **Error handling**: Robust failure management

#### `parse.py` - AI-Powered Parser
- **Natural language understanding**: Converts descriptions to extraction logic
- **Content analysis**: Suggests extraction possibilities
- **LLM integration**: Uses Ollama for intelligent parsing
- **Result formatting**: Clean, structured output

#### `app.py` - User Interface
- **Intuitive design**: Clean, modern Streamlit interface
- **Progress feedback**: Real-time operation status
- **Smart suggestions**: AI-generated extraction ideas
- **Result visualization**: Multiple output formats

### Supported Models

The scraper works with any Ollama model:
- **llama3.2** (recommended) - Fast and accurate
- **llama3.1** - More powerful for complex tasks
- **mistral** - Good alternative option
- **dolphin3** - Creative and detailed extractions
- **codellama** - Excellent for technical content

## 🔧 Configuration

### Environment Variables

Create a `.env` file for customization:

```env
# Default LLM model
DEFAULT_MODEL=llama3.2

# Scraping settings
DEFAULT_TIMEOUT=30
MAX_CONTENT_LENGTH=8000

# Chunking settings
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200
```

### Custom Settings

You can modify settings directly in the code:

```python
# In parse.py - Adjust LLM model
model = OllamaLLM(model="your-preferred-model")

# In scrape.py - Modify timeout settings
response = requests.get(website, headers=headers, timeout=60)

# In app.py - Change interface defaults
chunk_size = st.slider("Chunk Size", 500, 3000, 1000)
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Areas for Improvement
- 🌐 Add support for more LLM providers (OpenAI, Anthropic, etc.)
- 🔍 Implement more sophisticated parsing strategies
- 🎨 Enhance the user interface with more features
- 📊 Add data export capabilities (CSV, JSON, Excel)
- 🔒 Implement authentication for sensitive sites
- 📱 Add mobile-responsive design

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit: `git commit -m "Add feature-name"`
5. Push: `git push origin feature-name`
6. Create a Pull Request

## 📋 Requirements

### Python Packages
```
streamlit>=1.28.0
selenium>=4.15.0
webdriver-manager>=4.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
langchain>=0.1.0
langchain-ollama>=0.1.0
langchain-core>=0.1.0
lxml>=4.9.0
html5lib>=1.1
python-dotenv>=1.0.0
```

### System Requirements
- **Chrome browser** (for Selenium fallback)
- **Ollama** (for AI parsing)
- **Python 3.8+**
- **4GB+ RAM** (recommended for LLM operations)

## 🐛 Troubleshooting

### Common Issues

#### ❌ "LLM Analysis failed"
```bash
# Make sure Ollama is running
ollama serve

# Check available models
ollama list

# Pull the default model if missing
ollama pull llama3.2
```

#### ❌ "ChromeDriver issues"
```bash
# The scraper auto-downloads ChromeDriver, but if issues persist:
pip install --upgrade webdriver-manager
```

#### ❌ "Import errors"
```bash
# Reinstall dependencies
pip install -r requirement.txt --force-reinstall
```

#### ❌ "Scraping blocked"
- Try different user agents
- Use VPN if content is geo-blocked
- Check if site requires authentication
- Some sites block automated access

### Performance Tips

1. **Use smaller chunk sizes** for faster processing
2. **Choose appropriate models** (llama3.2 for speed, llama3.1 for accuracy)
3. **Limit content length** for large pages
4. **Use HTTP method first** before Selenium fallback

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** - For providing excellent local LLM capabilities
- **Streamlit** - For the amazing web app framework
- **LangChain** - For LLM integration tools
- **Selenium** - For robust web automation
- **BeautifulSoup** - For HTML parsing capabilities

**Made with ❤️ by Vatsal 

*Happy scraping! 🚀*