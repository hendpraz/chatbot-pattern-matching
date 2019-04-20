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
    n = len(txt) - 1 #Dikurangi tanda tanya
    m = len(string1)

    match = False
    wholeScore = m * 100 / n
    if(wholeScore >= 90):
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

def maxKMP(string):
    #knuth-morris-Prat
    max = 0
    maxIdx = -1
    countOfResult = 0
    idxes = []
    for i in range(numOfQuestion):
        # Kode
        x = knuthMorrisPrat(string,questionDB[i])
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
    return (countOfResult, idxes)


# REGULAR EXPRESSION #
def regex(string):
    #Regular expression
    #for i in range(numOfQuestion):
        #Change this later
        #x = re.search(string,questionDB[i])
        #print(x.string)
    return (0, [])

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
    n = len(txt) - 1 #Dikurangi tanda tanya
    m = len(string1)
    wholeScore = m * 100 / n
    match = False
    if(wholeScore >= 90):
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


def maxBM(str):
    #boyer moore
    max = 0
    maxIdx = -1
    countOfResult = 0
    idxes = []
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
    return (countOfResult, idxes)

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
    questionDB.append("Siapa nama ")
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
def DebugAll():
    initDB()
    talk("Halo, ada yang bisa dibantu?")
    while(True):
        string = str(input("Anda : "))
        if(string == "end"):
            break
        string = string.replace("?","")
        string = removeStopWords(string)
        print("Filtered string: " + string)

        #KMP
        hasilKMP, listHasilKMP = maxKMP(string)
        print("\n#### KMP ####")
        print("Banyak ditemukan = " + str(hasilKMP))
        print("Indeks : ")
        print(listHasilKMP)

        #BM
        hasilBM, listHasilBM = maxKMP(string)
        print("\n#### BM ####")
        print("Banyak ditemukan = " + str(hasilBM))
        print("Indeks : ")
        print(listHasilBM)

        #Regex
        hasilRE, listHasilRE = regex(string)
        print("\n#### RE ####")
        print("Indeks : ")
        print(listHasilRE)
        print("")

        listHasilTotal = list(set(listHasilKMP + listHasilBM))
        listHasilTotal = list(set(listHasilTotal + listHasilRE))
        hasilTotal = hasilKMP + hasilBM + hasilRE

        if(len(listHasilTotal) == 0):
            #hasilTotal == 0, panjang listHasilTotal <= 0
            talk("Aku tidak mengerti maksud Anda, coba hal lain")
        elif(hasilTotal == 0):
            #Tidak menemukan hasil sama sekali
            talk("Mungkin maksud Anda:")
            j = 0
            for i in listHasilTotal:
                if(j > 2):
                    break
                print(questionDB[i])
                j += 1
        elif(len(listHasilTotal) == 1):
            #hasilTotal != 0, dan hasil yang ditemukan tepat satu buah
            talk(answerDB[listHasilTotal[0]])
        elif(len(listHasilTotal) >= 1):
            #hasilTotal != 0, dan hasil yang ditemukan lebih dari satu
            talk("Pilih di antara pertanyaan-pertanyaan ini")
            j = 0
            for i in listHasilTotal:
                if(j > 2):
                    break
                print(questionDB[i])
                j += 1





DebugAll()
#DebugKMP()
#DebugBM()
#DebugRegex
