from bs4 import BeautifulSoup
import json


class JSONConverter:
    def __init__(self, data):
        self.data = data

    def extract_responsibilities(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        header = soup.find(
            "strong",
            string=lambda text: "ESSENTIAL FUNCTIONS AND RESPONSIBILITIES" in text,
        )
        if header:
            ul = header.find_next("ul")
            if ul:
                return [li.get_text(strip=True) for li in ul.find_all("li")]
        return []

    def convert_to_json(self):
        jobs_list = []
        for job in self.data.get("jobs", []):
            job_data = {
                "id": job.get("id", ""),
                "jobSlug": job.get("jobSlug", ""),
                "jobTitle": job.get("jobTitle", ""),
                "companyName": job.get("companyName", ""),
                "jobGeo": job.get("jobGeo", ""),
                "jobLevel": job.get("jobLevel", ""),
                "pubDate": job.get("pubDate", ""),
                "annualSalaryMin": job.get("annualSalaryMin", ""),
                "salaryCurrency": job.get("salaryCurrency", ""),
            }

            description = job.get("jobDescription", "")
            responsibilities = self.extract_responsibilities(description)

            job_data["responsibilities_1"] = (
                responsibilities[0] if len(responsibilities) > 0 else ""
            )
            job_data["responsibilities_2"] = (
                responsibilities[1] if len(responsibilities) > 1 else ""
            )
            job_data["responsibilities_3"] = (
                responsibilities[2] if len(responsibilities) > 2 else ""
            )

            jobs_list.append(job_data)

        json_data = {"jobs": jobs_list}
        return json.dumps(json_data, indent=4)
