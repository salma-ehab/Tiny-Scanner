from tkinter import *
import tkinter.filedialog
from tkinter.filedialog import askopenfilename

root = Tk()
root.title("Tiny Scanner")
root.resizable(width=True, height=True)
outFile = 'out.txt'

reservedWords = [
    'if',
    'then',
    'else',
    'end',
    'repeat',
    'until',
    'read',
    'write'
]
sepcialSymbols = "+–-*/=:<>();"
char = ''


def save():
    my_textLeft.delete("1.0", "end-1c")
    my_textRight.delete("1.0", "end-1c")
    file = open(outFile)
    content = file.read()
    lines = content.splitlines()
    file.close()

    print("Lines", lines)
    for element in lines:
        print("Element", element)
        varLeft, varRight = element.split(",")
        print("VarLeft", varLeft)
        print("VarRight", varRight)
        my_textLeft.insert("end-1c", "\n")
        my_textLeft.insert("end-1c", varLeft)
        my_textLeft.insert("end-1c", "\n")
        my_textLeft.insert("end-1c", "---------------------------------")
        my_textRight.insert("end-1c", "\n")
        my_textRight.insert("end-1c", varRight)
        my_textRight.insert("end-1c", "\n")
        my_textRight.insert("end-1c", "---------------------------------")


def openFile():
    fileName = askopenfilename(parent=root, filetypes=[("Text files", "*.txt")])
    fileInput = open(fileName, 'r')
    listInput = fileInput.readlines()
    linesInput = ''.join(listInput)
    codeInput.replace("1.0", "end-1c", linesInput)
    fileInput.close()


def getToken(i):
    token = ''
    token_type = ''
    while char[i] == '{' or \
            char[i] == ' ' or \
            char[i] == '\t':
        if char[i] == '{':
            while (char[i] != '}'):
                i += 1
            i += 1

        while char[i] == ' ' \
                or char[i] == '\t':
            i += 1
            if i >= len(char):
                return (i, '', '')

    if (char[i].isalpha()):
        while char[i].isalpha() or char[i].isdigit():
            token += char[i]
            i += 1
        if token in reservedWords:
            token_type = 'reserved word'
        else:
            token_type = 'identifier'

    elif (char[i].isdigit()):
        while char[i].isdigit():
            token += char[i]
            i += 1
            if char[i].isalpha():
                token+=char[i]
                i+=1
                token_type='error'
                while char[i].isalpha():
                    token += char[i]
                    i += 1
                    token_type = 'error'
            else:
                token_type = 'number'


    elif char[i] == ':':
        if char[i + 1] == '=':
            token = ':='
            i += 2
            token_type = 'assign operator'
        else:
            i += 1
            token = ':'
            token_type = 'error'

    elif char[i] in sepcialSymbols:
        token = char[i]
        i += 1
        if token == '+':
            token_type = "addition operator"
        elif token == '–':
            token_type = "subtract operator"
        elif token == '-':
            token_type = "subtract operator"
        elif token == '*':
            token_type = "multiplication operator"
        elif token == '/':
            token_type = "division operator"
        elif token == '=':
            token_type = "equal operator"
        elif token == '<':
            token_type = "less than operator"
        elif token == '>':
            token_type = "greater than operator"
        elif token == '(':
            token_type = "open bracket"
        elif token == ')':
            token_type = "closed bracket"
        elif token == ';':
            token_type = "semicolon operator"
    else:
        token_type = "error"
        while (char[i] != ' '):
            token += char[i]
            i += 1

    return (i, token, token_type)


def readTokens():
    indexString = codeInput.get("1.0", "end-1c")
    if (indexString != ''):
        global char
        char = indexString.replace('\n', ' ') + ' '
        index, sz = 0, len(char)
        output = []
        result = getToken(index)
        while (result[0] < sz):
            output.append(result[1] + ", " + result[2])
            result = getToken(result[0])

        outputFile = open(outFile, 'w')
        for line in output:
            outputFile.write(line + '\n')
        outputFile.close
        save()


def multiple_yview(*args):
    my_textLeft.yview(*args)
    my_textRight.yview(*args)


def selectFile(event):
    event.widget.config(cursor="pirate")


ScanFrame = Frame(root, padx=10)
upperFrame = Frame(ScanFrame, padx=10, pady=10)
Label(upperFrame, text="Input the code", font=("Verdana", 16)).pack(side=LEFT, fill=Y, expand=1)
upperFrame.pack(expand=1)

middleFrame = Frame(ScanFrame)
codeInput = Text(middleFrame, width=60, height=30, background="steel blue", font=("Verdana", 10), fg="white")  ##height
codeInput.pack(side=LEFT, fill=Y, expand=1)  # pack
codeInput.config(undo=True)
scroll = Scrollbar(middleFrame, command=codeInput.yview)
codeInput['yscrollcommand'] = scroll.set
scroll.pack(side=LEFT, fill=Y, expand=1)  # pack
middleFrame.pack(expand=1, fill=Y)

lowerFrame = Frame(ScanFrame)
scanBTN = Button(lowerFrame, text='Scan', command=lambda: (readTokens(), save()), width=20, font=("Verdana", 10))
scanBTN.pack(side=RIGHT, padx=10)
importBtn = Button(lowerFrame, text='Import', command=lambda: openFile(), width=20, font=("Verdana", 10))
importBtn.pack(side=LEFT, padx=10)
importBtn.bind("<Motion>", selectFile)
lowerFrame.pack(expand=1, fill=Y, pady=10)
ScanFrame.pack(side="left", fill=Y, expand=1)

resultFrame = Frame(root, padx=10)
Label(resultFrame, text="Results", font=("Verdana", 16), pady=10).pack()
my_textLeft = Text(resultFrame, height=8, width=30, pady=10, background="#7FB7E5", font=("Verdana", 10), fg="black")
my_textRight = Text(resultFrame, height=8, width=35, pady=10, background="#7FB7E5", font=("Verdana", 10), fg="black")

my_textLeft.pack(side=LEFT, fill=Y, padx=10)
my_textRight.pack(side=LEFT, fill=Y, padx=10)
my_scrollbarRight = Scrollbar(resultFrame, orient=VERTICAL, command=multiple_yview)
my_scrollbarRight.pack(fill=Y, expand=1, side=LEFT)
my_textLeft.configure(yscrollcommand=my_scrollbarRight.set)
my_textRight.configure(yscrollcommand=my_scrollbarRight.set)
resultFrame.pack(pady=20, padx=20, fill=Y, expand=1)

root.mainloop()
