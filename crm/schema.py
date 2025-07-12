import graphene
from .models import Product

class UpdateLowStockProducts(graphene.Mutation):
    """Mutation to update low-stock products by restocking them."""

    message = graphene.String()
    updated_products = graphene.List(graphene.String)

    def mutate(self, info):
        updated = []
        low_stock_products = Product.objects.filter(stock__lt=10)
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated.append(f"{product.name} (stock: {product.stock})")
        return UpdateLowStockProducts(
            message="Low-stock products updated.",
            updated_products=updated
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
