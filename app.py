from flask import Flask
from routes.noticias import noticias_bp
from routes.podcasts import podcasts_bp

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Registrar blueprints
app.register_blueprint(noticias_bp)
app.register_blueprint(podcasts_bp)

if __name__ == '__main__':
    app.run(debug=True)
