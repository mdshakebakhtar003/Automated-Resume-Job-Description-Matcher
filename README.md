# 📄 Automated Resume & JD Matcher

<<<<<<< HEAD
### Demo Video : https://www.youtube.com/watch?v=syFheQFF1Jg&t=4s
[![Watch Demo Video](http://img.youtube.com/vi/syFheQFF1Jg/0.jpg)](https://www.youtube.com/watch?v=syFheQFF1Jg&t=4s)

  
=======
>>>>>>> e9dfee2 (Prepare for Streamlit deployment)
🚀 A powerful AI-powered ATS Resume Analyzer that compares your resume against a job description and provides a structured analysis with match percentage, skill gaps, and improvement suggestions.

## 🌟 Features
✅ Upload PDF resumes  
✅ Compare with Job Descriptions  
✅ AI-powered Analysis (Match %, Skills, Courses)  
✅ Simple & Minimal UI like Gemini  
✅ Powered by Google Gemini API  

## 🔥 Live Demo  
[🔗 Check it out on Streamlit]

<<<<<<< HEAD
## 🛠 Tech Stack  
- **Frontend**: Streamlit  
- **AI Model**: Google Gemini  
- **Backend**: Python  
- **PDF Parsing**: PyMuPDF  
- **Deployment**: Streamlit Cloud  

## 🚀 Installation & Setup  
1. Clone the repo  
   ```bash
   git clone https://github.com/yourusername/resumeanalyzer.git
   cd resumeanalyzer
2. Install Dependencies
   ```bash
   pip install -r requirements.txt
3. Create a .env file and add
   ```bash
   GOOGLE_API_KEY=your_api_key_here
4. Run locally
   ```bash
   streamlit run app.py




## 🔗 Credits & Acknowledgment
This project utilizes Google Gemini API for resume analysis and job description comparison.
Special thanks to Google AI for providing powerful LLM capabilities.
=======
# � Automated Resume & JD Matcher

🚀 A lightweight Streamlit app that compares a resume to a job description using Google Gemini (Generative AI) and returns a structured analysis with a match percentage, strengths, gaps, and suggestions.

## 🌟 Features
- Upload PDF or TXT resumes
- Paste a Job Description to compare
- AI-powered Analysis (match %, skills, suggested improvements)

## 🛠 Tech Stack
- Frontend: Streamlit
- AI Model: Google Gemini (via google-generativeai)
- PDF Parsing: PyPDF2

## 🚀 Quick Start (Local)
1. Clone the repo
   ```powershell
   git clone https://github.com/yourusername/resumeanalyzer.git
   cd resumeanalyzer
   ```
2. Install dependencies
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure your Google API key
   - Option A (recommended for Streamlit Cloud): copy `.streamlit/secrets-template.toml` to `.streamlit/secrets.toml` and add your `GOOGLE_API_KEY` and optional `PROMPT`.
   - Option B (local): create a `.env` file with:
     ```text
     GOOGLE_API_KEY=your_api_key_here
     PROMPT="Provide a structured analysis comparing the resume to the job description..."
     ```
4. Run the app locally
   ```powershell
   streamlit run app.py
   ```

## ☁️ Deploy to Streamlit Cloud
1. Push this repo to GitHub.
2. On share.streamlit.io, create a new app and connect your GitHub repository.
3. In the Streamlit app settings, add a secret named `GOOGLE_API_KEY` (or upload a `.streamlit/secrets.toml` containing it).
4. Set the main file to `app.py` and deploy.

Note: Keep your API keys secret. Do not commit real keys to the repository.

## Credits
This project uses Google Gemini via the `google-generativeai` Python package.
>>>>>>> e9dfee2 (Prepare for Streamlit deployment)



