import spacy
#from spellchecker import SpellChecker

from nltk import Tree
import re
timeRe_local = "\d{1,2}:\d{2}"
en_nlp = spacy.load('en_core_web_sm')

shift_count = 0
shift_start = [] #mark shift start time

events = ["ARRIVAL",'COMMENCED DISCHARGING', 'COMPLETED DISCHARGING','stop loading','resume loading','shift','LOADING SUSPENDED',
            'lOADIND RESUMED', 'lOADIND CONTINUED', 'loading completed']
non_laytime_causes = ['RAIN','BAD WEATHER','shift','DRAFT CHECK','HOLIDAY','WEEKEND','OBSTRUCTED BY CARGO','TAKING EUIPMENT','fog']
laytime_causes = ['LACK OF PREPARE','OUT of ORDER','BLOCK','BROKEN','BROKE DOWN','TRAFFIC JAM','TAKING EQUIPMET','TERMINAL','DRAFT SURVIOR','draft surveyor'
                    'shift','AWAITING BERTHING']


        

def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_, tok.dep_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

# def to_nltk_tree(node):
#     if node.n_lefts + node.n_rights > 0:
#         return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
#     else:
#         return node.orth_

def time_to_seconds(t:str):
    (h, m) = t.split(':')
    result = int(h) * 3600 + int(m) * 60
    return result

def creat_dependency_tree(sentence:str):
    sentence = sentence.lower()
    document = en_nlp(sentence)    
    tree = [to_nltk_tree(sent.root).pretty_print() for sent in document.sents]
    

def find_time(sentence:str):
    time = []
    sentence = sentence.lower()
    document = en_nlp(sentence)    
    for token in document:
        #print(token,token.lemma_,token.tag_)
        if token.tag_ == 'CD':    
            if re.match(timeRe_local,token.lemma_):
                time.append(token.lemma_)
    #print("time",time)
    return time

def cal_duration(start:str, end:str):
    start_sec = time_to_seconds(start)
    end_sec = time_to_seconds(end)
    if start_sec > end_sec:
        return (start_sec - end_sec)/60  
    else:
        return (end_sec - start_sec)/60

def start_time(sentence:str):
    time = find_time(sentence)
    if len(time) > 1:
        start = time[0]
        end = time[1]
        start_sec = time_to_seconds(start)
        end_sec = time_to_seconds(end)
        if start_sec < end_sec:
            return start
        else:
            return end
    elif len(time) == 1:
        return time[0]
    else:
        return None

def end_time(sentence:str):
    time = find_time(sentence)
    if len(time) > 1:
        start = time[0]
        end = time[1]
        start_sec = time_to_seconds(start)
        end_sec = time_to_seconds(end)
        if start_sec < end_sec:
            return end
        else:
            return start
    elif len(time) == 1:
        return None
    else:
        return None
    
def sentence_contain(events):
    pass

def key_event(sentence:str):
    doc = en_nlp(sentence.lower())
    for event in events:
        event_doc  = en_nlp(event.lower())
        event_lemmas = [ token.lemma_ for token in event_doc]
        doc_lemmas = [token.lemma_ for token in doc]
        #print("event lammas", event_lemmas)
        #print("doc lemams", doc_lemmas)
        eventInDoc = True
        for event_lemma in event_lemmas:
            if not (event_lemma) in doc_lemmas:
                eventInDoc = False

        if eventInDoc:
            return event
    return None

def get_laytime_cause(sentence:str):
    doc = en_nlp(sentence.lower())
    for laytime_cause in laytime_causes:
        laytime_cause_doc  = en_nlp(laytime_cause)
        laytime_cause_lemmas = [token.lemma_ for token in laytime_cause_doc]
        doc_lemmas = [token.lemma_ for token in doc]
        laytime_causeInDoc = True
        for laytime_cause_lemma in laytime_cause_lemmas:
            if not (laytime_cause_lemma) in doc_lemmas:
                laytime_causeInDoc = False

        if laytime_causeInDoc:
            return laytime_cause
    return None
    
def get_non_laytime_cause(sentence:str):
    doc = en_nlp(sentence.lower())
    for non_laytime_cause in non_laytime_causes:
        non_laytime_cause_doc  = en_nlp(non_laytime_cause.lower())
        non_laytime_cause_lemmas = [token.lemma_ for token in non_laytime_cause_doc]
        doc_lemmas = [token.lemma_ for token in doc]
        non_laytime_causeInDoc = True
        for non_laytime_cause_lemma in non_laytime_cause_lemmas:
            if not (non_laytime_cause_lemma) in doc_lemmas:
                non_laytime_causeInDoc = False

        if non_laytime_causeInDoc:
            return non_laytime_cause
    return None
#return (start, end, duration, event, laytime_cause, non_laytime_cause)
def get_sentence_info(sentence:str):
    start = start_time(sentence)
    end = end_time(sentence)
    duration = 0
    if start != None and end != None:
        duration = cal_duration(start,end)
    else:
        duration = None

    event = key_event(sentence)
    laytime_cause = get_laytime_cause(sentence)
    non_laytime_cause = get_non_laytime_cause(sentence)
    
    if non_laytime_cause != None:
        print('laytime cause',non_laytime_cause.lower())
        if non_laytime_cause.lower() == 'shift':
            print("shift count",len(shift_start))
            if not start in shift_start:            
                shift_start.append(start)
        
            if len(shift_start) == 1:
                non_laytime_cause = 'shift number' + str(len(shift_start))
                laytime_cause = None
            else:
                non_laytime_cause = None
                laytime_cause = 'shift number' + str(len(shift_start))
    return start,end,duration,event,laytime_cause,non_laytime_cause


   


if __name__ == "__main__":
    sentence = "1212lT 1250LT VESSEL PROCEEDING TO PilOT BOARDING POSITION"
    sentence1 = "COMMENCED discharge from 10:00 to 20:00"
    #times = find_time(sentence)
    #creat_dependency_tree(sentence)
    #
    #print('duration', cal_duration(times[0], times[1]),'hours')
    # print("key event",key_event(sentence))
    # print("laytime cause",get_laytime_cause(sentence))
    # print("non laytime cause", get_non_laytime_cause(sentence))
    # print("start,end,duration,event,laytime_cause,non_laytime_cause",get_sentence_info(sentence))
    # print("start,end,duration,event,laytime_cause,non_laytime_cause",get_sentence_info(sentence1))
    