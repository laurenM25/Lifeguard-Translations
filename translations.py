from dotenv import load_dotenv
from pprint import pprint
import requests
import json
import os

load_dotenv()

#APIIII
def get_API_dump(word = "lifeguard"):
    request_url = f'https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key={os.getenv("API_KEY")}'

    dictionary_data = requests.get(request_url).json()
    print(json.dumps(dictionary_data, indent=2))

def get_word(word = "lifeguard"):
    request_url = f'https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key={os.getenv("API_KEY")}'

    dictionary_data = requests.get(request_url).json()
    return dictionary_data

### trying things out

if __name__ == "__main__":
    print('\n*** Get Translation ***\n')

    input = input("\nPlease enter a word to translate: ")
    get_API_dump(input)
    dictionary_data = get_word(input) #this is a list

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

    #word = dictionary_data["id"]
    #definitions = dictionary_data["shortdef"]

    #print(word)
    #print(definitions)

