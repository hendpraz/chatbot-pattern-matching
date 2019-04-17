import re

numOfQuestion = 0
questionDB = []
answerDB = []

def knuthMorrisPratt(str1, str2):
    return 90

def maxKMP(string):
    #knuth-morris-pratt
    max = 0
    idx = -1
    for i in range(numOfQuestion):
        # Kode
        x = knuthMorrisPratt(string,questionDB[i])
        if(x > max):
            max = x
            idx = i

    return (max, idx)

def regex(string):
    #Regular expression
    #for i in range(numOfQuestion):
        #Change this later
        #x = re.search(string,questionDB[i])
        #print(x.string)
    return 90, 0

def boyerMoore(str1,str2):
    return 90

def maxBM(str):
    #boyer moore
    max = 0
    idx = -1
    for i in range(numOfQuestion):
        # Kode
        x = boyerMoore(string,questionDB[i])
        if(x > max):
            max = x
            idx = i

    return (max, idx)

def otherFunc(string):
    #other algorithm for pattern matching
    max = 0
    idx = -1
    return (max, 0)

def initDB():
    #Add questions to database
    global numOfQuestion
    numOfQuestion = 1
    questionDB.append("Siapa nama kamu?")
    answerDB.append("Aku Zettary")

# Main program #
initDB()
string = str(input())
max, idx1 = maxKMP(string)
if(max >= 90):
    print(answerDB[idx])
    print("Answered with Knuth-Morris-Pratt")
else:
    max, idx2 = maxBM(string)
    if(max >= 90):
        print(answerDB[idx])
        print("Answered with Boyer-Moore")
    else:
        max,idx3 = regex(string)
        if(max >= 90):
            print(answerDB[idx])
            print("Answered with Regular Expression")
        else:
            #max, idx4 = otherFunc(string)
            print("Mungkin maksud Anda :")
            print(answerDB[idx1])
            if(idx1 != idx2):
                print(answerDB[idx2])
            if((idx2 != idx1) and (idx2 != idx3)):
                print(answerDB[idx3])
