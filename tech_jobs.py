import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from colorama import Fore, Style
from datetime import datetime, timedelta
import re


def parse_relative_date(relative_date):
    match = re.match(r'(\d+)([hd])', relative_date)
    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        if unit == 'h':
            return datetime.now() - timedelta(hours=amount)
        elif unit == 'd':
            return datetime.now() - timedelta(days=amount)
    return datetime.now()


def scrape_remoteok_jobs(queries):
    base_url = "https://remoteok.com/remote-dev-jobs"
    results = []

    for query in queries:
        params = {
            "q": query,
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/87.0.4280.88 Safari/537.36"
        }
        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            job_listings = soup.find_all("tr", class_="job")

            for job in job_listings:
                job_title = job.find("h2").text.strip()
                company = job.find("h3").text.strip()
                date_posted = job.find("time").text.strip()
                link = (
                    "https://remoteok.com" + job.find("a", class_="preventLink")["href"]
                )

                # Check if job is listed within 7 days... #job.find("time").text.strip()
                job_posted_date = parse_relative_date(date_posted)
                if (datetime.today() - job_posted_date) <= timedelta(days=7):
                    # Extract additional details from job details page
                    job_details_response = requests.get(link)
                    if job_details_response.status_code == 200:
                        job_details_soup = BeautifulSoup(
                            job_details_response.content, "html.parser"
                        )
                        salary = job_details_soup.find("span", class_="salary").text.strip()
                        location = job_details_soup.find("div", class_="job-location").text.strip()
                        key_responsibilities = [
                            li.text.strip()
                            for li in job_details_soup.find_all("li", class_="responsibility")
                        ]
                    else:
                        salary = "Not available"
                        location = "Not available"
                        key_responsibilities = ["Failed to retrieve key responsibilities"]

                    result = {
                        "Job Title": job_title,
                        "Company": company,
                        "Link": link,
                        "Date Posted": date_posted,
                        "Salary": salary,
                        "Location": location,
                        "Key Responsibilities": key_responsibilities,
                    }

                    results.append(result)
        else:
            print(
                f"Failed to retrieve data for query '{query}'. Status code: {response.status_code}"
            )

    return results


def main():
    queries = [
        "software developer",
        "content creator",
        "software engineer",
        "data scientist",
        "data analyst",
        "data engineer",
        "data entry",
        "web developer",
        "technical writer",
    ]

    remoteok_results = scrape_remoteok_jobs(queries)

    if remoteok_results:
        print("Job Listings from RemoteOK:")
        for result in remoteok_results:
            print(f"{Fore.BLUE}Job Title:{Style.RESET_ALL} {result['Job Title']}")
            print(f"{Fore.GREEN}Company:{Style.RESET_ALL} {result['Company']}")
            print(f"{Fore.CYAN}Link:{Style.RESET_ALL} {result['Link']}")
            print(f"{Fore.YELLOW}Date Posted:{Style.RESET_ALL} {result['Date Posted']}")
            print(f"{Fore.RED}Salary:{Style.RESET_ALL} {result['Salary']}")
            print(f"{Fore.WHITE}Location:{Style.RESET_ALL} {result['Location']}")
            print(f"{Fore.GREEN}Key Responsibilities:")
            for responsibility in result["Key Responsibilities"]:
                print(f"\t- {responsibility}")
            print("\n")
    else:
        print("Failed to retrieve job")
        
if __name__ == "__main__":
    main()
