import subprocess, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import EMAIL, API_TOKEN, PROXY, BASE_URL
from services.sync_store import get_last_sync, update_last_sync

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
        """
        Optimized Jira fetch:
        - Uses incremental sync when possible
        - Reduces full re-fetching of issues
        """
        start = 0
        out = []

        last_sync = get_last_sync(project)

        if last_sync:
            # Jira JQL does not reliably support epoch -> use relative window
            jql = f'project={project} AND updated >= -7d'
        else:
            jql = f'project={project}'

        while True:
            d = self.request(
                f'/rest/api/2/search?jql={jql}&startAt={start}&maxResults=100'
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

        res = []
        with ThreadPoolExecutor(max_workers=10) as ex:
            fut = [ex.submit(self.get_issue, i['key']) for i in issues]
            for f in as_completed(fut):
                res.append(f.result())

        # mark sync complete
        update_last_sync(project)

        return res
