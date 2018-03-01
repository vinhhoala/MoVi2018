"""Utilities functions
"""

def printHelp(appName):
    """Print out the message if the user does not enter correct parameter
    
    Arguments:
        appName {String} -- String name
    """
    print("Usage:")
    print('\tpython ' + appName + ' <Input_data_file>')


def writeToFile(file_path, content):
    """Append a content to a file
    
    Arguments:
        file_path {String} -- Path of output file
        content {String} -- Content to be written
    """

    output = open(file_path, 'a')
    output.write(content)
    output.close()