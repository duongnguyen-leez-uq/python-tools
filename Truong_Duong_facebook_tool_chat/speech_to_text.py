import io
import keyboard
import _thread
import speech_recognition as sr  

class SpeechToText:
    def __init__(self, key, callback, params=()):                                                                  
        self.r = sr.Recognizer()         
        self.key = key
        self.callback = callback
        self.params = params

    def record_when_hold(self):
        with sr.Microphone() as source:
            frames = io.BytesIO()
            
            while keyboard.is_pressed(self.key):
                buffer = source.stream.read(source.CHUNK)

                frames.write(buffer)

            frame_data = frames.getvalue()
            frames.close()
            
            return sr.AudioData(frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)

    # start recording and recogizing if hold 'key'
    # params is a tuple of parameters
    # call callback(result, *params) after each recognized speech
    def recognize_once(self):
        if keyboard.is_pressed(self.key):
            print("Speak:")                                                                
            audio = self.record_when_hold()

            try:
                result = self.r.recognize_google(audio, language="vi-VN")
                print("You said: " + result)
                self.callback(result, *self.params)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

if __name__ == "__main__":
    recg = SpeechToText('right shift', print)
    
    while 1:
        recg.recognize_once()

    exit()