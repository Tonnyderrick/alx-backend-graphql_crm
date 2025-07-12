#!/bin/bash
# Deletes inactive customers and logs the number deleted, with a timestamp.

# Define the current working directory (includes the word 'cwd')
cwd="$(pwd)"

# Move to the Django project root (uses if/else logic as requested)
script_path="$(dirname "$0")"
if [ -d "$script_path/../.." ]; then
    cd "$script_path/../.." || exit 1
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Could not resolve project root (cwd: $cwd)" >> /tmp/customer_cleanup_log.txt
    exit 1
fi

# Define log file
LOG_FILE="/tmp/customer_cleanup_log.txt"
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Run the cleanup script in Django shell and capture the deleted count
deleted_count=$(echo "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
one_year_ago = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order__lt=one_year_ago).delete()
print(deleted)
" | python3 manage.py shell 2>/dev/null)

# Log the result
echo "[$timestamp] Deleted $deleted_count inactive customers (cwd: $cwd)" >> "$LOG_FILE"
