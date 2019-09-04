import sys
#import tabula
import csv
import spacy
from nltk import Tree
import tabula
from sematic_analysis import find_time, creat_dependency_tree,get_sentence_info
from spell_check import spellCheck, timeTimeZoneToTime, isDate


def readCsv(fileName):    
    csvName =fileName + '.csv'
    data = []
    with open(csvName,'rt') as f:
        content = csv.reader(f)
        for row in content:
            print(row)
            data.append(row)
    return data

def pdf2Csv(pdfpath,fileName,output_path):    
    pdfName =pdfpath+fileName
    csvName = output_path+fileName + '.csv'
    # Read pdf into DataFrame
    df = tabula.read_pdf(pdfName, pages='all')


    # convert PDF into CSV
    tabula.convert_into(pdfName, csvName, output_format="csv", pages='all')
    data = readCsv(output_path+fileName)
    new_data = []
    for i in range(len(data)):
        row = data[i]
        new_row = []
        for j in range(len(row)):
            column = row[j]        
            if j == 1:
                if isDate(column.lower()):
                    new_row[0] == column
                    column = ""
            new_row.append(column)
        
        new_data.append(new_row)
    
    with open('b.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(new_data)

    # convert all PDFs in a directory
    #tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all)



def pressEnterToContiue():
    input("Press Enter to continue...")





if __name__ == "__main__":
    
    pdf_path = "pdf/"
    output_path = "output/"
    fileName = sys.argv[1]
    
    pdf2Csv(pdf_path,fileName,output_path)
    sys.exit()
    data = readCsv(output_path+fileName)

    #print(data)
    #fillMissValue(data)
    #print("after filling missing values")
    
    new_data = []
    for i in range(len(data)):
        row = data[i]
        new_row = []
        for j in range(len(row)):
            column = row[j]
            column = timeTimeZoneToTime(column.lower())
            column = spellCheck(column)
        
            if j == 1:
                if isDate(column.lower()):
                    new_row[0] == column
                    column = ""
            new_row.append(column)
        
        new_data.append(new_row)
    
    story = [" ".join(row) for row in new_data]
    print(story)
    with open(output_path+fileName+ '_spellCheck.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(new_data)
    pressEnterToContiue()

    #sys.exit()   
    #story_txt = ".".join(story)    
    #print(story_txt)    
    
    
    new_csv_rows = []
    first_column = ["Content", "Start time", "End time", "Duration", "Key event","Laytime cause","Non-laytime cause"]
    new_csv_rows.append(first_column)
    for i in range(len(story)):
        print("sentence",i,story[i])
        csv_row = []
        csv_row.append(story[i])
        
        #creat_dependency_tree(story[i])
        (start,end,duration,event,laytime_cause,non_laytime_cause) = get_sentence_info(story[i])
        if start == None and end == None:
            continue
        print(start,end,duration,event,laytime_cause,non_laytime_cause)
        csv_row.extend((start,end,duration,event,laytime_cause,non_laytime_cause))
        new_csv_rows.append(csv_row)
    
    with open(output_path+fileName+ '_semitic_anly.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(new_csv_rows)

    writeFile.close()