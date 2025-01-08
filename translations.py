from dotenv import load_dotenv
from pprint import pprint
import requests
import json
import os
from deep_translator import GoogleTranslator ##yesss this is working translator
from langdetect import detect


#  /usr/bin/python3
# ls -l /usr/local/bin | grep '../Library/Frameworks/Python.framework/Versions/3.11'

load_dotenv()

def get_word(word = "lifeguard"):
    request_url = f'https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key=8a8f2e5c-5576-4889-80df-f56827f54015'

    response = requests.get(request_url)
    response.raise_for_status()  # raises exception when not a 2xx response
    dictionary_data = requests.get(request_url).json() #keep this
    return dictionary_data

def full_translation(input):

    lan = detect(input)

    if lan == "es":
        tr = GoogleTranslator(source="es", target='en').translate(input)
    else:
        tr = GoogleTranslator(source='en', target='es').translate(input)
    return tr

#for debugging, etc
def get_API_dump(word = "lifeguard"):
    request_url = f'https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key=8a8f2e5c-5576-4889-80df-f56827f54015'

    dictionary_data = requests.get(request_url).json()
    print(json.dumps(dictionary_data, indent=2))



if __name__ == "__main__":
    print("translation of no me gusta eso: ", full_translation("no me gusta eso"))

    print('\n*** Get Translation ***\n')

    input = input("\nPlease enter a word to translate: ")

    ### try to use google translator - delete afterwards
    print("attempt to translate:")
    print(full_translation(input))  ##yesss translation works!

    #dump dictionary
    get_API_dump(input)
    dictionary_data = get_word(input) #this is a list


    if type(dictionary_data[0]) == str: #need for certain cases when a dictionary isn't returned but a list of related words to search up
        related_words = []
        for word in dictionary_data:
            related_words.append(word)

    for dictionary in dictionary_data:
        info = f'{dictionary["meta"]["id"]}'

        if "fl" in dictionary:
            info += f' ({dictionary["fl"]})'

        print(info) # meta data, includes id and fl
        print(dictionary['shortdef'])

        if "def" in dictionary:
            print("example sentences: ")

            for obj in dictionary["def"]: #dictionary["def"] is a list (of usually one item lmao), but obj is a dictionary with ONE key (sseq)
                sseq = obj["sseq"] #sseq is a list (list of senses)
                for thing in sseq:
                    dict = thing[0][1] # this type is dictionary
                    #access dt key, then check if includes vis key
                    dt = dict["dt"]
                    for element in dt:
                        if element[0] == "vis":
                            print(f'{element[1][0]["t"]}  >>  {element[1][0]["tr"]}')


        print()


