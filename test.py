from pythonds.basic.stack import Stack
import sys

def infixToPostfix(infixexpr):
    prec = {}
    prec["OR"] = 3
    prec["AND"] = 3
    prec["NOT"] = 2
    prec["("] = 1
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
    return " ".join(postfixList)

# print(infixToPostfix("A * B + C * D"))
# print(infixToPostfix("( A + B ) * C - ( D - E ) * ( F + G )"))
dic = {"circuitri": [1, [[790, 1]]], "entropi": [14, [[48, 1], [273, 2], [302, 1]]] }
# example = "panama OR ( user AND vary )"
# example1 = "NOT vary"
example2 = "circuitri OR entropi"
# print infixToPostfix(example)
# print infixToPostfix(example1)
print infixToPostfix(example2)