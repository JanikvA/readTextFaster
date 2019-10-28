#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import time

def getListOfWords(inputS:str):
    # Replace newlines (\n) with spaces
    tmpS=inputS.replace("\n"," ")
    #Word Definition
    listOfWords=tmpS.split(" ")
    # Filter word list for empty elements
    listOfWords= [e for e in listOfWords if e is not '']
    return listOfWords

class Application(tk.Frame):
    wpm=300
    listOfWords=None
    def __init__(self, master):
        super().__init__(master)
        self.master=master
        self.grid()
        self.create_widgets()
        self.currentWord=0
        self.stopIt=False
        if Application.listOfWords==None:
            Application.listOfWords=getListOfWords(self.master.clipboard_get())
            print("Reading every thing will take",len(Application.listOfWords)/Application.wpm*60, "seconds")


        self.master.bind("j", lambda event: self.start())
        self.master.bind("k", lambda event: self.stop())
        self.master.bind("l", lambda event: self.goBack())
        self.master.bind('q', lambda event: self.master.destroy())

    def create_widgets(self):
        self.readThis=tk.Label(self)
        self.readThis["fg"]="black"
        self.readThis["bg"]="white"
        self.readThis["text"]="READ"
        self.master.update()
        self.readThis.grid()

    def showWords(self, startIndex:int):
        self.stopIt=False
        for word in Application.listOfWords[startIndex:]:
            if self.stopIt:
                break
            self.readThis["text"]=word
            self.master.update()
            self.currentWord+=1
            time.sleep(60/Application.wpm)
        self.currentWord=0

    def start(self):
        self.stopIt=False
        self.showWords(self.currentWord)

    def stop(self):
        self.stopIt=True

    def goBack(self, words=10):
        #FIXME i think this always creates a new process of showWords. should handle this better
        self.stopIt=True
        self.currentWord=self.currentWord-words
        if self.currentWord<0:self.currentWord=0
        self.showWords(self.currentWord)
        
        
        
        


def main(args):
    stringToBeRead=""
    root=tk.Tk()
    mainApp=Application(root)
    if args.file:
        with open(args.file) as txtFile:
            bigStr=" ".join(txtFile.readlines()) 
            Application.listOfWords=getListOfWords()
    mainApp.mainloop()
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read text faster by minimzing eye movement. Defualt is content of clipboard")
    parser.add_argument("-f", "--file", default=None, help="Text file to be read")
    args = parser.parse_args()
    main(args)
