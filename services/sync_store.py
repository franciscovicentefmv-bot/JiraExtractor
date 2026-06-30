import json
import os
import time

STORE_PATH = "services/sync_state.json"


def load_state():
    if not os.path.exists(STORE_PATH):
        return {}
    with open(STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_last_sync(project):
    state = load_state()
    return state.get(project)


def update_last_sync(project):
    state = load_state()
    state[project] = int(time.time())
    save_state(state)
