import sys
from   os               import path
import plotly.graph_objects as go

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 2))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mDataSeries              import *
from CreateIndicator.Plots.mToolTip      import *
from CreateIndicator.Plots.mToolTipLines import *

# ___________________________________________________________________________ #
def plotCandle(
        fig, 
        df:        pd.DataFrame, 
        listIndex: list, 
        color       = 'gray',
        isHistogram = False
    ):

    numberRow = 2 if isHistogram else 1

    tooltip = F_toolTip(df)
    date    = dates(df)
    op      = opens(df)
    hg      = highs(df)
    lw      = lows(df)
    cl      = closes(df)

    fig.add_trace(
        go.Candlestick(
            x                     = [date[i] for i in listIndex],
            open                  = [op[i]   for i in listIndex],
            high                  = [hg[i]   for i in listIndex],
            low                   = [lw[i]   for i in listIndex],
            close                 = [cl[i]   for i in listIndex],
            text                  = tooltip,
            hoverinfo             = 'text',
            increasing_line_color = color,
            decreasing_line_color = color,
            increasing_fillcolor  = color,
            decreasing_fillcolor  = color
        ),
        row = numberRow,
        col = 1
    )
 
    if isHistogram:

        fig.update_layout(
            yaxis2 =
                dict(
                side     = 'right',
                showgrid = False,
            ),
            xaxis2 = dict(
                showgrid    = False,
                rangeslider = dict(
                    visible = False
                )
            )
        )

# ___________________________________________________________________________ #
def plotHistogram(
        fig, 
        listDates:  list, 
        listValues: list, 
        listColor:  list
    ):

    fig.add_trace(
        go.Bar(
            x            = [date   for date   in listDates],
            y            = [values for values in listValues], 
            showlegend   = False, 
            opacity      = 1,
            marker_color = [color for color in listColor],
            yaxis        = 'y',
            name         = '',
        ), 
        row         = 2, 
        col         = 1, 
        secondary_y = False
    )

    fig.update_layout(
        bargap = 0.05,
        yaxis2 =
            dict(
            side     = 'right',
            showgrid = False
        ),
        xaxis2 = dict(showgrid = False)
    )

# ___________________________________________________________________________ #
def plotLineColor(
        fig, 
        listDates:  list, 
        listPrices: list, 
        listColor:  list, 
        widthLine   = 1,
        isHistogram = False
    ):

    '''
        Line style set to "dotted" (dot).\n
        Note: It's not possible to change the line style
    '''

    numberRow = 2 if isHistogram else 1
    tooltip   = F_toolTipLines(listPrices)
    listLines = []

    # Protection
    widthLine = 1 if widthLine > 5 else widthLine

    listLines.append(
        go.Scatter(
            x         = [date   for date   in listDates],
            y         = [prices for prices in listPrices],
            mode      = 'markers',
            name      = '',
            text      = tooltip,
            hoverinfo = 'text',
            marker    = dict(
                size  = widthLine,
                color = [color for color in listColor]
            )
        )
    )

    if isHistogram:

        fig.update_layout(
            yaxis2 =
                dict(
                side     = 'right',
                showgrid = False
            ),
            xaxis2 = dict(showgrid = False)
        )

    for line in listLines:
        fig.add_trace(line, row = numberRow, col = 1)

# ___________________________________________________________________________ #
def plotLines(
        fig, 
        listDates:  list, 
        listPrices: list, 
        colorRGB    = 'white', 
        typeLine    = 'solid', 
        widthLine   = 1,
        isHistogram = False
    ):

    """
        Args:
            colorRGB : 'rgb'\n
            typeLine:  'solid' 'dash', 'dot' and 'dashdot'\n
            widthLine:  max 5.
    """

    numberRow = 2 if isHistogram else 1
    tooltip   = F_toolTipLines(listPrices)
    listLines = []

    # Protection
    widthLine = 1 if widthLine > 5 else widthLine

    listLines.append(
        go.Scatter(
            x         = listDates,
            y         = listPrices,
            mode      = 'lines',
            name      = '',
            text      = tooltip,
            hoverinfo = 'text',
            line      = dict(
                shape = 'linear',
                color = colorRGB, 
                dash  = typeLine, 
                width = widthLine
            )
        )
    )

    if isHistogram:

        fig.update_layout(
            yaxis2 =
                dict(
                side     = 'right',
                showgrid = False
            ),
            xaxis2 = dict(showgrid = False)
        )

    for line in listLines:
        fig.add_trace(line, row = numberRow, col = 1)
    

# ___________________________________________________________________________ #
def plotHorizontalLine(
        fig, 
        startDate:  pd.Timestamp, 
        endDate:    pd.Timestamp, 
        price:      float, 
        colorRGB    = 'white', 
        typeLine    = 'solid', 
        widthLine   = 1,
        isHistogram = False
    ):

    """
        Args:
            colorRGB: 'rgb'\n
            typeLine: 'solid' 'dash', 'dot' and 'dashdot'\n
            widthLine: max 5.
    """

    numberRow = 2 if isHistogram else 1
    tooltip   = F_toolTipLines([price])
    listLines = []

    # Protection
    widthLine = 1 if widthLine > 5 else widthLine

    listLines.append(
        go.Scatter(
            x         = [startDate, endDate],
            y         = [price, price],
            mode      = 'lines',
            name      = '',
            text      = tooltip,
            hoverinfo = 'text',
            line      = dict(
                shape = 'linear',
                color = colorRGB, 
                dash  = typeLine, 
                width = widthLine
            )
        )
    )

    if isHistogram:

        fig.update_layout(
            yaxis2 =
                dict(
                side     = 'right',
                showgrid = False
            ),
            xaxis2 = dict(showgrid = False)
        )

    for line in listLines:
        fig.add_trace(line, row = numberRow, col = 1)

# ___________________________________________________________________________ #
def plotVerticalLine(
        fig, 
        date:       pd.Timestamp, 
        startPrice: float, 
        endPrice:   float,
        colorRGB    = 'white', 
        typeLine    = 'solid', 
        widthLine   = 1,
        isHistogram = False
    ):

    """
        Args:
            colorRGB: 'rgb'\n
            typeLine: 'solid' 'dash', 'dot' and 'dashdot'\n
            widthLine: max 5
    """

    numberRow = 2 if isHistogram else 1
    tooltip   = F_toolTipLines([startPrice, endPrice])
    listLines = []

    # Protection
    widthLine = 1 if widthLine > 5 else widthLine

    listLines.append(
        go.Scatter(
            x         = [date, date],
            y         = [startPrice, endPrice],
            mode      = 'lines',
            name      = '',
            text      = tooltip,
            hoverinfo = 'text',
            line      = dict(
                shape = 'linear',
                color = colorRGB, 
                dash  = typeLine, 
                width = widthLine
            )
        )
    )

    if isHistogram:

        fig.update_layout(
            yaxis2 =
                dict(
                side     = 'right',
                showgrid = False
            ),
            xaxis2 = dict(showgrid = False)
        )

    for line in listLines:
        fig.add_trace(line, row = numberRow, col = 1)

# ___________________________________________________________________________ #
def plotLabel(
        fig,
        dateAnchor: pd.Timestamp, 
        price:      float, 
        text:       str,
        textAlign       = 'center',
        textColor       = 'white',
        fontSize        = 13, 
        showArrow       = False, 
        arrowPosition   = 'top',
        arrowHeight     = 10,
        arrowWidth      = 2,
        arrowType       = 0,
        rgbaBackground  = 'rgba(70, 70, 70, 0.663)', 
        rgbaBorderColor = 'rgba(80, 192, 28, 0.659)',
        isHistogram     = False
    ):

    """
        Args:
            textAlign:     'left', 'center' and 'right'\n
            arrowPosition: 'top', 'bottom', 'left' and 'right'\n
            arrowType: 
                0 -> Line,
                1 -> Arrow1,
                2 -> Arrow2,
                3 -> Arrow3,
                4 -> Arrow4,
                5 -> Arrow5,
                6 -> Circule,
                7 -> Square

    """

    # Protection
    textAlign  = 'center' if textAlign != 'left' and textAlign != 'center' and textAlign != 'right' else textAlign
    arrowType  = 0 if arrowType  > 7 else arrowType
    arrowWidth = 1 if arrowWidth > 5 else arrowWidth

    position = ( [0,  40] if arrowPosition == 'top'    else 
                 [0, -40] if arrowPosition == 'bottom' else
                 [-80, 0] if arrowPosition == 'right'  else [80, 0]
               )
    
    position[0] = position[0]+arrowHeight if arrowPosition == 'left' else position[0]-arrowHeight if arrowPosition == 'right'  else position[0]
    position[1] = position[1]+arrowHeight if arrowPosition == 'top'  else position[1]-arrowHeight if arrowPosition == 'bottom' else position[1]

    textAlign   = 'center' if arrowPosition == 'left' or arrowPosition == 'right' else textAlign
    yref        = 'y2' if isHistogram else 'y'

    fig.add_annotation(
        x           = dateAnchor,
        y           = price,
        text        = text, 
        xanchor     = textAlign,
        showarrow   = showArrow,
        arrowhead   = arrowType,  
        arrowcolor  = rgbaBorderColor,  
        ax          = position[0],
        ay          = position[1],
        arrowsize   = arrowWidth,
        bgcolor     = rgbaBackground,
        bordercolor = rgbaBorderColor,
        arrowwidth  = arrowWidth,
        borderpad   = 4,
        borderwidth = 4,
        font        = dict(
            color  = textColor,
            family = "Monaco, monospace",
            size   = fontSize
        ),
        yref = yref
    )

    if isHistogram:

        fig.update_layout(
            yaxis2 = dict(
                side     = 'right',
                showgrid = False
            ),
            xaxis2 = dict(showgrid = False)
        )

# ___________________________________________________________________________ #
def plotText(
        fig, 
        dateAnchor: pd.Timestamp, 
        price:      float, 
        text:       str, 
        textAlign   = 'center', 
        color       = 'white', 
        fontSize    = 13,
        isHistogram = False
    ):

    """
        Args:
            textAlign: 'left', 'center' and 'right'\n
    """

    # Protection
    textAlign = 'right' if textAlign == 'left' else 'left' if textAlign == 'right' else textAlign
    textAlign = 'center' if textAlign != 'left' and textAlign != 'center' and textAlign != 'right' else textAlign

    yref = 'y2' if isHistogram else 'y'

    fig.add_annotation(
        x         = dateAnchor,
        y         = price,
        text      = text,
        xanchor   = textAlign,
        showarrow = False,
        font      = dict(
            color  = color,
            family = "Monaco, monospace",
            size   = fontSize
        ),
        yref = yref
    )

    if isHistogram:

        fig.update_layout(
            yaxis2 = dict(
                side     = 'right',
                showgrid = False
            ),
            xaxis2 = dict(showgrid = False)
        )

# ___________________________________________________________________________ #
def plotFigure(
        fig, 
        dateAnchor: pd.Timestamp, 
        price:      float, 
        typeFigure  = 1, 
        direction   = 'top', 
        figureAlign = 'center', 
        color       = 'white', 
        fontSize    = 13,
        isHistogram = False
    ):

    """
        Args:
            typeFigure:  1 style '▲' and 2 style '△'\n
            direction:   'top', 'bottom', 'left' and 'right'\n
            figureAlign: 'left', 'center' and 'right'
    """

    # Protection
    typeFigure  = 1 if typeFigure != 1 and typeFigure != 2 else typeFigure
    direction   = 'top' if direction != 'top' and direction != 'bottom' and direction != 'left' and direction != 'right' else direction
    figureAlign = 'right' if figureAlign == 'left' else 'left' if figureAlign == 'right' else figureAlign
    figureAlign = 'center' if figureAlign != 'left' and figureAlign != 'center' and figureAlign != 'right' else figureAlign
    yref        = 'y2' if isHistogram else 'y'

    type1 = (
        '▲' if direction == 'top'    else '▼' 
            if direction == 'bottom' else '◀' 
            if direction == 'left'   else '▶' 
    )
    
    type2 = (
        '△' if direction == 'top'    else '▽' 
            if direction == 'bottom' else '◁' 
            if direction == 'left'   else '▷'
    )

    # 1 or 2
    figure = type1 if typeFigure == 1 else type2 if typeFigure == 2 else type1

    fig.add_annotation(
        x         = dateAnchor,
        y         = price,
        text      = figure, 
        xanchor   = figureAlign,
        showarrow = False,
        font      = dict(
            color = color,
            size  = fontSize
        ),
        yref = yref
    )

    if isHistogram:

        fig.update_layout(
            yaxis2 = dict(
                side     = 'right',
                showgrid = False
            ),
            xaxis2 = dict(showgrid = False)
        )

# ___________________________________________________________________________ #
def plotFill(
        fig,
        listDate:   list, 
        listPrice1: list, 
        listPrice2: list, 
        rgbaColor   = 'rgba(255, 0, 0, 0.082)',
        isHistogram = False
    ):

    numberRow = 2 if isHistogram else 1

    # Add the fill to the chart layout
    fig.add_trace(go.Scatter(
        x         = listDate   + listDate[::-1],
        y         = listPrice1 + listPrice2[::-1],
        fill      = 'toself',
        fillcolor = rgbaColor,
        line      = dict(color = rgbaColor),
        name      = ''
    ), row = numberRow, col = 1)

    if isHistogram:

        fig.update_layout(
            yaxis2 =
                dict(
                side     = 'right',
                showgrid = False
            ),
            xaxis2 = dict(showgrid = False)
        )

# ___________________________________________________________________________ #


