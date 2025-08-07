import os, json, base64
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = "articles.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_articles():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_articles(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route("/publish", methods=["POST"])
def publish_article():
    data = request.get_json()
    articles = load_articles()
    articles.append(data)
    save_articles(articles)
    return jsonify({"status": "success"})

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
