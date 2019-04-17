import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
#from ntlk.corpus import stopwords
#from ntlk.tokenize import word_tokenize

numOfQuestion = 0
questionDB = []
answerDB = []

factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()

def borderFunctionKMP(str, m):
    suffLen = 0

    border = [0]*m

    i = 1
    while (i < m):
        if (str[i] == str[suffLen]):
            suffLen = suffLen + 1
            border[i] = suffLen
            i = i + 1
        else:
            if (suffLen != 0):
                suffLen = border[suffLen - 1]
            else:
                border[i] = 0
                i = i + 1

    return border

def knuthMorrisPratt(string1, txt):
    tokenizedString = string1.split()
    countMatch = 0
    totalLength = len(txt)
    for pattern in tokenizedString:
        m = len(pattern)
        n = len(txt)

        border = borderFunctionKMP(pattern,m)
        i = 0
        j = 0
        while (i < n):
            if (pattern[j] == txt[i]):
                i = i + 1
                j = j + 1

            if (j == m):
                #Pattern ditemukan
                countMatch = countMatch + m + 1 #Ditambah sebuah spasi
                j = border[j-1]
            elif (i < n) and (pattern[j] != txt[i]):
                #Tidak cocok, geser
                if(j != 0):
                    j = border[j-1]
                else:
                    i = i + 1
    return (countMatch * 100.0 / totalLength)

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
    #Add questions and answers to database
    global numOfQuestion
    numOfQuestion = 1
    questionDB.append("Siapa nama ?")
    answerDB.append("Aku Zettary")

def removeStopWords(string):
    filteredString = ""
    wordTokens = string.split()
    found = False
    for w in wordTokens:
        if (w not in stopwords):
            if(found):
                filteredString = filteredString + " " + w
            else:
                filteredString = w
                found = True
    return filteredString

def talk(string):
    print("Zettary : "+string)

#C:\Users\admin\Anaconda3\Scripts

# Main program #
initDB()
talk("Halo, ada yang bisa dibantu?")
while(True):
    string = str(input("Anda : "))
    if(string == "end"):
        break
    string = string.replace("?","")
    string = removeStopWords(string)
    # DEBUG:
    #print("Filtered string:")
    #print(string)
    max, idx1 = maxKMP(string)
    #print("max = " + str(max))
    #print("idx = " + str(idx1))
    if(max >= 90):
        talk(answerDB[idx1])
        #print("Answered with Knuth-Morris-Pratt")
    else:
        max, idx2 = maxBM(string)
        if(max >= 90):
            print(answerDB[idx2])
            print("Answered with Boyer-Moore")
        else:
            max,idx3 = regex(string)
            if(max >= 90):
                print(answerDB[idx3])
                print("Answered with Regular Expression")
            else:
                #max, idx4 = otherFunc(string)
                print("Mungkin maksud Anda :")
                print(answerDB[idx1])
                if(idx1 != idx2):
                    print(answerDB[idx2])
                if((idx2 != idx1) and (idx2 != idx3)):
                    print(answerDB[idx3])
