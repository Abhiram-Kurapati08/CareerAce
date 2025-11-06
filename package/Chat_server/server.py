from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import logging
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = OllamaLLM(model="llama3.2:latest")

# Templates
summarization_template = """
You are an AI assistant. Summarize user details into:
1. Skills
2. Experience
3. Interests
4. Goals

User Details:
Skills: {skills}
Experience: {experience}
Interests: {interests}
Goals: {goals}
"""

advice_template = """
You are an AI assistant specializing in career guidance.

Based on the user's profile below, please provide detailed recommendations with clear spacing and formatting:

User Information:
Skills: {skills}
Experience: {experience}
Interests: {interests}
Goals: {goals}

Please structure your response as follows:

1. Career Path Recommendations
   • Provide 2-3 specific career paths
   • Include rationale for each recommendation
   • List potential job titles

2. Recommended Companies
   • List 3-5 specific companies to target
   • Explain why each company is a good fit
   • Include both large companies and emerging startups

3. Skills to Develop
   • List technical skills needed
   • List soft skills to improve
   • Prioritize skills by importance

4. Growth Strategies
   • Outline specific action items
   • Include networking suggestions
   • Recommend relevant certifications
"""

extraction_template = """
You are an AI assistant specializing in resume analysis.
Extract and list relevant skills and experiences strictly as:

Skills:
<list of skills>

Experiences:
<list of experiences>

Resume Text:
{resume_text}
"""

roadmap_template = """
You are an AI assistant creating a detailed career development roadmap.

User Information:
Skills: {skills}
Experience: {experience}
Interests: {interests}
Goals: {goals}

Please create a detailed roadmap with the following structure:

Immediate Steps (0-3 months):
- [List specific actions]
- [Include skill development goals]
- [Specify measurable outcomes]

Short-term Goals (3-6 months):
- [List key milestones]
- [Include learning objectives]
- [Specify networking goals]

Medium-term Goals (6-12 months):
- [Detail career progression steps]
- [Include advanced skill development]
- [List industry certifications]

Long-term Vision (1-2 years):
- [Outline career achievements]
- [Detail position transitions]
- [Include leadership development]

For each timeframe, include:
- Specific action items
- Required resources
- Success metrics
"""


summarization_prompt = ChatPromptTemplate.from_template(summarization_template)
advice_prompt = ChatPromptTemplate.from_template(advice_template)
extraction_prompt = ChatPromptTemplate.from_template(extraction_template)
roadmap_prompt = ChatPromptTemplate.from_template(roadmap_template)

user_data = {}

@app.route("/check", methods=["GET"])
def health_check():
    logging.debug("Health check: serving")
    return jsonify({"status": "serving"})

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"response": "No file part."})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"response": "No selected file."})
    if file and file.filename.endswith(".pdf"):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        resume_text = extract_text_from_pdf(file_path)
        if resume_text:
            response = model.invoke(extraction_prompt.format(resume_text=resume_text))
            if "Skills:" in response and "Experiences:" in response:
                skills, experience = response.split("Experiences:")
                user_data["skills"] = skills.replace("Skills:", "").strip()
                user_data["experience"] = experience.strip()
                user_data["step"] = "ask_interests"
                return jsonify({"response": "Enter your interests (e.g., technologies, industries)."})
            return jsonify({"response": "Error processing resume details."})
        else:
            return jsonify({"response": "Error extracting text from PDF."})
    return jsonify({"response": "Invalid file format. Only PDFs are allowed."})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if "step" not in user_data:
        user_data["step"] = "choose_option"

    if user_data["step"] == "ask_interests":
        user_data["interests"] = user_message
        user_data["step"] = "ask_goals"
        return jsonify({"response": "Enter your career goals."})

    elif user_data["step"] == "ask_goals":
        user_data["goals"] = user_message
        career_advice = model.invoke(
            advice_prompt.format(
                skills=user_data["skills"],
                experience=user_data["experience"],
                interests=user_data["interests"],
                goals=user_data["goals"]
            )
        )
        user_data["step"] = "offer_roadmap"
        return jsonify({"response": career_advice, "roadmap_option": True})

    return jsonify({"response": "Invalid request."})

@app.route("/generate_roadmap", methods=["POST"])
def generate_roadmap():
    if "skills" in user_data and "experience" in user_data and "interests" in user_data and "goals" in user_data:
        roadmap_response = model.invoke(
            roadmap_prompt.format(
                skills=user_data["skills"],
                experience=user_data["experience"],
                interests=user_data["interests"],
                goals=user_data["goals"]
            )
        )
        return jsonify({"response": roadmap_response.strip()})
    return jsonify({"response": "Missing user data for roadmap generation."})

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
            return text.strip()
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
