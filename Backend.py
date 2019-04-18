import re
from Stopwords import stopwords
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

    wholeScore = m * 100 / n
    if(wholeScore >= 90):
        # Periksa seluruh string secara eksak
        match = False
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
        else:
            return 0
    else:
        tokenizedString = string1.split()
        countMatch = 0
        totalLength = len(txt)
        n = len(txt) - 1 # Dikurangi tanda tanya
        for pattern in tokenizedString:
            m = len(pattern)

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
    #knuth-morris-Prat
    max = 0
    idx = -1
    for i in range(numOfQuestion):
        # Kode
        x = knuthMorrisPrat(string,questionDB[i])
        if(x >= max):
            max = x
            idx = i

    return (max, idx)


# REGULAR EXPRESSION #
def regex(string):
    #Regular expression
    #for i in range(numOfQuestion):
        #Change this later
        #x = re.search(string,questionDB[i])
        #print(x.string)
    return 90, 0

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
    if(wholeScore >= 90):
        # Seluruh string dicocokan
        badChar = badCharBM(string1)

        match = False
        shift = 0
        while(shift <= n-m):
            j = m - 1

            while(j >= 0) and (string1[j] == txt[shift+j]):
                j = j - 1

            if(j < 0):
                # Pattern ditemukan
                match = True
                break
                #if(shift + m < n):
                    #shift = shift + (m-badChar[ord(txt[shift+m])])
                #else:
                    #shift = 1
            else:
                shift = shift + max(1, j-badChar[ord(txt[shift+j])])
        if(match):
            return wholeScore
        else:
            return 0
    else:
        #Per substring
        tokenizedString = string1.split()
        countMatch = 0
        totalLength = len(txt)
        n = len(txt) - 1
        for pattern in tokenizedString:
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
                    break
                    #if(shift + m < n):
                        #shift = shift + (m-badChar[ord(txt[shift+m])])
                    #else:
                        #shift = 1
                else:
                    shift = shift + max(1, j-badChar[ord(txt[shift+j])])

        return (countMatch * 100.0 / totalLength)


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
    questionDB.append("Siapa nama?")
    answerDB.append("Aku Zettary")

    quest = open("pertanyaan.txt","r")
    for line in quest:
        numOfQuestion = numOfQuestion + 1
        questionDB.append(removeStopWords(line.strip()))

    ans = open("jawaban.txt","r")
    for line in ans:
        answerDB.append(line.strip())

    #print(questionDB)
    #print(answerDB)
    quest.close()
    ans.close()

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
    kmpMaxVal, kmpIdx = maxKMP(string)
    #print("max = " + str(kmpMaxVal))
    #print("idx = " + str(kmpIdx))
    if(kmpMaxVal >= 90):
        talk(answerDB[kmpIdx])
        #print("Answered with Knuth-Morris-Prat")
    else:
        bmMaxVal, bmIdx = maxBM(string)
        if(bmMaxVal >= 90):
            print(answerDB[bmIdx])
            #print("Answered with Boyer-Moore")
        else:
            reMaxVal, reIdx = regex(string)
            if(reMaxVal >= 90):
                print(answerDB[reIdx])
                #print("Answered with Regular Expression")
            else:
                #max, idx4 = otherFunc(string)
                print("Mungkin maksud Anda :")
                print(answerDB[idx1])
                if(idx1 != idx2):
                    print(answerDB[idx2])
                if((idx2 != idx1) and (idx2 != idx3)):
                    print(answerDB[idx3])
