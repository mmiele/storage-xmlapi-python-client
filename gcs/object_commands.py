'''
    Contains the GCS_Objects class which handles 
    Google Cloud Storage object operations.
    @version: 1.0
'''

__author__ = 'mielem@gmail.com'

import os
import mimetypes

# Local imports
import config 
from command_utilities import GCS_Command_Utility
from command_utilities import GCS_Error as err


GCS_END_POINT = 'storage.googleapis.com'
OBJECT_PERMISSIONS = ('READ', 'WRITE', 'FULL_CONTROL')

OBJECT_ACL_SCOPES = ('UserByEmail', 'GroupByEmail')

class GCS_Object(GCS_Command_Utility):
    '''
        Defines the functions to perform Google Cloud Storage object operations.
        @note: All the functions in the class use the following methods inherited 
        from GCS_Command_Utility class:
        1) _api_request 
        2) _display_response
    '''
  
    def upload_object(self):
        '''
            Inserts an object into a bucket.
            (Uploads a file into an object). 
           `User input:
                file path: The file path in the format dir/filename.
                object path: The object path in the format gs://bucketname/objectname.
                permission: The access permission to associate with the object.
            @return: The string XML representation of the response.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a PUT request.  
        '''
   
        # User input.
       
        # Get the path of the file to upload.
        file_path = raw_input("File path (in the format dir/filename): ")
        
        # Evaluate the absolute file path.
        abs_file_path = os.path.join(os.environ['HOME'], file_path)

        # Load file content.
        file = open(abs_file_path, 'r')
        file_contents = file.read()
    
        # Get the path of the object to create.
        bucket_object = raw_input("Target object path (in the format gs://bucketname/objectname): ")
        tmpstr=bucket_object.split('/', 3)
        bucket_name = tmpstr[2]
        object_name = tmpstr[3]
  
        # Get permission associate with the object.
        permission = raw_input(
                        "Object ACL. Enter for READ. No quotes, please.\n %s: " 
                        % str(OBJECT_PERMISSIONS))
        
        if not permission.strip():
            # Assign default value.
            permission = 'private'
    
    
        # Get the MIME type and encoding.
        guess_type, guess_encoding = mimetypes.guess_type(file_path)
      
        # Assign headers.
        headers = {'Content-Type' : guess_type,
                    'Content-Encoding' : guess_encoding,
                   'x-goog-acl' : permission}
        
        # Issue the request.
        try:
            url = '%s.%s/%s' % (bucket_name, GCS_END_POINT, object_name)
            method = 'PUT'
            response, content = self._api_request(
                                    url, method,
                                    headers=headers, 
                                    body=file_contents)  
        except err:
            raise

        # Display response
        self._display_response(response, content)
     
  
    def download_object(self):
        '''
            Gets an object from a bucket.
            (Downloads an object into a file). 
           `User input:
                file path: The file path in the format dir/filename.
                object path: The object path in the format gs://bucketname/objectname.
                permission: The access permission to associate wiht the object.
            @return: The string XML representation of the response.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a GET request.  
        '''
   
        # User input.
       
        # Get the destination file path: such as tmp/downloads/.
        file_path = raw_input("Destination file path (in the format dir/filename): ")
        
        # Evaluates the absolute file path.
        abs_file_path = os.path.join(os.environ['HOME'], file_path)

      
        #  Get the path of the object to download.
        bucket_object = raw_input("Object to download path (in the format gs://bucketname/objectname): ")
        tmpstr=bucket_object.split('/', 3)
        bucket_name = tmpstr[2]
        object_name = tmpstr[3]
  

        # Issue the request.
        try:
            url = '%s.%s/%s' % (bucket_name, GCS_END_POINT, object_name)
            method = 'GET'
            response, content = self._api_request(url, method)  
        except err:
            raise

        try:
            # Download object content.
            file = open(abs_file_path, 'wb')
            file.write(content)
        except IOError:
            raise
        
        # Display response
        self._display_response(response)
    
  
    def get_object_acls(self):
        '''
            Gets an object's ACLs.
            User input:
                bucket_name: The name of the bucket that contains the object.
                object_name: The name of the object for which to obtain the ACLs.
            @return: The string XML representation of the response.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a GET request.  
        '''
        
        # User input.
        
        #  Get the path of the object for which to obtain the ACLs.
        bucket_object = raw_input("Object path (in the format gs://bucketname/objectname): ")
        tmpstr=bucket_object.split('/', 3)
        bucket_name = tmpstr[2]
        object_name = tmpstr[3]

        
        # Issue the request.
        try:
            # Define URL in the format: [bucket_name].storage.googleapis.com.[object_name]
            # Also specify the acl query string parameter.
            url = '%s.%s/%s?acl' % (bucket_name, GCS_END_POINT, object_name)
            # Assign HTTP verb.
            method = 'GET'
            # Perform API call.
            response, content = self._api_request(url, method)
        except err:   
            raise
        
        # Display response
        self._display_response(response, content)
     
        
    def set_object_email_acl(self):
        '''
            Sets an object's ACL for individual or group e-mail.
            User input:
                bucket_name: The name of the bucket that contains the object.
                object_name: The name of the object for which to set the ACL.
                scope: The ACL applicable scope.
                email: Group or individual e-mail for which to create the ACL.
                permission: The access permission for the specified e-mail.
            @return: The string XML representation of the response.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a PUT request.  
        '''
        
        # User input.
       
        #  Get the path of the object for which to obtain the ACLs.
        bucket_object = raw_input("Object path (in the format gs://bucketname/objectname): ")
        tmpstr=bucket_object.split('/', 3)
        bucket_name = tmpstr[2]
        object_name = tmpstr[3]
        
        # Get ACL scope.
        scope = raw_input(
                        "Object ACL. Enter for UserByEmail. No quotes, please.\n %s: " 
                        % str(OBJECT_ACL_SCOPES))
        if not scope.strip():
            # Assign default value.
            scope = 'UserByEmail'
        
        # Get email.    
        email = raw_input("User or group email: ")
        
        # Get access permission to assign to the email.
        permission = raw_input(
                        "Object ACL. Enter for READ. No quotes, please.\n %s: " 
                        % str(OBJECT_PERMISSIONS))
        
        if not permission.strip():
            # Assign default value.
            permission = 'READ'
        
        # Format message body.
        body = self._get_acls_email_body(permission, scope, email)

        # Issue request.
        try:
            # Define URL in the format: [bucket_name].storage.googleapis.com.[object_name]
            # Also specify the acl query string parameter.
            url = '%s.%s/%s?acl' % (bucket_name, GCS_END_POINT, object_name)
            # Assign HTTP verb.
            method = 'PUT'
            # Perform API call.
            response, content = self._api_request(url, method, body=body)
        except err:   
            raise
        
        # Display response
        self._display_response(response, content)
  
        
    def get_object_metadata(self):
        '''
            Gets a Cloud Storage object's metadata .
            User input:
                bucket_name: The name of the bucket that contains the objects.
                object_name: The name of the object for which to obtain the ACLs.
            @return: The string XML representation of the object's ACLs.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a GET request.  
        '''
        
        # User input.
       
        #  Get the path of the object for which to obtain the ACLs.
        bucket_object = raw_input("Object path (in the format gs://bucketname/objectname): ")
        tmpstr=bucket_object.split('/', 3)
        bucket_name = tmpstr[2]
        object_name = tmpstr[3]
        
        try:
            # Define URL in the format: [bucket_name].storage.googleapis.com.[object_name]
            url = '%s.%s/%s' % (bucket_name, GCS_END_POINT, object_name)
            # Assign HTTP verb.
            method = 'HEAD'
            # Perform API call.
            response, content = self._api_request(url, method)
        except err:   
            raise
        
        # Display response
        self._display_response(response, content)
        
    
    def copy_object(self):
        '''
            Copies an object.
            User input:
                bucket_name: The name of the bucket that contains the objects.
                object_name: The name of the object to copy.
                new_object_name: The name of the new object.
                permission: The access permission of the new object. 
            @return: The string XML representation of the response.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a GET request.  
        '''
        
        # User input           
        bucket_name = raw_input("Source bucket name: ")
        object_name = raw_input("Name of the object to copy: ")
        
        target_bucket_name = raw_input("Target bucket name: ")
        
        target_object_name = raw_input("Target object name. Enter for the same name: ")
        if not target_object_name.strip():
            # Assign default value.
            target_object_name = object_name
        
        permission = raw_input(
                        "Object ACL. Enter for private. No quotes, please.\n %s: " 
                        % str(OBJECT_PERMISSIONS))
        if not permission.strip():
            # Assign default value.
            permission = 'private'
            
   
        try:
            # Define URL in the format: [bucket_name].storage.googleapis.com.[object_name]
            url = '%s.%s/%s' % (bucket_name, GCS_END_POINT, object_name)
            # Assign HTTP verb.
            method = 'HEAD'
            # Perform API call.
            response, content = self._api_request(url, method)
        except err:   
            raise
        
        content_length = 0
        for key, value in response.items():
            if key == "content-length":
               content_length = value
      
        copy_source = '%s/%s' % (bucket_name, object_name)
        
        
        headers = {'x-goog-copy-source': copy_source,
                   'x-goog-acl' : permission,
                   'Content-Length' : content_length
                   }
        try:
            # Define URL in the format: [bucket_name].storage.googleapis.com.[object_name]
            url = '%s.%s/%s' % (target_bucket_name, GCS_END_POINT, object_name)
            # Assign HTTP verb.
            method = 'PUT'
            # Perform API call.
            response, content = self._api_request(url, method, headers=headers)
        except err:   
            raise
        
        # Display response
        self._display_response(response, content)
        
        print "Object %s has been copied into object %s" % (object_name, target_object_name)
        
      
        
    def delete_object(self):
        '''
            Deletes an object.
            User input:
                bucket_name: The name of the bucket that contains the objects.
                object_name: The name of the object to delete.
            @return: The string XML representation of the response.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a DELETE request.  
        '''
        
        # User input.
        
        #  Get the path of the object for which to obtain the ACLs.
        bucket_object = raw_input("Object path (in the format gs://bucketname/objectname): ")
        tmpstr=bucket_object.split('/', 3)
        bucket_name = tmpstr[2]
        object_name = tmpstr[3]
        
        print "Are you sure you want to delete the bucket: %s ?: " % object_name
        
        delete = ''
        while delete != 'yes' and delete != 'no':
            delete = raw_input("Enter [yes | no]: ").strip()
      
        if delete == 'yes':
            try:
                # Define URL in the format: [bucket_name].storage.googleapis.com.[object_name]
                url = '%s.%s/%s' % (bucket_name, GCS_END_POINT, object_name)
                # Assign HTTP verb.
                method = 'DELETE'
                # Perform API call.
                response, content = self._api_request(url, method)
                # Display response
                self._display_response(response, content)
            except err:   
                raise
        else:
            print "Object %s not deleted. Bye!" % object_name
  
        # Display response
        self._display_response(response, content)
        
    