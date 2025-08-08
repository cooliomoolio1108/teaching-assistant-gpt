from flask import Flask
from flask_cors import CORS
from routes import api_routes
from services.openai_service import get_openai_response
from services.chromadb_service import vector_store
app = Flask(__name__)
CORS(app)

app.register_blueprint(api_routes, url_prefix="/api")

def test_gpt_connection():
    # Minimal test conversation
    messages = [{"role": "user", "content": "Say hello"}]
    try:
        print("🔌 Testing GPT connection...")
        response = get_openai_response(messages)
        print("✅ GPT is working:", response)
    except Exception as e:
        print("❌ GPT connection failed:", str(e))

if __name__ == "__main__":
    # test_gpt_connection()  # Run test BEFORE starting the app
    vector_db = vector_store
    app.run(debug=True, host="localhost", port=5000)
