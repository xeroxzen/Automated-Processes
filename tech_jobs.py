import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


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

                # Fetch job description from the job details page
                job_details_response = requests.get(link)
                if job_details_response.status_code == 200:
                    job_details_soup = BeautifulSoup(
                        job_details_response.content, "html.parser"
                    )
                    job_description = job_details_soup.find(
                        "div", class_="description"
                    ).get_text(strip=True)
                else:
                    job_description = "Failed to retrieve job description."

                result = {
                    "Job Title": job_title,
                    "Company": company,
                    "Link": link,
                    "Date Posted": date_posted,
                    "Job Description": job_description,
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
        "law",
        "softwaare engineer",
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
            print(
                f"{Fore.MAGENTA}Job Description:{Style.RESET_ALL} {result['Job Description']}"
            )
            print("\n")
    else:
        print("Failed to retrieve job listings from RemoteOK.")


if __name__ == "__main__":
    main()
