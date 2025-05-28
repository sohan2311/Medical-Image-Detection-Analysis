# Medical Image Detection Analysis

# 🩺 Vital⚕️Image 🧑🏻‍⚕️ Analytics 🩻📊

**VitalImage Analytics** is a medical imaging analysis application powered by Google’s **Gemini Pro** and built using **Python** and **Streamlit**. It allows users to upload medical images (X-ray, MRI, CT, etc.) and receive structured AI-generated clinical analysis including abnormalities, recommendations, and potential next steps — all presented in clear clinical language.

---

## 🌐 Local Application Access

Once the app is running locally, access it via:

📍 **[http://localhost:8501](http://localhost:8501)**

---

## 🚀 Features

- 📷 Upload medical images in `.jpg` or `.png` format.
- 🧠 Automated medical image analysis powered by Gemini 1.5 Pro.
- 📄 Clinical-grade findings, severity analysis, and anatomical references.
- 🧾 Actionable next-step suggestions for diagnostics or treatment support.
- 🔒 Built-in safety settings to ensure ethical, reliable outputs.

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository


git clone https://github.com/your-username/vitalimage-analytics.git
cd vitalimage-analytics

2️⃣ Install Dependencies

Install the required Python packages using pip:
pip install streamlit google-generativeai

3️⃣ Add Your Gemini API Key

Create a file named api_key.py in the root directory and add:
api_key = "YOUR_GEMINI_API_KEY"
Get your key from https://makersuite.google.com/app

4️⃣ Run the App
streamlit run app.py
Access the application at http://localhost:8501
📁 Project Structure

VitalImageAnalytics/
├── app.py                      # Main Streamlit app
├── api_key.py                  # Stores Gemini API key
├── Vital Image Analysis.png    # App logo image
└── README.md                   # Project README

🤖 Model & Prompt Details

Model: gemini-1.5-pro-latest
Framework: Google Generative AI (google-generativeai)
Temperature: 0.4 (Balanced Creativity)
Max Output Tokens: 4096
Safety Filters: Enabled for harassment, hate, explicit, and dangerous content
System Prompt:
A structured instruction defining model behavior as a responsible medical image analyst trained in scikit-learn-based logic with AI-powered interpretation skills.

⚠️ API Limitations & Alternatives

Gemini’s free API quota may limit:
Number of tokens/day
Requests/minute
If you exceed quota, you’ll see an error like:
google.api_core.exceptions.ResourceExhausted: 429 You exceeded your current quota...


✅ Free Alternative: Hugging Face Transformers
Install:
pip install transformers torch torchvision
Replace image analysis logic with:
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

raw_image = Image.open(uploaded_file).convert('RGB')

inputs = processor(raw_image, return_tensors="pt")
out = model.generate(**inputs)
caption = processor.decode(out[0], skip_special_tokens=True)

st.success("Image Analysis:")
st.write(caption)
Model Link: https://huggingface.co/Salesforce/blip-image-captioning-base
🛡️ Disclaimer

“This is an AI-generated analysis. Please consult a licensed medical professional before making any health-related decisions.”
👨‍💻 Contributing

We welcome contributions! Here’s how to get started:
Fork this repository
Create a new branch (git checkout -b feature-branch)
Commit your changes (git commit -m 'Add new feature')
Push to the branch (git push origin feature-branch)
Open a Pull Request
📜 License

Licensed under the MIT License. See LICENSE for more details.
📬 Contact

For feedback, bugs, or enhancements, feel free to reach out:

Sohan Maity

📧 Email: [sohan.maity2311@gmail.com.com]
🔗 GitHub: [https://github.com/sohan2311]
