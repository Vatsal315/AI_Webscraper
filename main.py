import streamlit as st
from scrape import scrape_website, create_content_chunks, analyze_content_with_llm
from bs4 import BeautifulSoup
import json

def clean_html_content(html_content):
    """Extract and clean text content from HTML"""
    if not html_content or html_content.startswith("❌"):
        return html_content
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        return f"Content extracted but couldn't clean it: {str(e)}\n\nRaw content: {html_content[:1000]}..."

def display_dom_data(dom_data):
    """Display parsed DOM data in organized sections"""
    if not dom_data:
        st.error("No DOM data available")
        return
    
    # Page Info
    st.subheader("📋 Page Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Title:** {dom_data['title']}")
    with col2:
        st.write(f"**Meta Description:** {dom_data['meta_description'][:100]}..." if len(dom_data['meta_description']) > 100 else dom_data['meta_description'])
    
    # Headings
    if any(dom_data['headings'].values()):
        st.subheader("📝 Headings Structure")
        for level, headings in dom_data['headings'].items():
            if headings:
                st.write(f"**{level.upper()}:**")
                for heading in headings[:5]:  # Show first 5
                    st.write(f"• {heading}")
                if len(headings) > 5:
                    st.write(f"... and {len(headings) - 5} more")
    
    # Links
    if dom_data['links']:
        st.subheader("🔗 Links Found")
        col1, col2 = st.columns(2)
        
        internal_links = [link for link in dom_data['links'] if not link['is_external']]
        external_links = [link for link in dom_data['links'] if link['is_external']]
        
        with col1:
            st.write(f"**Internal Links ({len(internal_links)}):**")
            for link in internal_links[:10]:
                st.write(f"• [{link['text']}]({link['url']})")
            if len(internal_links) > 10:
                st.write(f"... and {len(internal_links) - 10} more")
        
        with col2:
            st.write(f"**External Links ({len(external_links)}):**")
            for link in external_links[:10]:
                st.write(f"• [{link['text']}]({link['url']})")
            if len(external_links) > 10:
                st.write(f"... and {len(external_links) - 10} more")
    
    # Images
    if dom_data['images']:
        st.subheader("🖼️ Images Found")
        st.write(f"Found {len(dom_data['images'])} images")
        
        # Show first few images
        for i, img in enumerate(dom_data['images'][:3]):
            with st.expander(f"Image {i+1}: {img['alt'] or 'No alt text'}"):
                st.write(f"**Source:** {img['src']}")
                st.write(f"**Alt text:** {img['alt']}")
                st.write(f"**Title:** {img['title']}")
    
    # Contact Information
    contact = dom_data['contact_info']
    if contact['emails'] or contact['phones']:
        st.subheader("📞 Contact Information")
        col1, col2 = st.columns(2)
        
        with col1:
            if contact['emails']:
                st.write("**Emails:**")
                for email in contact['emails']:
                    st.write(f"• {email}")
        
        with col2:
            if contact['phones']:
                st.write("**Phone Numbers:**")
                for phone in contact['phones']:
                    st.write(f"• {phone}")
    
    # Lists
    if dom_data['lists']:
        st.subheader("📋 Lists Found")
        for i, lst in enumerate(dom_data['lists'][:3]):
            with st.expander(f"{lst['type'].upper()} List {i+1} ({len(lst['items'])} items)"):
                for item in lst['items'][:10]:
                    st.write(f"• {item}")
                if len(lst['items']) > 10:
                    st.write(f"... and {len(lst['items']) - 10} more items")
    
    # Tables
    if dom_data['tables']:
        st.subheader("📊 Tables Found")
        for i, table in enumerate(dom_data['tables'][:2]):
            with st.expander(f"Table {i+1} ({len(table)} rows)"):
                if table:
                    st.dataframe(table)
    
    # Forms
    if dom_data['forms']:
        st.subheader("📝 Forms Found")
        for i, form in enumerate(dom_data['forms']):
            with st.expander(f"Form {i+1} ({form['method'].upper()})"):
                st.write(f"**Action:** {form['action']}")
                st.write(f"**Method:** {form['method']}")
                st.write(f"**Inputs:** {len(form['inputs'])}")
                for inp in form['inputs'][:5]:
                    st.write(f"• {inp['type']} - {inp['name']} {'(required)' if inp['required'] else ''}")

def display_llm_analysis(analysis_results):
    """Display LLM analysis results in organized format"""
    if not analysis_results:
        st.error("No analysis results available")
        return
    
    if len(analysis_results) == 1 and 'error' in analysis_results[0]:
        st.error(analysis_results[0]['error'])
        return
    
    st.subheader("🤖 AI Analysis Results")
    
    # Summary stats
    total_chunks = len(analysis_results)
    avg_chunk_length = sum(r.get('chunk_length', 0) for r in analysis_results) / total_chunks if total_chunks > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Chunks", total_chunks)
    with col2:
        st.metric("Average Chunk Size", f"{avg_chunk_length:.0f} chars")
    with col3:
        st.metric("Total Content", f"{sum(r.get('chunk_length', 0) for r in analysis_results)} chars")
    
    # Display each analysis result
    for result in analysis_results:
        if 'error' in result:
            st.error(f"Error: {result['error']}")
            continue
            
        with st.expander(f"📝 Chunk {result['chunk_id']} Analysis ({result['chunk_length']} chars)"):
            st.write("**Original Content Preview:**")
            st.text(result['chunk_preview'])
            
            st.write("**AI Analysis:**")
            st.write(result['analysis'])

st.title("🤖 AI Web Scraper with LLM Analysis")
st.write("Advanced web scraper with AI-powered content analysis using local LLMs!")

url = st.text_input("Enter the URL of the website to scrape:", placeholder="https://example.com")

# Scraping options
st.subheader("⚙️ Scraping Options")
col1, col2, col3, col4 = st.columns(4)
with col1:
    parse_dom = st.checkbox("🔍 Parse DOM", value=True, help="Extract structured data from HTML")
with col2:
    show_raw_html = st.checkbox("🔧 Show HTML", help="Display raw HTML code")
with col3:
    show_cleaned_text = st.checkbox("📄 Show Text", help="Display cleaned text content")
with col4:
    show_json = st.checkbox("📋 Show JSON", help="Display DOM data as JSON")

# LLM Analysis Options
st.subheader("🤖 AI Analysis Options")
col1, col2, col3 = st.columns(3)
with col1:
    enable_llm = st.checkbox("🤖 Enable AI Analysis", help="Analyze content with local LLM")
with col2:
    analysis_type = st.selectbox(
        "Analysis Type",
        ["summarize", "extract_key_info", "analyze_sentiment", "find_contacts", 
         "extract_topics", "generate_questions", "critique", "keywords"],
        help="Choose what type of analysis to perform"
    )
with col3:
    model_name = st.selectbox(
        "LLM Model",
        ["llama3.2", "llama3.1", "llama2", "mistral", "codellama"],
        help="Choose the Ollama model to use"
    )

# Chunking options (advanced)
with st.expander("🔧 Advanced Chunking Options"):
    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.slider("Chunk Size", 500, 2000, 1000, help="Maximum characters per chunk")
    with col2:
        chunk_overlap = st.slider("Chunk Overlap", 50, 500, 200, help="Overlap between chunks")

if st.button("🚀 Start Scraping & Analysis"):
    if url:
        # Step 1: Scraping
        with st.spinner("🔍 Scraping the website..."):
            result = scrape_website(url, parse_dom=parse_dom)
        
        if isinstance(result, str) and result.startswith("❌"):
            st.error(result)
        else:
            st.success("✅ Scraping completed!")
            
            # Handle results based on whether DOM parsing was enabled
            if parse_dom and isinstance(result, dict):
                html_content = result['html']
                dom_data = result['dom_data']
                
                # Step 2: LLM Analysis (if enabled)
                if enable_llm:
                    with st.spinner(f"🤖 Analyzing content with {model_name}..."):
                        try:
                            # Create chunks
                            chunks = create_content_chunks(result, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                            
                            if chunks:
                                st.info(f"📄 Created {len(chunks)} content chunks for analysis")
                                
                                # Analyze with LLM
                                analysis_results = analyze_content_with_llm(chunks, analysis_type=analysis_type, model_name=model_name)
                                
                                # Display analysis results
                                display_llm_analysis(analysis_results)
                            else:
                                st.warning("No content chunks created for analysis")
                                
                        except Exception as e:
                            st.error(f"❌ LLM Analysis failed: {str(e)}")
                            st.info("💡 Make sure Ollama is installed and the model is available. Run: `ollama pull llama3.2`")
                
                # Display DOM data
                if dom_data:
                    display_dom_data(dom_data)
                
                # Show JSON if requested
                if show_json and dom_data:
                    st.subheader("📋 DOM Data (JSON)")
                    st.json(dom_data)
                
                # Show cleaned text if requested
                if show_cleaned_text:
                    st.subheader("📄 Cleaned Text Content")
                    cleaned_text = clean_html_content(html_content)
                    st.text_area("Cleaned content:", cleaned_text, height=300)
                
                # Show raw HTML if requested
                if show_raw_html:
                    st.subheader("🔧 Raw HTML")
                    st.code(html_content[:5000] + "..." if len(html_content) > 5000 else html_content, language="html")
            
            else:
                # Handle non-DOM parsing results
                
                # Step 2: LLM Analysis (if enabled)
                if enable_llm:
                    with st.spinner(f"🤖 Analyzing content with {model_name}..."):
                        try:
                            # Create chunks
                            chunks = create_content_chunks(result, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                            
                            if chunks:
                                st.info(f"📄 Created {len(chunks)} content chunks for analysis")
                                
                                # Analyze with LLM
                                analysis_results = analyze_content_with_llm(chunks, analysis_type=analysis_type, model_name=model_name)
                                
                                # Display analysis results
                                display_llm_analysis(analysis_results)
                            else:
                                st.warning("No content chunks created for analysis")
                                
                        except Exception as e:
                            st.error(f"❌ LLM Analysis failed: {str(e)}")
                            st.info("💡 Make sure Ollama is installed and the model is available. Run: `ollama pull llama3.2`")
                
                if show_cleaned_text:
                    st.subheader("📄 Cleaned Text Content")
                    cleaned_text = clean_html_content(result)
                    st.text_area("Cleaned content:", cleaned_text, height=300)
                
                if show_raw_html:
                    st.subheader("🔧 Raw HTML")
                    st.code(result[:5000] + "..." if len(result) > 5000 else result, language="html")
    else:
        st.warning("Please enter a URL to scrape!")





