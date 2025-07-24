import graphene
from graphene_django.types import DjangoObjectType
from .models import Customer, Product, Order
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import re

# === GraphQL Types ===

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order


# === Input Types ===

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int()

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()


# === Mutations ===

class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")

        if input.phone and not re.match(r"^\+?\d{7,15}$|^\d{3}-\d{3}-\d{4}$", input.phone):
            raise Exception("Invalid phone format")

        customer = Customer(
            name=input.name,
            email=input.email,
            phone=input.phone or ''
        )
        customer.save()  # ✅ Explicit .save()
        return CreateCustomer(customer=customer, message="Customer created successfully")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created = []
        errors = []

        for idx, data in enumerate(input):
            try:
                if Customer.objects.filter(email=data.email).exists():
                    raise ValidationError("Email already exists")

                if data.phone and not re.match(r"^\+?\d{7,15}$|^\d{3}-\d{3}-\d{4}$", data.phone):
                    raise ValidationError("Invalid phone format")

                customer = Customer(
                    name=data.name,
                    email=data.email,
                    phone=data.phone or ''
                )
                customer.save()  # ✅ Explicit .save()
                created.append(customer)
            except Exception as e:
                errors.append(f"Customer {data.name}: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be positive")
        if input.stock is not None and input.stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product(
            name=input.name,
            price=input.price,
            stock=input.stock if input.stock is not None else 0
        )
        product.save()  # Optional but consistent
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise Exception("Customer does not exist")

        products = Product.objects.filter(id__in=input.product_ids)
        if not products.exists():
            raise Exception("Invalid product IDs")

        total = sum(p.price for p in products)

        order = Order(
            customer=customer,
            order_date=input.order_date or now(),
            total_amount=total
        )
        order.save()
        order.products.set(products)
        return CreateOrder(order=order)


# === Root Query and Mutation ===

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
