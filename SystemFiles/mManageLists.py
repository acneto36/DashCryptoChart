
import sys
from   os              import path
from   PyQt5.QtWidgets import QListWidgetItem, QMessageBox
from   PyQt5.QtCore    import Qt

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths                   import *
from SystemFiles.mWriteRead  import *
from DataFrames.mReturnLists import *

# ___________________________________________________________________________ #
def F_sortList(sortList):
    sortList.sortItems()
    
# ___________________________________________________________________________ #
def F_selectPath(exchange, leftList = None, rightList = None):

    lstBase, lstSymbol = F_lstPaths(exchange)

    if leftList != None and rightList != None:
        
        F_sortList(leftList)
        F_sortList(rightList)

    return lstBase, lstSymbol

# ___________________________________________________________________________ #
def F_addNewItem(leftList):

    newItem = QListWidgetItem("         New item")
    leftList.addItem(newItem)
    F_sortList(leftList)

    newItem.setFlags(newItem.flags() | Qt.ItemIsEditable)
    leftList.clicked.connect(lambda: F_sortList(leftList))
    
# ___________________________________________________________________________ #
def F_moveItemsRight(leftList, rightList):

    selected_items = leftList.selectedItems()

    for item in selected_items:

        text    = item.text()
        newItem = QListWidgetItem(text)
        rightList.addItem(newItem)
        leftList.takeItem(leftList.row(item))
        F_sortList(rightList)

# ___________________________________________________________________________ #
def F_moveItemsLeft(leftList, rightList):

    selected_items = rightList.selectedItems()

    for item in selected_items:

        text     = item.text()
        new_item = QListWidgetItem(text)
        leftList.addItem(new_item)
        rightList.takeItem(rightList.row(item))
        F_sortList(leftList)

# ___________________________________________________________________________ #
def F_confirm(parent):
    result = QMessageBox.question(parent, "Confirmation", "Remove item?", 
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
    if result == QMessageBox.Yes:
        return True
    else:
        return False
    
# ___________________________________________________________________________ #
def F_removeSelectedItem(parent, leftList, rightList):

    selected_left_items = leftList.selectedItems()

    if F_confirm(parent):
        for item in selected_left_items:
            leftList.takeItem(leftList.row(item))

        selected_right_items = rightList.selectedItems()
        for item in selected_right_items:
            rightList.takeItem(rightList.row(item))

# ___________________________________________________________________________ #
def F_loadLists(lst, pathFile):

    lines = readingFile(pathFile)

    # Load lists with the updated content from the file.txt
    for line in lines:
        item = line.strip()
        lst.addItem(item)

    F_sortList(lst)

# ___________________________________________________________________________ #
def F_updateLists(leftList, rightList, exchange):

    lstBase, lstSymbol = F_selectPath(exchange)

    rightList.clear()
    leftList.clear()

    F_loadLists(rightList, lstSymbol)
    F_loadLists(leftList, lstBase)

    return lstBase ,lstSymbol

# ___________________________________________________________________________ #