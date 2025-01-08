from flask import Flask, render_template, request
from translations import get_word, full_translation
from waitress import serve
import logging

app = Flask(__name__)

@app.route('/')
@app.route('/homepage')
def index():
    return render_template('homepage.html')

@app.route('/fullTrans')
def full_Translation():
    #this is where it is
    word = request.args.get('word')
    if word == "":
        print("this word is empty! handle this case and make it stay on the page it was on")
    
    FT = full_translation(word) ## this is full translation of user input (googletrans akin)
    FT_split_list = FT.strip(",?¿.").split()
    split_list_w_definitions = {}
    for ele in FT_split_list:
        key_value = get_dictionary_entry(ele)
        split_list_w_definitions[key_value[0]] = key_value[1]
    split_list_w_definitions = refine_entries(split_list_w_definitions)
    return render_template(         #this is notttt correct idk how to get to this webpage
        'fullTrans.html', word = word, fullTrans = FT, fullTransSplit = FT_split_list, wordAndDefs = split_list_w_definitions)


@app.route('/translation')
def get_translation():
    word_input = request.args.get('word')
    dictionary_data = get_word(word_input) #this is a list

    if type(dictionary_data[0]) == str:
        related_words = []
        for word in dictionary_data:
            related_words.append(word)
        return render_template('suggestions.html', term = word_input, words = related_words) #dif template with suggestions

    dict_list = {}
    example_sentences = []

    for dictionary in dictionary_data:
        element1 = dictionary["meta"]["id"]
        if "fl" in dictionary:
            element1 += f' ({dictionary["fl"]})'
        element2 = dictionary['shortdef']
        dict_list[element1] = element2

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

    dict_list = refined_1d_dictionary(dict_list)
    return render_template(
        'translation.html',
        word = word_input,
        definitions = dict_list,
        examples = example_sentences)


#new function, added jan 6, 2025
def get_dictionary_entry(word):
    dictionary_data = get_word(word) #this is a list

    if type(dictionary_data[0]) == str:
        related_words = []
        for word in dictionary_data:
            related_words.append(word)
        return ("no relevant dictionary entry") #dif template with suggestions

    dict_list = {}

    for dictionary in dictionary_data:
        element1 = dictionary["meta"]["id"]
        if "fl" in dictionary:
            element1 += f' ({dictionary["fl"]})'
        element2 = dictionary['shortdef']
        if dictionary["meta"]["lang"] == "es": #THIS LIMITS TO JUST SPANISH ENTRIES
            dict_list[element1] = element2

    return ([word, dict_list])


def refine_entries(entries): #note: this will return as a dictionary of lists
    refined_dictionary = {}
    for key in entries:
        subkeys = entries[key]

        #format  --   [word, type, definitions]
        #example --  [que, conjunction, ['that', 'than', "the thing is that, I'm afraid that"]]
        byKey_list = []
        for subkey in subkeys:
            endIndex = -1
            if ":" in subkey:
                endIndex = subkey.index(":")
            elif " " in subkey:
                endIndex = subkey.index(" ")
            else:
                endIndex = len(subkey)

            subkey_word = subkey[0:endIndex].strip("'./123456")

            subkey_type = ""
            if "(" in subkey:
                subkey_type = subkey[subkey.index("(")+1:subkey.index(")")]

            subkey_definitions = []
            try:
                subkey_definitions = subkeys[subkey]
            except TypeError:
                logging.warning("subkeys is not a dictionary, therefore cannot be parsed by key values. \nThe dictionary: %s", subkeys)
            byKey_list.append([subkey_word, subkey_type, subkey_definitions])

        refined_dictionary[key] = byKey_list

    return refined_dictionary

def refined_1d_dictionary(dictionary):
    refined_list = []
    for key in dictionary:
        endIndex = -1
        if ":" in key:
            endIndex = key.index(":")
        elif " " in key:
            endIndex = key.index(" ")
        else:
            endIndex = len(key)

        key_word = key[0:endIndex].strip("'./123456")

        key_type = ""
        if "(" in key:
            key_type = key[key.index("(")+1:key.index(")")]
        key_definitions = dictionary[key]
        refined_list.append([key_word, key_type, key_definitions])

    return refined_list

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8000)
    #serve(app, host="0.0.0.0", port=8000)