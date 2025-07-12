#!/bin/bash
# This script deletes customers with no orders in the last year and logs the result

LOG_FILE="/tmp/customer_cleanup_log.txt"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

DELETED_COUNT=$(echo "
from datetime import datetime, timedelta
from crm.models import Customer

one_year_ago = datetime.nw() - tiedelta(days=365)
inactive_customeroms = Customer.objects.filter(order__isnull=True, created_at__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
" | python3 manage.py shell)

echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"

