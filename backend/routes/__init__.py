from flask import Blueprint
from .user_routes import user_routes
from .feedback_routes import feedback_routes
from .conversation import conversation_routes
from .message import message_routes
from .embed import embed_routes
from .chat import chat_routes
from .course import course_routes
from .file import file_routes

# Create a Blueprint for all routes
api_routes = Blueprint("api", __name__)

# Register individual route files
api_routes.register_blueprint(user_routes)
api_routes.register_blueprint(feedback_routes)
api_routes.register_blueprint(conversation_routes)
api_routes.register_blueprint(message_routes)
# api_routes.register_blueprint(embed_routes)
api_routes.register_blueprint(chat_routes)
api_routes.register_blueprint(course_routes)
api_routes.register_blueprint(file_routes)