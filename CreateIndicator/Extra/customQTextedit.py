
import sys
from   os              import path

from   PyQt5.QtCore    import Qt
from   PyQt5.QtWidgets import QTextEdit
from   PyQt5.QtGui     import (
    QFontMetrics, 
    QTextCursor,
    QTextCharFormat
)

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from CreateIndicator.Extra.mWriteReadInput import *
from SystemFiles.Fonts.mSystemFont         import *

# Control variable to avoid affecting typing in the text field.
numLines = 0
fontSize = 13

# ___________________________________________________________________________ #
def F_updateFontSize(qTextEdit: list):

    global fontSize

    name     = F_enumFont('jetbrains')
    fontMono = F_systemFont(name, fontSize)

    for i in range(len(qTextEdit)):
        qTextEdit[i].setFont(fontMono)

# ___________________________________________________________________________ #
def F_applyFontSize(textEdit):

    # Method for correcting font size when pasting text in the editor.
    global fontSize

    name     = F_enumFont('jetbrains')
    fontMono = F_systemFont(name, fontSize)

    # Create a QTextCharFormat and set the font in it.
    charFormat = QTextCharFormat()
    charFormat.setFont(fontMono)

    cursor = textEdit.textCursor()
    # Temporarily block signals to avoid infinite recursion.
    textEdit.blockSignals(True)

    cursor.beginEditBlock()
    cursor.select(QTextCursor.Document)
    cursor.mergeCharFormat(charFormat)
    cursor.endEditBlock()

    # Restore signals after modifying the text.
    textEdit.blockSignals(False)
   
# ___________________________________________________________________________ #
def F_removeScrollbar(numList: list):

    for i in range(len(numList)):
        numList[i].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

# ___________________________________________________________________________ #
def F_numTextEdit(txtNum1, txtNum2):

    # Method to number the lines.
    global numLines

    content    = txtNum1.toPlainText()
    lines      = content.splitlines()
    totalLines = len(lines)

    if numLines != totalLines:

        numLines = totalLines
        numbers  = "\n".join(str(i + 1).rjust(4) for i in range(totalLines + 1))

        txtNum2.setText(numbers)

# ___________________________________________________________________________ #
def F_tabPlainText(tabQTextEdit: list):

    for i in range(len(tabQTextEdit)):

        fontMetrics  = QFontMetrics(tabQTextEdit[i].font())
        tabStopWidth = fontMetrics.horizontalAdvance(' ') * 4
        tabQTextEdit[i].setTabStopWidth(tabStopWidth)

# ___________________________________________________________________________ #
def F_noWrap(qTextEdit: list):

    for i in range(len(qTextEdit)):
        qTextEdit[i].setLineWrapMode(QTextEdit.NoWrap)

# ___________________________________________________________________________ #
def F_syncScroll(self, srcEdit, dstEdit):
    
    # Method to synchronize the scroll bars and control both QTextEdits using the editor's scroll bar.
    sender = self.sender()

    if sender == srcEdit.verticalScrollBar():
        dstEdit.verticalScrollBar().setValue(sender.value())
        
    elif sender == dstEdit.verticalScrollBar():
        srcEdit.verticalScrollBar().setValue(sender.value())

# ___________________________________________________________________________ #
def F_styleSheetNum(qTextEdit: list):

    for i in range(len(qTextEdit)):

        qTextEdit[i].setStyleSheet(
            f""" QTextEdit {{
                background-color: #282A36;
                color: #D8DEE9;
                border: 1px solid #4C566A;
                }}
            """
        )

        qTextEdit[i].setReadOnly(True)