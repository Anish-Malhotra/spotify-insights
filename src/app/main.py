from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from app.gql.mutations import Mutation
from app.gql.queries import Query
from app.spotify.auth import form_login_url


# GQL Schema
schema = Schema(query=Query, mutation=Mutation)

# Webserver init
app = FastAPI()
graphene_app = GraphQLApp(
    on_get=make_graphiql_handler(),
    schema=schema,
)


# A workaround to redirect to the Spotify OAuth2 page with the requestor's ID set in a cookie for DB insert 
@app.get("/spotify_redirect")
def spotify_redirect(request: Request):
    login_url = form_login_url()
    spotify_user = request.query_params.get("spotify_username")
    
    response = RedirectResponse(url=login_url)
    response.set_cookie(key="spotify_username", value=spotify_user)
    return response


# Callback from the Spotify OAuth page in order to update the user's DB record with their authorization token
@app.get("/spotify_callback")
def spotify_callback(request: Request):
    code = request.query_params.get("code")
    user = request.cookies.get("spotify_username")
    if not code:
        raise Exception("Unable to retrieve code for Spotify authorization")
    
    if not user:
        raise Exception("Unable to determine user to authorize")
    
    result = schema.execute(
        '''
            mutation updateProfile($code: String!, $user: String!) {
                updateProfileWithAuthToken(code: $code, user: $user) {
                    spotifyProfile {
                        userId
                        spotifyUsername
                        authorizationToken
                        tokenExpiry
                    }
                }
            }
        ''',
        variables={'code': code, 'user': user}
    )
    return result.data


# GraphiQL playground
app.mount("/graphql", graphene_app)