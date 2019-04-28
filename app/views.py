from app import app

from flask import render_template

from flask import request, redirect

@app.route("/")
def index():
    return render_template("/public/index.html")

@app.route("/about")
def about():
    return render_template("/public/about.html")

@app.route("/upload_doc", methods=["GET", "POST"])
def upload_pic():

    if request.method == "POST":

        document = request.form

        # Detect if any of the fields is missing, and if it is, send out an alarm for corrertly fill the form
        missing = list()

        for k, v in document.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/upload_doc.html", feedback=feedback)

        title = document.get("title")
        body = document["body"]

        print(document)
        print(title)
        print(body)

        return redirect(request.url)

    return render_template("/public/upload_doc.html")



