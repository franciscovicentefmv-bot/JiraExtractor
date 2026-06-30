from services.calculations import process_project
from services.analytics import build_kpis


def build_dashboard(client, project_keys):
    """
    Aggregates KPI data across multiple projects for dashboard.
    """

    result = []

    for p in project_keys:

        issues = client.download_project(p)

        durations, transitions = process_project(p, issues)

        kpis = build_kpis(durations, transitions)

        total_time = sum(durations.values())

        result.append({
            "project": p,
            "total_time_hours": round(total_time.total_seconds() / 3600, 2),
            "kpis": kpis
        })

    return result