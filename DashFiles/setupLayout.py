from   dash                  import dcc, html
import dash_bootstrap_components as dbc

# ___________________________________________________________________________ #
class SetupLayout:
   
    def __init__(self, app, symbols, indicators, inputs):

        self.SYMBOLS    = symbols
        self.INDICATORS = indicators
        self.INPUTS     = inputs
        self.app        = app

        self.previous_indicator_count = len(indicators)

    def setup_layout(self):

        self.app.layout = html.Div(

            style = {
                'background-color': '#111111',
                'padding':          '5px',
                'height':           '96.5vh',
                'marginTop':        '5px',
            },
            
            children = [
                dcc.Location(id = 'url', refresh = False),

                # Div father 2 row, 2 col
                html.Div(
                    children = [
                        # Div child 1
                        html.Div(
                            children = [
                                dcc.Dropdown(
                                    id      = 'symbol-dropdown',
                                    options = [{'label': symbol, 'value': symbol} for symbol in self.SYMBOLS],
                                    value   = self.SYMBOLS[0],
                                    style   = {
                                        'width':    '150px', 
                                        'fontSize': '13px', 
                                        'display':  'inline-block'
                                    }  
                                ),

                                html.Label('   Inputs:  ', style = {'position': 'relative', 'top': '-5px', 'color': 'white'}),
                                dcc.Dropdown( 
                                    id      = 'inputs-dropdown',
                                    options = [{'label': inputs, 'value': inputs} for inputs in self.INPUTS],
                                    style   = {'position': 'relative', 'fontSize': '15px', 'width': '180px', 'display': 'inline-block'}
                                ),

                                dbc.Button( 
                                    'Open',
                                    id       = 'openInput',
                                    type     = 'number',
                                    n_clicks = 0,
                                    style    = {
                                        'color':         '#000000',
                                        'border-radius': '25%',
                                        'border':        '2px solid #EF2929',
                                        'width':         '100px',
                                        'fontFamily':    'Monaco, monospace',
                                        'fontSize':      '16px',
                                        'position':      'relative',
                                        'left':          '15px',
                                        'top':           '-12px'
                                    }
                                ),

                                html.Label(
                                    'Seconds: ',
                                    style = {
                                        'position': 'relative', 
                                        'left':     '50px',
                                        'top':      '-10px',
                                        'fontSize': '15px',
                                        'color':    'white'
                                    }
                                ),

                                dcc.Input(
                                    id    = 'interval',
                                    type  = 'number', 
                                    min   = 0, 
                                    max   = 1000, 
                                    step  = 1, 
                                    value = 3,
                                    style = {
                                        'width':      '50px',
                                        'display':    'inline-block',
                                        'fontFamily': 'Monaco, monospace',
                                        'fontSize':   '15px',
                                        'position':   'relative',
                                        'left':       '50px',
                                        'top':        '-12px'
                                    },
                                    placeholder = "Interval"
                                ),

                                dbc.Button( 
                                    'Pause',
                                    id       = 'pause-button',
                                    type     = 'number',
                                    n_clicks = 0,
                                    style    = {
                                        'color':         '#000000',
                                        'border-radius': '25%',
                                        'border':        '2px solid #EF2929',
                                        'width':         '100px',
                                        'fontFamily':    'Monaco, monospace',
                                        'fontSize':      '15px',
                                        'position':      'relative',
                                        'left':          '60px',
                                        'top':           '-12px'
                                    }
                                ),

                                dcc.Interval(
                                    id          = 'update',
                                    interval    = 3000,
                                    n_intervals = 0     
                                ),

                                dcc.Input( 
                                    id       = 'last-price', 
                                    type     = 'text', 
                                    value    = '',
                                    readOnly = True,
                                    style    = {
                                        'width':      '230px',
                                        'fontFamily': 'Monaco, monospace',
                                        'fontSize':   '15px',
                                        'display':    'inline-block',
                                        'textAlign':  'center',
                                        'position':   'relative',
                                        'left':       '120px',
                                        'top':        '-12px'
                                    }
                                ), 
                                dcc.Store(id = 'zoomInfo')
                            ],

                            style = {
                                'gridRow':     '1',
                                'gridColumn':  'span 2',  # Colspan
                                'background':  'linear-gradient(to right, #555753 , #170101)',
                                'height':      '40px',
                                'width':       '100%',
                                'marginRight': '20px',
                                'display':     'inline-block',
                                'white-space': 'nowrap'
                            }
                        ),
                        # Div Flex, child 2
                        html.Div( 
                            children = [

                                # Checklist left
                                html.Div(
                                    children = [
                                        html.Div("___Indicators___", style = {'font-weight': 'bold', 'color': 'white'}),
                                        dcc.Checklist(
                                            id      = 'listIndicator',
                                            options = [{'label': indicators, 'value': indicators} for indicators in self.INDICATORS],
                                            value   = [],
                                            labelStyle = {'color': '#f0f0f0'},
                                            style   = {
                                                'position': 'relative', 
                                                'top':      '50px',
                                                'fontSize': '14px'
                                            }
                                        ),
                                    ],

                                    style = {
                                            'background':  'linear-gradient(to right, #1A2140 , #515473)',
                                            'height':      '91vh',
                                            'width':       '160px',
                                            'marginRight': '5px',
                                        }
                                ),

                                # Graph right
                                html.Div( 
                                    children = [
                                        dcc.Graph(
                                            id     = 'candlestick-graph',
                                            config = {'scrollZoom': True, 'displayModeBar': True},
                                            style  = {
                                                'width':        '100%',
                                                'height':       '91vh', 
                                                'margin-left':  'auto', 
                                                'margin-right': '0'
                                            }
                                        )
                                    ],

                                    style = {
                                        'backgroundColor': '#111111',
                                        'height':          '90vh',
                                        'width':           '100%',
                                    }
                                ),
                            ],
                            style = {
                                'display':       'flex',
                                'flexDirection': 'row',  
                                'width':         '100%', 
                                'gridColumn':    'span 2',
                            }
                        ),
                    ],

                    style = {
                        'display':             'grid',
                        'gridTemplateRows':    'auto auto',  # 2 rows
                        'gridTemplateColumns': '50% 50%',    # 2 cols
                        'gap':                 '5px',        # Spacing between cells
                    }
                )
            ]
        )

# ___________________________________________________________________________ #