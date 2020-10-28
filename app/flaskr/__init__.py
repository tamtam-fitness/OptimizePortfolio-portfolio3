from flask import Flask

def create_app():
    """Flaskのappを作成する関数"""
    from flaskr.views import bp
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(bp)
    return app