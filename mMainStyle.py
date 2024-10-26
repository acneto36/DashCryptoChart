from SystemFiles.Fonts.mSystemFont import *


# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ #
def F_buttonStyle(widget, fontSizeMax: int, fontSizeMin: int):

    name    = F_enumFont('bold')
    fontMax = F_systemFont(name, fontSizeMax)
    fontMin = F_systemFont(name, fontSizeMin)
    
    widget.setStyleSheet(f"""
        QPushButton {{
            font-family: '{fontMax.family()}';
            font-size: {fontMax.pointSize()}px;
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 178, 102, 255),
                stop:0.232804 rgba(195, 123, 51, 255),
                stop:0.98 rgba(0, 0, 0, 255),
                stop:1 rgba(0, 0, 0, 0));
            color: rgb(230, 230, 230);
            border: none;
        }}

        QPushButton:hover {{
            font-family: '{fontMin.family()}';
            font-size: {fontMin.pointSize()}px;
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 178, 102, 255),
                stop:0.232804 rgba(195, 123, 51, 255),
                stop:0.98 rgba(0, 0, 0, 255),
                stop:1 rgba(0, 0, 0, 0));
            color: rgb(230, 230, 230);
            border: none;
        }}
    """)

    
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ #
def F_calendarStyle(
        widget, 
        fontName: str, 
        fontSize: int, 
        headerBackground      = '#cccccc', 
        headerGradient        = '#333333', 
        dayBackground         = '#888A88', 
        dayFontColor          = '#EEEEEC', 
        navigationBarGradient = '#333333', 
        alternateBackground   = '#555753', 
        hoverBackground       = '#8F5902', 
        disabledDayColor      = '#ECEC47'
    ):

    # Obter a fonte e criar o QFont
    font    = F_enumFont(fontName)
    newFont = F_systemFont(font, fontSize)

    # Estilo para o QCalendarWidget
    widget.setStyleSheet(f"""
        QCalendarWidget QToolButton {{
            height: 30px;
            width: 70px;
            icon-size: 30px, 30px;
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 {headerBackground}, stop: 1 {headerGradient});
        }}

        /*  Fundo do menu de meses */
        #periodCalendar QToolButton QMenu {{
            background-color: {alternateBackground};      
            color: {dayFontColor};
            font-size: 15px;
        }}

        /* Ajuste interno do menu de seleção de mês */
        #periodCalendar QToolButton QMenu::item {{
            padding: 5px;
        }}

        /* Barra de nomes dos dias da semana */
        #periodCalendar QWidget {{
            alternate-background-color: {alternateBackground};
            color: {dayFontColor};
        }}

        #qt_calendar_yearbutton {{
            color: {dayFontColor};
            margin: 5px;
            border-radius: 5px;
            padding: 0px 10px;
            font-size: 20px;
        }}

        #qt_calendar_monthbutton {{
            color: {dayFontColor};
            margin: 5px;
            border-radius: 5px;
            padding: 0 10px;
            font-size: 20px;
            width: 120px;
        }}

        #qt_calendar_monthbutton:hover,
        #qt_calendar_yearbutton:hover {{
            background-color: #55aaff;
        }}

        #qt_calendar_yearedit {{
            color: white;
            font-size: 20px;
        }}

        /* Seção de dias */
        QCalendarWidget QAbstractItemView:enabled {{
            font-family: '{newFont.family()}';
            font-size: {newFont.pointSize()}px;
            background-color: {dayBackground};  
            font-weight: bold;
        }}

        /* Barra de navegação do mês e ano */
        QCalendarWidget QWidget#qt_calendar_navigationbar {{ 
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 {headerBackground}, stop: 1 {navigationBarGradient}); 
        }}

        /* Dias de outro mês */
        #periodCalendar QAbstractItemView:disabled {{ 
            color: {disabledDayColor};
        }}

        #qt_calendar_calendarview::item:hover {{
            border-radius: 5px;
            background-color: {hoverBackground};
        }}
    """)

