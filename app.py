"""
🚀 AI Web Scraper - The Ultimate Content Extraction Tool
=======================================================

This is the main Streamlit app that brings everything together! It's like having
a super-powered web browser that can not only visit any website, but also
intelligently extract exactly what you're looking for using plain English.

No more copy-pasting, no more manual data entry - just describe what you want
and watch the AI work its magic!

Features:
- Natural language content extraction
- Smart suggestions based on page analysis  
- Beautiful, intuitive interface
- Real-time progress feedback
- Multiple extraction templates

Author: Your Friendly AI Developer 🤖
"""

# Core libraries for the web interface and functionality
import streamlit as st
from scrape import scrape_website
from parse import parse_with_llm, get_parsing_suggestions, EXAMPLE_DESCRIPTIONS
import time

# Configure the Streamlit page for the best user experience
st.set_page_config(
    page_title="AI Web Scraper",    # What shows in the browser tab
    page_icon="🤖",                # Cute robot icon
    layout="wide"                  # Use full screen width for better content display
)

# 🎨 Make it look beautiful! Custom CSS styling for a professional appearance
st.markdown("""
<style>
    /* Main header styling - big and bold to grab attention */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Description text - softer color for readability */
    .description-text {
        font-size: 1.2rem;
        color: #cccccc;
        margin-bottom: 2rem;
    }
    
    /* Suggestion buttons - styled to look clickable and friendly */
    .suggestion-button {
        margin: 5px;
        padding: 5px 10px;
        background-color: #262730;
        border: 1px solid #4CAF50;
        border-radius: 20px;
        color: white;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# 💾 Session State Management - Keep track of what the user has done
# This is like the app's memory - it remembers scraped content between interactions
if 'scraped_content' not in st.session_state:
    st.session_state.scraped_content = ""      # Store the scraped HTML content
if 'dom_visible' not in st.session_state:
    st.session_state.dom_visible = False       # Track if user wants to see DOM content

# 🎯 Main Application Header
st.markdown('<h1 class="main-header">🤖 AI Web Scraper</h1>', unsafe_allow_html=True)

# 🌐 URL Input Section with helpful examples
st.markdown("### Enter a Website URL:")

# Create columns for URL input and quick examples
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input("", placeholder="https://example.com", label_visibility="collapsed")

with col2:
    # 💡 Quick URL examples dropdown for user convenience
    example_urls = {
        "Select an example...": "",
        "🗞️ Tech News": "https://news.ycombinator.com",
        "📚 Quotes": "https://quotes.toscrape.com", 
        "📖 Books": "https://books.toscrape.com",
        "🛠️ Test HTML": "https://httpbin.org/html",
        "🎓 W3Schools": "https://w3schools.com",
        "💻 GitHub": "https://github.com",
        "📰 Dev.to": "https://dev.to"
    }
    
    selected_example = st.selectbox("Quick Examples:", list(example_urls.keys()))
    
    # If user selects an example, update the URL
    if selected_example != "Select an example..." and example_urls[selected_example]:
        url = example_urls[selected_example]
        st.rerun()  # Refresh to show the selected URL

# 🚀 The Big Red Button - Start the scraping process!
if st.button("🔍 Scrape Site", type="primary"):
    if url:
        # Show a friendly spinner while we work
        with st.spinner("🌐 Scraping the website... This may take a moment!"):
            # This is where the magic happens - scrape the website
            result = scrape_website(url)
            
        # Check if something went wrong during scraping
        if isinstance(result, str) and result.startswith("❌"):
            st.error(result)
            st.info("💡 **Tip:** Some websites block automated access. Try a different URL or check if the site is accessible.")
        else:
            # Success! Let the user know and store the results
            st.success("✅ Website scraped successfully!")
            st.balloons()  # A little celebration! 🎉
            
            # Save the scraped content in session state so we can use it later
            st.session_state.scraped_content = result
            st.session_state.dom_visible = True  # Auto-expand DOM viewer
    else:
        # Remind user they need to enter a URL
        st.warning("⚠️ Please enter a URL to scrape!")
        st.info("💡 Try one of the example URLs above to get started!")

# DOM Content Section (only show if content exists)
if st.session_state.scraped_content:
    
    # View DOM Content expandable section
    with st.expander("👁️ View DOM Content", expanded=st.session_state.dom_visible):
        if isinstance(st.session_state.scraped_content, str):
            # Show first 2000 characters of HTML
            content_preview = st.session_state.scraped_content[:2000]
            if len(st.session_state.scraped_content) > 2000:
                content_preview += "\n\n... [Content truncated for display]"
            
            st.code(content_preview, language="html", line_numbers=True)
            st.info(f"📄 Total content length: {len(st.session_state.scraped_content)} characters")
    
    st.markdown("---")
    
    # Parsing section
    st.markdown("### 🔍 Describe what you want to parse?")
    
    # Get intelligent suggestions based on scraped content
    if st.button("💡 Get Smart Suggestions"):
        with st.spinner("Analyzing content for suggestions..."):
            suggestions = get_parsing_suggestions(st.session_state.scraped_content)
            st.session_state.suggestions = suggestions
    
    # Show suggestions if available
    if 'suggestions' in st.session_state:
        st.markdown("**💡 Smart Suggestions (click to use):**")
        
        # Create columns for suggestions
        cols = st.columns(3)
        for i, suggestion in enumerate(st.session_state.suggestions):
            with cols[i % 3]:
                if st.button(f"📋 {suggestion}", key=f"suggestion_{i}"):
                    st.session_state.parse_description = suggestion
    
    # Show example descriptions
    st.markdown("**📚 Quick Examples:**")
    cols = st.columns(2)
    
    col_items = list(EXAMPLE_DESCRIPTIONS.items())
    for i, (name, description) in enumerate(col_items[:6]):  # Show first 6
        with cols[i % 2]:
            if st.button(f"🎯 {name}", key=f"example_{i}"):
                st.session_state.parse_description = description
    
    # Text area for custom description
    parse_description = st.text_area(
        "Or describe in your own words:",
        value=st.session_state.get('parse_description', ''),
        height=100,
        placeholder="Example: Extract all email addresses and phone numbers from the page"
    )
    
    # Parse button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Parse Content", type="primary", use_container_width=True):
            if parse_description.strip():
                with st.spinner("🤖 AI is analyzing and extracting information..."):
                    # Add some visual feedback
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    result = parse_with_llm(st.session_state.scraped_content, parse_description)
                    progress_bar.empty()
                
                # Display results
                st.markdown("---")
                st.markdown("### 🎯 Extracted Information")
                
                if result and result != "No matching information found.":
                    st.success("✅ Information successfully extracted!")
                    
                    # Display in a nice format
                    st.markdown("**🔍 Your Request:**")
                    st.info(parse_description)
                    
                    st.markdown("**📋 Extracted Data:**")
                    
                    # Try to format the result nicely
                    if '\n' in result:
                        # If multiple lines, show as bullet points
                        lines = [line.strip() for line in result.split('\n') if line.strip()]
                        for line in lines:
                            st.write(f"• {line}")
                    else:
                        st.write(result)
                    
                    # Add copy button functionality
                    st.code(result, language="text")
                    
                    # Show result stats
                    word_count = len(result.split())
                    char_count = len(result)
                    st.caption(f"📊 Results: {word_count} words, {char_count} characters")
                    
                else:
                    st.warning("🔍 No matching information found. Try rephrasing your description or check if the content exists on the page.")
                    
                    # Provide helpful suggestions
                    st.markdown("**💡 Tips:**")
                    st.write("• Be more specific about what you're looking for")
                    st.write("• Check the DOM content to see what's available")
                    st.write("• Try using the smart suggestions above")
                    
            else:
                st.warning("Please describe what you want to parse!")

else:
    # 👋 Welcome screen - show when no content has been scraped yet
    st.markdown('<p class="description-text">Enter a website URL above and click "Scrape Site" to get started!</p>', unsafe_allow_html=True)
    
    # 🌟 Showcase what this amazing tool can do
    st.markdown("### 🌟 What can you extract?")
    st.markdown("*With just a simple description in plain English, you can extract:*")
    
    # Split into two columns for better layout
    example_cols = st.columns(2)
    
    with example_cols[0]:
        st.markdown("""
        **📞 Contact Information:**
        - Email addresses and phone numbers
        - Physical addresses and locations  
        - Contact forms and support info
        
        **🔗 Links & Navigation:**
        - All website links and URLs
        - Social media profiles and handles
        - Download links and resources
        
        **📰 Content & Articles:**
        - Article headlines and titles
        - News summaries and excerpts
        - Blog post content and metadata
        
        **💼 Business Data:**
        - Product names, descriptions & prices
        - Service offerings and features
        - Company information and team details
        """)
    
    with example_cols[1]:
        st.markdown("""
        **📊 Structured Data:**
        - Table contents and spreadsheet data
        - List items and bullet points
        - Form fields and input options
        
        **🎯 Custom Extraction:**
        - Any specific information you describe
        - Based on your natural language input
        - Powered by advanced AI understanding
        
        **🏷️ Metadata & SEO:**
        - Page titles and descriptions
        - Keywords and tags
        - Image alt text and captions
        
        **📅 Events & Dates:**
        - Event listings and schedules
        - Publication dates and timestamps
        - Deadlines and important dates
        """)
    
    # 💡 Pro tips section
    st.markdown("---")
    st.markdown("### 💡 Pro Tips for Best Results")
    
    tips_cols = st.columns(3)
    with tips_cols[0]:
        st.info("""
        **🎯 Be Specific**
        
        Instead of "get links", try:
        "Extract all social media links and their platform names"
        """)
        
    with tips_cols[1]:
        st.info("""
        **📝 Use Examples**
        
        Click the quick example buttons to see pre-written descriptions that work well
        """)
        
    with tips_cols[2]:
        st.info("""
        **🔍 Try Suggestions**
        
        Use "Get Smart Suggestions" to see what the AI thinks you can extract from any page
        """)