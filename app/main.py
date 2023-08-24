from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler


schema = Schema()

app = FastAPI()
graphene_app = GraphQLApp(
    on_get=make_graphiql_handler(),
    schema=schema,
)

app.mount("/graphql", graphene_app)