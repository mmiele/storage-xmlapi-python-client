'''
    Contains the GCS_Buckets class which handles 
    Google Cloud Storage bucket operations.
    @version: 1.0
'''

__author__ = 'mielem@gmail.com'

import config 
from command_utilities import GCS_Command_Utility
from command_utilities import GCS_Error as err


GCS_END_POINT = 'storage.googleapis.com'

BUCKET_ACLS = ('private', 'public-read', 
               'public-read-write', 'authenticated-read',
               'bucket-owner-read', 'bucket-owner-full-control')

BUCKET_LOCATIONS = {'Europe' : 'EU',
                    'USA' : 'US'}

DEFAULT_X_ORIGINS = '*'
DEFAULT_RESPONSE_HEADER = 'GCS-Demo'
DEFAULT_MAX_AGE_SECS = 1800


class GCS_Bucket(GCS_Command_Utility):
    '''
        Defines the commands to perform Google Cloud Storage bucket operations.
        It executes the commands and returns the response or an error.
        @note: All the methods in the class use the following methods inherited 
        from GCS_Command_Utility class:
        1) _api_request 
        2) _display_response
    '''
  
   
    def list_buckets(self):
        '''
            Lists the buckets contained in a project.
            @raise err: The GCS_Error exception if the API request failed..
            @note: Performs a GET request which is the default method.
            The project ID is recorded at the application first time start-up. 
        '''
    
        try:
            url = GCS_END_POINT
            response, content = self._api_request(url)
        except err:   
            raise
        
        # Display response
        self._display_response(response, content)
        
    
    def list_objects(self):
        '''
            Lists the objects contained in a bucket.
            User input:
                bucket_name: The name of the bucket that contains the objects.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a GET request. 
        '''
 
        bucket_name = raw_input("Bucket name: ")
        print 'List objects contained in the bucket "%s".' % bucket_name
       
        try:
             # Assign URL in the format: [bucket_name].storage.googleapis.com
            url = '%s.%s/' % (bucket_name, GCS_END_POINT)
            # Assign HTTP verb.
            method = 'GET'
            # Perform API call.
            response, content = self._api_request(url, method)
        except err:  
            raise
           
        self._display_response(response, content)
    
                
    def get_bucket_cors(self):
        '''
            Gets CORS of a bucket.
            User input:
                bucket_name: The name of the bucket for which to get the CORS.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a GET request. 
            This operation requires a full control scope.
        '''
 
        bucket_name = raw_input("Bucket name: ")

        print 'Get bucket "%s" CORS.' % bucket_name
       
        try:
            # Define URL in the format: [bucket_name].storage.googleapis.com.
            # Also specify the cors query string parameter.
            url = '%s.%s/?cors' % (bucket_name, GCS_END_POINT)
            # Assign HTTP verb.
            method = 'GET'
            # Perform API call.
            response, content = self._api_request(url, method)
        except err:  
            raise
           
        self._display_response(response, content)
    

    def set_bucket_cors(self):
        '''
            Sets a bucket Cross Domain Origins
            User input:
                bucket_name: The name of the bucket for which to set the CORS.
                cors_origins: The cross domain origins allowed to make requests.
                methods: The methods allowed to the cross domain origins.
                response_headers: Response headers the user agent can share across origins.
                max_age_secs: The seconds the client must wait before repeating the preflight request.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a PUT request. 
            This operation requires a full control scope.
        '''
 
        # Get user's input.
        
        # Get bucket name.
        bucket_name = raw_input("Bucket name: ")
        
        
        # Get cross origins 
        xorigins = {}
        xorigins = raw_input("Cross origins. Enter for default value %s: " 
                             % DEFAULT_X_ORIGINS)
        
        if not xorigins:
            # Assign default value.
            xorigins = DEFAULT_X_ORIGINS
        
        # Get cross origins 
        methods = {}
        methods_selection = raw_input(
                                "Cross origins methods. Separate methods with comma. Enter for default value %s: " 
                                % config.DEFAULT_METHOD)
     
        if not methods_selection:
            # Assign default value.
            methods_selection = config.DEFAULT_METHOD
        
        i = 0
        for verb in methods_selection.split(','):
            methods[i] = verb
            i = i+1

        
        # Get response headers
        response_headers = {}
        response_headers_selection = raw_input("Response headers. Enter for default value %s: " 
                                     % DEFAULT_RESPONSE_HEADER)
        
        if not response_headers:
            # Assign default value.
            response_headers_selection = DEFAULT_RESPONSE_HEADER
            
        response_headers = [word.strip() for word in response_headers_selection.split(',')]
            
        max_age_secs = raw_input("Max age in seconds. Enter for default value %s: " 
                                     % DEFAULT_MAX_AGE_SECS)
       
       
        if not max_age_secs.strip():
        # Assign default value.
            max_age_secs = DEFAULT_MAX_AGE_SECS
            
        # Get bucket location
        body = None
        body = self._get_cors_body(xorigins, methods, response_headers, max_age_secs)
        
        
        try:
            # Define URL in the format: [bucket_name].storage.googleapis.com.
            url = '%s.%s/?cors' % (bucket_name, GCS_END_POINT)
            # Assign HTTP verb.
            method = 'PUT'
            # Perform API call.
            response, content = self._api_request(url, method,  body=body)
           
        except err:
            raise
        
        self._display_response(response, content)
        
 
    def get_bucket_location(self):
        '''
            Gets a bucket location.
            User input:
                bucket_name: The name of the bucket for which to get the location.
            @raise err: The GCS_Error exception if the API request failed.
            @note: Performs a GET request.
            6
            This operation requires a full control scope.
        '''
 
        # Get user's input.
        
        # Get bucket name.
        bucket_name = raw_input("Bucket name: ")

        print 'Get bucket "%s" location.' % bucket_name
       
        try:
            # Define URL in the format: [bucket_name].storage.googleapis.com.
            # Also specify the location query string parameter.
            url = '%s.%s/?location' % (bucket_name, GCS_END_POINT)
            # Assign HTTP verb.
            method = 'GET'
            # Perform API call.
            response, content = self._api_request(url, method)
 
        except err:  
            raise
           
        self._display_response(response, content)
                

    def create_bucket(self):
        '''
            Creates a bucket and inserts it in a project. 
            User input:
                1) bucket_name: The name of the bucket to create.
                2) bucket_acl; The ACL to assign to the bucket.
                3) bucket_location: The location (US or EU) where to create the bucket 
            @raise err: The GCS_Error exception if the API request failed.
            ValueError: If the name of the bucket does not conform the specifications.
            @note: Performs a PUT request. Prompt user to enter:
            bucket name, bucket ACL and bucket location.
            Remember this operation requires full control or read/write scope.
            Otherwise, it will return 403 Forbidden operation error.
            If this is the case, assign the proper scope to the request. 
        '''
    
        print 'Enter required values ....'
        
        name_OK = False
        
        # Get bucket name.
        while name_OK == False:
            try:
                bucket_name = raw_input("Bucket name: ")
                name_OK = self._verify_bucket_name(bucket_name)
            except ValueError, e:
                print "Error: %s"  % e
        
        # Get bucket ACL
        headers = {}
        
        bucket_acl = raw_input(
                        "Bucket ACL. Enter for private. No quotes, please.\n %s: " 
                        % str(BUCKET_ACLS))
        
        if bucket_acl.strip():
            headers['x-googl-acl'] = bucket_acl  
        else:
            # Assign default value.
           headers['x-googl-acl'] = 'private'
        
        
        # Get bucket location
        body = None
        bucket_location = raw_input(
                            "Bucket Location. Enter for USA. No quotes, please. %s: " 
                            % str(BUCKET_LOCATIONS.keys()))
        
        if not bucket_location.strip():
            # Assign default location.
            bucket_location = BUCKET_LOCATIONS["USA"]
       
        # Format message body.
        body = self._get_location_xml(bucket_location)
        
        try:
            url = '%s.%s' % (bucket_name, GCS_END_POINT)
            method = 'PUT'
            response, content = self._api_request(
                                    url, method,
                                    headers=headers, body=body)
            print 'Bucket %s created.' % bucket_name
        except err:
            raise
        
        self._display_response(response, content)
      
     
    def delete_bucket(self):
        '''
            Deletes the given bucket.
            User input:
                bucket_name: The name of the bucket to delete.
            @raise error: The GCS_Error exception if the API request failed.
        '''
        
        # User input.
        
        # Get bucket name.
        bucket_name = raw_input("Bucket: ")
        
        print "Are you sure you want to delete the bucket: %s ?: " % bucket_name
        
        delete = ''
        while delete != 'yes' and delete != 'no':
            delete = raw_input("Enter [yes | no]: ").strip()
        
        if delete == 'yes':
            try:
                url = '%s.%s' % (bucket_name, GCS_END_POINT)
                method = 'DELETE'
                response, content = self._api_request(url, method)
                print "Bucket %s deleted." % bucket_name
            except err:
                raise
            self._display_response(response, content)
            
        else:
            print "Bucket %s not deleted. Bye!" % bucket_name
  