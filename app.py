
import streamlit as st
from pathlib import Path
import requests
import base64
import json
from io import BytesIO
from PIL import Image


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


st.set_page_config(page_title="Vital_Image Analytics", page_icon="🩺")

# Display logo (uncomment and update path if you have the logo file)
# st.image("/Users/sohanmaity/Desktop/Programming/Project/Medical Image Detection App/Vital Image Analysis.png", width=150)


st.title("🩺 Vital⚕️Image 🧑🏻‍⚕️ Analytics 🩻📊")


st.subheader("An Application that can help users to identify medical images")


st.info("🤖 Powered by Together AI's Llama Vision model for advanced medical image analysis")


uploaded_file = st.file_uploader(
    "Upload a medical image file for Analysis", 
    type=["jpg", "png", "jpeg"],
    help="Supported formats: JPG, PNG, JPEG"
)


submit_button = st.button("🔍 Generate the Analysis", type="primary")


if submit_button:
    if uploaded_file is not None:
        # Display the uploaded image
        st.subheader("📷 Uploaded Medical Image")
        st.image(uploaded_file, caption="Medical Image for Analysis", use_column_width=True)
        
        # Show loading spinner while processing
        with st.spinner("🔄 Analyzing medical image... Please wait."):
            try:
                # Process the uploaded image
                image_data = uploaded_file.getvalue()
                
                # Generate analysis using Together AI
                analysis_result = analyze_medical_image(image_data, system_prompt)
                
                # Display the results
                st.subheader("📋 Medical Image Analysis Results")
                
                # Create an expandable section for the full analysis
                with st.expander("📊 Detailed Analysis Report", expanded=True):
                    st.write(analysis_result)
                
                # Success message
                st.success("✅ Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"❌ An error occurred during analysis: {str(e)}")
                
        # Important medical disclaimer
        st.warning("""
        ⚠️ **IMPORTANT MEDICAL DISCLAIMER**: 
        
        This is an AI-generated analysis for educational and supportive purposes only. 
        This tool is NOT a substitute for professional medical diagnosis or treatment. 
        Always consult with a qualified healthcare professional for medical diagnosis, 
        treatment decisions, and medical advice.
        """)
        
    else:
        st.error("❌ Please upload a medical image file before generating analysis.")
        st.info("💡 **Tip**: Click on 'Browse files' above to select a medical image (X-ray, CT, MRI, etc.)")

# Sidebar with additional information
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. **Upload Image**: Click 'Browse files' to select a medical image
    2. **Generate Analysis**: Click the 'Generate the Analysis' button
    3. **Review Results**: Read the AI-generated analysis report
    4. **Consult Professional**: Always verify findings with a medical professional
    """)
    
    st.header("📋 Supported Image Types")
    st.markdown("""
    - X-rays
    - CT Scans
    - MRI Images
    - Ultrasound Images
    - Other medical imaging formats
    """)
    
    st.header("⚠️ Important Notes")
    st.markdown("""
    - This tool is for educational purposes only
    - Always consult healthcare professionals
    - AI analysis should not replace medical expertise
    - Ensure image quality is adequate for analysis
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Vital_Image Analytics</strong> - Powered by Together AI</p>
    <p><em>Supporting healthcare professionals with AI-powered medical image analysis</em></p>
</div>
""", unsafe_allow_html=True)


if st.checkbox("🔧 Show API Configuration (Debug)"):
    st.json({
        "API Endpoint": TOGETHER_API_URL,
        "Model": MODEL_NAME,
        "API Key Status": "✅ Loaded" if api_key else "❌ Not Found"
    })