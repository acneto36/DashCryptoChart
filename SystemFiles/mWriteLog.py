import datetime

numLinesLog: int = 60

def F_writeLog(pathFile: str, text: str):

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    # Open the file in read/write mode ('a+' allows reading and writing).
    with open(pathFile, 'a+') as file:

        file.seek(0)
        lines = file.readlines()

        # Add the new log entry.
        newLogEntry = f'{text} | DATE: {timestamp}\n'
        newLines = newLogEntry.splitlines(keepends = True)  # Break the text into multiple lines if there are breaks.

        # Insert the new entry in the log.
        lines.extend(newLines)

        # Remove the oldest lines to maintain the limit.
        if len(lines) > numLinesLog:
            lines = lines[-numLinesLog:]  # Keep only the last X lines.

        # Write back to the file.
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)

# ___________________________________________________________________________ #
def F_writeConsole(pathFile: str, text: str):  # Print in indicators

    with open(pathFile, 'a+') as file:

        file.seek(0)
        lines = file.readlines()

        newLogEntry = f'{text}\n'
        newLines    = newLogEntry.splitlines(keepends = True)

        lines.extend(newLines)

        if len(lines) > numLinesLog:
            lines = lines[-numLinesLog:]
        
        file.seek(0)
        file.truncate(0)
        file.writelines(lines)