from collections import defaultdict
from datetime import datetime

def process_project(project_key, issues):
    durations = defaultdict(int)
    transitions = defaultdict(int)
    for issue in issues:
        history = issue.get('changelog', {}).get('histories', [])
        for h in history:
            for item in h.get('items', []):
                if item.get('field') == 'status':
                    transitions[item.get('toString')] += 1
    return durations, transitions
