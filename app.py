
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from sklearn.ensemble import RandomForestClassifier
import re
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


tfidf_loaded_model = pickle.load(open('tfidf.pickle', 'rb'))
rf_loaded_model = pickle.load(open('RandomForest_model.pickle', 'rb'))
le_model = pickle.load(open('Labelencoder_object.pickle', 'rb'))

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method== 'POST':

        a_title = request.form['title']
        a_descrip = request.form['description']

        if a_title == '' and a_descrip == '':
            result= "none"

        else:
            a_title = re.sub('\\n', ' ', str(a_title))  # remove '\\n'
            a_title = re.sub('http://\S+|https://\S+', '', str(a_title))  # remove http links in the text
            a_title = re.sub(r'\d+(\.\d+)?', 'number', str(a_title))  # Replace digits with 'number'
            a_title = re.sub(r'\s+', ' ', str(a_title))  # Replace whitespace between terms with a single space
            a_title = re.sub(r'[^\w\d\s]', '', str(a_title))  # removing special characther like !, |

            a_descrip = re.sub('\\n', ' ', str(a_descrip))  # remove '\\n'
            a_descrip = re.sub('http://\S+|https://\S+', '', str(a_descrip))  # remove http links in the text
            a_descrip = re.sub(r'\d+(\.\d+)?', 'number', str(a_descrip))  # Replace digits with 'number'
            a_descrip = re.sub(r'\s+', ' ', str(a_descrip))  # Replace whitespace between terms with a single space
            a_descrip = re.sub(r'[^\w\d\s]', '', str(a_descrip))  # removing special characther like !, |

            ps = PorterStemmer()

            corpus = []
            clean_data = a_title
            clean_data = clean_data.lower()
            clean_data = clean_data.split()
            clean_data = [ps.stem(word) for word in clean_data if not word in stopwords.words('english')]
            clean_data = ' '.join(clean_data)
            corpus.append(clean_data)

            corpus1 = []
            clean_data = a_descrip
            clean_data = clean_data.lower()
            clean_data = clean_data.split()
            clean_data = [ps.stem(word) for word in clean_data if not word in stopwords.words('english')]
            clean_data = ' '.join(clean_data)
            corpus1.append(clean_data)
            # merge_text=''
            merge_text = corpus + corpus1

            merge_text = ' '.join(merge_text)

            test_data = tfidf_loaded_model.transform([merge_text])

            pred = rf_loaded_model.predict(test_data)

            result = le_model.inverse_transform(pred)

    return render_template('result.html', prediction= result)


if __name__ == '__main__':
    app.run(debug= True)