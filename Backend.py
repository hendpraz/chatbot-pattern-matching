import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
#from ntlk.corpus import stopwords
from ntlk.tokenize import word_tokenize

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
    tokenizedString = word_tokenize(string1)
    countMatch = 0
    totalLength = len(txt) - 1 #Dikurang tanda tanya
    for pattern in tokenizedString:
        m = len(pattern)
        n = len(txt) - 1

        border = borderFunctionKMP(pattern,m)
        i = 0
        while (i < n):
            if (pattern[j] == txt[i]):
                i = i + 1
                j = j + 1

            if (j == m):
                #Pattern ditemukan
                countMatch = countMatch + m + 1 #Ditambah sebuah spasi
            elif(i < n):
                #Tidak cocok, geser
                if()
    return (countMatch * 1.0 / totalLength)

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
    questionDB.append("Siapa nama kamu?")
    answerDB.append("Aku Zettary")

def removeStopWords(string):
    filteredString = ""
    wordTokens = word_tokenize(string)
    for w in wordTokens
        if not w in stopwords
            filteredString = filteredString + " " + w

# Main program #
initDB()
string = str(input())
string = removeStopWords(string)
# DEBUG:
print("Filetered string:")
print(string)
max, idx1 = maxKMP(string)
print("max = " + str(max))
print("idx = " + str(idx))
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
