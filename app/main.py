from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from app.db.db import init_db

from app.gql.mutations import Mutation
from app.gql.queries import Query


schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()
graphene_app = GraphQLApp(
    on_get=make_graphiql_handler(),
    schema=schema,
)

@app.on_event("startup")
def on_start():
    init_db()
    

app.mount("/graphql", graphene_app)