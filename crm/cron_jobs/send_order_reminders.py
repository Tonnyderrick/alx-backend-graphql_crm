#!/usr/bin/env python3
"""
Script to query recent orders and log reminder messages.
"""

from datetime import datetime, timedelta
import requests
from gql import gql, Client  # ✅ Added imports as requested

# GraphQL endpoint
url = "http://localhost:8000/graphql"

# GraphQL query for orders within the last 7 days
query = """
query GetRecentOrders($since: DateTime!) {
  orders(orderDate_Gte: $since) {
    id
    customer {
      email
    }
  }
}
"""

# Calculate date 7 days ago
since = (datetime.now() - timedelta(days=7)).isoformat()

# Send the request
response = requests.post(
    url,
    json={"query": query, "variables": {"since": since}},
    headers={"Content-Type": "application/json"}
)

# Log file path
log_file = "/tmp/order_reminders_log.txt"
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

try:
    data = response.json()["data"]["orders"]
    with open(log_file, "a") as f:
        for order in data:
            log_line = f"[{timestamp}] Order ID {order['id']} - Email: {order['customer']['email']}\n"
            f.write(log_line)
    print("Order reminders processed!")
except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] Error processing order reminders: {str(e)}\n")
    print("Failed to process order reminders.")
