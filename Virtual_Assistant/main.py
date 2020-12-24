"""
Goals:
Can it run math quickly? -> Kinda uses Wolfra-maplha
Can it connect to API -> yep 2
Any chatting capabilities - maybe an option to text to virtual assistant as well as text it?
Speech to Text then Text to Speech
Connect to my electronic perhaps
It needs to be a fast virtual assistant e.g. can do math quickly/ can answer
Maybe search up Virtual Assistant tutorials>


"""
from gtts import gTTS
import pyttsx3
from sys import argv
import wolframalpha
import webbrowser
import time
import playsound
import speech_recognition as sr
import os
import datetime
import warnings
import calendar
import random
from youtubesearchpython import SearchVideos
from nltk import tokenize
import wikipediaapi

# ignore warnings
warnings.filterwarnings('ignore')
adjusted_noise = False
OFFLINE = True
AWAKE = False



def record_audio(query=None):
    # recogniser object
    global adjusted_noise  # use global variable
    rec = sr.Recognizer()

    # open mic and start recording
    with sr.Microphone() as source:
        if not adjusted_noise:
            rec.adjust_for_ambient_noise(source)
            #  print('ADJUSTED FOR NOISE')
            adjusted_noise = True
        if query:
            print(query)
        else:
            print("How can I help?")
        audio = rec.listen(source)
        data = ''
        try:
            data = rec.recognize_google(audio)
            print(f"You said {data}")
        except sr.UnknownValueError:
            print("Google speech recognition could not understand the audio, unknown error")
        except sr.RequestError as e:
            print("Request results from Google Speech Recognition Server error" + str(e))
        # return what we said as a string
        return data


def virtual_response_offline(audio_string):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio_string)
    engine.runAndWait()


def virtual_response(audio_string):
    global OFFLINE
    if OFFLINE:
        print(audio_string)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(audio_string)
        engine.runAndWait()
    else:
        myObj = gTTS(text=audio_string, lang='en', slow=False)
        r = random.randint(1, 10000000)
        audio_file = 'audio-' + str(r) + '.mp3'
        #  save converted audio to a file
        myObj.save(audio_file)
        playsound.playsound(audio_file)
        os.remove(audio_file)


def wake_word(text):
    WAKE_WORDS = ['hey eve', 'eve']
    text = text.lower()  # converting text to lowercase
    # check for phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    # if wake word isn't found, return false
    return False


def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    month_num = now.month
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    day_num = now.day
    ordinal_subscript = ['st', 'nd', 'rd', 'th']
    if day_num == 1 or day_num == 21 or day_num == 31:
        date = str(day_num) + ordinal_subscript[0]
    elif day_num == 2 or day_num == 22:
        date = str(day_num) + ordinal_subscript[1]
    elif day_num == 3 or day_num == 23:
        date = str(day_num) + ordinal_subscript[2]
    else:
        date = str(day_num) + ordinal_subscript[3]
    return f'Today is {weekday}, {date}  {months[month_num - 1]} {now.year}'


def greeting(text):
    # Greeting inputs
    GREETING_INPUTS = ['hello', 'hey', 'hi', 'wassup', 'whats good']

    # Greeting response
    GREETING_RESPONSES = ['howdy', 'hi', 'hello', 'hey']

    # If users input is a greeting, then return a randomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return (random.choice(GREETING_RESPONSES)).capitalize() + '! '

    # If no greeting was detected
    return ''


def getPerson(text):
    wordList = text.split()  # splits the text to words
    print(len(wordList))
    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + '_' + wordList[i + 3]


def get_sentences(text, sen=2):
    strings = tokenize.sent_tokenize(text)
    strings = [strings[x] for x in range(sen)]
    return strings


def get_video(message, n=1):
    search = SearchVideos(message, offset=1, mode="dict", max_results=2)
    search = search.result()
    result = [str(search['search_result'][0]['title']), str(search['search_result'][0]['link'])]
    return result


# API
app_id = "PH9HTQ-3YEV3KQ3TW"
client = wolframalpha.Client(app_id)

argc = len(argv)
print(argc)
if argc != 1 and argc != 2:
    print("Usage: filename [mode]")
    exit()

while True:
    text = record_audio()
    join_words = ['and', 'not', 'or', 'but']
    for word in join_words:
        text = text.replace(word, '')  # remove joining words
    if 'what is your name' in text:
        virtual_response(greeting(text) + 'My name is Eve')
    # check for the wake word / phrase
    if wake_word(text) or AWAKE:
        AWAKE = True
        text = text.replace('and', '')  # remove and or
        text = text.replace('or', '')
        # check to see if the user has said anything about data
        if 'search' in text:
            search = record_audio('What would you like to search for')
            url = 'https://www.google.co.uk/search?q=' + search
            webbrowser.get().open(url)
            virtual_response('Here is what I found for: ' + search.capitalize())
        if 'find location' in text or "find a location" in text:
            location = record_audio('What is the locations?')
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            virtual_response('Here is the location of: ' + location.capitalize())
        # check to see if the user said 'who is'
        if 'who is' in text or "who's" in text:
            if "who's" in text:
                new_text = text.split("who's", 1)[1]
            else:
                new_text = text.split('who is', 1)[1]
            print(new_text.strip())
            wiki_wiki = wikipediaapi.Wikipedia('en')
            page_py = wiki_wiki.page(new_text)
            if page_py.exists():
                print("Page - Title: %s" % page_py.title)
                wiki = ' '.join(map(str, get_sentences(page_py.summary, sen=2)))  # convert list to string for display
                print("Page - Summary:")
                virtual_response(wiki)
        if 'what is' in text or "what's" in text:
            try:
                if 'what is the date today' in text or "what's the date today" in text:
                    date = getDate()
                    virtual_response(date)
                    if 'what is the date today' in text:
                        text = text.replace('what is the date today', '')
                    else:
                        text = text.replace("what's the date today", '')
                if 'what is' in text:
                    new_text = text.split('what is', 1)[1]
                    print(new_text.strip())
                else:
                    new_text = text.split("what's", 1)[1]
                    print(new_text.strip())
                virtual_response('Asking Wolfram Alpha...')
                res = client.query(new_text)
                wolf_ans = next(res.results).text
                virtual_response("The answer is " + wolf_ans)
            except:
                print("Error. Can't query to Wolframaplha API.")
        if 'find video' in text:
            video_query = record_audio('What video would you like me to find?')
            result = get_video(video_query)
            print(f"Title {result[0]}\n Link: {result[1]}")
            virtual_response("Here are the results: ")
            response = record_audio("Would you like me to open the link?")
            if 'yes' in response:
                webbrowser.get().open(result[1])
                virtual_response('Here is the video: ')
            elif 'no' in response:
                virtual_response('okay')
        if 'I want to play a game' in text:
            virtual_response('What game would you like to play? I can play Pong Or Mario')
            video_query = record_audio('Listening...')
            if 'pong' in video_query.lower():
                os.system('love Pong')
            elif 'mario' in video_query.lower():
                os.system('love Mario')
            else:
                virtual_response('Sorry! I can only play Mario Or Pong!')
            virtual_response('Exited!')
            time.sleep(1)

    if 'exit' in text:
        exit(0)
        # assistant respond back using audio and text from response
