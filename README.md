
# Cryptocurrency Technical Analysis Project.

Project built in **Python** using the **Dash Plotly** library for technical analysis. The purpose of this project is focused on market studies, primarily in **cryptocurrencies**.

O projeto oferece:
- **Candlestick Visualization**: Displays candlestick charts for price analysis.
- **Cryptocurrency Selection**:  Option to choose which cryptocurrency to view from a pre-selected list.
- **Custom Indicators**:         Dedicated interface to create and view custom indicators.

On the main application screen, in the **Help** menu, there is a more detailed tutorial about its functionality and the methods that can be used to create indicators.

## Project Structure

- **mainDash.py**:            Main file to initialize the Dash application.
- **start_Linux.sh**:        `bash` file to run the project directly on Linux.
- **startWin_noPrompt.bat**: `bat` file to run on Windows without the command prompt visible.
- **startWin_Prompt.bat**:   `bat` file to run on Windows with the command prompt visible.

## Installation

  - Clone the repository:
    ```bash
    git clone https://github.com/acneto36/DashCrypto-Chart.git
    ```

### Linux

1. Install `pip` and other necessary dependencies:
    ```bash
    sudo apt install python3-pip
    ```

    ```bash
    sudo apt install python-tk
    ```

    ```bash
    sudo apt install python3-pil python3-pil.imagetk


2. Within the project, install the necessary libraries with:

    ```bash
    pip3 install -r requirements.txt
    ```

3. If you receive an error similar to this:

    ```bash
    error: externally-managed-environment

    × This environment is externally managed
    ╰─> To install Python packages system-wide, try apt install
        python3-xyz, where xyz is the package you are trying to
        install.
    ```

4. Run the command below if you do not wish to create a virtual environment:

    ```bash
    pip3 install --break-system-packages -r requirements.txt
    ```
### Windows

1. Install the full Python package, including pip and tk.

2. Within the project, run the following command to install the necessary libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Portable version:

    If you want to create a portable version, download the compressed package, unzip it, and copy the 
    `Python312` folder and the 2 `bat` files to the root of the project.
    Replace the two `bat` files in the project with those contained in the compressed package.

    This way, there is no need to install Python and download all its dependencies, as the package already includes everything.

### Possible errors

  - There may be delays in receiving data from the exchange, which can cause slowdowns in the application, leading to freezing and not updating from that moment.  
    One error due to delays for some reason is the deselection of saved indicators for a specific symbol.  
    However, when the issue is more serious, it may require restarting the application completely.  
    The first time you open the application, it usually takes a little longer, but if the delay is too long, it can result in an error.

## Chart
![home](https://github.com/user-attachments/assets/fe47e12f-62da-4881-b8da-a974b8d1cc7d)