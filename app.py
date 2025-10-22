import streamlit as st
import google.generativeai as genai
import PyPDF2
import re
from fpdf import FPDF
import tempfile
import os
from pathlib import Path
from dotenv import load_dotenv
import unicodedata


# =====================================
# Load Secrets (Streamlit secrets > env vars > .env)
# =====================================
try:
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") if hasattr(st, "secrets") else None
    PROMPT = st.secrets.get("PROMPT") if hasattr(st, "secrets") else None
except Exception:
    GOOGLE_API_KEY = None
    PROMPT = None

# Fallback to environment variables
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not PROMPT:
    PROMPT = os.environ.get("PROMPT")

# Try loading a local .env file as a last resort
if (not GOOGLE_API_KEY or not PROMPT) and Path(".env").exists():
    load_dotenv()
    if not GOOGLE_API_KEY:
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not PROMPT:
        PROMPT = os.environ.get("PROMPT")

# Configure Google Gemini API only if key present
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception:
        # we'll handle API errors at call time
        pass


def _sanitize_for_pdf(s: str) -> str:
    """Return a PDF-safe (latin-1/ascii) string for FPDF.
    Replace common unicode punctuation with ASCII equivalents and
    strip characters that can't be encoded.
    """
    if not s:
        return ""
    # Common substitutions
    s = s.replace('\u2013', '-').replace('\u2014', '-')
    s = s.replace('\u2018', "'").replace('\u2019', "'")
    s = s.replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\u2026', '...')
    # Normalize to decompose accents etc.
    s = unicodedata.normalize('NFKD', s)
    # Try latin-1; if it fails, fall back to ASCII stripping
    try:
        s.encode('latin-1')
        return s
    except UnicodeEncodeError:
        return s.encode('ascii', 'ignore').decode('ascii')

# =====================================
# Streamlit Page Configuration
# =====================================
st.set_page_config(
    page_title="Automated Resume & Job Matcher",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# Custom CSS Styling
# =====================================
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #2b7cff;
        text-align: center;
        font-weight: bold;
    }
    .stTextArea textarea {
        font-size: 15px !important;
    }
    .upload-box {
        border: 2px dashed #2b7cff;
        border-radius: 10px;
        padding: 20px;
        background-color: #ffffff;
    }
    .result-box {
        border: 1px solid #2b7cff;
        border-radius: 8px;
        padding: 20px;
        background-color: #ffffff;
        color: #000000 !important;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    .stProgress > div > div > div {
        background-color: #2b7cff;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# Page Header
# =====================================
st.title("🤖 Automated Resume & Job Description Matcher")
st.write("Upload your **resume** and paste a **job description** below to analyze how well they match using Google Gemini AI.")

# =====================================
# Layout: Two Columns
# =====================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader(
        "Upload a Resume (PDF or TXT)",
        type=["pdf", "txt"],
        help="Upload your resume file here."
    )

with col2:
    st.subheader("🧾 Job Description")
    job_description = st.text_area(
        "Paste the Job Description",
        height=260,
        placeholder="Paste the job description here..."
    )

# =====================================
# Process Button
# =====================================
if st.button("🔍 Analyze Match", use_container_width=True):
    if not resume_file or not job_description.strip():
        st.error("⚠️ Please upload a resume and enter a job description.")
    else:
        try:
            if not GOOGLE_API_KEY:
                st.error("⚠️ No Google API key found. Add `GOOGLE_API_KEY` to Streamlit secrets or set it as an environment variable. See the README for details.")
                st.stop()

            # Extract resume text
            resume_text = ""
            if resume_file.name.endswith(".txt"):
                resume_text = resume_file.read().decode("utf-8")
            elif resume_file.name.endswith(".pdf"):
                pdf_reader = PyPDF2.PdfReader(resume_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text

            with st.spinner("🤔 Analyzing the resume and job description..."):
                full_prompt = f"""
{PROMPT}

--- Resume ---
{resume_text}

--- Job Description ---
{job_description}
"""

                # Use the latest Gemini model
                try:
                    model = genai.GenerativeModel("models/gemini-2.5-flash")
                    response = model.generate_content(full_prompt)
                except Exception as api_e:
                    st.error(f"🚨 Error calling Google Generative API: {api_e}")
                    st.stop()

            # =====================================
            # Display Results
            # =====================================
            st.success("✅ Analysis Complete!")
            st.markdown("### 🧩 Detailed Analysis")
            # response may have different shapes depending on the SDK; try common attributes
            ai_text = getattr(response, "text", None) or getattr(response, "output", None) or str(response)
            st.markdown(f"<div class='result-box'>{ai_text}</div>", unsafe_allow_html=True)

            # Optional: Extract match percentage (if AI provides it)
            match = re.search(r"(\d{1,3})\s*%", ai_text)
            score = min(int(match.group(1)), 100) if match else None

            if score:
                st.markdown("### 📊 Match Score")
                st.progress(score / 100)
                st.write(f"**Match Percentage:** {score}%")

            # =====================================
            # Download Report Section
            # =====================================
            st.markdown("### 📥 Download Report")

            # Generate a PDF file of the analysis
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Resume & Job Match Report", ln=True, align="C")

            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=_sanitize_for_pdf(f"Match Percentage: {score if score else 'N/A'}%"))
            pdf.ln(5)
            pdf.multi_cell(0, 10, txt=_sanitize_for_pdf(ai_text))

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                pdf.output(tmp.name)
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Analysis Report (PDF)",
                    data=f,
                    file_name="Resume_Analysis_Report.pdf",
                    mime="application/pdf",
                )

            # Clean up temporary file after download
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        except Exception as e:
            st.error(f"🚨 An error occurred: {e}")
