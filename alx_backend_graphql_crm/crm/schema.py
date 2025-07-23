import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello from ALX GraphQL CRM!")

schema = graphene.Schema(query=Query)
