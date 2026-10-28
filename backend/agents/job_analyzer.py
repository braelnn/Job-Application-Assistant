import os
import json
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
user = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def scrape_job_url(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    feedback = requests.get(url, headers=headers, timeout=10)
    feedback.raise_for_status()

    soup = BeautifulSoup(feedback.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    return text[:6000]


def analyze_job(job_text: str) -> dict:
    prompt = f"""
You are a job analysis expert. Given the job description below, extract the following
information and return it as valid JSON only — no explanation, no markdown fences.

JSON structure:
{{
  "job_title": "string",
  "company": "string",
  "required_skills": ["list of must-have skills"],
  "preferred_skills": ["list of nice-to-have skills"],
  "keywords": ["top 5 ATS keywords from the posting"],
  "responsibilities": ["top 3 key responsibilities"],
  "summary": "2 sentence plain English summary of the role"
}}

Job Description:
\"\"\"
{job_text}
\"\"\"
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


def run(job_url: str = None, job_text: str = None) -> dict:
    if not job_url and not job_text:
        raise ValueError("Provide either a job_url or job_text.")

    if job_url:
        try:
            print(f"[Job Analyzer] Scraping URL: {job_url}")
            job_text = scrape_job_url(job_url)
            print(f"[Job Analyzer] Scraped {len(job_text)} characters.")
        except Exception as e:
            if job_text:
                print(f"[Job Analyzer] URL scraping failed ({e}). Using pasted text.")
            else:
                raise RuntimeError(f"Could not scrape URL and no fallback text provided. Error: {e}")

    print("[Job Analyzer] Sending to OpenAI for analysis...")
    result = analyze_job(job_text)
    print(f"[Job Analyzer] Done. Job: {result.get('job_title')} @ {result.get('company')}")
    return result


# Quick test 
if __name__ == "__main__":
    print(" Job Analyzer Agent")
    print("Choose input method:")
    print("1 - Paste a job URL")
    print("2 - Paste job description text manually")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        job_url = input("Paste the job URL: ").strip()
        result = run(job_url=job_url)

    elif choice == "2":
        print("Paste the job description below.")
        print("When done, type END on a new line and press Enter:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        job_text = "\n".join(lines)
        result = run(job_text=job_text)

    else:
        print("Invalid choice.")
        exit()

    print("\n Analysis Result")
    print(json.dumps(result, indent=2))