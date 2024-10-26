from PyQt5.QtCore import QRegExp

from PyQt5.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat, 
    QColor, 
    QFont,
)


# ___________________________________________________________________________ #
class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent = None):
        super(Highlighter, self).__init__(parent)

        self.highlightingRules = []

        # Color the words inside the parentheses
        self.highlightingRules.append((QRegExp("\\(.*\\)"), self.createFormat(QColor('#d8cece'))))

        # Functions
        self.highlightingRules.append((QRegExp("\\b\\w+\\b(?=\\()"), self.createFormat(QColor('#5bca00'))))
        
        conditions = ['def', 'try', 'class', 'except', 'if', 'else', 'elif', 'for', 'in', 'as', 'break', 'pass', 'continue', 'import', 'from',
                      'return', 'global', 'while', 'lambda', 'f', 'r', 'n']
        
        for i in range(len(conditions)):
            self.highlightingRules.append((QRegExp(f"\\b{conditions[i]}\\b"),  self.createFormat(QColor('#E94E47'), True)))

        compare = ['=', '>=', '<=', '!=', '==']

        for i in range(len(compare)):
            self.highlightingRules.append((QRegExp(f"\\{compare[i]}\\s*"),  self.createFormat(QColor('#ebd300'))))

        others = ['True', 'False', 'None', 'or', 'and', 'not', '__init__', '__file__', 'self']

        for i in range(len(others)):
            self.highlightingRules.append((QRegExp(f"\\b{others[i]}\\b"),  self.createFormat(QColor('#00FCFC'))))

        types = ['int', 'str', 'float', 'bool', 'list', 'tuple', 'dict', 'complex']

        for i in range(len(types)):
            self.highlightingRules.append((QRegExp(f"\\b{types[i]}\\b"),  self.createFormat(QColor('#59b403'), True)))


        self.highlightingRules.append((QRegExp(",\\s*"), self.createFormat(QColor('#fcfcfc'))))

        # NUMBER
        self.highlightingRules.append((QRegExp("\\b\\d+\\b"), self.createFormat(QColor('#dd6d12'))))

        comments = ['#.*', "'.*\\'", '".*\\"']

        for i in range(len(comments)):
            self.highlightingRules.append((QRegExp(f"\\{comments[i]}"),  self.createFormat(QColor('#85BCC2'))))  # 529B0C
            
        self.highlightingRules.append((QRegExp("\\\\"),  self.createFormat(QColor('#b31c08'))))

        # Color parentheses
        self.highlightingRules.append((QRegExp("\\(|\\)"), self.createFormat(QColor('#ebd300'))))

        # Color braces
        self.highlightingRules.append((QRegExp("\\{|\\}"), self.createFormat(QColor('#ebd300'))))

        # Color brackets
        self.highlightingRules.append((QRegExp("\\[|\\]"), self.createFormat(QColor('#ebd300'))))

        # CONSTANT
        self.highlightingRules.append(
            (QRegExp("\\b[A-Z_]+\\b"), self.createFormat(QColor('#9932CC'))) 
        )

    # ___________________________________________________________________________ #
    def createFormat(self, color, isBold = False):

        format = QTextCharFormat()
        format.setForeground(QColor(color))

        if isBold:
            format.setFontWeight(QFont.Bold)

        return format
    
    # ___________________________________________________________________________ #
    def highlightBlock(self, text):

        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index      = expression.indexIn(text)

            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index  = expression.indexIn(text, index + length)