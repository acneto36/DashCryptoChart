import re
from   os                                    import path
import customtkinter                             as ctk 
import mttkinter                                 as mtk
from   tkinter                               import ttk
from   PIL                                   import Image
from   CTkColorPicker                        import *
from   CreateIndicator.Extra.mWriteReadInput import *
from   CTkToolTip                            import *
from   tkcalendar                            import Calendar, DateEntry
from   datetime                              import date


currentDir = path.dirname(path.realpath(__file__))
pathIcon   = path.join(currentDir, '..', 'Icons', 'blueDefault.png')
pathCheck  = path.join(currentDir, '..', 'Icons', 'check.png')


def F_font(fontSize = 22):

    defaultFont = ctk.CTkFont(family = 'Default', size = fontSize, weight = 'bold')
    fontTuple   = (defaultFont.actual('family'), defaultFont.actual('size'), defaultFont.actual('weight'))

    return fontTuple

# --------------------------------------------------------------------------- #
def createFrame(
        window: ctk.CTk, 
        row        = 0,
        column     = 0,
        padx       = 2,
        pady       = 2,
        width      = 200,
        height     = 200,
        background = '#444444',
        position   = 'we',
        colspan    = 1
    ):

    _frame = ctk.CTkFrame(
        window,
        width    = width, 
        height   = height, 
        fg_color = background
    )

    _frame.grid(
        row        = row, 
        column     = column, 
        padx       = padx, 
        pady       = pady,
        sticky     = position,
        columnspan = colspan
    )

    return _frame

# --------------------------------------------------------------------------- #
def createLabel(
        frame:  ctk.CTkFrame, 
        row        = 0, 
        column     = 0, 
        text       = 'Label', 
        textColor  = 'white', 
        background = '#444444', 
        position   = 'w', 
        colspan    = 1,
        textAlignm = 'w',
        width      = 50
    ):

    _label = ctk.CTkLabel(
        frame, 
        text          = text, 
        text_color    = textColor, 
        bg_color      = background, 
        fg_color      = background,
        font          = F_font(),
        width         = width,
        corner_radius = 5,
        anchor        = textAlignm
    )

    _label.grid(
        row        = row, 
        column     = column, 
        padx       = 5, 
        pady       = 5, 
        sticky     = position,
        columnspan = colspan
    )

    return _label

# --------------------------------------------------------------------------- #
def createEntry(
        frame: ctk.CTkFrame,
        row         = 0, 
        column      = 0, 
        width       = 100, 
        textColor   = 'black', 
        background  = 'white', 
        position    = 'w',
        placeHolder = 'Entry'
    ):

    _textEdit = ctk.CTkEntry(
        frame, 
        bg_color         = textColor, 
        fg_color         = background,
        width            = width,
        font             = F_font(),
        border_width     = 2,
        placeholder_text = placeHolder
    )

    _textEdit.grid(
        row    = row, 
        column = column, 
        padx   = 5, 
        pady   = 5,
        sticky = position
    )

    return _textEdit

# --------------------------------------------------------------------------- #
def createButton(
        frame: ctk.CTkFrame, 
        row          = 0, 
        column       = 0, 
        colspan      = 1, 
        text         = 'Button', 
        textColor    = 'white',
        background   = '#a70000', 
        position     = 'w',
        width        = 50,
        cornerRadius = 15,
        image        = None,
        command      = None 
    ):
    
    _button = ctk.CTkButton(
        frame, 
        text          = text,
        bg_color      = 'transparent', 
        fg_color      = background,
        width         = width,
        font          = F_font(),
        border_width  = 0,
        corner_radius = cornerRadius,
        text_color    = textColor,
        image         = image,
        command       = command
    )

    _button.grid(
        row        = row, 
        column     = column, 
        columnspan = colspan, 
        padx       = 5, 
        pady       = 5, 
        sticky     = position
    )

    return _button

# --------------------------------------------------------------------------- #
def createCheckbox(
        frame: ctk.CTkFrame, 
        row        = 0, 
        column     = 0, 
        text       = 'CheckBox', 
        textColor  = 'white', 
        background = '#444444', 
        checkColor = 'green', 
        position   = 'w',
        variable   = None
    ):

    _checkBox = ctk.CTkCheckBox(
        frame,
        text            = text,
        text_color      = textColor, 
        fg_color        = textColor,
        bg_color        = background,
        checkmark_color = checkColor,
        border_width    = 2, 
        border_color    = textColor,
        font            = F_font(),
        variable        = variable,
        onvalue         = True,
        offvalue        = False
    )

    _checkBox.grid(
        row    = row,
        column = column,
        padx   = 5,
        pady   = 5,
        sticky = position
    )

    return _checkBox

# --------------------------------------------------------------------------- #
def createSlider(
        frame: ctk.CTkFrame,
        row          = 0, 
        column       = 0, 
        from_        = 0,
        to           = 1,
        buttonLength = 5,
        background   = '#444444',
        buttonColor  = '#2d92cc',
        command      = None,
        position     = 'w',
        variable     = None
    ):

    _slider = ctk.CTkSlider(
        frame,
        from_         = from_,
        to            = to,
        width         = 100,
        bg_color      = background,
        button_length = buttonLength,
        button_color  = buttonColor,
        command       = command,
        variable      = variable
    )

    _slider.grid(
        row    = row,
        column = column,
        padx   = 5,
        pady   = 5,
        sticky = position
    )

    _slider.set(0)

    return _slider

# --------------------------------------------------------------------------- #
def createOptions( 
        frame: ctk.CTkFrame,
        row               = 0, 
        column            = 0,  
        values: list      = None, 
        valueDefault: str = None, 
        colspan           = 1,
        textColor         = 'black', 
        background        = 'white', 
        position          = 'w',
        width             = 50
    ):

    varMenu     = ctk.StringVar( value = valueDefault)
    _optionMenu = ctk.CTkOptionMenu(
        frame,
        values              = values,
        variable            = varMenu,
        width               = width,
        fg_color            = background,
        button_color        = 'yellow',
        text_color          = textColor,
        dropdown_fg_color   = background,
        dropdown_text_color = 'black',
        dropdown_font       = F_font(),
        font                = F_font()
    )

    _optionMenu.grid(
        row        = row, 
        column     = column, 
        padx       = 5, 
        pady       = 5,
        sticky     = position,
        columnspan = colspan
    )

    return _optionMenu

# --------------------------------------------------------------------------- #
def createSpinbox( 
        frame: ctk.CTkFrame,
        row        = 0, 
        column     = 0, 
        minimum    = 0, 
        maximum    = 10, 
        increment  = 1,
        textColor  = 'black',
        background = 'white', 
        position   = 'w',
        width      = 5,
        fontSize   = 18,
        padx       = 5,
        pady       = 5
    ):

    _spinbox = mtk.mtTkinter.Spinbox(
        frame, 
        from_     = minimum, 
        to        = maximum, 
        width     = width,
        bg        = background, 
        fg        = textColor,
        font      = F_font(fontSize),
        increment = increment,
        buttonbackground = 'yellow'
    ) 

    _spinbox.grid(
        row    = row, 
        column = column, 
        padx   = padx, 
        pady   = pady, 
        sticky = position
    )

    spinVar = ctk.StringVar()
    
    _spinbox.configure(
        textvariable    = spinVar, 
        validate        = "key", 
        validatecommand = (
            frame.register(
                setInputInt if int(increment) else setInputFloat
            ), "%P"
        )
    )

    return _spinbox

# ___________________________________________________________________________ #
def createHSeparator(
        frame: ctk.CTkFrame, 
        row        = 0, 
        column     = 0, 
        colspan    = 2
    ):

    '''
        Params:
            row     = Position of the separator horizontally.\n
            column  = Start of the line in the selected column.\n
            colspan = Width of the separator measured in columns.
    '''

    _separator = ttk.Separator(frame, orient = 'horizontal')
    _separator.grid(row = row, column = column, columnspan = colspan, sticky = 'we', padx = 2, pady = 6)

    return _separator

# ___________________________________________________________________________ #
def createVSeparator(
        frame: ctk.CTkFrame, 
        row         = 0, 
        column      = 0, 
        rowspan     = 5
    ):

    '''
        Params:
            row     = Line that starts the separator.\n
            column  = Vertical position of the separator.\n
            rowspan = Height of the separator measured in lines.\n
    '''

    column = 2 if column == 0 else 5 if column == 1 else 8

    _separator = ttk.Separator(frame, orient = 'vertical')
    _separator.grid(row = row, column = column, rowspan = rowspan, sticky = 'ns', padx = 6, pady = 2)

    return _separator

# >>>>>>>>>>>>>>>>>>>>>>>>>> SIMPLE INPUT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #
def inputLabel(
        frame: ctk.CTkFrame, 
        row        = 0, 
        column     = 0, 
        text       = 'Label', 
        width      = 100,    
        textColor  = 'black',
        background = 'white',
        textAlignm = 'left',
        position   = 'left'
    ):

    '''
        Param textAlignm:
            The original format that receives "w, e, s, n" has been changed.\n
            New format "left, right, center".

        Param position:
            left, right, center or full
    '''

    position   = 'w' if position   == 'left' else 'e' if position   == 'right' else 'ns' if position == 'center' else 'we'
    textAlignm = 'w' if textAlignm == 'left' else 'e' if textAlignm == 'right' else 'center'

    def value():
        return _label.cget("text")

    _label = createLabel(
        frame, 
        row, 
        column, 
        text       = text, 
        width      = width, 
        textColor  = textColor, 
        background = background, 
        position   = position, 
        textAlignm = textAlignm
    )

    _label.value = value

    return _label

# ___________________________________________________________________________ #
def inputButton(
        frame: ctk.CTkFrame, 
        row        = 0, 
        column     = 0, 
        text       = 'button',
        textColor  = 'white',
        background = '#a70000',
        position   = 'left'
    ):

    '''
        Param position:
            The original format that receives "w, e, s, n" has been changed.\n
            New format "left, right, center, full".
    '''
    
    position = 'w' if position == 'left' else 'e' if position == 'right' else 'ns' if position == 'center' else 'we'

    _button = createButton(
        frame, 
        row, 
        column, 
        text = text, textColor = textColor, background = background, position = position
    )
   
    return _button

# ___________________________________________________________________________ #
def inputEntry(
        frame: ctk.CTkFrame, 
        row          = 0, 
        column       = 0, 
        text         = 'Label', 
        width        = 100,    
        textColor    = 'black',
        background   = 'white',
        defaultValue = '',
        textType     = 'text',
        position     = 'left',
        placeHolder  = 'Entry'
    ):

    '''
        Param textType:
            Text formatting with options for "int", "float", or "text".\n
            text  -> Accepts any character.\n
            int   -> Accepts only integer numbers.\n
            float -> Accepts numbers with decimal places.
        
        Param position:
            left, right, center or full
    '''

    position = 'w' if position == 'left' else 'e' if position == 'right' else 'ns' if position == 'center' else 'we'

    def value():
        return _entry.get()

    columnObj, columnLabel = columns(column)

    createLabel(frame, row, columnLabel, text = text, textColor = 'white', background = '#444444', position = 'w')
    _entry = createEntry(frame, row, columnObj, width, textColor, background, position = position, placeHolder = placeHolder)
    
    if textType != 'text':

        entryVar = ctk.StringVar()

        _entry.configure(
            textvariable    = entryVar, 
            validate        = "key", 
            validatecommand = (
                frame.register(
                    setInputInt if textType == 'int' else setInputFloatEntry
                ), "%P"
            )
        )

        def onFocusOut(event):
            if not entryVar.get():     # If the field is empty  
                _entry.insert(0, '0')  # Fill with '0'
        
        _entry.bind("<FocusOut>", onFocusOut)

    # Insert the default value in the field.
    _entry.insert(0, defaultValue if defaultValue else '0')

    _entry.value = value

    return _entry

# ___________________________________________________________________________ #
def inputIntSpinbox(
        frame: ctk.CTkFrame, 
        row          = 0, 
        column       = 0,
        text         = 'Label',  
        minimum      = 0, 
        maximum      = 10, 
        width        = 5,
        textColor    = 'black',
        background   = 'white',
        defaultValue = 0,
        position     = 'left'
    ):

    '''
        Param position:
            left, right or center
    '''

    position = 'w' if position == 'left' else 'e' if position == 'right' else 'ns'

    def value():
        return _spin.get()

    columnObj, columnLabel = columns(column)

    createLabel(frame, row, columnLabel, text = text, textColor = 'white', background = '#444444', position = 'w')
    
    _spin = createSpinbox(frame, row, columnObj, minimum, maximum, 1, textColor, background, position, width)
    _spin.insert(0, defaultValue)

    _spin.value = value

    return _spin

# ___________________________________________________________________________ #
def inputFloatSpinbox(
        frame: ctk.CTkFrame, 
        row          = 0, 
        column       = 0,
        text         = 'Label',  
        minimum      = 0, 
        maximum      = 10, 
        width        = 5,
        textColor    = 'black',
        background   = 'white',
        defaultValue = 0.0,
        position     = 'left'
    ):

    '''
        Param position:
            left, right or center
    '''

    position = 'w' if position == 'left' else 'e' if position == 'right' else 'ns'

    def value():
        return _spin.get()

    columnObj, columnLabel = columns(column)

    createLabel(frame, row, columnLabel, text = text, textColor = 'white', background = '#444444', position = 'w')
   
    _spin = createSpinbox(frame, row, columnObj, minimum, maximum, 0.1, textColor, background, position, width)
    _spin.insert(0, defaultValue)

    _spin.value = value
    
    return _spin

# ___________________________________________________________________________ #
def inputOptions(
        frame: ctk.CTkFrame,
        row          = 0, 
        column       = 0, 
        text         = 'Label', 
        values: list = [],
        defaultValue = '',
        width        = 70 ,
        position     = 'left'   
    ):

    '''
        Param position:
            left, right or center
    '''

    position = 'w' if position == 'left' else 'e' if position == 'right' else 'ns'

    def value():
        return _options.get()

    columnObj, columnLabel = columns(column)

    createLabel(frame, row, columnLabel, text = text, textColor = 'white', background = '#444444', position = 'w')

    _options = createOptions(frame, row, columnObj, values, defaultValue, position = position, width = width)

    _options.value = value

    return _options

# ___________________________________________________________________________ #
def inputCheckbox(
        frame: ctk.CTkFrame, 
        row          = 0, 
        column       = 0, 
        text         = 'checkbox',
        defaultValue = 'False',
        textColor    = 'white',
        background   = 'transparent',
        position     = 'left'
        
    ):

    '''
        Param position:
            left, right, or center
    '''

    position = 'w' if position == 'left' else 'e' if position == 'right' else 'ns'

    checkVar = ctk.BooleanVar()

    checkVar.set(0)

    def value():
        return checkVar.get()
    
    _checkBox = createCheckbox(
        frame, 
        row, 
        column, 
        text = text, textColor = textColor, background = background, checkColor = '#4bbb00', position = position
    )

    _checkBox.configure(variable = checkVar)

    if defaultValue == 'True':
        checkVar.set(1)

    # Property to get the state of the checkbox.
    _checkBox.value = value

    return _checkBox

# ___________________________________________________________________________ #
def inputSlider(
        frame: ctk.CTkFrame, 
        row          = 0, 
        column       = 0, 
        startValue   = 0,
        endValue     = 1,
        defaultValue = 0.0,
        buttonColor  = '#2d92cc',
        background   = '#444444',
        position     = 'left',
        text         = ''
    ):

    '''
        Param position:
            left, right, center or full
    '''

    position = 'w' if position == 'left' else 'e' if position == 'right' else 'ns' if position == 'center' else 'we'

    def value(value):

        _lb.configure(text = f"{text} {float(value):.2f}")
        return value
    
    columnObj, columnLabel = columns(column)

    _slider = createSlider(
        frame, 
        row, 
        columnObj, 
        startValue,
        endValue,
        buttonLength = 5, buttonColor = buttonColor, background = background, position = position        
    )

    _slider.configure(command = value)
    _slider.set(float(defaultValue))

    _lb = createLabel(frame, row, columnLabel, text = f'{text} {defaultValue}', textColor = 'white', background = '#444444', position = 'w')  
    
    # Property to get the value of the slider.
    _slider.value = lambda: _slider.get()

    return _slider

# ___________________________________________________________________________ #
def inputColor(
        frame: ctk.CTkFrame,
        row          = 0, 
        column       = 0, 
        text         = 'Label', 
        color        = '#a70000',
        defaultColor = '#a70000',
        position     = 'left'
    ):

    '''
        Param position:
            left or right
    '''

    position = 'w' if position == 'left' else 'e'


    icon = ctk.CTkImage(Image.open(pathIcon), size =(20, 20))

    def value():
        return _color.cget("fg_color") 
    
    def defColor():
        _color.configure(fg_color = defaultColor)

    columnObj, columnLabel = columns(column)

    createLabel(frame, row, columnLabel, text = text, textColor = 'white', background = '#444444', position = 'w')
    
    _color = createButton(
        frame, 
        row, 
        columnObj, 
        text = '', background = color, position = position, width = 70, cornerRadius = 5
    )
    _color.configure(command = lambda: buttonColor(_color, row, columnObj))

    _default = createButton(
        frame, 
        row, 
        columnObj, 
        text = '', background = '#444444', position = position, width = 10, cornerRadius = 5, image = icon
    )
    _default.configure(command = defColor)
    
    CTkToolTip(
        _default, 
        message      = "Default color",  
        bg_color     = '#646464', 
        text_color   = '#ffffff',
        border_width = 2,
        border_color = 'white'
    )

    # Property to get the color of the button.
    _color.value = value 
   
    return _color

# ___________________________________________________________________________ #
def inputCalendar(
        frame,
        row      = 0,
        column   = 0,
        date     = '2024-01-01',
        fontSize = 15
    ):

    def value():
        return _calendar.get_date()
    
    date = date.split('-')

    _calendar = Calendar(
        frame,
        selectMode             = 'day',
        year                   = int(date[0]),
        month                  = int(date[1]),
        day                    = int(date[2]),
        font                   = F_font(fontSize),
        date_pattern           = 'y-mm-dd',
        normalbackground       = '#D3D7CF',
        weekendbackground      = '#BF9E6B',
        headersbackground      = '#636363',
        headersforeground      = 'white',
        othermonthbackground   = '#83B6EB',
        othermonthwebackground = '#af8d59',
        othermonthforeground   = '#EEEEE2',
        othermonthweforeground = '#EEEEE2'
    )

    _calendar.grid(
        row    = row,
        column = column,
        sticky = 'w'
    )

    _calendar.value = value

    return _calendar

# ___________________________________________________________________________ #
def inputDatetime(
        frame: ctk.CTkFrame,
        row      = 0,
        column   = 0,
        text     = 'date',
        dateTime = '2024-01-01 00:00'
    ) -> str:

    icon = ctk.CTkImage(Image.open(pathCheck), size =(20, 20))

    def value():

        hours   = f'{int(_spinHour.get()):02}'
        minutes = f'{int(_spinMinute.get()):02}'

        return f'{_datetime.get_date()} {hours}:{minutes}'
    
    columnObj, columnLabel = columns(column)

    dateTime = re.split('[-: ]', dateTime)

    createLabel(frame, row, columnLabel, text = text, textColor = 'white', background = '#444444', position = 'w')
    
    _dateFrame = createFrame(frame, row, columnObj, background = "transparent")

    _datetime  = DateEntry(
        _dateFrame,
        date_pattern           = "yyyy-mm-dd",
        width                  = 10,
        font                   = F_font(16),
        normalbackground       = '#D3D7CF',
        weekendbackground      = '#BF9E6B',
        headersbackground      = '#636363',
        headersforeground      = 'white',
        othermonthbackground   = '#83B6EB',
        othermonthwebackground = '#af8d59',
        othermonthforeground   = '#EEEEE2',
        othermonthweforeground = '#EEEEE2'
    )

    _datetime.grid(
        row    = 0,
        column = 0,
        padx   = 5,
        sticky = 'w'
    )
    _datetime.set_date(date(int(dateTime[0]), int(dateTime[1]), int(dateTime[2])))

    tm = ctk.StringVar()
    _datetime.configure(
        textvariable    = tm, 
        validate        = "key", 
        validatecommand = (
            frame.register(
                setInputDate
            ), "%P"
        )
    )

    _spinHour = createSpinbox(_dateFrame, 0, 1, padx = 1, minimum = 0, maximum = 23, width = 2, position = 'w', fontSize = 16)
    _spinHour.insert(0, int(dateTime[3]))

    _spinMinute = createSpinbox(_dateFrame, 0, 2, padx = 1, minimum = 0, maximum = 59, width = 2, position = 'w', fontSize = 16)
    _spinMinute.insert(0, int(dateTime[4]))

    _btn = createButton(_dateFrame, 0, 3, text = '', width = 10, cornerRadius = 4, image = icon, background = 'transparent')
    _btn.configure(command = value)
    
    CTkToolTip(
        _btn, 
        message      = "Confirm",  
        bg_color     = '#646464', 
        text_color   = '#ffffff',
        border_width = 2,
        border_color = 'white'
    )

    _datetime.value = value

    return _datetime

# ___________________________________________________________________________ #
# ___________________________ FUNCTIONS _____________________________________ #

def columns(column: int):
     
    columnObj   = 1 if column == 0 else 4 if column == 1 else 7 if column == 2 else 10
    columnLabel = 0 if column == 0 else 3 if column == 1 else 6 if column == 2 else 9

    return columnObj, columnLabel

# ___________________________________________________________________________ #
def buttonColor(button, row, column):

    try:
        pickColor = AskColor()      # open the color picker
        color     = pickColor.get() # get the color string

        button.grid(row = row, column = column)
        button.configure(fg_color = color)

    except:
        pass

# ___________________________________________________________________________ #
def setInputFloat(newValue):

    if newValue == "":
        return True

    regex = r'^-?\d*\.?\d{0,4}$'

    return bool(re.match(regex, newValue))
    
# ___________________________________________________________________________ #
def setInputInt(newValue):

    if newValue == "":
        return True

    regex = r'^-?\d*$'

    return bool(re.match(regex, newValue))

# ___________________________________________________________________________ #
def setInputDate(newValue):

    if newValue == "":
        return True

    regex = r'^[\d-]*$'

    return bool(re.match(regex, newValue))

# ___________________________________________________________________________ #
def setInputFloatEntry(newValue):

    if newValue == "":
        return True

    regex = r'^-?\d*\.?\d*$'

    return bool(re.match(regex, newValue))

