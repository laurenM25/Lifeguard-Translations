#btw, use apple's xcode to build app. download on desktop. 
import speech_recognition as sr
import translations

#recognizer + microphone
r = sr.Recognizer()
mic = sr.Microphone()

#capture mic input
def getAudio():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        return audio

#process audio
def processAudio(audio):
    return r.recognize_google(audio)

#print out audio
def askQuestion():
    sample = processAudio(getAudio())
    return sample
    #print(sample)

def findSpanishSuggestions(input):
    keys = translations.findInEnglishValues(input)
    return translations.spanishMatches(keys)

def main():
    translations.get_API()
    question = askQuestion()
    suggestions = findSpanishSuggestions(question)
    print(suggestions)

main()