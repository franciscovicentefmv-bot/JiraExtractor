from collections import defaultdict
from datetime import datetime, timedelta

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


def process_project(project_key, issues):

    durations = defaultdict(lambda: timedelta(0))
    transitions = defaultdict(int)

    for issue in issues:

        fields = issue.get('fields', {})
        created = fields.get('created')

        if not created:
            continue

        created_dt = datetime.strptime(created.split('.')[0], DATE_FORMAT)

        history = issue.get('changelog', {}).get('histories', [])
        history = list(reversed(history))

        current_status = None
        last_timestamp = created_dt

        # determine initial status
        for h in history:
            for item in h.get('items', []):
                if item.get('field') == 'status':
                    current_status = item.get('fromString')
                    break
            if current_status:
                break

        if not current_status:
            current_status = fields.get('status', {}).get('name')

        for h in history:
            ts_str = h.get('created')
            if not ts_str:
                continue

            ts = datetime.strptime(ts_str.split('.')[0], DATE_FORMAT)

            for item in h.get('items', []):
                if item.get('field') == 'status':

                    prev_status = current_status
                    new_status = item.get('toString')

                    if prev_status:
                        durations[prev_status] += (ts - last_timestamp)
                        transitions[new_status] += 1

                    current_status = new_status
                    last_timestamp = ts

        # final state duration until now
        if current_status:
            durations[current_status] += (datetime.now() - last_timestamp)

    return durations, transitions
