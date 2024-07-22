from flask import Flask, render_template, request
import pandas as pd
import textdistance
import re
from collections import Counter


app = Flask(__name__)

# storing each word in list
words = []

with open('autocorrect book.txt', 'r', encoding='utf-8') as f:
    data = f.read().lower()
    words = re.findall(r'\w+', data)
    words += words
    
# get the unique words in the list
V = set(words)    
# counting unique words
word_freq_dict = Counter(words)
# total words
Total = sum(word_freq_dict.values())

probs = {}

# calculating the probability of each unique word
for k in word_freq_dict.keys():
    probs[k] = word_freq_dict[k] / Total
    
@app.route('/')
def index():
    return render_template('index.html', suggestions=None) 

# clicking the suggest
@app.route('/suggest', methods=['POST'])
def suggest():
    # getting the input word from user
    keyword = request.form['keyword'].lower()
    if keyword:
        # find the similarity of a word
        similarities = [1- textdistance.jaccard.distance(v, keyword) for v in word_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df.columns = ['Word', 'Prob']
        df['Similarity'] = similarities # store the similar words similarity in Similarity column
        # sort the words in descending order
        suggestions = df.sort_values(['Similarity', 'Prob'], ascending=False).head(10)[['Word', 'Similarity']]
        # Convert DataFrame to list of dictionaries
        suggestions_list = suggestions.to_dict('records')
        return render_template('index.html', suggestions=suggestions_list)
    

if __name__ == "__main__":
    app.run(debug=True)    
        
