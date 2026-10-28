import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
user = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PASS_SCORE = 85  


def score_documents(tailored_cv: str, cover_letter: str, job_analysis: dict) -> dict:
    """
    Sends the tailored CV and cover letter to OpenAI for scoring.
    Returns a dict with scores and specific feedback.
    """

    job_title        = job_analysis.get("job_title", "the role")
    company          = job_analysis.get("company", "the company")
    required_skills  = ", ".join(job_analysis.get("required_skills", []))
    keywords         = ", ".join(job_analysis.get("keywords", []))
    responsibilities = "\n".join(f"- {r}" for r in job_analysis.get("responsibilities", []))

    prompt = f"""
You are a senior hiring manager and CV expert reviewing application documents
for a {job_title} position at {company}.

Job Requirements:
Required Skills:      {required_skills}
ATS Keywords:         {keywords}

Key Responsibilities:
{responsibilities}

---
TAILORED CV:
\"\"\"
{tailored_cv}
\"\"\"

---
COVER LETTER:
\"\"\"
{cover_letter}
\"\"\"

---
Evaluate both documents and return ONLY valid JSON — no explanation, no markdown fences.

JSON structure:
{{
  "cv_score": <integer 0-100>,
  "cover_letter_score": <integer 0-100>,
  "overall_score": <integer 0-100>,
  "cv_feedback": {{
    "strengths": ["what the CV does well"],
    "improvements": ["specific things to fix or add"]
  }},
  "cover_letter_feedback": {{
    "strengths": ["what the cover letter does well"],
    "improvements": ["specific things to fix or add"]
  }},
  "missing_keywords": ["important ATS keywords missing from either document"],
  "verdict": "PASS" or "REVISE"
}}

Use "PASS" if overall_score >= {PASS_SCORE}, otherwise use "REVISE".
"""

    feedback = user.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = feedback.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


def revise_with_feedback(
    tailored_cv: str,
    cover_letter: str,
    job_analysis: dict,
    feedback: dict
) -> tuple:
    """
    Takes the previous CV + cover letter + critic feedback
    and asks OpenAI to revise both documents.
    Returns (revised_cv, revised_cover_letter).
    """

    job_title = job_analysis.get("job_title", "the role")
    company   = job_analysis.get("company", "the company")

    cv_improvements = "\n".join(f"- {i}" for i in feedback["cv_feedback"]["improvements"])
    cl_improvements = "\n".join(f"- {i}" for i in feedback["cover_letter_feedback"]["improvements"])
    missing_kw      = ", ".join(feedback.get("missing_keywords", []))

    prompt = f"""
You are an expert CV and cover letter writer. Revise the documents below based
on the specific feedback provided. Do not invent experience that isn't there.

Role: {job_title} at {company}

--- FEEDBACK TO ADDRESS ---

CV Improvements needed:
{cv_improvements}

Cover Letter Improvements needed:
{cl_improvements}

Missing keywords to weave in (where truthfully applicable):
{missing_kw}

--- CURRENT CV ---
\"\"\"
{tailored_cv}
\"\"\"

--- CURRENT COVER LETTER ---
\"\"\"
{cover_letter}
\"\"\"

Return ONLY valid JSON — no markdown, no explanation:
{{
  "revised_cv": "full revised CV as plain text",
  "revised_cover_letter": "full revised cover letter as plain text"
}}
"""

    feedback = user.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    raw = feedback.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    return result["revised_cv"], result["revised_cover_letter"]


def run(
    tailored_cv: str,
    cover_letter: str,
    job_analysis: dict,
    max_iterations: int = 3
) -> dict:
    """
    Main entry point for the Critic Agent.
    Scores the documents, and if below PASS_SCORE, revises and re-scores.
    Loops up to max_iterations times.

    Returns a dict with the final CV, cover letter, score, and feedback.
    """

    current_cv     = tailored_cv
    current_cl     = cover_letter
    iteration      = 1

    while iteration <= max_iterations:
        print(f"\n[Critic] Iteration {iteration}/{max_iterations} — Scoring documents...")
        feedback = score_documents(current_cv, current_cl, job_analysis)

        overall = feedback.get("overall_score", 0)
        verdict = feedback.get("verdict", "REVISE")

        print(f"[Critic] CV Score: {feedback['cv_score']} | "
              f"Cover Letter Score: {feedback['cover_letter_score']} | "
              f"Overall: {overall} | Verdict: {verdict}")

        if verdict == "PASS" or iteration == max_iterations:
            if iteration == max_iterations and verdict != "PASS":
                print("[Critic] Max iterations reached. Returning best version.")
            else:
                print("[Critic] Documents passed quality check.")
            return {
                "tailored_cv":    current_cv,
                "cover_letter":   current_cl,
                "overall_score":  overall,
                "cv_score":       feedback["cv_score"],
                "cover_letter_score": feedback["cover_letter_score"],
                "feedback":       feedback,
                "iterations":     iteration,
            }

        print(f"[Critic] Score {overall} below {PASS_SCORE}. Revising...")
        current_cv, current_cl = revise_with_feedback(
            current_cv, current_cl, job_analysis, feedback
        )
        iteration += 1


#  Quick test 
if __name__ == "__main__":
    from job_analyzer  import run as analyze_job
    from resume_tailor import run as tailor_cv
    from cover_letter  import run as write_cover_letter

    print("Critic Agent (Full Pipeline Test)")
    print("\nStep 1: Provide the job.")
    print("1 - Paste a job URL")
    print("2 - Paste job description text manually")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        job_url = input("Paste the job URL: ").strip()
        job_analysis = analyze_job(job_url=job_url)
    elif choice == "2":
        print("Paste the job description. Type END on a new line when done:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        job_analysis = analyze_job(job_text="\n".join(lines))
    else:
        print("Invalid choice.")
        exit()

    print("\nStep 2: Paste your CV. Type END on a new line when done:\n")
    cv_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        cv_lines.append(line)
    cv_text = "\n".join(cv_lines)

    print("\n[Pipeline] Step 1 — Tailoring CV...")
    tailored   = tailor_cv(cv_text, job_analysis)

    print("\n[Pipeline] Step 2 — Writing Cover Letter...")
    cover      = write_cover_letter(tailored, job_analysis)

    print("\n[Pipeline] Step 3 — Critic reviewing and refining...")
    final      = run(tailored, cover, job_analysis, max_iterations=3)

    print(f" FINAL SCORE: {final['overall_score']}/100 after {final['iterations']} iteration(s)")
    print("\n FINAL TAILORED CV ")
    print(final["tailored_cv"])
    print("\n FINAL COVER LETTER ")
    print(final["cover_letter"])
    print("\n CRITIC FEEDBACK")
    print(json.dumps(final["feedback"], indent=2))