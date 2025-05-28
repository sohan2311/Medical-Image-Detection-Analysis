#import necessary modules

import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

#configure gen_ai with the api key

genai.configure(api_key=api_key)

#set up the model

generation_config = {
    "temperature" : 0.4,
    "top_p" : 1,
    "top_k" : 32,
    "max_output_tokens" : 4096,
    
}

# apply safety settings

from google.generativeai.types import HarmCategory, HarmBlockThreshold

safety_settings = [
    {
        "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
        "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    },
    {
        "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    },
    {
        "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    },
    {
        "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    }
]



system_prompt = """
System Prompt for AI Medical Image Analyst Model :

As a highly skilled and responsible AI system trained in advanced medical imaging analysis using scikit-learn and powered by Gemini Pro, your primary task is to support clinical professionals by accurately analyzing medical images and generating structured, insightful, and actionable outputs.

Your Core Responsibilities:

1.Detailed Image Analysis :
Analyze the uploaded medical image (e.g., X-ray, CT, MRI, ultrasound) for structural, functional, or pathological abnormalities.
Focus on detecting early signs of disease, unusual patterns, or irregular features.

2.Findings Report :
Document all anomalies or areas of concern in clear clinical terminology.
Include measurements, severity grading (if applicable), and anatomical references.

3.Recommendations & Next Steps :
Suggest evidence-based next steps such as further diagnostics, clinical referrals, or monitoring strategies.
Provide risk assessments when relevant.

4.Treatment Suggestions (if appropriate and within scope) :
Offer non-prescriptive suggestions that can assist the physician, such as therapy options or supportive care, aligned with standard clinical guidelines.

Important Notes:
1.Scope of Response: Limit your analysis strictly to human health-related medical images.

2.Clarity of Image: If the image quality is inadequate for reliable interpretation, clearly state this and explain the limitation.
Uncertainty Acknowledgment: If predictions or insights are probabilistic, express confidence levels (e.g., “High likelihood of...”, “Low certainty due to noise in the image…”).

3.Clinical Disclaimer:
“This is an AI-generated analysis. Please consult a licensed medical professional before making any health-related decisions.”


"""
# model configuration

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",  # Use latest stable model name
    generation_config=generation_config,
    safety_settings=safety_settings
)





#set the page configuration

st.set_page_config(page_title="VitalImage Analytics" , page_icon = ":robot:")

#set the logo

st.image ("/Users/sohanmaity/Desktop/Programming/Project/Medical Image Detection App/Vital Image Analysis.png" , width = 150)
st.title ("🩺 Vital⚕️Image 🧑🏻‍⚕️ Analytics 🩻📊")

#set the subtitle

st.subheader("An Application that can help users to identify medical images")
uploaded_file = st.file_uploader("Upload a medical image file for Analysis", type=["jpg", "png"])
                                 
submit_button = st.button ("Generate the Analysis")

if submit_button:
    
    #process the uploaded image
    image_data=uploaded_file.getvalue()
    
    
    #making our image ready
    image_parts = [
        {
            "mime_type" : "image/jpeg",
            "data" : image_data
        },   
    ]
    
    #making our prompt ready
    prompt_parts = [
        "Describe what the people are doing in this image:\n",
        image_parts[0],
        system_prompt,    
    ]
    
    #generate a response based on prompt and image
    response = model.generate_content(prompt_parts)
    print(response.text)
    
    
    




