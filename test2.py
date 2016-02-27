from pythonds.basic.stack import Stack
import sys
prec = {}
prec["OR"] = 3
prec["AND"] = 3
prec["NOT"] = 2
prec["("] = 1

def infixToPostfix(infixexpr):
    # prec = {}
    # prec["OR"] = 3
    # prec["AND"] = 3
    # prec["NOT"] = 2
    # prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()
    for token in tokenList:
        if token.isalpha() and token not in (["OR", "AND", "NOT"]):
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())

    return postfixList
    # return " ".join(postfixList)

# print(infixToPostfix("A * B + C * D"))
# print(infixToPostfix("( A + B ) * C - ( D - E ) * ( F + G )"))
dic = {"circuitri": [1, [[790, 1]]], "entropi": [14, [[48, 1], [273, 2], [302, 1]]] }
# example = "panama OR ( user AND vary )"
# example1 = "NOT vary"
example2 = "circuitri OR entropi AND is"
# print infixToPostfix(example)
# print infixToPostfix(example1)
resultPostFix = infixToPostfix(example2)
print resultPostFix

temp = []
for res in resultPostFix:
    temp1 = dic[res][1] if (res not in prec) else []
    if (res not in prec):
        print res

print prec