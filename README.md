# AI Job Application Assistant
## Project Overview

The AI Job Application Assistant is a multi-agent pipeline that takes a
candidate's CV and a job posting (URL or pasted text) as input, and
produces a tailored CV and cover letter optimized for that specific role.
The system uses a critic agent that scores the output and automatically
refines it for up to 3 iterations until quality passes a threshold.

---

## Architecture

```
User (React Frontend)
        ↓
FastAPI Backend (main.py)
        ↓
Orchestrator (orchestrator.py)
        ↓
┌─────────────────────────────────────┐
│  Agent 1: Job Analyzer              │
│  → Scrapes job URL or reads text    │
│  → Extracts skills, keywords, roles │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│  Agent 2: Resume Tailor             │
│  → Rewrites CV to match job         │
│  → Weaves in ATS keywords           │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│  Agent 3: Cover Letter Writer       │
│  → Writes personalized cover letter │
│  → Matches tone and requirements    │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│  Agent 4: Critic Agent              │
│  → Scores CV + cover letter 0-100  │
│  → Revises if score below 75        │
│  → Loops up to 3 iterations         │
└─────────────────────────────────────┘
        ↓
Final Output (Tailored CV + Cover Letter + Scores)
```
---

## Project Structure

```
job-application-assistant/
├── backend/
│   ├── agents/
│   │   ├── job_analyzer.py      
│   │   ├── resume_tailor.py     
│   │   ├── cover_letter.py      
│   │   └── critic.py            
│   ├── orchestrator.py          
│   ├── main.py                  
│   ├── evaluate.py              
│   ├── test_cases.py            
│   ├── results.csv              
│   ├── evaluation_results.csv   
│   ├── requirements.txt         
│   └── .env                     
└── frontend/
    ├── src/
    │   ├── App.jsx             
    │   ├── components/
    │       ├── InputForm.jsx    
    │       ├── Results.jsx      
    │       └── ScoreCard.jsx   
    │          
    ├── .env                    
    
```
### Prerequisites
- Python 3.10+
- Node.js 20+
- OpenAI API Key

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

## Running the Application

You need two terminals running simultaneously.

**Terminal 1 — Start the Backend:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn main:app --reload
```
Backend runs at: `http://localhost:8000`

**Terminal 2 — Start the Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs at: `http://localhost:5173`

Open your browser at `http://localhost:5173`




