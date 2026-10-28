# backend/orchestrator.py

import sys
import csv
import os
from datetime import datetime
from agents.job_analyzer  import run as analyze_job
from agents.resume_tailor import run as tailor_cv
from agents.cover_letter  import run as write_cover_letter
from agents.critic        import run as critique


def save_to_csv(result: dict):
    """
    Saves the pipeline result to results.csv in the backend folder.
    Appends a new row each time so all runs are preserved.
    """
    filepath = os.path.join(os.path.dirname(__file__), "results.csv")
    file_exists = os.path.isfile(filepath)

    row = {
        "timestamp":            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "job_title":            result["job_analysis"].get("job_title", ""),
        "company":              result["job_analysis"].get("company", ""),
        "cv_score":             result["cv_score"],
        "cover_letter_score":   result["cover_letter_score"],
        "overall_score":        result["overall_score"],
        "iterations":           result["iterations"],
        "tailored_cv":          result["tailored_cv"].replace("\n", " | "),
        "cover_letter":         result["cover_letter"].replace("\n", " | "),
        "missing_keywords":     ", ".join(result["feedback"].get("missing_keywords", [])),
        "verdict":              result["feedback"].get("verdict", ""),
    }

    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"\n[Orchestrator] Results saved to results.csv")


def run_pipeline(cv_text: str, job_url: str = None, job_text: str = None) -> dict:
    """
    Orchestrates the full multi-agent pipeline:
      1. Job Analyzer  → extract job requirements
      2. Resume Tailor → rewrite CV to match job
      3. Cover Letter  → write personalized cover letter
      4. Critic        → score + refine both docs (up to 3 iterations)
    """
    print("AI Job Application Assistant")

    # Step 1
    print("\n[Orchestrator] Step 1/4 → Job Analyzer Agent")
    job_analysis = analyze_job(job_url=job_url, job_text=job_text)

    # Step 2
    print("\n[Orchestrator] Step 2/4 → Resume Tailor Agent")
    tailored_cv = tailor_cv(cv_text, job_analysis)

    # Step 3
    print("\n[Orchestrator] Step 3/4 → Cover Letter Agent")
    cover_letter = write_cover_letter(tailored_cv, job_analysis)

    # Step 4
    print("\n[Orchestrator] Step 4/4 → Critic Agent (max 3 iterations)")
    final = critique(tailored_cv, cover_letter, job_analysis, max_iterations=3)

    print(f"\n Pipeline complete!")
    print(f"Score      : {final['overall_score']}/100")
    print(f"Iterations : {final['iterations']}")

    return {
        "job_analysis":         job_analysis,
        "tailored_cv":          final["tailored_cv"],
        "cover_letter":         final["cover_letter"],
        "overall_score":        final["overall_score"],
        "cv_score":             final["cv_score"],
        "cover_letter_score":   final["cover_letter_score"],
        "feedback":             final["feedback"],
        "iterations":           final["iterations"],
    }


if __name__ == "__main__":
    print("=== Full Pipeline Test ===")
    print("1 - Paste a job URL")
    print("2 - Paste job description text")
    choice = input("\nEnter 1 or 2: ").strip()

    job_url  = None
    job_text = None

    if choice == "1":
        job_url = input("Paste the job URL: ").strip()
    elif choice == "2":
        print("Paste the job description. Type END when done:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        job_text = "\n".join(lines)
    else:
        print("Invalid choice.")
        sys.exit(1)

    print("\nPaste your CV. Type END when done:\n")
    cv_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        cv_lines.append(line)
    cv_text = "\n".join(cv_lines)

    result = run_pipeline(cv_text=cv_text, job_url=job_url, job_text=job_text)

    print("\n── FINAL TAILORED CV ──")
    print(result["tailored_cv"])
    print("\n── FINAL COVER LETTER ──")
    print(result["cover_letter"])
    print("\n── SCORES ──")
    print(f"  CV Score           : {result['cv_score']}/100")
    print(f"  Cover Letter Score : {result['cover_letter_score']}/100")
    print(f"  Overall Score      : {result['overall_score']}/100")
    print(f"  Iterations         : {result['iterations']}")

    save_to_csv(result)