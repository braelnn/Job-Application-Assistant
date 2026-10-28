import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
user = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run(cv_text: str, job_analysis: dict) -> str:
    """
    Takes the tailored CV and job analysis.
    Returns a personalized cover letter as plain text.
    """

    job_title        = job_analysis.get("job_title", "the role")
    company          = job_analysis.get("company", "the company")
    required_skills  = ", ".join(job_analysis.get("required_skills", []))
    keywords         = ", ".join(job_analysis.get("keywords", []))
    responsibilities = "\n".join(f"- {r}" for r in job_analysis.get("responsibilities", []))
    summary          = job_analysis.get("summary", "")

    prompt = f"""
You are an expert cover letter writer. Write a compelling, personalized cover
letter for the candidate below applying for the role described.

Target Role: {job_title} at {company}
Job Summary: {summary}

Required Skills:      {required_skills}
ATS Keywords to use:  {keywords}

Key Responsibilities:
{responsibilities}

Instructions:
1. Open with a strong, specific first paragraph — mention the exact role and company.
2. Paragraph 2: Match the candidate's top experience to the job's key responsibilities.
3. Paragraph 3: Highlight 2-3 skills from the required skills list with concrete examples from their CV.
4. Closing paragraph: Express enthusiasm, mention fit, include a call to action.
5. Keep it to 4 paragraphs, under 350 words.
6. Tone: professional but human — not stiff or generic.
7. Output plain text only — no markdown, no asterisks, no subject lines.

Candidate CV:
\"\"\"
{cv_text}
\"\"\"

Write the cover letter now:
"""

    print(f"[Cover Letter] Writing cover letter for {job_title} @ {company}...")

    feedback = user.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )

    cover_letter = feedback.choices[0].message.content.strip()
    print("[Cover Letter] Done.")
    return cover_letter


# Test 
if __name__ == "__main__":
    from job_analyzer import run as analyze_job
    from resume_tailor import run as tailor_cv

    print(" Cover Letter Agent ")
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

    print("\n[Pipeline] Running Resume Tailor first...")
    tailored_cv = tailor_cv(cv_text, job_analysis)

    print("\n[Pipeline] Now generating Cover Letter...")
    cover_letter = run(tailored_cv, job_analysis)

    print("\ Cover Letter ")
    print(cover_letter)