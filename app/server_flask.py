from flask import Flask, jsonify
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    # A simple root route so clicking the base URL doesn't 404
    @app.get("/")
    def index():
        return jsonify({"status": "ok", "message": "Use /health, /generate_gap, /generate_manuscript"})

    # Return JSON instead of HTML for ANY unhandled error
    @app.errorhandler(Exception)
    def handle_any_error(e):
        # print full traceback to the console running Flask
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    return app

if __name__ == "__main__":
    # debug=False → no pink debugger page, just JSON via handler above
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
