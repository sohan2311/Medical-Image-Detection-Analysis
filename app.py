import streamlit as st
from pathlib import Path
import requests
import base64
import json
from io import BytesIO
from PIL import Image
import time

from api_key import api_key

TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL_NAME = "meta-llama/Llama-Vision-Free"

def encode_image_to_base64(image_data):
    """Convert image data to base64 string"""
    return base64.b64encode(image_data).decode('utf-8')

def analyze_medical_image(image_data, system_prompt):
    """Send image to Together AI for analysis"""
    base64_image = encode_image_to_base64(image_data)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please analyze this medical image according to your system instructions. Provide a detailed medical analysis including findings, recommendations, and next steps."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.4,
        "top_p": 1.0,
        "max_tokens": 4096,
        "stream": False
    }
    
    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    
    except requests.exceptions.RequestException as e:
        return f"❌ Error calling Together AI API: {str(e)}"
    except KeyError as e:
        return f"❌ Error parsing API response: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

def display_typing_effect(text, container, typing_speed=0.03):
    """Display text with typing effect and blinking cursor"""
    cursor_html = """
    <style>
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    .typing-cursor {
        animation: blink 1s infinite;
        font-weight: bold;
        color: #667eea;
    }
    </style>
    """
    

    words = text.split(' ')
    displayed_text = ""
    
    for i, word in enumerate(words):
        displayed_text += word
        if i < len(words) - 1:
            displayed_text += " "
        

        html_content = f"""
        {cursor_html}
        <div style="background: linear-gradient(135deg, #252538 0%, #2a2a42 100%); 
                   padding: 1.5rem; border-radius: 10px; 
                   border: 1px solid rgba(102, 126, 234, 0.3);
                   color: #e0e6ed; line-height: 1.6;">
            {displayed_text.replace('\n', '<br>')}<span class="typing-cursor">|</span>
        </div>
        """
        
        container.markdown(html_content, unsafe_allow_html=True)
        time.sleep(typing_speed)
    

    final_html = f"""
    <div style="background: linear-gradient(135deg, #252538 0%, #2a2a42 100%); 
               padding: 1.5rem; border-radius: 10px; 
               border: 1px solid rgba(102, 126, 234, 0.3);
               color: #e0e6ed; line-height: 1.6;">
        {text.replace('\n', '<br>')}
    </div>
    """
    container.markdown(final_html, unsafe_allow_html=True)

system_prompt = """
System Prompt for AI Medical Image Analyst Model:

As a highly skilled and responsible AI system trained in advanced medical imaging analysis, your primary task is to support clinical professionals by accurately analyzing medical images and generating structured, insightful, and actionable outputs.

Your Core Responsibilities:

1. Detailed Image Analysis:
Analyze the uploaded medical image (e.g., X-ray, CT, MRI, ultrasound) for structural, functional, or pathological abnormalities.
Focus on detecting early signs of disease, unusual patterns, or irregular features.

2. Findings Report:
Document all anomalies or areas of concern in clear clinical terminology.
Include measurements, severity grading (if applicable), and anatomical references.

3. Recommendations & Next Steps:
Suggest evidence-based next steps such as further diagnostics, clinical referrals, or monitoring strategies.
Provide risk assessments when relevant.

4. Treatment Suggestions (if appropriate and within scope):
Offer non-prescriptive suggestions that can assist the physician, such as therapy options or supportive care, aligned with standard clinical guidelines.

Important Notes:
1. Scope of Response: Limit your analysis strictly to human health-related medical images.

2. Clarity of Image: If the image quality is inadequate for reliable interpretation, clearly state this and explain the limitation.

3. Uncertainty Acknowledgment: If predictions or insights are probabilistic, express confidence levels (e.g., "High likelihood of...", "Low certainty due to noise in the image...").

4. Clinical Disclaimer:
Always end your analysis with: "This is an AI-generated analysis. Please consult a licensed medical professional before making any health-related decisions."
"""

st.set_page_config(
    page_title="Vital Image Analytics", 
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e6ed;
    }
    
    /* Streamlit default text color override */
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
        color: #e0e6ed !important;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    .ai-badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Upload section styling */
    .upload-section {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 30px rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    .upload-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e0e6ed;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Results section styling */
    .results-section {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 30px rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    .results-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e0e6ed;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Processing animation styles */
    .processing-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 30px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .processing-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    
    .spinner {
        display: inline-block;
        animation: spin 2s linear infinite;
        font-size: 1.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Typing cursor animation */
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    .typing-cursor {
        animation: blink 1s infinite;
        font-weight: bold;
        color: #667eea;
        font-size: 1.2em;
    }
    
    /* Typing container */
    .typing-container {
        background: linear-gradient(135deg, #252538 0%, #2a2a42 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #e0e6ed;
        line-height: 1.6;
        min-height: 100px;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.3), 0 0 20px rgba(102, 126, 234, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e0e6ed;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #7289ea 0%, #8659c2 100%);
    }
    
    /* Warning and info boxes */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.2);
        background: linear-gradient(135deg, #2d2d42 0%, #3a3a54 100%) !important;
        color: #e0e6ed !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: linear-gradient(135deg, #252538 0%, #2a2a42 100%);
        border: 2px dashed rgba(102, 126, 234, 0.5);
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #2a2a46 0%, #2f2f4a 100%);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        border-radius: 15px;
        margin-top: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Image display styling */
    .stImage > img {
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #252538 0%, #2a2a42 100%) !important;
        border-radius: 10px;
        font-weight: 600;
        color: #e0e6ed !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Select box and input styling */
    .stSelectbox > div > div, .stTextInput > div > div {
        background: linear-gradient(135deg, #252538 0%, #2a2a42 100%) !important;
        color: #e0e6ed !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: #e0e6ed !important;
    }
    
    /* Sidebar background */
    .css-1d391kg, .css-1cypcdb {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%) !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #1d4e5a 0%, #2d5a4a 100%) !important;
        color: #a8e6cf !important;
        border: 1px solid rgba(168, 230, 207, 0.3) !important;
    }
    
    /* Error message styling */
    .stError {
        background: linear-gradient(135deg, #5a1d1d 0%, #4a2d2d 100%) !important;
        color: #ffb3b3 !important;
        border: 1px solid rgba(255, 179, 179, 0.3) !important;
    }
    
    /* Warning message styling */
    .stWarning {
        background: linear-gradient(135deg, #5a4d1d 0%, #4a3d2d 100%) !important;
        color: #ffdb99 !important;
        border: 1px solid rgba(255, 219, 153, 0.3) !important;
    }
    
    /* Info message styling */
    .stInfo {
        background: linear-gradient(135deg, #1d3d5a 0%, #2d3a4a 100%) !important;
        color: #a8d8ea !important;
        border: 1px solid rgba(168, 216, 234, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="main-title">🩺 Vital Image Analytics 📊</div>
    <div class="main-subtitle">Advanced AI-Powered Medical Image Analysis</div>
    <div class="ai-badge">🤖 Powered by Together AI's Llama Vision</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="upload-section">
        <div class="upload-title">📁 Upload Medical Image</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Select a medical image for analysis",
        type=["jpg", "png", "jpeg"],
        help="Supported formats: JPG, PNG, JPEG • Max file size: 200MB",
        label_visibility="collapsed"
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        submit_button = st.button("🔍 Analyze Image", type="primary", use_container_width=True)

with col2:
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">📋 Quick Guide</div>
        <p style="font-size: 0.9rem; color: #b8c5d1; line-height: 1.5;">
            1. Upload a medical image (X-ray, CT, MRI, etc.)<br>
            2. Click "Analyze Image" to start processing<br>
            3. Review the AI-generated analysis<br>
            4. Consult with a medical professional
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">🏥 Supported Images</div>
        <p style="font-size: 0.9rem; color: #b8c5d1; line-height: 1.5;">
            • X-rays & Radiographs<br>
            • CT Scans<br>
            • MRI Images<br>
            • Ultrasound Images<br>
            • Other medical imaging
        </p>
    </div>
    """, unsafe_allow_html=True)

if submit_button:
    if uploaded_file is not None:
        st.markdown("""
        <div class="results-section">
            <div class="results-title">🩻 Uploaded Image</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_img1, col_img2, col_img3 = st.columns([1, 3, 1])
        with col_img2:
            st.image(uploaded_file, caption="Medical Image for Analysis", use_column_width=True)
        
        st.markdown("""
        <div class="processing-section">
            <div class="processing-title">
                <span class="spinner">🔄</span>
                Processing Analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:

            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 Analyzing image structure...")
                elif i < 60:
                    status_text.text("🧠 Running AI analysis...")
                elif i < 90:
                    status_text.text("📊 Generating report...")
                else:
                    status_text.text("✅ Analysis complete!")
                
                time.sleep(0.02)
            
            progress_bar.empty()
            status_text.empty()
            

            image_data = uploaded_file.getvalue()
            analysis_result = analyze_medical_image(image_data, system_prompt)
            

            st.markdown("""
            <div class="results-section">
                <div class="results-title">📋 Analysis Results</div>
            </div>
            """, unsafe_allow_html=True)
            

            st.markdown("### 🤖 AI Analysis in Progress...")
            typing_container = st.empty()
            

            display_typing_effect(analysis_result, typing_container, typing_speed=0.02)
            

            with st.sidebar:
                st.markdown("""
                <div class="sidebar-section">
                    <div class="sidebar-title">⚙️ Typing Settings</div>
                </div>
                """, unsafe_allow_html=True)
                
                typing_speed = st.slider(
                    "Typing Speed", 
                    min_value=0.01, 
                    max_value=0.1, 
                    value=0.02, 
                    step=0.01,
                    help="Adjust how fast the AI types the response"
                )
            
            st.success("✅ Analysis completed successfully! The AI has finished typing the response.")
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
        

        st.markdown("""
        <div style="background: linear-gradient(135deg, #5a1d1d 0%, #4a2d2d 100%); 
                    padding: 1.5rem; border-radius: 15px; margin-top: 2rem;
                    border: 1px solid rgba(255, 179, 179, 0.3);
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
            <h4 style="color: #ffb3b3; margin-bottom: 1rem;">⚠️ Important Medical Disclaimer</h4>
            <p style="color: #ffcccc; margin-bottom: 0; line-height: 1.6;">
                This AI analysis is for educational and supportive purposes only. It is <strong>NOT</strong> 
                a substitute for professional medical diagnosis or treatment. Always consult with a 
                qualified healthcare professional for medical diagnosis, treatment decisions, and medical advice.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #5a4d1d 0%, #4a3d2d 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center;
                    border: 1px solid rgba(255, 219, 153, 0.3);
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
            <h4 style="color: #ffdb99; margin-bottom: 1rem;">📤 No Image Selected</h4>
            <p style="color: #ffdb99; margin-bottom: 0;">
                Please upload a medical image file before starting the analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">🔧 System Status</div>
    </div>
    """, unsafe_allow_html=True)
    
    api_status = "🟢 Connected" if api_key else "🔴 Disconnected"
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #252538 0%, #2a2a42 100%); 
               padding: 1rem; border-radius: 8px; margin-bottom: 1rem;
               border: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="margin: 0; font-size: 0.9rem; color: #e0e6ed;">
            <strong>API Status:</strong> {api_status}<br>
            <strong>Model:</strong> {MODEL_NAME.split('/')[-1]}<br>
            <strong>Provider:</strong> Together AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">📚 Resources</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #252538 0%, #2a2a42 100%); 
               padding: 1rem; border-radius: 8px; margin-bottom: 1rem;
               border: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="margin: 0; font-size: 0.9rem; line-height: 1.5;">
            • <a href="#" style="color: #8db4ff; text-decoration: none;">Medical Image Guidelines</a><br>
            • <a href="#" style="color: #8db4ff; text-decoration: none;">AI Analysis Accuracy</a><br>
            • <a href="#" style="color: #8db4ff; text-decoration: none;">Privacy & Security</a><br>
            • <a href="#" style="color: #8db4ff; text-decoration: none;">User Manual</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.checkbox("🔧 Show Debug Info"):
        st.json({
            "API Endpoint": TOGETHER_API_URL,
            "Model": MODEL_NAME,
            "API Key Status": "✅ Loaded" if api_key else "❌ Not Found"
        })


st.markdown("""
<div class="footer">
    <h4 style="color: #e0e6ed; margin-bottom: 1rem;">Vital Image Analytics</h4>
    <p style="color: #b8c5d1; margin-bottom: 0.5rem;">
        Empowering healthcare professionals with AI-powered medical image analysis
    </p>
    <p style="color: #9aa5b1; font-size: 0.9rem; margin-bottom: 0;">
        Built with ❤️ using Streamlit & Together AI • Version 1.0 • <a href="https://www.linkedin.com/in/sohan-maity-26881a288/" target="_blank">Sohan Maity</a> •
        <a href="https://github.com/sohan2311/Medical-Image-Detection-Analysis/tree/main" target="_blank">View Source Code in GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)
