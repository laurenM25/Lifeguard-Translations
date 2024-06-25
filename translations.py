#set up data to compare recording with
f = open("sampleData.txt", encoding="utf-8", mode="a+")
f.seek(0)
lines = f.readlines()
dictionary = {} #key: english    value: spanish
for line in lines:
    englishYspanish = line.split(": ")
    english = englishYspanish[0]
    spanish = englishYspanish[1]
    dictionary.update({english: spanish})

def englishValues():
    return dictionary.keys()

def spanishValues():
    return dictionary.values()

def findInEnglishValues(input):        # my dictionary should really also associate with keywords/topics
    values = englishValues()
    matches = []
    for value in values:
        words = value.split(" ")
        for word in words:
            if input == word:
                matches.append(value) # adds the english key to list
            
    return matches

def spanishMatches(englishKeys):  #given a list of english phrases, finds matching spanish ones
    matches = []
    for key in englishKeys:
        spanish = dictionary.get(key)
        matches.append(spanish)

    return matches