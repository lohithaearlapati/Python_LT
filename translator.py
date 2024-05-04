from tkinter import *
import googletrans
import textblob
import pyttsx3

from tkinter import ttk,messagebox



root=Tk()
root.title('MY APP')
root['bg']='black'
root.geometry("950x300+300+200")

def translate_it():
    #delete any previous translation
    translated_text.delete(1.0,END)
    try:
     
        #get languages from dictionary keys 
        #get the from language key
         for key, value in languages.items():
            if(value == original_combo.get()):
                from_language_key = key
           

         for key,value in languages.items():
            if(value == translated_combo.get()):
                to_language_key = key

          #turn original text into a textblob     
            words = textblob.TextBlob(original_text.get(1.0,END))



           #translate text    
         words = words.translate(from_lang = from_language_key , to = to_language_key)

         #Initialize speech engine
         engine = pyttsx3.init()

         #play with voices
         voices = engine.getProperty("voices")
         #for voice in voices:
            # engine.setProperty('voice ' , voice.id)
             #engine.say(words)


         #Pass text to speech engine
         engine.say(words)  

         #run the engine
         engine.runAndWait()
         #output translated text to screen
         translated_text.insert(1.0, words)

    except Exception as e:
        messagebox.showerror("Translator",e)
        


def clear():
    #clear the textboxes
    original_text.delete(1.0,END)
    translated_text.delete(1.0,END)

#grab language list from googletrans
languages=googletrans.LANGUAGES

language_list=list(languages.values())
print(language_list)

#text boxes 
original_text= Text(root,height=10,width=40)
original_text.grid(row=0,column=0,pady=20,padx=10)

translate_button = Button(root,text="TRANSLATE!",font=("HELVECTICA",24),command=translate_it)
translate_button.grid(row=0,column=1,padx=10)

translated_text= Text(root,height=10,width=40)
translated_text.grid(row=0,column=2,pady=20,padx=10)

#comboboxes
original_combo=ttk.Combobox(root,width=50,value=language_list)
original_combo.current(21)
original_combo.grid(row=1,column=0)



translated_combo=ttk.Combobox(root,width=50,value=language_list)
translated_combo.current(26)
translated_combo.grid(row=1,column=2)

#clear button
clear_button=Button(root,text="CLEAR",command=clear)
clear_button.grid(row=2,column=1)





root.mainloop()