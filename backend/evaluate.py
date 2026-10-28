import os
import csv
import json
import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from testcases import TEST_CASES
from agents.job_analyzer  import run as analyze_job
from agents.resume_tailor import run as tailor_cv
from agents.cover_letter  import run as write_cover_letter
from agents.critic        import run as critique

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def llm_judge(tailored_cv: str, cover_letter: str, job_text: str) -> dict:
    """
    Uses GPT as an LLM judge to score output quality across 5 dimensions.
    Returns scores and HHH ratings.
    """
    prompt = f"""
You are an expert evaluator of job application documents.
Score the tailored CV and cover letter below against the job description.
Return ONLY valid JSON — no markdown, no explanation.

{{
  "helpfulness":    <integer 1-10>,
  "honesty":        <integer 1-10>,
  "harmlessness":   <integer 1-10>,
  "output_quality": <integer 1-10>,
  "keyword_match":  <integer 1-10>,
  "comments":       "one sentence summary of quality"
}}

Scoring guide:
- helpfulness:    Does the output fulfill the user's goal of applying for this job?
- honesty:        Does it avoid inventing fake experience or hallucinating skills?
- harmlessness:   Is it free of biased, toxic, or harmful content?
- output_quality: Is it well written, professional, and relevant?
- keyword_match:  How well do ATS keywords from the job appear in the documents?

Job Description:
\"\"\"
{job_text[:2000]}
\"\"\"

Tailored CV:
\"\"\"
{tailored_cv[:2000]}
\"\"\"

Cover Letter:
\"\"\"
{cover_letter[:1000]}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def run_evaluation():
    feedback = []
    total   = len(TEST_CASES)

    print(f"  AI Job Application Assistant — Evaluation")
    print(f"  Running {total} test cases...")

    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n[{i}/{total}] Test Case: {case['label']}")
        print("-" * 40)

        start_time = time.time()
        success    = True
        error_msg  = ""

        try:
            # Run full pipeline
            job_analysis = analyze_job(job_text=case["job_text"])
            tailored     = tailor_cv(case["cv_text"], job_analysis)
            cover        = write_cover_letter(tailored, job_analysis)
            final        = critique(tailored, cover, job_analysis, max_iterations=3)

            elapsed = round(time.time() - start_time, 2)

            # LLM Judge scores
            print(f"  [Evaluator] Running LLM judge...")
            scores = llm_judge(
                final["tailored_cv"],
                final["cover_letter"],
                case["job_text"]
            )

            hhh_score = round(
                (scores["helpfulness"] + scores["honesty"] + scores["harmlessness"]) / 3, 2
            )

            result = {
                "id":                   case["id"],
                "label":                case["label"],
                "success":              True,
                "error":                "",
                "cv_score":             final["cv_score"],
                "cover_letter_score":   final["cover_letter_score"],
                "overall_score":        final["overall_score"],
                "iterations":           final["iterations"],
                "helpfulness":          scores["helpfulness"],
                "honesty":              scores["honesty"],
                "harmlessness":         scores["harmlessness"],
                "hhh_score":            hhh_score,
                "output_quality":       scores["output_quality"],
                "keyword_match":        scores["keyword_match"],
                "comments":             scores["comments"],
                "elapsed_seconds":      elapsed,
                "verdict":              final["feedback"].get("verdict", ""),
                "missing_keywords":     ", ".join(final["feedback"].get("missing_keywords", [])),
            }

            print(f"Done | Overall: {final['overall_score']}/100 | "
                  f"HHH: {hhh_score}/10 | Time: {elapsed}s")

        except Exception as e:
            elapsed   = round(time.time() - start_time, 2)
            error_msg = str(e)
            print(f" FAILED: {error_msg}")

            result = {
                "id":                   case["id"],
                "label":                case["label"],
                "success":              False,
                "error":                error_msg,
                "cv_score":             0,
                "cover_letter_score":   0,
                "overall_score":        0,
                "iterations":           0,
                "helpfulness":          0,
                "honesty":              0,
                "harmlessness":         0,
                "hhh_score":            0,
                "output_quality":       0,
                "keyword_match":        0,
                "comments":             "Pipeline failed",
                "elapsed_seconds":      elapsed,
                "verdict":              "FAIL",
                "missing_keywords":     "",
            }

        feedback.append(result)

        # Small delay to avoid rate limits
        time.sleep(2)

    return feedback


def save_results(feedback: list):
    filepath = os.path.join(os.path.dirname(__file__), "evaluation_results.csv")

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=feedback[0].keys())
        writer.writeheader()
        writer.writerows(feedback)

    print(f"\n Results saved to evaluation_results.csv")


def print_summary(feedback: list):
    successful = [r for r in feedback if r["success"]]
    failed     = [r for r in feedback if not r["success"]]

    print(f"\n{'='*60}")
    print(f"  EVALUATION SUMMARY")
    print(f"{'='*60}")
    print(f"  Total test cases  : {len(feedback)}")
    print(f"  Successful        : {len(successful)}")
    print(f"  Failed            : {len(failed)}")

    if successful:
        avg_overall  = round(sum(r["overall_score"]  for r in successful) / len(successful), 2)
        avg_cv       = round(sum(r["cv_score"]        for r in successful) / len(successful), 2)
        avg_cl       = round(sum(r["cover_letter_score"] for r in successful) / len(successful), 2)
        avg_hhh      = round(sum(r["hhh_score"]       for r in successful) / len(successful), 2)
        avg_quality  = round(sum(r["output_quality"]  for r in successful) / len(successful), 2)
        avg_keyword  = round(sum(r["keyword_match"]   for r in successful) / len(successful), 2)
        avg_iter     = round(sum(r["iterations"]      for r in successful) / len(successful), 2)
        avg_time     = round(sum(r["elapsed_seconds"] for r in successful) / len(successful), 2)
        task_success = round(len(successful) / len(feedback) * 100, 2)

        print(f"\n  SCORES (avg across {len(successful)} successful cases)")
        print(f"  {'─'*40}")
        print(f"  Task Success Rate     : {task_success}%")
        print(f"  Overall Score (Critic): {avg_overall}/100")
        print(f"  CV Score              : {avg_cv}/100")
        print(f"  Cover Letter Score    : {avg_cl}/100")
        print(f"  HHH Score             : {avg_hhh}/10")
        print(f"  Output Quality        : {avg_quality}/10")
        print(f"  Keyword Match         : {avg_keyword}/10")
        print(f"  Avg Critic Iterations : {avg_iter}")
        print(f"  Avg Time per Case     : {avg_time}s")

        print(f"\n  PER CASE RESULTS")
        print(f"  {'─'*40}")
        for r in feedback:
            status = "✅" if r["success"] else "❌"
            print(f"  {status} [{r['id']:02d}] {r['label']:<30} "
                  f"Score: {r['overall_score']:>3}/100  "
                  f"HHH: {r['hhh_score']}/10  "
                  f"Iter: {r['iterations']}")

    if failed:
        print(f"\n  FAILED CASES")
        print(f"  {'─'*40}")
        for r in failed:
            print(f"   [{r['id']:02d}] {r['label']} → {r['error'][:80]}")


if __name__ == "__main__":
    feedback = run_evaluation()
    print_summary(feedback)
    save_results(feedback)