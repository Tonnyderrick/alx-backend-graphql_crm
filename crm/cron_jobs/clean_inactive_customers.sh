#!/bin/bash
# Deletes customers with no orders in the past year and logs the result.

timestamp=$(date '+%Y-%m-%d %H:%M:%S')
deleted_count=$(echo "from crm.models import Customer; from django.utils import timezone; from datetime import timedelta; one_year_ago = timezone.now() - timedelta(days=365); deleted, _ = Customer.objects.filter(last_order__lt=one_year_ago).delete(); print(deleted)" | python3 manage.py shell 2>/dev/null)

echo "[$timestamp] Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
