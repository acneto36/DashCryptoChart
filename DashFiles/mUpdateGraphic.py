import sys
from   os               import path
import plotly.graph_objects as go
from   plotly.subplots  import make_subplots

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from paths                          import *
from CreateIndicator.Plots.mToolTip import *  
from DataFrames.mFormatNumber       import * 
from SystemFiles.mWriteRead         import *


# ___________________________________________________________________________ #
def F_updateGraph(df):

    pathWave       = readingFile(PATH_HWaves)[0]
    foundHistogram = readingFile(PATH_Histogram)[0]
    heightWave     = float(pathWave) if int(foundHistogram) > 0 else 0
    hovertext      = F_toolTip(df)

    heightHistogram = heightWave / 10 if heightWave <= 5 else 0.5

    lastPrice   = df['close'].iloc[-1]
    formatPrice = '.3f' if greaterThanZero(formatNumber(lastPrice)) else '.9f'

    valueH = [5, 4, 3, 2, 1]
    fractH = [1, 1.11, 1.25, 1.45, 1.65]

    separatorY = next(
        (heightHistogram * fract for value, fract in zip(valueH, fractH) if heightWave == value), 
        0
    )
    
    fig = make_subplots(
        rows             = 2, 
        cols             = 1, 
        shared_xaxes     = True if int(foundHistogram) > 0 else False, 
        vertical_spacing = 0.0, # Space between graph and histogram
        row_heights      = [0.5, heightHistogram] # [graphic, histogram]
    )

    fig.add_trace(
        go.Candlestick(
            x         = df['date'],
            open      = df['open'],
            high      = df['high'],
            low       = df['low'],
            close     = df['close'],
            text      = hovertext,
            hoverinfo = 'text'
        ), row = 1,
           col = 1
    )

    fig.update_layout(
        template = 'plotly_dark',
        yaxis    = dict(
            showgrid   = False, 
            side       = 'right', 
            automargin = False,
            tickformat = formatPrice
        ),
        xaxis = dict(
            showgrid   = False, 
            title      = None, 
            rangeslider_visible = False
        ),
        title      = None,
        hovermode  = None,
        showlegend = False,
        dragmode   = 'pan',
        modebar    = dict(
            color       = 'black',
            bgcolor     = 'white',
            activecolor = 'aqua',
            orientation = 'v',
        ),
        hoverlabel = dict(
            bgcolor     = 'black',
            bordercolor = 'gray',
            font_color  = 'white',
            font_size   = 13,
            font_family = 'Monaco, monospace',
        ),
        modebar_add = [
            'drawline',
            'drawopenpath',
            'drawclosedpath',
            'drawcircle',
            'drawrect',
            'eraseshape',
        ],
        newshape = dict(
            line = dict(
                color = '#08a3ca',
                dash  = 'solid',
                width = 5
            )
        ),
        paper_bgcolor = 'rgba(0, 0, 0, 0)',        # Background
        plot_bgcolor  = 'rgba(61, 61, 61, 0.479)', # Chart

        # Row separator
        shapes = [
            dict(
                type    = "line",
                xref    = "paper",
                yref    = "paper",
                x0      = 0,
                y0      = separatorY,
                x1      = 1,
                y1      = separatorY,
                line    = dict(color = "#ffffff", width = 1),
                opacity = 0.7
            )
        ],
    )

    return fig

# ___________________________________________________________________________ #