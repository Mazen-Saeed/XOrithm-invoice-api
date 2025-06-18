from ariadne.asgi import GraphQL
from ariadne import load_schema_from_path, make_executable_schema
from .query import query, analytics, account
from .mutation import mutation
from app.db    import SessionLocal

type_defs = load_schema_from_path("app/graphql/schema.graphql")
schema = make_executable_schema(type_defs, query, mutation, analytics, account)

def get_context(request):
    return {"db": SessionLocal()}

graphql_app = GraphQL(
    schema,
    context_value=get_context,
    debug=True
)
