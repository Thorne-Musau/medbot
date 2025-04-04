# Import route modules to make them available when importing from api.routes
from . import auth
from . import chat
from . import diagnosis

# Export the routers for easier imports
auth_routes = auth.router
chatbot_routes = chat.router
diagnosis_routes = diagnosis.router 