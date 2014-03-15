'''
    Contains the GCS_Command class which provides the entry point for 
    processing the user's input.
    Based on the user's selection, the related Google Cloud Storage
    operation is executed.
    @version: 1.0
'''

__author__ = 'mielem@gmail.com'

import os

# Local imports.
from gcs.authentication import GCS_Authentication
from gcs.bucket_commands import GCS_Bucket
from gcs.object_commands import GCS_Object
import config


# The file that contains the project ID.
PROJECT_FILE = os.path.join(os.path.dirname(__file__), 'project.dat')


class GCS_Command(GCS_Authentication, GCS_Bucket, GCS_Object):
    '''
        Performs critical initializations and allows the user's to set 
        the project ID and change the authorization scope.
        Inherits from the base classes which allow authentication, and 
        Google Cloud Storage operations.
        The storage commands implementation are delegated to the related
        parent classes:
            1) GCS_Authentication: Performs application OAuth2 authentication. 
            2) GCS_Buckets: Contains the methods to perform bucket operations.
            3) GCS_Objects: Contains the methods to perform object operations.
        @note: This is a key class that glues together the user's selection and the 
        Google Cloud Storage operations.
    '''
    
    def __init__(self, debug_level):
        '''
            Defines and initializes the class attributes.
            In particular:
            1) Obtains and stores the project ID.
            2) Authenticates the application 
            
        '''
        # Set default authorization scope.
        config.app_data['scope'] = config.scope_choices['RO_SCOPE']
        
        # Obtain and store the project ID.
        self.get_gcs_project_id()
        
        # Authenticate the application.
        self._create_http_auth_client(False, debug_level)
       

    def get_gcs_project_id(self):
        '''
            Obtains the Google Cloud Storage project ID from the user 
            and stores it in a local file.
            @note: If the project ID is already stored, the function 
            just retrieves it.
        '''
        project_file = None
        project_id = None
        
        try:
            # Retrieve stored project ID.
            project_file = open(PROJECT_FILE, 'r')
            project_id = project_file.read()
        except IOError:
            # Store project ID.
            project_file = open(PROJECT_FILE, 'w')
            project_id = raw_input(
                            'Enter your project id (found in the API console): ')
            project_file.write(project_id)
            project_file.close()
      
        config.app_data['project_id'] = project_id
    
    
    def change_auth_scope(self):
        '''
            Changes the current scope for the authenticated client.
            @note: This function forces the authorization cycle to repeat which
            prompts the user to reissue the authorization credentials.   
        '''
        print 'Enter required value ....'
        new_scope = raw_input("Scope: %s: " % config.scope_choices.keys())
        print new_scope
        
        if not new_scope.strip():
            # Assign default value.
            new_scope = scope_choices['RO_SCOPE']
            print "Assigned default scope: %s: " % new_scope
        else:
            # Update global application information.
            config.app_data['scope'] =  config.scope_choices[new_scope]
            
      
        # Create authenticated request to access Google Cloud Storage.
        self._create_http_auth_client(True, None)
    
     
    def get_app_data(self):
        '''
            Displays application data.
        '''
        # App_data is a dictionary of a key value pairs.
        print "<---------- Application data ------------->"
        for key, value in config.app_data.items():
            print key, ":", value
        
        
