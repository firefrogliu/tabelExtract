from autocorrect import spell
import re
spell_check_white_list = ["H/", "h/"]
timeTimeZoneRe = "((\d|o|O){4})(lt|LT|Lt|lT)" #some zeors are miss detected into O
timeRe = "(\d|o|O){4}"
timeReFront = "^\d{2}"
timeReBack = "\d{2}$"
eightToBRe = "(\d|B|b|O|o){2,3}:(\d|B|b|O|o){2,3}"
timeWithSplash = "(\d|'){2,3}:(\d|'){2,3}"
O = "o|O"
B = "B|b"
Splash = "'"

TtoColonRe = "(\d|b|B|o|O){2}(t|T)(\d|b|B|o|O){2}"
T = "t|T"
oneToColonRe = "(\d|b|B|o|O){2}(1)(\d|b|B|o|O){2}"
one = "1"

Ire = "^(I|i)$"

months = "(jan|feb|mar|apr|may|jun|jly|aug|sep|oct|nov|dec)"
dateRe = "\d{1,2}-"+months+"-\d{1,2}"

def isDate(word):
    print("im here")
    if re.match(dateRe,word):
        print(word,"is date")
        return True
    else:
        print(word,"is not date")
        return False

    
def removeI(word):
    if re.match(Ire,word):
        word = ""
    return word

def change1toColon(word):
    if re.match(oneToColonRe,word):
        print("change 1 to : in",word)
        timeHour = re.search(timeReFront,word)[0]
        timeMin = re.search(timeReBack,word)[0]
        word = timeHour + ":"+timeMin
    return word

def changeTtoColon(word):
    if re.match(TtoColonRe,word):
        print("change T to : in",word)
        word = re.sub(T,":",word)
    return word

def removeTimeSpash(word): #remove ' in 11:15    
    if re.match(timeWithSplash,word):
        print("removing ' in",word)
        word = re.sub(Splash,"",word)
    return word

def eightToBCheck(word):
    if re.match(eightToBRe,word):
        print("change B to 8, O to 0 in",word)
        word = re.sub(O,"0",word)
        word = re.sub(B,"8",word)
    return word

def spellCheck(sentence):
    words = sentence.split()
    new_words = []

    misspelled = words

    for word in misspelled:
        in_white_list = False
        for white_word in spell_check_white_list:
            if re.match(white_word,word):
                in_white_list = True
        
        new_word = word
        wordOri = word
        if not in_white_list:    
            word = removeI(word)
            print("after remove i",word)
            word = change1toColon(word)
            word = changeTtoColon(word)
            word = eightToBCheck(word)
            word = removeTimeSpash(word)
            if word == "":
                new_word = word
            else:        
                new_word = spell(word)
            if new_word != wordOri:
                print("altered", word,'to',new_word)
        new_words.append(new_word)
    return " ".join(new_words)

def timeTimeZoneToTime(sentence):
    words = sentence.split()
    new_words = []
    for word in words:
        #print(word)
        new_word = word
        if re.search(timeTimeZoneRe,word):                       
            #print(word,"match",timeTimeZoneRe)
            #print("find  all", timeRe,word)
            time = re.search(timeRe,word)[0]
            #print('time',time)
            #time = time[0]           
            time = re.sub(O,"0",time)
            #print("time",time)
            timeHour = re.search(timeReFront,time)[0]
            timeMin = re.search(timeReBack,time)[0]
            new_word = timeHour + ":"+timeMin
        
        new_words.append(new_word)

    return " ".join(new_words)


if __name__ == "__main__":
    sentence = "12-feb-12"
    #sentence1 = "COMMENCED discharge from 10:00 to 20:00"
    #times = find_time(sentence)
    #creat_dependency_tree(sentence)
    #
    #print('duration', cal_duration(times[0], times[1]),'hours')
    # print("key event",key_event(sentence))
    # print("laytime cause",get_laytime_cause(sentence))
    # print("non laytime cause", get_non_laytime_cause(sentence))
    # print("start,end,duration,event,laytime_cause,non_laytime_cause",get_sentence_info(sentence))
    # print("start,end,duration,event,laytime_cause,non_laytime_cause",get_sentence_info(sentence1))
    #print(timeTimeZoneToTime(sentence.lower()))
    print("im here")
    isDate(sentence)

    #print("spell white space ",spell(" "))