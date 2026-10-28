import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
user = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run(cv_text: str, job_analysis: dict) -> str:
    """
    Takes the user's original CV and the job analysis from Job Analyzer Agent.
    Returns a rewritten, tailored CV as plain text.
    """

    required_skills  = ", ".join(job_analysis.get("required_skills", []))
    preferred_skills = ", ".join(job_analysis.get("preferred_skills", []))
    keywords         = ", ".join(job_analysis.get("keywords", []))
    responsibilities = "\n".join(f"- {r}" for r in job_analysis.get("responsibilities", []))
    job_title        = job_analysis.get("job_title", "the role")
    company          = job_analysis.get("company", "the company")

    prompt = f"""
You are an expert CV writer. Tailor the candidate's CV to match the job below
without inventing experience they do not have.

Target Role: {job_title} at {company}

Required Skills:   {required_skills}
Preferred Skills:  {preferred_skills}
ATS Keywords:      {keywords}

Key Responsibilities:
{responsibilities}

Instructions:
1. Rewrite the CV to highlight experience that matches the job.
2. Naturally weave in ATS keywords where truthfully applicable.
3. Strengthen bullet points under each role to mirror the responsibilities.
4. Keep the same sections and same jobs — do NOT add fake experience.
5. Make the Professional Summary first and tailor it directly to this role.
6. Output plain text only — no markdown, no asterisks, no ## headers.

Original CV:
\"\"\"
{cv_text}
\"\"\"

Write the tailored CV now:
"""

    print(f"[Resume Tailor] Tailoring CV for {job_title} @ {company}...")

    feedback = user.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    tailored_cv = feedback.choices[0].message.content.strip()
    print("[Resume Tailor] Done.")
    return tailored_cv


# Quick test 
if __name__ == "__main__":
    from job_analyzer import run as analyze_job

    print("Resume Tailor Agent")
    print("\nStep 1: Provide the job to tailor for.")
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

    print("\nStep 2: Paste your CV below. Type END on a new line when done:\n")
    cv_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        cv_lines.append(line)
    cv_text = "\n".join(cv_lines)

    tailored_cv = run(cv_text, job_analysis)

    print("\n Tailored CV")
    print(tailored_cv)