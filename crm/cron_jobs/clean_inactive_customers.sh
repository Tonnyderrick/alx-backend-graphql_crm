#!/bin/bash
# Deletes inactive customers and logs the number deleted, with environment context.

SCRIPT_PATH="${BASH_SOURCE[0]}"
CURRENT_DIR=$(pwd)
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
CWD=$(basename "$CURRENT_DIR")

# Change to the project root if needed
cd "$SCRIPT_DIR"/../../ || exit 1

# Log file path
LOG_FILE="/tmp/customer_cleanup_log.txt"
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Check if in correct directory before running
if [ "$CWD" != "cron_jobs" ]; then
    deleted_count=$(echo "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
one_year_ago = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order__lt=one_year_ago).delete()
print(deleted)
" | python3 manage.py shell 2>/dev/null)

    echo "[$timestamp] Deleted $deleted_count inactive customers" >> "$LOG_FILE"
else
    echo "[$timestamp] Script was run from inside cron_jobs directory. Skipping cleanup." >> "$LOG_FILE"
fi
