from   os import path
import sys

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from SystemFiles.Fonts.mSystemFont   import *

def F_createButtonStyle(
        widget, 
        fontName: str, 
        fontSize: int, 
        background = '#914316', 
        fontColor  = '#EEEEEC', 
        borderColor = '#9C5C39', 
        borderWidth = '5px', 
        borderRadius = '10px'
    ):

    font    = F_enumFont(fontName)
    newFont = F_systemFont(font, fontSize)

    widget.setStyleSheet(f"""
        QPushButton {{
            font-family: '{newFont.family()}';
            font-size: {newFont.pointSize()}px;
            background-color: {background};
            color: {fontColor};
            border-left: 2px solid {borderColor};
            border-right: 2px solid {borderColor};
            border-bottom: 2px solid {borderColor};
            border-top: 2px solid {borderColor};
            border-width: {borderWidth};
            border-radius: {borderRadius};
        }}

        QPushButton:hover {{
            background-color: {background};
            color: #EEEEEC;
            font: bold 14px;
            border-width: 2px;
            border-radius: 8px;
        }}

        QPushButton:pressed {{
            font: bold 18px;
            background-color: {background};
            color: white;
        }}
    """)

def F_labelStyle(
        widget, 
        fontName:  str, 
        fontSize:  int, 
        background   = '#535353', 
        fontColor    = '#e0e0e0',
        border       = '2px solid',
        borderColor  = '#20BABF',
        borderWidth  = '1px',
        borderRadius = '5px'
    ):

    font    = F_enumFont(fontName)
    newFont = F_systemFont(font, fontSize)

    widget.setStyleSheet(f"""
            QLabel {{
                font-family: '{newFont.family()}';
                font-size: {newFont.pointSize()}px;
                background-color: {background};
                color: {fontColor}; 
                border-bottom: {border} {borderColor};
                border-top: {border} {borderColor};
                border-width: {borderWidth};
                border-radius: {borderRadius};
            }}
        """)