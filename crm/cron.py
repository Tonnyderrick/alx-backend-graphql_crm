from datetime import datetime
import requests

def update_low_stock() -> None:
    """
    Executes the UpdateLowStockProducts mutation and logs updated product stock levels.
    """
    log_file = "/tmp/low_stock_updates_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """
    mutation {
        updateLowStockProducts {
            message
            updatedProducts
        }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )

        data = response.json().get("data", {}).get("updateLowStockProducts", {})
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] {data.get('message')}\n")
            for product in data.get("updatedProducts", []):
                f.write(f"  - {product}\n")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] ERROR: {str(e)}\n")
