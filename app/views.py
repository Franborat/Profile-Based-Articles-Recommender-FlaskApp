from app import app

from flask import render_template

from flask import request, redirect

import pickle
from sklearn import svm
import re
from nltk.stem import PorterStemmer

@app.route("/")
def index():
    return render_template("/public/index.html")

@app.route("/about")
def about():
    return render_template("/public/about.html")

@app.route("/upload_doc", methods=["GET", "POST"])
def upload_doc():

    if request.method == "POST":

        document = request.form
        title = document.get("title")
        body = document["body"]

        # Detect if any of the fields is missing, and if it is, send out an alarm for corrertly fill the form
        missing = list()

        for k, v in document.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/upload_doc.html", feedback=feedback)

        # 1st: Get the doc to process in a list
        corpus = list()
        corpus.append(body)

        # 2nd: Load our tools

        # picke - loading
        with open('app/model/model.pickle', 'rb') as f:
            model = pickle.load(f)

        with open('app/model/vectorizer.pickle', 'rb') as f:
            vectorizer = pickle.load(f)

        with open('app/model/tfidfconverter.pickle', 'rb') as f:
            tfidfconverter = pickle.load(f)

        # Functions:

        def stem(corpus):
            stemmer = PorterStemmer()
            stem_corpus=[' '.join([stemmer.stem(word) for word in text.split(' ')]) for text in corpus]
            no_numbers_corpus = [re.sub(r'\d+', '', text) for text in stem_corpus ]
    
            return no_numbers_corpus

        # 3rd: Process the document

        text_stem = stem(corpus)
        text_bow  = vectorizer.transform(text_stem)
        text_tfidf = tfidfconverter.transform(text_bow)

        result = model.predict(text_tfidf)
        result_clean = result[0]

        return render_template("public/upload_doc.html", result_clean=result_clean)

        print(type(corpus))

        return redirect(request.url)

    return render_template("/public/upload_doc.html")



