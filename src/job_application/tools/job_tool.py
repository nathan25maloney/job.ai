import json
import os
import requests
from crewai import Agent, Task
from langchain.tools import tool
from bs4 import BeautifulSoup


class JobTool:

    @tool("Search for job positions based on the search criteria.")
    def scrape_and_summarize_website(self, website):
        """Useful to scrape and summarize a website content"""
        url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        payload = json.dumps({"url": website})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(text=True)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing researches and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                allow_delegation=False
            )
            task = Task(
                agent=agent,
                description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
            )
            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)

    def search_jobs(self, search_criteria):
        job_sites = [
            ("Indeed", f"https://www.indeed.com/jobs?q={'+'.join(search_criteria.split())}"),
            ("Google Careers", f"https://careers.google.com/jobs/results/?q={'+'.join(search_criteria.split())}"),
            ("Microsoft Careers", f"https://careers.microsoft.com/us/en/search-results?keywords={'+'.join(search_criteria.split())}"),
            ("Amazon Jobs", f"https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query={'+'.join(search_criteria.split())}"),
            ("LinkedIn Jobs", f"https://www.linkedin.com/jobs/search/?keywords={'+'.join(search_criteria.split())}"),
            ("Stack Overflow Jobs", f"https://stackoverflow.com/jobs?q={'+'.join(search_criteria.split())}"),
            ("We Work Remotely", f"https://weworkremotely.com/remote-jobs/search?term={'+'.join(search_criteria.split())}"),
            ("Remote.co", f"https://remote.co/remote-jobs/search/?search_keywords={'+'.join(search_criteria.split())}"),
            ("Freelancer.com", f"https://www.freelancer.com/jobs/?keyword={'+'.join(search_criteria.split())}"),
            ("Upwork", f"https://www.upwork.com/ab/jobs/search/?q={'+'.join(search_criteria.split())}")
        ]

        all_jobs = []
        for site_name, url in job_sites:
            try:
                summary = self.scrape_and_summarize_website(url)
                all_jobs.append({"site": site_name, "summary": summary})
            except Exception as e:
                print(f"Failed to retrieve job postings from {site_name}: {e}")

        return all_jobs

# Example usage:
if __name__ == "__main__":
    search_criteria = "software engineer"
    tool = JobTool()
    job_listings = tool.search_jobs(search_criteria)
    for job in job_listings:
        print(f"Site: {job['site']}")
        print(f"Summary: {job['summary']}")
        print("-" * 40)
