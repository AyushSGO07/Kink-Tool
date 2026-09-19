import json
import requests
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
import urllib.parse
from langchain_core.prompts import load_prompt

load_dotenv()


st.set_page_config(page_title="Star Matcher", page_icon="☀️", layout="wide")

# Helper function to get image from Wikipedia
@st.cache_data
def get_image_url(name):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(name)}&prop=pageimages&format=json&pithumbsize=500"
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            if 'thumbnail' in page_info:
                return page_info['thumbnail']['source']
    except Exception:
        pass
    # Fallback avatar
    return f"https://ui-avatars.com/api/?name={urllib.parse.quote(name)}&background=random&color=fff&size=500&font-size=0.33"

# Custom CSS for Premium Glassmorphism & Typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide standard Streamlit header/footer for a cleaner app feel */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Animated Dynamic Fractal-like Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #6a1939, #a03c30, #24243e);
        background-size: 400% 400%;
        animation: gradientBG 24s ease infinite;
        background-attachment: fixed;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Vertical Centering & Zoom-in effect */
    /* Streamlit's main app container */ho
    .appview-container > section:first-child {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 100vh;
    }

    /* Remove Streamlit's aggressive default padding */
    .css-18e3th9 {
        padding-top: 0rem !important;
    }

    /* Glassmorphic Main Container */
    .block-container {
        max-width: 1000px !important;
        background: rgba(12, 8, 20, 0.25) !important;
        backdrop-filter: blur(40px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(160%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 40px 80px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        border-radius: 36px !important;
        padding: 55px 65px !important;
        margin: auto !important;
    }
    
    @media (max-width: 768px) {
        .block-container {
            padding: 35px 25px !important;
            border-radius: 26px !important;
        }
    }

    /* Hero Heading Section */
    .hero-container {
        text-align: center;
        margin-bottom: 50px;
    }
    
    .hero-title {
        font-weight: 800;
        font-size: 3.6rem !important;
        letter-spacing: -1.2px;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #ffffff 0%, #e0d0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 30px rgba(255, 255, 255, 0.1);
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 300;
        letter-spacing: 0.4px;
    }

    /* Form Fields Styling */
    .stSelectbox label p {
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.5) !important;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    /* Dropdown Input Glass */
    .stSelectbox > div[data-baseweb="select"] {
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px;
        transition: all 0.3s ease;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
        padding: 4px;
    }
    
    .stSelectbox > div[data-baseweb="select"]:hover {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }

    .stSelectbox > div[data-baseweb="select"] * {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Premium Handcrafted Glass Button */
    .stButton>button {
        background: rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: rgba(255, 255, 255, 0.95) !important;
        padding: 18px 32px;
        font-size: 1.3rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        margin-top: 40px;
    }
    
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-2px);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .stButton>button:active {
        transform: translateY(1px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    /* Section Headings */
    .section-title {
        font-weight: 400;
        font-size: 1.6rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 60px;
        margin-bottom: 40px;
    }

    /* Premium Handcrafted Profile Match Card */
    .star-card {
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        border-radius: 36px;
        padding: 50px 45px;
        margin-bottom: 45px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }
    
    .star-card:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.02);
        box-shadow: 0 30px 70px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    /* Elegant Image Treatment */
    .star-image {
        width: 160px;
        height: 160px;
        object-fit: cover;
        border-radius: 50%;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        padding: 4px;
        background: rgba(255, 255, 255, 0.02);
    }
    
    .star-card:hover .star-image {
        transform: scale(1.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    }
    
    .star-name {
        color: rgba(255, 255, 255, 0.95);
        font-size: 2.3rem;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin-bottom: 14px;
    }
    
    .star-reason {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.65);
        margin-bottom: 30px;
        line-height: 1.7;
        font-weight: 300;
        max-width: 85%;
    }
    
    .star-attributes-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin-bottom: 35px;
    }
    
    /* Subdued Glass Chips */
    .star-attribute {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 8px 18px;
        border-radius: 999px;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
    }
    
    .star-card:hover .star-attribute {
        background: rgba(255, 255, 255, 0.08);
        color: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .search-btn {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.85) !important;
        text-decoration: none;
        padding: 12px 30px;
        border-radius: 999px;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        backdrop-filter: blur(10px);
    }
    
    .search-btn:hover {
        background: rgba(255, 255, 255, 0.15);
        color: #fff !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Kink Tool</div>
    <div class="hero-subtitle">☀️ Find Your Perfect Star Match</div>
</div>
""", unsafe_allow_html=True)

# Form Section
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        sexuality = st.selectbox("Select your Sexuality", ['Straight', 'Gay', 'Lesbian', 'Bi-Sexual', 'Yeahh Kinda That'])
    with col2:
        age = st.selectbox('Select age of your Star', ['18-25', '25-30', '30-40', '40+'])
    
    body_features = st.selectbox('Your Preference', ['Thick Thighs', 'Big Ass', 'Big Boobs', 'Petite', 'Athletic', 'Curvy', 'Blonde', 'Brunette', 'Redhead'])

model = GoogleGenerativeAI(
    model="gemini-3.6-flash",
    max_retries=5
)
# Use a relative path so it works in deployment environments
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(current_dir, 'prompt.json')
template = load_prompt(prompt_path)

if st.button('✨ Find My Match ✨'):
    with st.spinner("Analyzing preferences and searching for the perfect matches..."):
        try:
            chain = template | model 
            results = chain.invoke({
                'sexuality': sexuality, 
                'age': age, 
                'body_features': body_features
            })
            
            clean_results = results.replace("```json", "").replace("```", "").strip()
            
            try:
                stars = json.loads(clean_results)
                
                st.markdown("<div class='section-title'>Top Matches</div>", unsafe_allow_html=True)
                
                # We can use columns to make it look even better on wide screens
                # For 3 matches, let's just stack them for consistent elegant vertical rhythm
                for star in stars:
                    name = star.get("name", "Unknown Star")
                    reason = star.get("match_reason", "")
                    attributes = star.get("attributes", [])
                    
                    search_query = urllib.parse.quote(name)
                    search_url = f"https://www.google.com/search?tbm=isch&q={search_query}"
                    image_url = get_image_url(name)
                    
                    attr_html = "".join([f"<span class='star-attribute'>{attr}</span>" for attr in attributes])
                    
                    st.markdown(f"""
                    <div class="star-card">
                        <img src="{image_url}" class="star-image" alt="{name}">
                        <div class="star-name">{name}</div>
                        <div class="star-reason">{reason}</div>
                        <div class="star-attributes-container">{attr_html}</div>
                        <a href="{search_url}" target="_blank" class="search-btn">🔍 View More Images</a>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except json.JSONDecodeError:
                st.error("Could not parse the results. Please try again.")
                st.code(results)
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "exhausted" in error_msg or "quota" in error_msg:
                st.error("⚠️ **API Quota Exhausted!** You have hit the rate limit for the Gemini API. Please wait a minute before trying again, or check your API billing limits in Google AI Studio.")
            else:
                st.error(f"An error occurred: {e}")

import time

def generate_with_retry(model, prompt, retries=4):
    for attempt in range(retries):
        try:
            return model.generate_content(prompt)

        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                wait = 2 ** attempt
                print(f"Gemini busy. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise

    raise Exception("Gemini is temporarily unavailable. Please try again later.")
