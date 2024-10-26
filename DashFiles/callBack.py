
import sys
from   os                import path
from   dash.dependencies import Input, Output, State
import pandas                as pd
import json

srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)


from paths                        import *
from SystemFiles.mInstanceModules import *
from SystemFiles.mWriteLog        import *
from SystemFiles.mWriteRead       import *
from DataFrames.mRecreateFile      import *
from DashFiles.mUpdateGraphic     import *
from DataFrames.mFormatNumber import *

# ___________________________________________________________________________ #
class CallBack:

    def __init__(self, symbolToCsv, app):

        self.symbolToCsv = symbolToCsv
        self.app         = app
        self.openInput   = 0
        self.openCreate  = 0
        self.newSymbol   = None
        self.fig         = None
        self.lastPrice   = None
        self.df          = None
        self.firstRun    = True

    # ___________________________________________________________________________ #  
    def F_callbacks(self):

        # ___________________________________________________________________________ #
        # "Callback for the button to pause the chart update."
        @self.app.callback(
            Output('update', 'disabled'),       # "Disable the update interval."
            Output('pause-button', 'children'), # "Change the button text."
            Input('pause-button', 'n_clicks'),  # "Monitor the number of clicks on the button."
            State('update', 'disabled')         # "Retrieve the current state of the update interval."
        )
        def toggle_update_interval(n_clicks, update_disabled):

            if n_clicks is None:
                n_clicks = 0

            if n_clicks % 2 == 0:  # "If the number of clicks is even, enable the update."
                return False, 'Pause'
            else:                  # "If the number of clicks is odd, pause the update."
                return True, 'Update'

        # ___________________________________________________________________________ #
        @self.app.callback(
            Output('update', 'interval'),
            Input('interval', 'value')
        )
        def update_interval(update):
            # "Convert the value to milliseconds and set it as the interval."
            return update*1000

        # ___________________________________________________________________________ #
        @self.app.callback(
            Output('zoomInfo', 'data'),
            [Input('candlestick-graph', 'relayoutData'),
            Input('zoomInfo', 'data'),
            Input('symbol-dropdown', 'value')]
        )
        def update_zoom_info(relayoutData, zoomInfo, selectedSymbol):

            if zoomInfo is None:
                zoomInfo = {"symbol": selectedSymbol}

                return zoomInfo
            
            else:
                if selectedSymbol not in zoomInfo.get("symbol", {}):
                    zoomInfo = {"symbol": selectedSymbol}

                else:
                    zoomInfo.update(relayoutData)

                return zoomInfo

        # ___________________________________________________________________________ #
        @self.app.callback(
            Output('candlestick-graph', 'figure'),
            Output('last-price', 'value'),
            Output('listIndicator', 'value'),  # "Update the checked values of the checklist."
            Input('symbol-dropdown', 'value'),
            Input('inputs-dropdown', 'value'), 
            Input('update', 'n_intervals'),
            Input('openInput', 'n_clicks'),
            Input('listIndicator', 'value'),
            State('zoomInfo', 'data')
        )
        def update_graph(selectedSymbol, selectedInput, update, click, lstInputInd, zoomInfo):
            
            defaultList = []

            if self.firstRun:
                lstInputInd   = F_readIndicator(PATH_PlotInd, selectedSymbol)
                self.firstRun = False

            try:
                F_checkEmptyIndicator(PATH_PlotInd)

                csv_file = self.symbolToCsv[selectedSymbol]
                self.df  = pd.read_csv(csv_file)

            except:
                pass


            # Ensure that if an error occurs in the callback, open the input screen for correction
            self.openInput = F_selectInput( selectedInput, selectedSymbol, click, self.openInput, self.df )

            F_writeFile(selectedSymbol, PATH_Symbol)

            try:
                self.lastPrice = formatNumber(self.df["close"].iloc[-1])
                self.fig       = F_updateGraph(self.df)

                if self.newSymbol != selectedSymbol: 

                    self.newSymbol = selectedSymbol
                    defaultList    = F_readIndicator(PATH_PlotInd, selectedSymbol)
                    lstInputInd    = defaultList # Update lstInputInd
                    self.firstRun  = True

                else:
                    defaultList = lstInputInd # Update defaultList
                    F_savePlotIndicator(selectedSymbol, defaultList)

                if len(defaultList) > 0:
                    
                    F_instanceInd(self.fig, self.df, selectedSymbol, defaultList) 

                else:
                    # Flag to determine if a histogram is selected, defaulting to no histogram
                    # Code sequence to indicate that there is a histogram in SystemFiles.mSelectIndicator
                    F_writeFile('0', PATH_Histogram)

                zoomInfo['symbol'] = selectedSymbol

                if zoomInfo:
                    for axisName in ['axis', 'axis2']:
                        if f'x{axisName}.range[0]' in zoomInfo:

                            self.fig['layout'][f'x{axisName}']['range'] = [
                                zoomInfo[f'x{axisName}.range[0]'],
                                zoomInfo[f'x{axisName}.range[1]']
                            ]

                        if f'y{axisName}.range[0]' in zoomInfo:
                            
                            self.fig['layout'][f'y{axisName}']['range'] = [
                                zoomInfo[f'y{axisName}.range[0]'],
                                zoomInfo[f'y{axisName}.range[1]']
                            ]

                with open(PATH_ZoomInfo, 'w') as f:
                    json.dump(zoomInfo, f)


            except Exception as e:
                
                if not str(e).contains('NoneType'):

                    F_writeLog(PATH_Log, f'Error callBack: {e}')
                    
                print("Error callBack: ", e)

                lstInputInd = F_readIndicator(PATH_PlotInd, selectedSymbol)
                print(f'Backup lstInputInd: {lstInputInd}')

                self.fig = F_updateGraph(self.df)
                pass

            finally:
                return self.fig, f'Price: {self.lastPrice}', defaultList
    
    # ___________________________________________________________________________ #