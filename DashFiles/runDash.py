import sys
import dash
import socket
import webbrowser
from   os        import path
from   threading import Timer


srcPath = path.realpath(path.join(path.dirname(__file__), *(['..']) * 1))

if srcPath not in sys.path:
    sys.path.append(srcPath)

from DataFrames.mValuesDataFrame import *
from DashFiles.callBack          import *
from DashFiles.setupLayout       import *

# ___________________________________________________________________________ #
class RunDash:

    def __init__(self):

        SYMBOLS, LSTINDS, LSTINPS, symbolCsv, _ = F_valuesDataFrame()

        self.port          = 8010
        self.stopRequested = False
        self.app           = dash.Dash(__name__, update_title = None)

        setupLayoutInstance = SetupLayout(self.app, SYMBOLS, LSTINDS, LSTINPS)
        setupLayoutInstance.setup_layout()

        callBackInstance = CallBack(symbolCsv, self.app)
        callBackInstance.F_callbacks()

    # ___________________________________________________________________________ #
    def F_portInUse(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', self.port))
                return False
            
            except socket.error as e:
                return True

    # ___________________________________________________________________________ #
    def run(self):

        if self.F_portInUse():
            print(f"Port {self.port} is already in use. Changing the port......")
            self.port += 1

        else:

            Timer(1, self.open_browser).start() # Não alterar use_reloader para True, vai dar bug
            self.app.run_server(debug = True, use_reloader = False, port = self.port)

    # ___________________________________________________________________________ #
    def stop(self):
        
        self.stopRequested = True
        print('Dash stopped')

    # ___________________________________________________________________________ #
    def open_browser(self):
        
        webbrowser.open_new(f'http://127.0.0.1:{self.port}/')

