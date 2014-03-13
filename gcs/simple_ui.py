'''
    Simple UI to interact with Google Cloud Storage.
    @version: 1.0
'''

__author__ = 'mielem@gmail.com'

import os

MENU = '''
         ***** Project Operations *****
         p1 -- GET Service          -- List Buckets in a Project    
 
         ***** Bucket Operations  *****
         b1 -- GET Bucket           -- List objects in a bucket      
         b2 -- PUT Bucket           -- Create a bucket. (RW or FC scope) 
         b3 -- DELETE Bucket        -- Delete a bucket. (RW or FC scope)
         b4 -- GET Bucket CORS      -- Get a bucket CORS. (FC scope)   
         b5 -- SET Bucket CORS      -- Set a bucket CORS. (FC scope)  
         b6 -- GET Bucket Location  -- Get a bucket location. (FC scope)   
        
         ***** Object Operations  *****
         o1 -- PUT Object           -- Upload an object  
         o2 -- GET Object           -- Download an object  
         o3 -- PUT Object           -- Copy an object to another bucket 
         o4 -- PUT Object           -- Update an object's ACLs  
         o5 -- GET Object           -- Get an object ACLs  
         o6 -- HEAD Object          -- Get an object metadata
         o7 -- DELETE Object        -- Delete an object  

         ***** Support Operations  *****
         s1 -- Change scope         -- Change application scope.
         s2 -- Get app data         -- Display application data.
                                       
         Make your selection. Enter to clear or X to exit.
'''

class GCS_SimpleUI():
    '''
         Defines a simple UI that performs the following operations:
            1) Displays selection menu (simple UI).
            2) Obtains user's choice.
            3) Selects operation based on the user's choice.
    '''
    

    def __init__(self):
        '''. 
            Defines and initializes the class attributes.
        '''
        self.choice = ''
        self.menu = MENU
          
        
    def _get_user_selection(self):
        '''
            Displays the selection menu and obtains user's selection.
        '''
        if self.choice != "":
            print "\nEnter to clear and get the menu."
            raw_input()
            os.system('clear')
        
        print  self.menu
     
        self.choice = raw_input("\t >>> ")

   
    def simple_ui(self, gcs_commands):
        '''
             Displays menu and processes user's selection. Then calls the related 
             Google Cloud Storage operation.
             @param gcs_commands: The object that contains the Google Cloud Storage
             command details.
             @note: The function performs an endless loop during which it displays 
             the selection menu, obtains user's selection and executes the 
             related Google Cloud Storage request. 
             It exits the loop when the user terminates the application.
        '''
        
        while self.choice.lower() != "x":
            self._get_user_selection()
            
            print "<---------- Debug information goes here if debug is enabled ------------->"
            
            # Project Operations 
            if self.choice == "p1":
                # Execute GET request to list buckets in the project."
                gcs_commands.list_buckets()

            # Bucket Operations
            elif self.choice == "b1":
                # Execute GET request to List objects in a bucket."
                gcs_commands.list_objects()
            elif self.choice == "b2":
                # Execute PUT request to add a new bucket to the project."
                gcs_commands.create_bucket()
            elif self.choice == "b3":
                # Execute DELETE request to delete a bucket.
                gcs_commands.delete_bucket()
            
            elif self.choice == "b4":
                # Execute GET request to obtain a bucket CORS.
                gcs_commands.get_bucket_cors()
 
            elif self.choice == "b5":
                # Execute PUT request to set a bucket CORS.
                gcs_commands.set_bucket_cors()
                       
            elif self.choice == "b6":
                # Execute GET request to obtain a bucket location.
                gcs_commands.get_bucket_location()
                       
    
            # Object Operations 
            elif self.choice == "o1":
                # Execute PUT request to upload an object.
                gcs_commands.upload_object()
            
            elif self.choice == "o2":
                # Execute GET request to download an object.
                gcs_commands.download_object()

            elif self.choice == "o3":
                # Execute GET request to copy an object.
                gcs_commands.copy_object()
                
            elif self.choice == "o4":
                # Execute GET request to obtain an object ACLs.
                gcs_commands.set_object_email_acl()
            
            elif self.choice == "o5":
                # Execute GET request to obtain an object ACLs.
                gcs_commands.get_object_acls()
            
            elif self.choice == "o6":
                # Execute GET request to obtain an object metadata.
                gcs_commands.get_object_metadata()
            
            elif self.choice == "o7":
                # Execute DELETE request to delete an object.
                gcs_commands.delete_object()
  
            
            # Support Operations       
            elif self.choice == "s1":
                print "Change authentication scope."
                gcs_commands.change_auth_scope()

            elif self.choice == "s2":
                print "Display application data."
                gcs_commands.get_app_data()
            
            else:
                if self.choice != "x":
                    print "Invalid Choice"
                else:
                    print "Not Implemented"
                    
                os.system("clear")
                    
    
        