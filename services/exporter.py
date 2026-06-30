import pandas as pd
import os

from config import EXPORT_FOLDER

def create_excel_files(project, durations, transitions):
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)

    dur_file = os.path.join(EXPORT_FOLDER, f"{project}_durations.xlsx")
    trans_file = os.path.join(EXPORT_FOLDER, f"{project}_transitions.xlsx")

    pd.DataFrame([dict(durations)]).to_excel(dur_file, index=False)
    pd.DataFrame([dict(transitions)]).to_excel(trans_file, index=False)

    return [dur_file, trans_file]
