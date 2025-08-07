import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

DATA_FILE = "articles.json"
UPLOAD_FOLDER = "images"
BASE_URL = os.environ.get("BASE_URL", "https://serveur-marche.onrender.com")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_articles():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_articles(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route("/", methods=["GET"])
def index():
    return "API marche disponible", 200

@app.route("/publish", methods=["POST"])
def publish_article():
    title = request.form.get("title")
    description = request.form.get("description")
    prix = request.form.get("prix")
    devise = request.form.get("devise")
    quantite = int(request.form.get("quantite", 1))
    
    image = request.files.get("image")
    image_url = ""

    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
        image_url = f"{BASE_URL}/images/{filename}"

    article = {
        "title": title,
        "description": description,
        "prix": prix,
        "devise": devise,
        "quantite": quantite,
        "image": image_url
    }

    articles = load_articles()
    articles.append(article)
    save_articles(articles)

    return jsonify({"status": "success", "article": article})

@app.route("/articles", methods=["GET"])
def get_articles():
    articles = load_articles()
    return jsonify(articles)

@app.route("/buy/<int:index>/<string:devise>", methods=["POST"])
def buy(index, devise):
    articles = load_articles()
    if 0 <= index < len(articles):
        if articles[index]["quantite"] > 0:
            articles[index]["quantite"] -= 1
            if articles[index]["quantite"] == 0:
                articles.pop(index)
            save_articles(articles)
            return jsonify({"status": "ok", "message": "Article acheté"})
    return jsonify({"status": "error", "message": "Indisponible"})

@app.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

