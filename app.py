from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

app = Flask(__name__)

# Load the dataset
dataset = pd.read_csv('dark.csv')
dataset = pd.read_csv('dark_patterns.csv')
dataset = pd.read_csv('normie.csv')

# Separate features (X) and target variable (y)
X_train = dataset['text']
y_train = dataset['Pattern Category']

# Create a pipeline with TfidfVectorizer and SVC
model = make_pipeline(TfidfVectorizer(), SVC())

# Fit the model with the training data
model.fit(X_train, y_train)


def download_file(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(folder, os.path.basename(url))
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {url}")
        return filename
    else:
        print(f"Failed to download: {url}")
        return None


def extract_html_and_js(url, output_folder):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract HTML and JS content here (customize based on your needs)
        # For example, you might want to extract text from certain HTML elements
        # and then use the model for prediction
        text_to_predict = " ".join([p.get_text() for p in soup.find_all('p')])
        prediction = model.predict([text_to_predict])[0]
        return prediction
    else:
        print(f"Failed to extract HTML and JS from: {url}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        url = request.form['url']
        output_folder = 'downloads'  # You can customize this folder
        downloaded_file = download_file(url, output_folder)
        if downloaded_file:
            result = extract_html_and_js(url, output_folder)
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Failed to download the file'})


if __name__ == '__main__':
    app.run(debug=True)
