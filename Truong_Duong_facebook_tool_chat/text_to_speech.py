import pyttsx3

engine = pyttsx3.init()

vn_id = 'MSTTS_V110_viVN_An'

for voice in engine.getProperty('voices'):
    if vn_id in voice.id:
        engine.setProperty('voice', voice.id)

def handle(message):
    rplc = {
        ' yee ': ' giê... ',
        ' k ': ' không ',
        ' cx ': ' cũng ',
        ' t ': ' tao ',
        ' m ': ' mày ',
        ' ei ': ' ê... ' 
    }
    
    result = ' ' + message.lower() + ' '

    for word in rplc:
        result = result.replace(word, rplc[word])
    
    return result

def say(message):
    engine.say(handle(message))
    engine.runAndWait()

if __name__ == '__main__':
    say('t nè')
    engine.runAndWait()