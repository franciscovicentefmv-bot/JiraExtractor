import pandas as pd
import os

from config import EXPORT_FOLDER
from services.analytics import build_kpis


def create_excel_files(project, durations, transitions):

    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)

    # RAW TABLES
    durations_rows = [
        {"State": k, "TimeSpent": str(v)}
        for k, v in durations.items()
    ]

    transitions_rows = [
        {"State": k, "Transitions": v}
        for k, v in transitions.items()
    ]

    # KPI TABLE
    kpis = build_kpis(durations, transitions)

    dur_file = os.path.join(EXPORT_FOLDER, f"{project}_durations.xlsx")
    trans_file = os.path.join(EXPORT_FOLDER, f"{project}_transitions.xlsx")
    kpi_file = os.path.join(EXPORT_FOLDER, f"{project}_kpis.xlsx")

    pd.DataFrame(durations_rows).to_excel(dur_file, index=False)
    pd.DataFrame(transitions_rows).to_excel(trans_file, index=False)
    pd.DataFrame(kpis).to_excel(kpi_file, index=False)

    return [dur_file, trans_file, kpi_file]
