# @author Ashish Tamrakar
# @Date 2016-02-26
# Program to find the inverted file and then boolean query of the string to find the list of document id of the Cransfield collection.
# Python v2.7.10
import re
from stemmer import PorterStemmer
import json
from pythonds.basic.stack import Stack

pObj = PorterStemmer()


def addToDict(listWords, stemWord):
    """
    Returns the listWords frequency.
    """
    if (stemWord in listWords):
        listWords[stemWord] += 1
    else:
        listWords[stemWord] = 1
    return listWords


def addDoc(docId, listWords):
    """
    Return the dictionary with {id, unique terms, and terms containing its term and term frequency}
    """
    sortedList = sorted(listWords.items(), key=lambda t: t[0])
    output = {'id': docId, 'unique': len(sortedList), 'terms': sortedList}
    return output


def createInvFileHash(invFileHash, docList):
    """
    Creates/Updates the invFileHash from the documentList obtained.
    """
    id = docList['id']
    for term in docList['terms']:
        if (term):
            if (term[0] in invFileHash):
                invFileHash[term[0]][0] += 1
                invFileHash[term[0]][1].append([id, term[1]])
            else:
                invFileHash[term[0]] = [1, [[id, term[1]]]]
    return invFileHash


def writeToFile(invFileHash):
    """
    Writes to the file
    """
    with open('output.json', 'w') as f:
        json.dump(invFileHash, f)


def loadFromFile():
    """
    Loads the Inverted File Hash JSON file.
    """
    with open('output.json', 'r') as f:
        return json.load(f)


def infixToPostfix(infixexpr, prec):
    """
    Converts the Infix expression of queries into postfix expression
    """
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()
    for token in tokenList:
        if token.isalpha() and token not in (["OR", "AND", "NOT"]):
            stemWord = pObj.stem(token, 0, len(token) - 1)
            postfixList.append(stemWord)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            if (not opStack.isEmpty() and opStack.peek() == "NOT"):
                postfixList.append(opStack.pop())

            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token] and token != "NOT"):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())

    return postfixList


def computeBooleanQuery(resultPostFix, dic, prec, stopwords):
    """
    Computes the boolean query and return the list with document id
    """
    wholeDocument = [x for x in range(1, 1401)]
    opStack = Stack()
    for item in resultPostFix:
        if (item not in prec):
            if (item in dic):
                data = [item[0] for item in dic[item][1]]
            elif (item in stopwords):
                data = ['S']
            else:
                data = []
            opStack.push(data)
        else:
            if (item == "AND"):
                list2 = opStack.pop()
                list1 = opStack.pop()
                if ('S' in list1 and 'S' in list2):
                    result = ['S']
                elif ('S' in list1):
                    result = list2
                elif ('S' in list2):
                    result = list1
                else:
                    result = list(set(list1).intersection(list2))
                opStack.push(result)
            elif (item == "OR"):
                list2 = opStack.pop()
                list1 = opStack.pop()
                if ('S' in list1 and 'S' in list2):
                    result = ['S']
                elif ('S' in list1):
                    result = list2
                elif ('S' in list2):
                    result = list1
                else:
                    result = list(set(list1).union(list2))
                opStack.push(result)
            elif (item == "NOT"):
                list1 = opStack.pop()
                if ('S' in list1):
                    result = []
                else:
                    result = list(set(wholeDocument) - set(list1))
                opStack.push(result)
    finalResult = opStack.pop()
    return (finalResult if ('S' not in finalResult) else [])


def booleanQueryString(condition, stopwords):
    """
    Process the conversion of Infix expression to postfix and then compute the boolean query of string.
    """
    # Precedence of operators - 1. (,)  2. NOT  3. AND, OR
    prec = {'OR': 3, 'AND': 3, 'NOT': 2, '(': 1}

    # load from invFileHash
    dic = loadFromFile()

    resultPostFix = infixToPostfix(condition, prec)
    result = computeBooleanQuery(resultPostFix, dic, prec, stopwords)

    print "\nQuery->", condition, ":"
    print "Total Number of Documents:", len(result)
    print sorted(result)
    return result


def main():
    # Reading the document from the file
    file = open("cran.all.1400", "r")
    documents = file.read()
    # Reading stop words from the file
    fileStopwords = open('stopwords.txt', 'r')
    stopwordsList = fileStopwords.read()
    stopwords = stopwordsList.split()

    # List that maintains the document id number, number of unique terms in document, for each term in the document, its term and it's term frequency.
    docId = 1
    invFileHash = {}

    # Splits the multiple documents of the same file into list
    document = re.split(".I | \n.I", documents)[1:]

    for doc in enumerate(document):
        startIndex = doc[1].index('.W\n')
        text = doc[1][startIndex + 3:]
        words = re.findall(r'\w+', text)

        listWords = {}
        for word in words:
            flagStopwords = word.lower() in stopwords
            if (not flagStopwords and word.isalpha()):
                stemWord = pObj.stem(word, 0, len(word) - 1)
                listWords = addToDict(listWords, stemWord)

        docList = addDoc(docId, listWords)
        docId += 1
        invFileHash = createInvFileHash(invFileHash, docList)

    # Writes the invFileHash to output.json file in JSON format
    writeToFile(invFileHash)

    # Boolean query string
    condition = "vary"
    booleanQueryString(condition, stopwords)

    condition = "vary AND user"
    booleanQueryString(condition, stopwords)

    condition = "panama OR NOT user"
    booleanQueryString(condition, stopwords)

    condition = "panama OR NOT user AND vary"
    booleanQueryString(condition, stopwords)

    condition = "panama OR NOT ( user AND vary )"
    booleanQueryString(condition, stopwords)

    condition = "panama OR NOT ( is AND the )"
    booleanQueryString(condition, stopwords)


main()
