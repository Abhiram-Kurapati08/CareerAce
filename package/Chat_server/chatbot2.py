import PyPDF2
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize the model
model = OllamaLLM(model="llama3.2:latest")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
            return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

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

roadmap_template = """
You are an AI assistant. Based on the user's skills, experience, interests, and goals, generate a roadmap that helps them achieve their career goals, broken down into steps.

User Information:
Skills: {skills}
Experience: {experience}
Interests: {interests}
Goals: {goals}
"""
roadmap_prompt = ChatPromptTemplate.from_template(roadmap_template)

# Function to generate and return the roadmap
def generate_roadmap(skills, experience, interests, goals):
    try:
        roadmap_response = model.invoke(
            roadmap_prompt.format(
                skills=skills,
                experience=experience,
                interests=interests,
                goals=goals
            )
        )
        return roadmap_response.strip()
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        return "Error generating roadmap."

advice_template = """
You are an AI assistant specializing in career guidance.
Based on the user's skills, experience, interests, and goals, provide:
1. Career path recommendations.
2. Companies to apply to.
3. Skills to learn.
4. Growth strategies.

User Information:
Skills: {skills}
Experience: {experience}
Interests: {interests}
Goals: {goals}
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

# Initialize templates
summarization_prompt = ChatPromptTemplate.from_template(summarization_template)
advice_prompt = ChatPromptTemplate.from_template(advice_template)
extraction_prompt = ChatPromptTemplate.from_template(extraction_template)

def generate_and_save_summary(skills, experience, interests, goals):
    try:
        summary_response = model.invoke(
            summarization_prompt.format(
                skills=skills,
                experience=experience,
                interests=interests,
                goals=goals
            )
        )
        with open("user_detail_summary.txt", "w") as file:
            file.write(summary_response.strip())
        print("\nSummary saved in 'user_detail_summary.txt'!")
        print("\nGenerated Summary:")
        print(summary_response.strip())
    except Exception as e:
        print(f"Error generating summary: {e}")

def provide_career_advice(skills, experience, interests, goals):
    try:
        response = model.invoke(
            advice_prompt.format(
                skills=skills,
                experience=experience,
                interests=interests,
                goals=goals
            )
        )
        print("\nCareer Advice:")
        print(response, "\n")
    except Exception as e:
        print(f"Error generating advice: {e}")
    generate_and_save_summary(skills, experience, interests, goals)

def chatbot():
    print("Welcome to the Career Guidance Chatbot!")
    print("Choose an option:")
    print("A) Upload your resume for automatic extraction.")
    print("B) Enter details manually.")
    
    choice = input("Enter A or B: ").strip().upper()
    skills, experience = "", ""
    
    if choice == "A":
        resume_path = input("Enter your resume PDF path: ").strip()
        resume_text = extract_text_from_pdf(resume_path)
        if resume_text:
            print("Resume text extracted successfully!")
            try:
                response = model.invoke(extraction_prompt.format(resume_text=resume_text))
                print("\nExtracted Information:")
                print(response)
                if "Skills:" in response and "Experiences:" in response:
                    skills, experience = response.split("Experiences:")
                    skills = skills.replace("Skills:", "").strip()
                    experience = experience.strip()
                else:
                    print("\nUnable to parse the response properly. Please review it manually.")
                    skills, experience = response, ""
            except Exception as e:
                print(f"Error extracting details: {e}")
        else:
            print("Failed to extract text. Try again.")
    elif choice == "B":
        skills = input("Enter your skills (comma-separated): ")
        experience = input("Enter your experience (e.g., internships, projects): ")
    else:
        print("Invalid choice. Restart the program and choose A or B.")
        return
    
    interests = input("Enter your interests (e.g., technologies, industries): ")
    goals = input("Enter your career goals: ")
    provide_career_advice(skills, experience, interests, goals)

    # Prompt the user for a roadmap
    roadmap_choice = input("\nWould you like to generate a roadmap to achieve your goals? (yes/no): ").strip().lower()
    if roadmap_choice == 'yes':
        roadmap = generate_roadmap(skills, experience, interests, goals)
        print("\nYour Career Roadmap:")
        print(roadmap)
    else:
        print("No roadmap generated.")

if __name__ == "__main__":
    chatbot()
