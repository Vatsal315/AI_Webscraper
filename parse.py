"""
🧠 AI-Powered Content Parser - Natural Language Information Extraction
=====================================================================

This module is where the magic happens! It takes messy web content and uses AI to
extract exactly what you asked for in plain English. No more CSS selectors or 
XPath nightmares - just describe what you want and let the AI figure it out!

Think of this as having a super-smart assistant who can read any webpage and
pull out exactly the information you need, no matter how it's formatted.

Features:
- Natural language parsing ("extract all email addresses")  
- Smart content analysis and suggestions
- Multiple extraction strategies
- Clean, formatted output

Author: Your Friendly AI Developer 🤖
"""

# AI and language processing libraries
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from bs4 import BeautifulSoup
import json
import re

# The secret sauce! This template teaches the AI how to extract information
# We're basically giving the AI very specific instructions on how to behave
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Format:** If multiple items are found, separate them with newlines or commas as appropriate."
)

# Initialize our AI model - Llama 3.2 is a great balance of speed and accuracy
model = OllamaLLM(model="llama3.2")


def clean_dom_content(html_content):
    """
    🧹 The Content Janitor - HTML Cleaning and Preparation
    
    Raw HTML is messy! It's full of JavaScript, CSS, navigation menus, footers,
    and all sorts of stuff we don't need. This function is like having a really
    good editor who removes all the fluff and gives us just the good stuff.
    
    Think of it as preparing a messy document for reading - we remove all the
    annotations, formatting codes, and irrelevant sections, leaving just the
    content that matters.
    
    Args:
        html_content (str): Raw HTML from the website
    
    Returns:
        str: Clean, readable text ready for AI processing
    """
    # Handle edge case - no content provided
    if not html_content:
        return ""
    
    try:
        # Parse the HTML so we can work with it intelligently  
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove all the stuff we definitely don't want
        # These elements rarely contain useful information for extraction
        unwanted_tags = ["script", "style", "noscript", "header", "footer", "nav"]
        print(f"   🗑️ Removing {len(unwanted_tags)} types of unwanted elements...")
        
        for tag_type in unwanted_tags:
            for element in soup(tag_type):
                element.decompose()  # This completely removes the element
        
        # Extract just the text content (no HTML tags)
        text = soup.get_text()
        
        # Now for some serious text cleaning!
        # Split into lines and clean each one
        lines = (line.strip() for line in text.splitlines())
        
        # Split lines on double spaces and clean each chunk
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # Join everything back together with single spaces
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        print(f"   ✅ Cleaned content: {len(clean_text)} characters")
        return clean_text
        
    except Exception as e:
        # If something goes wrong, at least return something useful
        print(f"   ⚠️ Cleaning failed, using fallback: {str(e)}")
        return str(html_content)[:5000]  # First 5000 chars as backup


def parse_with_llm(dom_content, parse_description):
    """
    🤖 The AI Oracle - Natural Language Information Extraction
    
    This is where the real magic happens! You describe what you want in plain English,
    and our AI reads through the content like a human would, picking out exactly what
    you asked for. No programming required!
    
    It's like having a super-smart research assistant who can instantly scan any
    document and extract specific information based on your instructions.
    
    Args:
        dom_content (str): The HTML content to parse
        parse_description (str): What you want to extract (in plain English)
    
    Returns:
        str: The extracted information, formatted nicely
    """
    try:
        # Show the user what we're working on
        description_preview = parse_description[:100] + "..." if len(parse_description) > 100 else parse_description
        print(f"🔍 AI is analyzing content for: '{description_preview}'")
        
        # First, clean up the content - remove HTML junk
        print("   🧹 Cleaning and preparing content...")
        cleaned_content = clean_dom_content(dom_content)
        
        # AI models have limits on how much text they can process at once
        # If the content is too long, we'll trim it (with a note)
        if len(cleaned_content) > 8000:
            print(f"   ✂️ Content is long ({len(cleaned_content)} chars), trimming to 8000 chars...")
            cleaned_content = cleaned_content[:8000] + "\n\n[Note: Content was truncated due to length]"
        
        # Build the AI prompt using our template
        print("   🛠️ Crafting AI prompt...")
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model  # This creates a processing pipeline
        
        # Send everything to the AI and wait for the magic to happen!
        print("   🤖 Sending to AI for analysis...")
        response = chain.invoke({
            "dom_content": cleaned_content,
            "parse_description": parse_description
        })
        
        # Clean up the AI's response
        result = response.strip() if response else ""
        
        # Give feedback on what we found
        if result:
            word_count = len(result.split())
            print(f"✅ AI extraction successful! Found {len(result)} characters ({word_count} words)")
        else:
            print("🤷 AI didn't find matching information")
        
        return result if result else "No matching information found."
        
    except Exception as e:
        # If something goes wrong, give a helpful error message
        print(f"❌ AI parsing failed: {str(e)}")
        print("   💡 This might be due to Ollama not running or model not available")
        return f"Error during parsing: {str(e)}"


def get_parsing_suggestions(dom_content):
    """
    💡 The Smart Suggestion Engine - AI-Powered Content Analysis
    
    Ever looked at a webpage and wondered "what can I extract from this?" This
    function is like having a data analyst scan the page and suggest all the
    interesting things you could pull out.
    
    It looks for patterns in the HTML and text to intelligently suggest what
    types of information are available. Much smarter than guessing!
    
    Args:
        dom_content (str): HTML content to analyze
    
    Returns:
        list: Smart suggestions for what you could extract
    """
    try:
        print("   🔍 Analyzing page structure for extraction opportunities...")
        soup = BeautifulSoup(dom_content, 'html.parser')
        suggestions = []
        
        # Look for different types of HTML elements and what they might contain
        print("   📊 Checking for structured content...")
        
        # Headings usually contain important topics/sections
        if soup.find_all('h1'):
            suggestions.append("Main headings and titles")
        
        # Paragraphs contain the main body content
        if soup.find_all('p'):
            suggestions.append("All paragraph text content")
        
        # Links are always interesting - they show connections and navigation
        if soup.find_all('a', href=True):
            suggestions.append("All links and URLs")
        
        # Images might have useful alt text or be part of galleries
        if soup.find_all('img'):
            suggestions.append("Image sources and alt text")
        
        # Lists often contain structured information
        if soup.find_all(['ul', 'ol']):
            suggestions.append("List items and bullet points")
        
        # Tables are goldmines of structured data
        if soup.find_all('table'):
            suggestions.append("Table data and structured information")
        
        # Forms tell us what kind of data the site collects
        if soup.find_all('form'):
            suggestions.append("Form fields and input elements")
        
        # Now let's get smart and look for patterns in the actual text content
        print("   🕵️ Scanning text for extractable patterns...")
        text_content = soup.get_text()
        
        # Email addresses - these are always valuable
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, text_content):
            suggestions.append("Email addresses")
        
        # Phone numbers in various formats
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        if re.search(phone_pattern, text_content):
            suggestions.append("Phone numbers")
        
        # Price information - always interesting for e-commerce sites
        price_patterns = [r'\$\d+', r'\d+\s*USD', r'Price:', r'Cost:']
        if any(re.search(pattern, text_content, re.IGNORECASE) for pattern in price_patterns):
            suggestions.append("Prices and pricing information")
        
        # Dates - useful for articles, events, etc.
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or DD/MM/YYYY
            r'\b\w+\s+\d{1,2},?\s+\d{4}\b'         # Month DD, YYYY
        ]
        if any(re.search(pattern, text_content) for pattern in date_patterns):
            suggestions.append("Dates and timestamps")
        
        print(f"   ✅ Found {len(suggestions)} potential extraction opportunities")
        
        # Return the top 8 most relevant suggestions
        return suggestions[:8]
        
    except Exception as e:
        # If our smart analysis fails, at least provide some generic useful suggestions
        print(f"   ⚠️ Smart analysis failed ({str(e)}), providing generic suggestions")
        return [
            "Main headings and titles",
            "All links and URLs", 
            "Contact information",
            "Product names and descriptions",
            "Prices and costs",
            "Email addresses and phone numbers"
        ]


# 📚 The Extraction Recipe Book - Pre-made Parsing Templates
# ================================================================
# 
# These are battle-tested extraction descriptions that work great for common use cases.
# Think of them as recipes - you could create your own, but why not use ones that
# are already perfected? Each description is carefully crafted to get the best
# results from the AI.
#
# Pro tip: Use these as starting points and modify them for your specific needs!

EXAMPLE_DESCRIPTIONS = {
    # Business and contact information - perfect for company websites
    "Contact Info": "Extract all email addresses, phone numbers, and contact information",
    
    # Navigation and linking - great for site structure analysis
    "Links": "Extract all links, URLs, and their anchor text",
    
    # Content structure - perfect for blogs and news sites
    "Headlines": "Extract all main headings, titles, and article headlines", 
    
    # E-commerce focused - ideal for shopping sites
    "Products": "Extract product names, descriptions, and prices",
    
    # Publishing and media - great for news sites and blogs
    "Articles": "Extract article titles, summaries, and publication dates",
    
    # Social media presence - find all social profiles
    "Social Media": "Extract social media links, usernames, and handles",
    
    # Media content - useful for galleries and media sites
    "Images": "Extract image URLs, alt text, and captions",
    
    # Event information - perfect for event listing sites
    "Events": "Extract event names, dates, locations, and descriptions",
    
    # Career and hiring - ideal for job boards
    "Jobs": "Extract job titles, companies, locations, and requirements",
    
    # Customer feedback - great for review sites and e-commerce
    "Reviews": "Extract customer reviews, ratings, and feedback"
}
        