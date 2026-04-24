from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
import os
import re

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Skills database (all roles covered)
skills_data = {
    "frontend developer": ["html", "css", "javascript", "react"],
    "backend developer": ["python", "java", "sql", "fastapi"],
    "full stack developer": ["html", "css", "javascript", "python", "sql"],
    "devops engineer": ["docker", "kubernetes", "aws", "jenkins"],

    "data analyst": ["python", "sql", "excel", "power bi", "tableau"],
    "data scientist": ["python", "machine learning", "pandas", "numpy"],

    "mobile developer": ["android", "kotlin", "flutter", "java"],
    "software tester": ["testing", "selenium", "manual testing"],

    "cyber security": ["network security", "ethical hacking", "penetration testing", "cryptography"],
    "cloud engineer": ["aws", "azure", "gcp", "cloud computing"]
}

# ✅ Request model
class ResumeInput(BaseModel):
    text: str
    role: str


# ✅ TEXT ANALYSIS
@app.post("/analyze-text")
def analyze_text(data: ResumeInput):
    return analyze_logic(data.text, data.role)


# ✅ PDF ANALYSIS
@app.post("/analyze-pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    role: str = Form(...)
):
    file_path = f"temp_{file.filename}"

    # Save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    # ❗ Handle empty PDF text
    if text.strip() == "":
        return {"error": "PDF has no readable text"}

    return analyze_logic(text, role)


# ✅ CORE ANALYSIS LOGIC (FIXED)
def analyze_logic(text, role):

    text = text.lower().replace("\n", " ")

    # 🔥 Normalize role
    role = role.strip().lower()

    # 🔥 Ensure role exists
    if role not in skills_data:
        return {
            "error": f"Role '{role}' not supported",
            "available_roles": list(skills_data.keys())
        }

    skills_list = skills_data[role]

    found = []

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.append(skill)

    missing = [s for s in skills_list if s not in found]

    suggestions = [f"Add {s} projects" for s in missing]

    score = int((len(found) / len(skills_list)) * 100)

    return {
        "found": found,
        "missing": missing,
        "suggestions": suggestions,
        "score": score
    }


# ✅ ROOT (optional)
@app.get("/")
def home():
    return {"message": "API is running"}