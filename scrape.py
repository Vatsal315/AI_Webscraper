"""
🌐 AI Web Scraper - Advanced Web Scraping with Intelligence
==========================================================

This module handles the core web scraping functionality with multiple fallback methods.
It's designed to be robust, stealthy, and intelligent - just like a human browsing the web!

Features:
- Multi-method scraping (HTTP requests + Selenium browser automation)
- Anti-detection mechanisms (random user agents, stealth mode)
- Automatic content cleaning and parsing
- AI-powered content chunking for LLM processing

Author: Your Friendly AI Developer 🤖
"""

# Core web scraping and automation libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Utility libraries for web requests and content processing
import time
import requests
from bs4 import BeautifulSoup
import random
import json
from urllib.parse import urljoin, urlparse

# AI and language processing libraries
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
import re


def get_random_user_agent():
    """
    🎭 The Art of Digital Disguise
    
    This function helps our scraper blend in with real human traffic by rotating
    through different browser signatures. Think of it as changing costumes to
    avoid being recognized at a party!
    
    Why do we need this?
    - Websites can block requests from bots/scrapers
    - Different user agents help us appear as different real users
    - Reduces the chance of getting our IP blocked
    
    Returns:
        str: A realistic browser user agent string
    """
    # A collection of real browser user agents from popular browsers and OS combinations
    # These are actual user agent strings from Chrome, Safari, and other browsers
    user_agents = [
        # Chrome on macOS (most common)
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # Chrome on Windows (very common)
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # Chrome on Linux (less common but still valid)
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # Safari on macOS (native Apple browser)
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
    ]
    
    # Pick one at random - keeps us unpredictable!
    return random.choice(user_agents)


def scrape_with_requests(website):
    """
    🚀 The Speed Demon - Fast HTTP Scraping
    
    This is our first line of attack! It uses simple HTTP requests to grab content
    quickly and efficiently. Most websites work fine with this method, and it's
    much faster than launching a full browser.
    
    Think of this as knocking on the front door and politely asking for the content.
    About 80% of websites will happily comply!
    
    Args:
        website (str): The URL we want to scrape
    
    Returns:
        str: HTML content if successful, None if it fails
    """
    try:
        # Let the user know we're starting with the simple approach
        print("🌐 Trying simple HTTP request (fast method)...")
        
        # Craft headers that make us look like a real browser
        # These headers are crucial - they tell the website we're a legitimate browser
        headers = {
            'User-Agent': get_random_user_agent(),  # Our digital disguise!
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # What content types we accept
            'Accept-Language': 'en-US,en;q=0.5',  # We prefer English content
            'Accept-Encoding': 'gzip, deflate',    # We can handle compressed responses
            'Connection': 'keep-alive',            # We want to keep the connection open
        }
        
        # Make the actual request with a reasonable timeout
        # 30 seconds should be enough for most websites to respond
        response = requests.get(website, headers=headers, timeout=30)
        
        # This will raise an exception if we get a 4xx or 5xx status code
        response.raise_for_status()
        
        print("✅ Simple request successful! Got the content quickly.")
        return response.text
        
    except Exception as e:
        # If anything goes wrong, we'll try the browser method instead
        print(f"❌ Simple request failed: {str(e)}")
        print("   Don't worry, we'll try with a real browser next!")
        return None


def scrape_with_selenium(website):
    """
    🎭 The Heavy Artillery - Full Browser Automation
    
    When simple HTTP requests fail, we bring out the big guns! This method launches
    a real Chrome browser and navigates like a human would. It can handle:
    - JavaScript-heavy websites
    - Sites that check for bot behavior
    - Dynamic content that loads after the page
    
    It's slower but much more powerful - like having a robot butler browse for you!
    
    Args:
        website (str): The URL we want to scrape
    
    Returns:
        str: HTML content if successful, None if it fails
    """
    try:
        print("🚀 Launching Chrome Browser with Selenium (stealth mode)...")
        
        # Configure Chrome options for maximum stealth and performance
        options = Options()
        
        # Run headlessly (no visible browser window) - saves resources and looks less suspicious
        options.add_argument("--headless")
        
        # Security and compatibility options
        options.add_argument("--no-sandbox")                    # Bypass OS security model (safe in containers)
        options.add_argument("--disable-dev-shm-usage")         # Overcome limited resource problems
        
        # Anti-detection measures - make us look less like a bot
        options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation traces
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Remove automation flags
        options.add_experimental_option('useAutomationExtension', False)  # Disable automation extension
        
        # Use our random user agent for this browser session
        options.add_argument(f"--user-agent={get_random_user_agent()}")
        
        # Create the browser instance with automatic ChromeDriver management
        # WebDriverManager handles downloading the right ChromeDriver version automatically!
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Extra stealth: Remove the 'webdriver' property that websites can detect
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Navigate to the website (just like a human clicking a link)
        driver.get(website)
        print("✅ Website loaded successfully with full browser!")
        
        # Give the page time to fully load (including JavaScript)
        # Some sites load content dynamically after the initial page load
        print("⏳ Waiting for dynamic content to load...")
        time.sleep(3)
        
        # Extract the complete HTML (including any JavaScript-generated content)
        html = driver.page_source
        
        # Always clean up by closing the browser
        driver.quit()
        print("🔒 Browser closed - cleaned up resources")
        return html
        
    except Exception as e:
        print(f"❌ Browser automation failed: {str(e)}")
        print("   This might be due to ChromeDriver issues or heavy anti-bot protection")
        return None
    



def parse_dom_content(html_content, base_url):
    """Parse HTML content and extract structured DOM data"""
    if not html_content or html_content.startswith("❌"):
        return None
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract structured data
        dom_data = {
            'title': soup.title.string.strip() if soup.title else 'No title found',
            'meta_description': '',
            'headings': {
                'h1': [h.get_text().strip() for h in soup.find_all('h1')],
                'h2': [h.get_text().strip() for h in soup.find_all('h2')],
                'h3': [h.get_text().strip() for h in soup.find_all('h3')],
            },
            'links': [],
            'images': [],
            'paragraphs': [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()],
            'lists': [],
            'tables': [],
            'forms': [],
            'contact_info': {
                'emails': [],
                'phones': [],
                'addresses': []
            }
        }
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            dom_data['meta_description'] = meta_desc.get('content', '')
        
        # Extract links
        for link in soup.find_all('a', href=True):
            link_text = link.get_text().strip()
            link_url = urljoin(base_url, link['href'])
            if link_text:
                dom_data['links'].append({
                    'text': link_text,
                    'url': link_url,
                    'is_external': urlparse(link_url).netloc != urlparse(base_url).netloc
                })
        
        # Extract images
        for img in soup.find_all('img'):
            img_src = img.get('src', '')
            if img_src:
                dom_data['images'].append({
                    'src': urljoin(base_url, img_src),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        
        # Extract lists
        for ul in soup.find_all(['ul', 'ol']):
            list_items = [li.get_text().strip() for li in ul.find_all('li')]
            if list_items:
                dom_data['lists'].append({
                    'type': ul.name,
                    'items': list_items
                })
        
        # Extract tables
        for table in soup.find_all('table'):
            table_data = []
            for row in table.find_all('tr'):
                row_data = [cell.get_text().strip() for cell in row.find_all(['td', 'th'])]
                if row_data:
                    table_data.append(row_data)
            if table_data:
                dom_data['tables'].append(table_data)
        
        # Extract forms
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'inputs': []
            }
            for input_field in form.find_all(['input', 'textarea', 'select']):
                form_data['inputs'].append({
                    'type': input_field.get('type', input_field.name),
                    'name': input_field.get('name', ''),
                    'placeholder': input_field.get('placeholder', ''),
                    'required': input_field.has_attr('required')
                })
            dom_data['forms'].append(form_data)
        
        # Extract potential contact information using simple patterns
        import re
        text_content = soup.get_text()
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        dom_data['contact_info']['emails'] = list(set(re.findall(email_pattern, text_content)))
        
        # Extract phone numbers (simple patterns)
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US format
            r'\b\(\d{3}\)\s?\d{3}[-.]?\d{4}\b',  # (123) 456-7890
            r'\b\+\d{1,3}[-.\s]?\d{1,14}\b'  # International
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, text_content)
            dom_data['contact_info']['phones'].extend(phones)
        dom_data['contact_info']['phones'] = list(set(dom_data['contact_info']['phones']))
        
        return dom_data
        
    except Exception as e:
        print(f"❌ DOM parsing failed: {str(e)}")
        return None


def create_content_chunks(content, chunk_size=1000, chunk_overlap=200):
    """
    ✂️ The Content Chopper - Smart Text Splitting for AI
    
    Large web pages can overwhelm AI models, so we need to break them into bite-sized
    chunks. But we're smart about it - we don't just cut randomly! We split at natural
    boundaries (sentences, paragraphs) and add overlap so context isn't lost.
    
    Think of it like preparing a large document for reading - you'd break it into
    chapters with some overlap so you don't lose the story flow!
    
    Args:
        content: The content to chunk (can be HTML string or structured data)
        chunk_size (int): Maximum characters per chunk (default: 1000)
        chunk_overlap (int): Characters to overlap between chunks (default: 200)
    
    Returns:
        list: List of text chunks ready for AI processing
    """
    print(f"📄 Creating smart content chunks for AI processing...")
    
    # First, we need to convert whatever content we have into clean text
    if isinstance(content, dict) and 'dom_data' in content:
        # If we have structured DOM data, extract it intelligently
        print("   📊 Processing structured DOM data...")
        dom_data = content['dom_data']
        text_parts = []
        
        # Start with the most important content - title and description
        if dom_data['title']:
            text_parts.append(f"Title: {dom_data['title']}")
        if dom_data['meta_description']:
            text_parts.append(f"Description: {dom_data['meta_description']}")
        
        # Add headings (these are super important for context)
        for level, headings in dom_data['headings'].items():
            for heading in headings:
                text_parts.append(f"{level.upper()}: {heading}")
        
        # Add the main content - paragraphs
        text_parts.extend(dom_data['paragraphs'])
        
        # Add list items (these often contain key information)
        for lst in dom_data['lists']:
            text_parts.extend(lst['items'])
        
        # Combine everything with proper spacing
        content_text = "\n".join(text_parts)
        
    elif isinstance(content, str):
        # If we have raw HTML, clean it up first
        print("   🧹 Cleaning HTML content...")
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove stuff we don't need (scripts, styles, etc.)
        for script in soup(["script", "style"]):
            script.decompose()
            
        content_text = soup.get_text()
    else:
        # Fallback - convert whatever we have to string
        content_text = str(content)
    
    # Clean up whitespace - multiple spaces/newlines become single spaces
    print("   🧽 Normalizing whitespace...")
    content_text = re.sub(r'\s+', ' ', content_text).strip()
    
    # Now for the smart splitting! LangChain's RecursiveCharacterTextSplitter
    # tries different separators in order, so it splits naturally
    print("   ✂️ Splitting content intelligently...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,      # Target size per chunk
        chunk_overlap=chunk_overlap, # How much chunks should overlap
        length_function=len,        # How to measure chunk size
        # Try these separators in order - paragraph breaks first, then sentences, etc.
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    )
    
    # Do the actual splitting
    chunks = text_splitter.split_text(content_text)
    
    print(f"✅ Successfully created {len(chunks)} smart chunks")
    print(f"   📏 Average chunk size: {sum(len(chunk) for chunk in chunks) // len(chunks) if chunks else 0} characters")
    
    return chunks


def analyze_content_with_llm(chunks, analysis_type="summarize", model_name="llama3.2"):
    """Process content chunks through LLM and return analysis"""
    print(f"🤖 Analyzing content with {model_name}...")
    
    try:
        # Initialize Ollama LLM
        llm = OllamaLLM(model=model_name)
        
        # Define analysis prompts
        prompts = {
            "summarize": "Summarize the following content in 2-3 sentences, focusing on the main points:",
            "extract_key_info": "Extract the most important information, key facts, and main topics from this content:",
            "analyze_sentiment": "Analyze the sentiment and tone of this content. Is it positive, negative, or neutral? Explain:",
            "find_contacts": "Find any contact information, company names, or important details from this content:",
            "extract_topics": "What are the main topics and themes discussed in this content? List them:",
            "generate_questions": "Generate 3-5 relevant questions that this content answers:",
            "critique": "Provide a brief critique or analysis of this content - what's good, what could be improved:",
            "keywords": "Extract the main keywords and important terms from this content:"
        }
        
        prompt_template = prompts.get(analysis_type, prompts["summarize"])
        results = []
        
        for i, chunk in enumerate(chunks):
            try:
                print(f"📝 Processing chunk {i+1}/{len(chunks)}...")
                
                # Create full prompt
                full_prompt = f"{prompt_template}\n\n{chunk}\n\nAnalysis:"
                
                # Get LLM response
                response = llm.invoke(full_prompt)
                
                results.append({
                    'chunk_id': i + 1,
                    'chunk_preview': chunk[:200] + "..." if len(chunk) > 200 else chunk,
                    'analysis': response.strip(),
                    'chunk_length': len(chunk)
                })
                
            except Exception as e:
                print(f"❌ Error processing chunk {i+1}: {str(e)}")
                results.append({
                    'chunk_id': i + 1,
                    'chunk_preview': chunk[:200] + "..." if len(chunk) > 200 else chunk,
                    'analysis': f"Error processing this chunk: {str(e)}",
                    'chunk_length': len(chunk)
                })
        
        print(f"✅ Completed analysis of {len(results)} chunks")
        return results
        
    except Exception as e:
        print(f"❌ LLM analysis failed: {str(e)}")
        return [{'error': f"LLM analysis failed: {str(e)}"}]


def scrape_website(website, parse_dom=False):
    """Multi-method web scraper - tries multiple approaches"""
    print(f"🔍 Starting to scrape: {website}")
    
    if not website:
        return "❌ Please provide a valid URL"
    
    # Add protocol if missing
    if not website.startswith(('http://', 'https://')):
        website = 'https://' + website
    
    # Method 1: Try simple requests first (faster and less detectable)
    html = scrape_with_requests(website)
    
    # Method 2: If simple requests fail, try Selenium
    if not html:
        print("🔄 Falling back to Selenium...")
        html = scrape_with_selenium(website)
    
    if html:
        print("✅ Scraping completed successfully!")
        
        if parse_dom:
            print("🔍 Parsing DOM content...")
            dom_data = parse_dom_content(html, website)
            return {
                'html': html,
                'dom_data': dom_data,
                'url': website
            }
        else:
            return html
    else:
        return "❌ All scraping methods failed. The website might be blocking requests or requires special handling."







