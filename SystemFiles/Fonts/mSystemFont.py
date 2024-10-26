from   os import path
import sys

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from PyQt5.QtGui import QFontDatabase, QFont

currentDir = path.join('SystemFiles', 'Fonts', 'ListFont')

# ___________________________________________________________________________ #
def F_systemFont(fontName: str, fontSize: int):

    fontPath     = path.join(currentDir, fontName)
    fontId       = QFontDatabase.addApplicationFont(fontPath)
    fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
    newFont      = QFont(fontFamilies[0], fontSize) 

    return newFont

# ___________________________________________________________________________ #
def F_enumFont(fontName: str):

    font = ('georgia.ttf'               if fontName == 'georgia'    else
            'NotoSans-Regular.ttf'      if fontName == 'notosans'   else
            'OpenSans-Regular.ttf'      if fontName == 'opensans'   else
            'Ubuntu-Regular.ttf'        if fontName == 'ubuntu'     else
            'Ubuntu-Bold.ttf'           if fontName == 'ubuntub'     else
            'JetBrainsMono-Regular.ttf' if fontName == 'jetbrains'  else
            'JetBrainsMono-Bold.ttf'    if fontName == 'jetbrainsb' else  'georgiab.ttf'
    )

    return font

# ___________________________________________________________________________ #
def F_fontStyle(
        widget, 
        typeWidget: str, 
        fontName:   str, 
        fontSize:   int, 
        border     = '1px solid',
        background = '#535353', 
        fontColor  = '#eeeeee'
    ):

    font    = F_enumFont(fontName)
    newFont = F_systemFont(font, fontSize)

    widget.setStyleSheet(f"""
        {typeWidget} {{
            font-family: '{newFont.family()}';
            font-size: {newFont.pointSize()}px;
            background-color: {background};
            color: {fontColor}; 
            border: {border}; 
        }}
    """)
    
