from flask import Flask, Response, request, abort

from database.mongodb import MongoDB

from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors)

connection = MongoDB.get_connection()
db = connection.newsarticles

# Get all articles
cursor = db.articles.find()
# Sort by date
cursor.sort("date", -1)
# Convert to list
articles = list(cursor)

# Remove the image field from each article
for article in articles:
    article.pop("image")
    article.pop("_id")
    article.pop("content")
    article.pop("keywords")



@app.route("/latest", methods=["GET"])
def latest_news():
    # Get the page number from the query string
    if 'page' in request.args:
        page = request.args.get("page")
        if page.isnumeric() and int(page) > 0:
            page = int(page)
        else:
            abort(400, "Page number must be an interger and greater than 0")
    else:
        abort(400, "Page number must be specified")

    # Get articles by the page number
    data = articles[(page - 1) * 10:page * 10]
    

    return {
        "articles": data,
        "results": len(data),
    }


@app.route("/health")
def health():
    return Response("OK", status=200)
