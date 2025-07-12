#!/usr/bin/env python3
"""
Cron job for logging heartbeat messages every 5 minutes.
"""

from datetime import datetime
import requests

from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client

def log_crm_heartbeat() -> None:
    """
    Logs a timestamped heartbeat message to confirm CRM is alive.
    Also tries to query the GraphQL hello field to verify it's working.
    """
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional GraphQL hello query check
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            message = f"{timestamp} CRM is alive (GraphQL OK)\n"
        else:
            message = f"{timestamp} CRM is alive (GraphQL ERROR)\n"
    except Exception as e:
        message = f"{timestamp} CRM is alive (GraphQL FAIL: {str(e)})\n"

    with open(log_file, "a") as f:
        f.write(message)
