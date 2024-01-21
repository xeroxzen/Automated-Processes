import time

import requests
from bs4 import BeautifulSoup


def scrape_indeed_jobs(query, location):
    base_url = "https://remoteok.com/"
    params = {
        "q": query,
        "l": location,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        job_listings = soup.find_all("div", class_="jobsearch-SerpJobCard")

        results = []

        for job in job_listings:
            job_title = job.find("a", class_="jobtitle").text.strip()
            company = job.find("span", class_="company").text.strip()
            location = job.find("div", class_="recJobLoc")["data-rc-loc"]
            link = "https://remoteok.com" + job.find("a", class_="jobtitle")["href"]

            result = {
                "Job Title": job_title,
                "Company": company,
                "Location": location,
                "Link": link,
            }

            results.append(result)
            time.sleep(2)

        return results
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None


def main():
    query = "law human rights international law AI regulation"
    location = "United Kingdom"  # Replace with your preferred location

    indeed_results = scrape_indeed_jobs(query, location)

    if indeed_results:
        print("Job Listings from Indeed:")
        for result in indeed_results:
            print(result)
    else:
        print("Failed to retrieve job listings from Indeed.")


if __name__ == "__main__":
    main()
