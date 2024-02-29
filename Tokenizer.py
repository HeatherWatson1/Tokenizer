# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:37:20 2023

@author: Heather Watson
"""
import sys

fullpath = input("Enter full file path to desired.jack file ") 


jackFile = open(fullpath, 'r')

result = open("Tokenized" + ".xml", 'w')
result.write("<tokens>")


text = jackFile.read()


#i = 0
#length = len(text) 
#comment = False
#twoChar = "  "
#text = ("\n".join(text.splitlines()))

Lines = text.splitlines()

#SCUFFED
multiLineComment = False
for aline in Lines:
    aline = aline.lstrip() #remove leading white space
    if multiLineComment == True:
        if aline.endswith("*/") == True:
            multiLineComment = False #end of multiple line comments.
            pass 
        else:
            multiLineComment = True
            pass
    elif aline[0:2] == "//":
        pass #ignore single line comments
    elif aline[0:2] == "/*":
        if aline.endswith("*/") == True:
            multiLineComment = False
            pass
        else:
            multiLineComment = True
            pass
    elif len(aline) == 0:
        pass
    else:
        aword = aline.split(" ")
        #print(aword)
        if len(aword) != 0:
            i = 0
            while i < len(aword):
                if aword[i] == "class" or aword[i] == "constructor" or aword[i] == "method" or aword[i] == "function" :
                    result.write("\n<keyword> " + aword[i] + " </keyword>")
                    print("\n<keyword> " + aword[i] + " </keyword>")
                elif aword[i] == "int" or aword[i] == "boolean" or aword[i] == "char" or aword[i] == "void" or aword[i] == "var" or aword[i] == "do":
                    result.write("\n<keyword> " + aword[i] + " </keyword>")
                    print("\n<keyword> " + aword[i] + " </keyword>")
                elif aword[i] == "static" or aword[i] == "field" or aword[i] == "let" or aword[i] == "if" or aword[i] == "else":
                    result.write("\n<keyword> " + aword[i] + " </keyword>")
                    print("\n<keyword> " + aword[i] + " </keyword>")
                elif aword[i] == "while" or aword[i] == "return" or aword[i] == "true" or aword[i] == "false" or aword[i] == "null" or aword[i] == "this":
                    result.write("\n<keyword> " + aword[i] + " </keyword>")
                    print("\n<keyword> " + aword[i] + " </keyword>")
                elif aword[i] == "(" or aword[i] == ")" or aword[i] == "[" or aword[i] == "]" or aword[i] == "{" or aword[i] == "}" or aword[i] == ";" or aword[i] == "=":
                    result.write("\n<symbol> " + aword[i] + " </symbol>")
                    print("\n<symbol> " + aword[i] + " </symbol>")
                elif aword[i] == "." or aword[i] == "+" or aword[i] == "*" or aword[i] == "/" or aword[i] == "&" or aword[i] == "|" or aword[i] == "~" or aword[i] == "<" or aword[i] == ">":
                    if aword[i] == "<":
                        aword[i] = "&lt;"
                    result.write("\n<symbol> " + aword[i] + " </symbol>")
                    print("\n<symbol> " + aword[i] + " </symbol>")
                elif aword[i] == "//":
                    while i < len(aword):
                        i=i+1
                elif aword[i].find('"') != -1:
                    #split the word at the " and process before the "
                    index = aword[i].find('"')
                    theWord = aword[i]
                    letterlist = []
                    for aletter in theWord[0:index]:
                        if aletter.isalpha():
                            letterlist.append(aletter)
                        elif aletter != '"':
                            #print current letter list and reset
                            if len(letterlist) != 0:
                                result.write("\n<identifier> " + "".join(letterlist) +" </identifier>" )
                                print("\n<identifier> " + "".join(letterlist) +" </identifier>" )
                            letterlist = []
                            #now print symbol
                            if aletter == "<":
                                aletter = "&lt;"
                            result.write("\n<symbol> " + aletter + " </symbol>")
                            print("\n<symbol> " + aletter + " </symbol>")
                    
                    #process 2nd half
                    end = len(theWord)
                    slist = []
                    slist.append(theWord[index+1:end])
                    i = i+1
                    
                    while i < len(aword) and aword[i].find('"') == -1:
                        slist.append(aword[i])
                        i=i+1
                    result.write("\n<stringConstant> " + " ".join(slist) +" </stringConstant>" )  
                    print("\n<stringConstant> " + " ".join(slist) +" </stringConstant>")
                    
                    nextWord = aword[i]
                    for aletter in nextWord[0:index]:
                        if aletter.isalpha():
                            letterlist.append(aletter)
                        elif aletter != '"':
                            #print current letter list and reset
                            if len(letterlist) != 0:
                                result.write("\n<identifier> " + "".join(letterlist) +" </identifier>" )
                                print("\n<identifier> " + "".join(letterlist) +" </identifier>" )
                            letterlist = []
                            #now print symbol
                            result.write("\n<symbol> " + aletter + " </symbol>")
                            print("\n<symbol> " + aletter + " </symbol>")
                    
                    
                else:
                    if aword[i].isalpha():
                        result.write("\n<identifier> " + aword[i] +" </identifier>" )
                        print("\n<identifier> " + aword[i] +" </identifier>" )
                    else:
                        letterlist = []
                        numlist = []
                        count = 1
                        for aletter in aword[i]:
                            
                            length = len(aword[i])
                            
                            if aletter.isalpha() and count == length:
                                letterlist.append(aletter)
                                if len(letterlist) != 0:
                                    result.write("\n<identifier> " + "".join(letterlist) +" </identifier>" )
                                    print("\n<identifier> " + "".join(letterlist) +" </identifier>" )
                            
                            if aletter.isalpha():
                                letterlist.append(aletter)
    
                            elif aletter.isnumeric():
                                numlist.append(aletter)
                            else:
                                #print current letter list and reset
                                if len(letterlist) != 0:
                                    keyCheck = "".join(letterlist)
                                    if keyCheck == "class" or keyCheck == "constructor" or keyCheck == "method" or keyCheck == "function" or keyCheck == "int" or keyCheck == "boolean" or keyCheck == "char" or keyCheck == "void" or keyCheck == "null" or keyCheck == "this":
                                        result.write("\n<keyword> " + "".join(letterlist) +" </keyword>" )
                                        print("\n<keyword> " + "".join(letterlist) +" </keyword>" )
                                    elif keyCheck == "var" or keyCheck == "do" or keyCheck == "static" or keyCheck == "field" or keyCheck == "let" or keyCheck == "if" or keyCheck == "else" or keyCheck == "while" or keyCheck == "return" or keyCheck == "true" or keyCheck == "false" :
                                        result.write("\n<keyword> " + "".join(letterlist) +" </keyword>" )
                                        print("\n<keyword> " + "".join(letterlist) +" </keyword>" )
                                    else:
                                        result.write("\n<identifier> " + "".join(letterlist) +" </identifier>" )
                                        print("\n<identifier> " + "".join(letterlist) +" </identifier>" )
                                    letterlist = []
                                elif len(numlist) != 0:
                                    result.write("\n<integerConstant> " + "".join(numlist) +" </integerConstant>" )
                                    print("\n<integerConstant> " + "".join(numlist) +" </integerConstant>" )
                                    numlist=[]
                                
                                #now print symbol
                                if aletter == "<":
                                    aletter = "&lt"
                                result.write("\n<symbol> " + aletter + " </symbol>")
                                print("\n<symbol> " + aletter + " </symbol>")
                            
                            count = count + 1
                    
                        
                    
                    
                
                    #print(aword[i])
                    #letterlist = [ ]
                    #for aletter in aword:
                    #    letterlist.append(aletter)
                    #print(letterlist)
                    #result.write("\n\t<stringConstant> " + aword[i] + " </stringConstant>")
                i=i+1
        
    
    
        
 
   

jackFile.close()

result.write("\n</tokens>")
result.close()

sys.exit()