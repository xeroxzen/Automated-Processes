import time

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from retry import retry

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


@retry(exceptions=requests.RequestException, tries=3, delay=2, backoff=2)
def make_request(url, params=None):
    return requests.get(url, params=params, headers=headers)


def scrape_job_board(base_url, queries):
    results = []

    for query in queries:
        params = {"q": query}
        url = f"{base_url}/jobs"

        try:
            response = make_request(url, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve data for query '{query}'. Error: {e}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        job_listings = soup.find_all("div", class_="jobsearch-SerpJobCard")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            job_listings = soup.find_all("div", class_="jobsearch-SerpJobCard")

            for job in job_listings:
                job_title = job.find("a", class_="jobtitle").text.strip()
                company = job.find("span", class_="company").text.strip()
                location = job.find("div", class_="recJobLoc")["data-rc-loc"]
                link = (
                    "https://www.indeed.com" + job.find("a", class_="jobtitle")["href"]
                )

                job_details_response = requests.get(link)
                if job_details_response.status_code == 200:
                    job_details_soup = BeautifulSoup(
                        job_details_response.content, "html.parser"
                    )
                    job_description = job_details_soup.find(
                        "div", class_="jobsearch-jobDescriptionText"
                    ).get_text(strip=True)
                else:
                    job_description = "Failed to retrieve job description."

                result = {
                    "Job Title": job_title,
                    "Company": company,
                    "Location": location,
                    "Link": link,
                    "Job Description": job_description,
                }

                results.append(result)

                time.sleep(2)
        else:
            print(
                f"Failed to retrieve data for query '{query}'. Status code: {response.status_code}"
            )

    return results


def main():
    tech_queries = [
        "software developer",
        "content creator",
        "software engineer",
        "web developer",
        "data engineer",
        "integration engineer",
        "data scientist",
        "data analyst",
        "cybersecurity",
    ]
    law_queries = [
        "attorney",
        "legal assistant",
        "paralegal",
        "law clerk",
        "lawyer",
        "AI Regulator",
        "AI Ethics",
        "AI Policy",
        "AI Law",
        "AI Lawyer",
        "AI Attorney",
        "AI Paralegal",
        "AI Legal Assistant",
        "AI Law Clerk",
        "AI Law Firm",
        "AI Law Office",
        "AI Law Department",
        "AI Law School",
        "AI Law Professor",
        "AI Law Student",
        "AI Law Graduate",
        "AI Law Degree",
        "AI Law License",
        "AI Law Bar Exam",
        "AI Law Bar Association",
    ]

    tech_job_boards = [
        ("Indeed", "https://www.indeed.com/jobs"),
        ("LinkedIn", "https://www.linkedin.com/jobs"),
        ("Glassdoor", "https://www.glassdoor.com/Job/index.htm"),
        ("AngelList", "https://angel.co/jobs"),
        ("Dice", "https://www.dice.com/jobs"),
        ("CareerBuilder", "https://www.careerbuilder.com/jobs"),
        ("Monster", "https://www.monster.com/jobs"),
        ("Stack Overflow", "https://stackoverflow.com/jobs"),
        ("Hacker News", "https://news.ycombinator.com/jobs"),
        ("Remote.co", "https://remote.co/remote-jobs"),
        ("We Work Remotely", "https://weworkremotely.com/"),
        ("Toptal", "https://www.toptal.com/careers"),
        ("Pitch", "https://pitch.com/jobs"),
        ("GitHub", "https://jobs.github.com/positions"),
        ("Remote OK", "https://remoteok.io/remote-dev-jobs"),
    ]

    law_job_boards = [
        ("Indeed", "https://www.indeed.com/jobs"),
        ("LinkedIn", "https://www.linkedin.com/jobs"),
        ("Monster", "https://www.monster.com/jobs"),
        ("Lawjobs.com", "https://www.lawjobs.com/"),
        ("FindLaw", "https://www.findlaw.com/legaljobs"),
        ("LegalCrossing", "https://www.legalcrossing.com/"),
        (
            "National Law Review Career Center",
            "https://www.nationallawreview.com/career-center",
        ),
        ("Vault Law", "https://www.vault.com/"),
    ]

    all_results = []

    for board_name, board_url in tech_job_boards:
        print(f"\n{Fore.YELLOW}Scraping {board_name} for Tech Jobs:{Style.RESET_ALL}")
        results = scrape_job_board(board_url, tech_queries)
        all_results.extend(results)

    for board_name, board_url in law_job_boards:
        print(f"\n{Fore.YELLOW}Scraping {board_name} for Law Jobs:{Style.RESET_ALL}")
        results = scrape_job_board(board_url, law_queries)
        all_results.extend(results)

    if all_results:
        print("\nCombined Job Listings:")
        for result in all_results:
            print(f"\n{Fore.BLUE}Job Title:{Style.RESET_ALL} {result['Job Title']}")
            print(f"{Fore.GREEN}Company:{Style.RESET_ALL} {result['Company']}")
            print(f"{Fore.CYAN}Location:{Style.RESET_ALL} {result['Location']}")
            print(f"{Fore.CYAN}Link:{Style.RESET_ALL} {result['Link']}")
            print(
                f"{Fore.MAGENTA}Job Description:{Style.RESET_ALL} {result['Job Description']}"
            )
    else:
        print("Failed to retrieve job listings from the specified job boards.")


if __name__ == "__main__":
    main()
