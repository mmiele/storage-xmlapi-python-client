'''
    This is the main entry point of the application which allows you to 
    interact with Google Cloud Storage (GCS) using XML API.
    @note: The example displays the response for each request. 
    The debug level is set to 1 by default. This is to display the 
    request and response header for each request. 
    This allows you to see the actual traffic on the wire as documented at: 
    https://developers.google.com/storagedocs/reference-methods.
'''
__author__ = 'mielem@gmail.com'

import logging
import os
import sys

import gflags

# Local imports.
from gcs.simple_ui import GCS_SimpleUI 
from gcs.commands import GCS_Command


# Define the application's parameters the user must enter
# at the activation time.
FLAGS = gflags.FLAGS

# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
gflags.DEFINE_enum(
    'logging_level', 'INFO', LOG_LEVELS, 'Set the level of logging detail.')


def __init__app(debug_level):
    '''
      Initializes the application.
      @param degbug_level: The level to display request/response 
      debugging information.
      @note: Instantiates the following classes:
      1) GCS_SimpleUI. It creates and displays the application simple UI.
      2) GCS_Command. It allows you to issue commands to interact with 
         the storage service.
    '''
            
    # Instantiate GCS_SimpleUI class.
    ui = GCS_SimpleUI()
    
    # Instantiate GCS_Command class. 
    gcs_commands = GCS_Command(debug_level)

    # Display menu, get user's input and execute Google Cloud 
    # Storage request based on user's selection.
    ui.simple_ui(gcs_commands)

def main(argv):
    '''
        Main entry point for the application.
        It processes the command line arguments and starts 
        the application. 
    '''
  
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        print "%s\\nUsage: %s ARGS\\n%s" % (e, argv[0], FLAGS)
        sys.exit(1)

    # Set the logging according to the command-line flag
    numeric_level = getattr(logging, FLAGS.logging_level.upper())
    if not isinstance(numeric_level, int):
        logging.error('Invalid log level: %s', FLAGS.logging_level)
        logging.basicConfig(level=numeric_level)
    
    # Set the debug level based on the user's passed argument. 
    if FLAGS.logging_level == 'DEBUG': 
        # You can assign a debug level between 1 and 4.
        # To assign this level to the authenticated (HTTP) client
        # you must recreate the client (and related stored information)
        # by reassigning the scope (selection s1).
        debug_level = 1
    else:
        debug_level = 0

    # Initialize the application.
    __init__app(debug_level)
    
   
if __name__ == '__main__':
  main(sys.argv)
  
 
