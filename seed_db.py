# seed_db.py

import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

def seed():
    # Clear existing data
    Customer.objects.all().delete()
    Product.objects.all().delete()

    # Seed customers
    Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
    Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")

    # Seed products
    Product.objects.create(name="Laptop", price=999.99, stock=10)
    Product.objects.create(name="Phone", price=499.50, stock=15)

    print("Database seeded successfully.")

if __name__ == '__main__':
    seed()
