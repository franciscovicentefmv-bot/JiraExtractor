from datetime import timedelta


def build_kpis(durations, transitions):
    """
    Build KPI summary for enterprise dashboard.
    """

    total_time = sum(durations.values(), timedelta(0))

    kpis = []

    for state, time_spent in durations.items():

        pct = (time_spent / total_time * 100) if total_time.total_seconds() > 0 else 0

        kpis.append({
            "State": state,
            "TimeSpentHours": round(time_spent.total_seconds() / 3600, 2),
            "Transitions": transitions.get(state, 0),
            "PercentOfFlow": round(pct, 2)
        })

    return kpis
