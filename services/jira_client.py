import subprocess, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import EMAIL, API_TOKEN, PROXY, BASE_URL

class JiraClient:
    def _curl(self, endpoint):
        url = BASE_URL + endpoint
        cmd = 'curl -s -x "' + PROXY + '" -u "' + EMAIL + ':' + API_TOKEN + '" --insecure -H "Accept: application/json" "' + url + '"'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode != 0:
            raise Exception(res.stderr)
        return json.loads(res.stdout)

    def request(self, endpoint):
        for i in range(5):
            try:
                return self._curl(endpoint)
            except:
                time.sleep(5)
        raise Exception("fail")

    def get_projects(self):
        return self.request('/rest/api/2/project')

    def get_project_issues(self, project):
        start = 0
        out = []

        while True:
            d = self.request(
                f'/rest/api/2/search?jql=project={project}&startAt={start}&maxResults=100'
            )

            out.extend(d.get('issues', []))
            start += 100

            if start >= d.get('total', 0):
                break

        return out

    def get_issue(self, key):
        return self.request(f'/rest/api/2/issue/{key}?expand=changelog')

    def download_project(self, project):
        issues = self.get_project_issues(project)

        # deduplicate keys to avoid redundant API calls
        seen = set()
        unique = []

        for i in issues:
            key = i.get('key')
            if key and key not in seen:
                seen.add(key)
                unique.append(i)

        res = []

        # safer concurrency (reduce Jira API pressure)
        with ThreadPoolExecutor(max_workers=6) as ex:
            fut = [ex.submit(self.get_issue, i['key']) for i in unique]

            for f in as_completed(fut):
                try:
                    res.append(f.result())
                except Exception:
                    pass

        return res
