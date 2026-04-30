import json
import os
import uuid

from datetime import datetime


LOG_FILE = "backend/database/logs.json"


def load_logs():

    if not os.path.exists(LOG_FILE):

        return []

    with open(LOG_FILE, "r") as file:

        return json.load(file)


def save_log(log):

    logs = load_logs()

    enriched_log = {

        "id": str(uuid.uuid4()),

        "timestamp": datetime.utcnow().isoformat(),

        **log
    }

    logs.append(enriched_log)

    with open(LOG_FILE, "w") as file:

        json.dump(logs, file, indent=4)

    return enriched_log
