import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from form import TextForm
from flask import Flask, render_template, abort, request, session

DATA_JSON_FILE = '01_Processing/email-text-data.json'
data = pd.read_json(DATA_JSON_FILE)
data.sort_index(inplace=True)
vectorizer = CountVectorizer(stop_words='english')
all_features = vectorizer.fit_transform(data.MESSAGE)
X_train, X_test, y_train, y_test = train_test_split(all_features, data.CATEGORY, test_size=0.3, random_state=88)
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

app = Flask(__name__,template_folder='templates')
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

@app.route("/", methods=["GET", "POST"])
def home_page():
    status = 0
    form = TextForm()
    if form.validate_on_submit():
        message = form.message.data
        lis=[message]
        doc_term_matrix = vectorizer.transform(lis)
        if classifier.predict(doc_term_matrix)[0] == 0:
            status = 1
        else:
            status = 2
        return render_template('index.html', form=form, status=status)
    return render_template("index.html", form=form, status=status)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)