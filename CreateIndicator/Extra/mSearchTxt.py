from PyQt5.QtGui import QTextCharFormat, QColor, QTextCursor, QFont


def F_performSearch(textBoxInd, searchText, lblCount):

    # Clear the previous highlights
    cursor = textBoxInd.textCursor()  # We obtain the cursor from QPlainTextEdit
    cursor.beginEditBlock()           # For better performance when applying multiple changes

    # Remove any previous highlights
    cursor.select(QTextCursor.Document)  # Select the entire document
    defaultFormat = QTextCharFormat()    # Create a standard format
    cursor.setCharFormat(defaultFormat)  # Apply the standard format to remove highlights

    cursor.endEditBlock()  # End the editing block

    # If there is no text to search, we exit
    if not searchText:
        lblCount.setText('')
        return

    # We create a format to highlight the found text
    highlightFormat = QTextCharFormat()
    highlightFormat.setBackground(QColor('#888A85'))  # Highlight color
    highlightFormat.setFontWeight(QFont.Bold)           # You can also make the text bold

    # We start the search from the beginning of the document
    cursor   = textBoxInd.textCursor()
    cursor.movePosition(QTextCursor.Start)  # Start from the beginning of the document
    startPos = cursor.position()            # Start position for the search

    count    = 0

    # Loop to find all occurrences of the search text
    while True:
        # Find the next occurrence of the search text
        cursor = textBoxInd.document().find(searchText, startPos)
        if cursor.isNull():  # If no more occurrences are found, exit the loop
            count = 0
            
            break
        
        count += 1 
        # Set the format for the found text
        cursor.mergeCharFormat(highlightFormat)

        # Set the next starting position for the search
        startPos = cursor.position()  # Update the position to continue the search

        lblCount.setText(f"{count}")

# ___________________________________________________________________________ #
def F_clearSearch(txtSearch, lblCount):

    txtSearch.clear()
    lblCount.setText('')

