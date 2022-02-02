from flask import Flask, Response, request, abort

from database.mongodb import MongoDB

from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors)

connection = MongoDB.get_connection()
db = connection.newsarticles


@app.route("/all", methods=["GET"])
def all_news():
    if 'page' in request.args:
        page = request.args.get("page")
        if page.isnumeric() and int(page) > 0:
            page = int(page)
        else:
            abort(400, "Page number must be an interger and greater than 0")
    else:
        abort(400, "Page number must be specified")
    cursor = db.articles.find({}).skip((page - 1) * 10).limit(20)
    data = []

    for article in cursor:
        article["_id"] = str(article["_id"])
        article.pop("article", None)
        data.append(article)

    return {
        "articles": data,
        "results": len(data),
    }


@app.route("/search", methods=["GET"])
def search():
    return Response("OK", status=200)


@app.route("/health")
def health():
    return Response("OK", status=200)
