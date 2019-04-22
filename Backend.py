#!/usr/bin/python

import sys
import re
from utils import stopwords, listSynonym, FAQs
#from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
#from ntlk.corpus import stopwords
#from ntlk.tokenize import word_tokenize

numOfQuestion = 0
questionDB = []
answerDB = []

#factory = StopWordRemoverFactory()
#stopwords = factory.get_stop_words()

# KNUTH MORRIS PRAT #
def bigThree(value,idxes):
    #Mengembalikan indeks indeks dengan nilai terbesar
    newIdxes = [0]*3
    #SelectionSort
    for i in range(3):
        max = 0
        maxIdx = -1
        for j in range(i,len(idxes)):
            if(value[j] > max):
                max = value[j]
                maxIdx = j
        #Swap
        temp = idxes[i]
        idxes[i] = idxes[maxIdx]
        idxes[maxIdx] = temp

        temp = value[i]
        value[i] = value[maxIdx]
        value[maxIdx] = temp


    for i in range(3):
        newIdxes[i] = idxes[i]

    return newIdxes

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

def knuthMorrisPrat(string1, txt):
    n = len(txt) #Dikurangi tanda tanya
    m = len(string1)

    match = False
    wholeScore = m * 100 / n
    if(wholeScore >= 90) and (wholeScore <= 110):
        # Periksa seluruh string secara eksak
        border = borderFunctionKMP(string1,m)
        i = 0
        j = 0
        while (i < n):
            if (string1[j] == txt[i]):
                i = i + 1
                j = j + 1

            if (j == m):
                #Pattern ditemukan
                match = True
                j = border[j-1]
            elif (i < n) and (string1[j] != txt[i]):
                #Tidak cocok, geser
                if(j != 0):
                    j = border[j-1]
                else:
                    i = i + 1

        if(match):
            return wholeScore

    if(not match):
        tokenizedString = string1.split()
        countMatch = 0
        totalLength = len(txt)
        n = len(txt) - 1 # Dikurangi tanda tanya

        for substring in tokenizedString:
            #Cari setiap sinonimnya
            listOfPattern = findSynonym(substring)
            for pattern in listOfPattern:
                m = len(pattern)

                border = borderFunctionKMP(pattern,m)
                patternMatch = False
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
                        patternMatch = True
                        break #BreakWhile
                    elif (i < n) and (pattern[j] != txt[i]):
                        #Tidak cocok, geser
                        if(j != 0):
                            j = border[j-1]
                        else:
                            i = i + 1

                if(patternMatch):
                    break #BreakFor
        return (countMatch * 100.0 / totalLength)

def resultKMP(string):
    #knuth-morris-Prat
    max = -1
    maxIdx = -1
    countOfResult = 0
    idxes = []
    maxValues =[]
    for i in range(numOfQuestion):
        # Kode
        x = knuthMorrisPrat(string,questionDB[i])
        if(x >= 90):
            #Ketemu
            countOfResult = countOfResult + 1
            maxValues.append(x)
            idxes.append(i)
        if(x > max):
            max = x
            maxIdx = i

    if(countOfResult == 0):
        if(maxIdx != -1):
            idxes.append(maxIdx)
    elif(countOfResult > 3):
        idxes = bigThree(maxValues,idxes)
    return ((countOfResult > 0), idxes)

# BOYER MOORE #
def badCharBM(string):
    #Banyak jenis karakter = 256
    #Diinisialisasi dengan -1
    badChar = [-1]*256

    m = len(string)
    for i in range(m):
        #Mengubah ke nilai char (tabel ASCII)
        badChar[ord(string[i])] = i

    return badChar

def boyerMoore(string1,txt):
    n = len(txt) #Dikurangi tanda tanya
    m = len(string1)
    wholeScore = m * 100 / n
    match = False
    if(wholeScore >= 90) and (wholeScore <= 100):
        # Seluruh string dicocokan
        badChar = badCharBM(string1)
        shift = 0
        while(shift <= n-m):
            j = m - 1
            while(j >= 0) and (string1[j] == txt[shift+j]):
                j = j - 1

            if(j < 0):
                # Pattern ditemukan
                match = True
                break #BreakWhile
            else:
                shift = shift + max(1, j-badChar[ord(txt[shift+j])])
        if(match):
            return wholeScore

    if(not match):
        #Per substring
        tokenizedString = string1.split()
        countMatch = 0
        totalLength = len(txt)
        n = len(txt) - 1
        for substring in tokenizedString:
            #Cari setiap sinonimnya
            listOfPattern = findSynonym(substring)
            patternMatch = False
            for pattern in listOfPattern:
                m = len(pattern)
                badChar = badCharBM(pattern)

                shift = 0
                while(shift <= n-m):
                    j = m - 1
                    while(j >= 0) and (pattern[j] == txt[shift+j]):
                        j = j - 1

                    if(j < 0):
                    # Pattern ditemukan
                        countMatch = countMatch + m + 1 #Ditambah sebuah spasi
                        patternMatch = True
                        break #BreakWhile
                    else:
                        shift = shift + max(1, j-badChar[ord(txt[shift+j])])
                if(patternMatch):
                    break #BreakFor

            return (countMatch * 100.0 / totalLength)


def resultBM(str):
    #boyer moore
    max = -1
    maxIdx = -1
    countOfResult = 0
    idxes = []
    maxValues = []
    for i in range(numOfQuestion):
        # Kode
        x = boyerMoore(str,questionDB[i])
        if(x >= 90):
            #Ketemu
            countOfResult = countOfResult + 1
            idxes.append(i)
        if(x > max):
            max = x
            maxIdx = i

    if(countOfResult == 0):
        if(maxIdx != -1):
            idxes.append(maxIdx)
    elif(countOfResult > 3):
        idxes = bigThree(maxValues,idxes)
    return ((countOfResult > 0), idxes)

# REGULAR EXPRESSION #
def buildString(tokenizedString, line, j):
    stringBuilt = "(.*)"
    for i in range(len(tokenizedString)):
        if(i == j):
            stringBuilt = stringBuilt + line + "(.*)"
        else:
            stringBuilt = stringBuilt + tokenizedString[i] + "(.*)"

def resultRegex(string):
    #Regular expression
    maxIdx = -1
    max = -1
    countOfResult = 0
    idxes = []
    maxValues = []
    for i in range(numOfQuestion):
        #Change this later
        tokenizedString = string.split()
        j = 0
        for substring in tokenizedString:
            substringSynonyms = findSynonym(substring)
            for line in substringSynonyms:
                pattern = buildString(tokenizedString, line, j)
                x = re.search(string,questionDB[i],re.M)
                if(x):
                    score = len(string) * 100.0 / len(questionDB[i])
                    countOfResult += 1
                    maxValues.append(score)
                    idxes.append(i)
                    if(score >= max):
                        max = score
                    break #BreakFor

            if(x):
                break #BreakFor
            else:
                j += 1

    if(countOfResult == 0):
        if(maxIdx != -1):
            idxes.append(maxIdx)
    elif(countOfResult > 3):
        idxes = bigThree(maxValues,idxes)
    return ((countOfResult > 0), idxes)

# OTHER FUNCTION
def otherFunc(string):
    #other algorithm for pattern matching
    max = 0
    idx = -1
    return (max, 0)

def initDB():
    #Add questions and answers to database
    global numOfQuestion
    numOfQuestion = 1
    questionDB.append("Siapa nama Anda")
    answerDB.append("Aku Fluffball")

    quest = open("pertanyaan.txt","r")
    for line in quest:
        numOfQuestion = numOfQuestion + 1
        questString = line
        questString = questString.replace("?","")
        questString = removeStopWords(questString.strip()) + " "
        questionDB.append(questString)

    ans = open("jawaban.txt","r")
    for line in ans:
        answerDB.append(line.strip())

    #print(questionDB)
    #print(answerDB)
    quest.close()
    ans.close()

    #Add FAQs
    for tuple in FAQs:
        numOfQuestion = numOfQuestion + 1
        que, ans = tuple
        questionDB.append(removeStopWords(que) + " ")
        answerDB.append(ans)


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

def findSynonym(string):
    #Mencari sinonim dari suatu string
    found = False
    idx = -1
    for listOfWords in listSynonym:
        idx = idx + 1
        for word in listOfWords:
            if(string == word):
                found = True
                break
        if(found):
            break

    if(found):
        # Jika ada sinonimnya, kembalikan list of Synonym ke-idx
        return listSynonym[idx]
    else:
        # Jika tidak ada sinonimnya, kembalikan list berisi string itu sendiri
        listOneWord = []
        listOneWord.append(string)
        return listOneWord

def talk(string):
    print("Fluffball : "+string)

# Main program #
def useKMP(string):
    found, listHasil = resultKMP(string)
    tampikanHasil(found,listHasil)

def useBM(string):
    found, listHasil = resultBM(string)
    tampikanHasil(found,listHasil)

def useRegex(string):
    found, listHasil = resultRegex(string)
    tampikanHasil(found,listHasil)

def tampikanHasil(found, listHasil):
    if(found):
        if(len(listHasil) == 1):
            print(answerDB[listHasil[0]])
        else: #len(listHasil) > 1
            first = True
            otp = ""
            for i in listHasil:
                if(first):
                    otp = questionDB[i].strip()+"?"
                    first = False
                else:
                    otp = otp +", "+questionDB[i].strip()+"?"
            print("Pilih pertanyaan ini : "+otp)

    else:
        otp = "Mungkin maksud Anda : "
        if(len(listHasil) == 0):
            print(otp + questionDB[i].strip()+"?")
        else:
            print(otp + questionDB[listHasil[0]]+"?")

def DebugAll():
    initDB()
    talk("Halo, ada yang bisa dibantu?")
    talk("Pilih metode pencarian")
    print("1. Knuth-Morris-Prat")
    print("2. Boyer-Moore")
    print("3. Regular expression")

    choice = int(input("Anda : "))
    while(True):
        if(choice >= 1) and (choice <= 3):
            string = str(input("Anda : "))
            if(string == "end"):
                break
            string = string.replace("?","")
            string = removeStopWords(string)

            if(choice == 1):
                useKMP(string)
            elif(choice == 2):
                useBM(string)
            elif(choice == 3):
                useRegex(string)
        else:
            talk("Invalid input!! Masukkan kembali pilihan Anda")
            choice = int(input("Anda : "))

def Execute():
    initDB()
    chatLog = open("chatLog.txt","r")
    for line in chatLog:
        getQuestion = line
    getQuestion = getQuestion.strip()
    getQuestion = getQuestion.replace("?","")
    getQuestion = removeStopWords(getQuestion)
    if(sys.argv[1] == '1'):
        useKMP(getQuestion)
    elif(sys.argv[1] == '2'):
        useBM(getQuestion)
    elif(sys.argv[1] == '3'):
        useRegex(getQuestion)

#DebugAll()
#DebugKMP()
#DebugBM()
#DebugRegex
Execute()
