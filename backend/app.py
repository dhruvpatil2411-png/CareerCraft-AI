
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from pathlib import Path
import os
import json
import re
import time

# ========================================
# LOAD ENVIRONMENT
# ========================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ========================================
# FLASK APP
# ========================================

app = Flask(__name__)
CORS(app)

client = (
    genai.Client(api_key=GEMINI_API_KEY)
    if GEMINI_API_KEY
    else None
)

# Model shown in your available-model list
GEMINI_MODEL = "gemini-3.1-flash-lite"


# ========================================
# HOME ROUTE
# ========================================

@app.get("/")
def home():
    return jsonify({
        "status": "success",
        "message": "CareerCraft AI backend is running"
    })


# ========================================
# RULE-BASED FALLBACK
# ========================================

def fallback_analysis(student_data):
    raw_skills = student_data.get("skills", [])

    if isinstance(raw_skills, str):
        raw_skills = raw_skills.split(",")

    skills = " ".join(str(s) for s in raw_skills)

    profile = " ".join([
        skills,
        str(student_data.get("interest", "")),
        str(student_data.get("goal", "")),
        str(student_data.get("education", ""))
    ]).lower()

    if any(word in profile for word in [
        "machine learning", "artificial intelligence",
        "data science", "data analyst", "python",
        "statistics", " ai ", " ml "
    ]):
        career = "AI / Data Science Beginner"
        score = 75
        strengths = [
            "Interest in technology and problem-solving",
            "Opportunity to develop programming skills",
            "Potential to build data-driven projects"
        ]
        gaps = [
            "Python programming fundamentals",
            "Statistics and data analysis",
            "Machine learning fundamentals"
        ]
        projects = [
            "Student Performance Predictor",
            "Resume Skill Gap Analyzer",
            "Data Visualization Dashboard"
        ]

    elif any(word in profile for word in [
        "web", "html", "css", "javascript",
        "frontend", "front-end", "full stack",
        "full-stack", "website"
    ]):
        career = "Web Developer"
        score = 75
        strengths = [
            "Interest in web development",
            "Opportunity to build practical projects",
            "Potential to create a project portfolio"
        ]
        gaps = [
            "JavaScript fundamentals",
            "Responsive design and accessibility",
            "APIs, Git and deployment"
        ]
        projects = [
            "Personal Portfolio Website",
            "Student Task Manager",
            "Career Guidance Web App"
        ]

    elif any(word in profile for word in [
        "cybersecurity", "cyber security",
        "network security", "ethical hacking"
    ]):
        career = "Cybersecurity Beginner"
        score = 70
        strengths = [
            "Interest in computer security",
            "Opportunity to practise analytical thinking",
            "A structured learning pathway"
        ]
        gaps = [
            "Networking fundamentals",
            "Linux and operating system basics",
            "Security principles and safe lab practice"
        ]
        projects = [
            "Security Awareness Website",
            "Password Strength Checker",
            "Network Concepts Learning Guide"
        ]

    elif any(word in profile for word in [
        "ui/ux", "ui ux", "design", "figma", "user experience"
    ]):
        career = "UI/UX Designer"
        score = 70
        strengths = [
            "Interest in user experience",
            "Opportunity for creative problem-solving",
            "Potential to demonstrate work in a portfolio"
        ]
        gaps = [
            "User research and personas",
            "Wireframing and prototyping",
            "Accessibility and usability testing"
        ]
        projects = [
            "Student Portal Redesign",
            "Mobile App Prototype",
            "Website Usability Review"
        ]

    else:
        career = "Software Developer"
        score = 70
        strengths = [
            "Opportunity to build technical skills",
            "Potential to practise logical thinking",
            "Clear path for project-based learning"
        ]
        gaps = [
            "Programming fundamentals",
            "Problem-solving and data structures",
            "Git, testing and documentation"
        ]
        projects = [
            "Student Management System",
            "Personal Portfolio Website",
            "Task Tracking Application"
        ]

    return {
        "career": career,
        "match_score": score,
        "why_this_career": (
            "This preliminary recommendation is based on matching "
            "the skills and interests you entered. It is a starting "
            "point for exploration, not a validated prediction."
        ),
        "strengths": strengths,
        "skill_gaps": gaps,
        "roadmap": [
            {
                "step": 1,
                "title": "Learn the fundamentals",
                "description": (
                    "Study the core concepts of your chosen field "
                    "and practise regularly."
                )
            },
            {
                "step": 2,
                "title": "Practise your skills",
                "description": (
                    "Complete beginner exercises and small tasks."
                )
            },
            {
                "step": 3,
                "title": "Build a portfolio project",
                "description": (
                    "Create a small working project and document "
                    "what you learned."
                )
            },
            {
                "step": 4,
                "title": "Prepare for opportunities",
                "description": (
                    "Improve your resume and practise interview questions."
                )
            }
        ],
        "projects": projects,
        "interview_tips": [
            "Explain your own contribution to each project.",
            "Practise fundamentals and explain your reasoning.",
            "Be honest about the skills you are still learning."
        ],
        "analysis_mode": "rule_based_fallback",
        "notice": (
            "Gemini was unavailable. This is a predefined rule-based "
            "recommendation, not AI-generated analysis."
        )
    }


# ========================================
# HELPER: CLEAN MODEL JSON
# ========================================

def clean_json_text(text):
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    return text.strip()


# ========================================
# AI CAREER ANALYSIS
# ========================================

@app.post("/api/analyze")
def analyze():
    student_data = request.get_json(silent=True)

    if not isinstance(student_data, dict) or not student_data:
        return jsonify({
            "error": "No student data received."
        }), 400

    print("=" * 40)
    print("CAREERCRAFT AI ANALYSIS REQUEST")
    print("Received student profile.")
    print("=" * 40)

    prompt = f"""
You are CareerCraft AI, a career guidance assistant.

Analyze the student's full profile, including education, age,
interests, technical skills, soft skills, skill level and career goal.

Give practical, beginner-friendly recommendations.
Do not guarantee employment.
Treat the match score as an approximate guidance score, not a
scientifically validated prediction.

Student Profile:
{json.dumps(student_data, indent=2, ensure_ascii=False)}

Return ONLY valid JSON without Markdown using this structure:
{{
  "career": "Recommended career",
  "match_score": 75,
  "why_this_career": "Short explanation",
  "strengths": ["Strength 1", "Strength 2", "Strength 3"],
  "skill_gaps": ["Gap 1", "Gap 2", "Gap 3"],
  "roadmap": [
    {{"step": 1, "title": "Title", "description": "Action"}},
    {{"step": 2, "title": "Title", "description": "Action"}},
    {{"step": 3, "title": "Title", "description": "Action"}},
    {{"step": 4, "title": "Title", "description": "Action"}}
  ],
  "projects": ["Project 1", "Project 2", "Project 3"],
  "interview_tips": ["Tip 1", "Tip 2", "Tip 3"]
}}
"""

    # Try Gemini twice for temporary overload errors.
    if client is not None:
        for attempt in range(2):
            try:
                print(
                    f"Sending request to {GEMINI_MODEL}, "
                    f"attempt {attempt + 1}"
                )

                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )

                ai_text = getattr(response, "text", None)

                if not ai_text:
                    raise ValueError("Gemini returned an empty response.")

                result = json.loads(clean_json_text(ai_text))

                required_fields = [
                    "career",
                    "match_score",
                    "why_this_career",
                    "strengths",
                    "skill_gaps",
                    "roadmap",
                    "projects",
                    "interview_tips"
                ]

                if not all(field in result for field in required_fields):
                    raise ValueError(
                        "Gemini response is missing required fields."
                    )

                result["analysis_mode"] = "gemini"

                print("Gemini analysis completed successfully.")
                return jsonify(result), 200

            except Exception as error:
                error_text = str(error)
                print("Gemini request failed:", error_text)

                temporary_error = any(code in error_text for code in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "INTERNAL",
                    "504"
                ])

                if attempt == 0 and temporary_error:
                    time.sleep(1)
                    continue

                break

    # If Gemini is unavailable, return an explicitly labelled fallback.
    print("Using rule-based fallback.")
    result = fallback_analysis(student_data)
    return jsonify(result), 200


# ========================================
# START SERVER
# ========================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
