from flask import Flask, render_template, request
from translations import get_API_dump, get_word
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/translation')
def get_translation():
    word = request.args.get('word')
    dictionary_data = get_word(word) #this is a list
    dict_list = {}
    example_sentences = []

    for dictionary in dictionary_data:
        element1 = dictionary["meta"]["id"]
        if "fl" in dictionary:
            element1 += f' ({dictionary["fl"]})'
        element2 = dictionary['shortdef']
        dict_list[element1] = element2
       # dict_list.update({element1: element2}) #add key value to dictionary (word and shortdef)

        if "def" in dictionary: #example sentence
            for obj in dictionary["def"]: 
                sseq = obj["sseq"] 
                for thing in sseq:
                    dict = thing[0][1] 
                    #access dt key, then check if includes vis key
                    if "dt" in dict:
                        dt = dict["dt"]
                        for element in dt:
                            if element[0] == "vis":
                                example_sentences.append(f'{element[1][0]["t"]}  >>  {element[1][0]["tr"]}') #add sentence to list

    return render_template(
        'translation.html',
        word = word,
        definitions = dict_list,
        examples = example_sentences)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)