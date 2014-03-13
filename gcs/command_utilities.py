'''
    Contains a utility class which defines auxiliary 
    methods needed to perform storage operations and 
    interact with the user.
    Also it contains an error class to handle HTTP request errors.
'''
import config
import re
import httplib2
import xml.dom.minidom as md
import xml.etree.ElementTree as xml

# Define constants.
XML_API_DEFAULT_VERSION = '2'
HTTP_ERROR_LEVEL = '300'
  
class GCS_Command_Utility(object):
    '''
        Defines the utility functions needed to process 
        Google Cloud Storage commands and interact 
        with the user.
    '''
  
    def _api_request(self, url, method=None, headers=None, body=None):
        '''
            Sends an authorized HTTP request to Google Cloud Storage 
            using XML API.
            @param url: The API URL endpoint.
            @param method: The HTTP request method (GET, POST, etc).
            @param headers: Any additional headers to send.
            @param body: The request body.
        
            @return: The response dictionary and string content.
            @raise exception: GCS_Error if the API request did not succeed.
        '''
        if not method: 
            method = config.DEFAULT_METHOD
        
        if not headers: 
            headers = {}
            headers['x-goog-project-id'] = config.app_data['project_id']
            headers['Content-Length'] = '0'
            
            # headers['x-goog-api-version'] = self._api_version

        if method == 'POST' or method == 'PUT' or body:
            if body:
                headers['Content-Length'] = '%d' % (len(body))


        try:
            auth_client = config.app_data['auth_http_client']
            
            response, content = auth_client.request(
                                    'http://' + url, method=method, 
                                    headers=headers, body=body)
            
        except httplib2.ServerNotFoundError, se:
            raise GCS_Error(NOT_FOUND, 'Server not found.')

        if response.status >= HTTP_ERROR_LEVEL:
            raise GCS_Error(response.status, response.reason)
        
        return response, content

    def _prettify_xml(self, xml_string):
        '''
            Returns a pretty-printed XML string for the xml_string.
            @param xml_string: The XML string to make pretty.
            @return: The pretty string.
        '''
        parsed = md.parseString(xml_string)
        return parsed.toprettyxml(indent="\t")
    
    def _display_response(self, response, content=None):
        '''
            Displays the response header and body.
        '''
        # Response is a dictionary of a key value pairs.
        print "<---------- Response header ------------->"
        for key, value in response.items():
            print key, ":", value
        
        if content:
            print "<---------- Response body ------------->"
            body = self._prettify_xml(content)
            print body
     
    def _verify_bucket_name(self, bucket_name):
        '''
            Check if a bucket name is correct.
            @param bucket_name: The name of the bucket to verify.
            @return: True if the bucket name is correct; otherwise, False.
        '''
        
        name_OK = False
        
        if not re.match(r'^[\w\-\.]+$', bucket_name):
            raise ValueError(
                        'Bucket names can only contain letters, numbers, -, _, or .')
        elif not re.match(r'^[a-zA-Z0-9]+.*', bucket_name):
            raise ValueError(
                        'Bucket names can only start with letters or numbers.')
        elif not re.match(r'.*[a-zA-Z0-9]+$', bucket_name):
            raise ValueError(
                        'Bucket names can only end with letters or numbers. ' + bucket_name)
        else:
            if len(bucket_name) < 3 or len(bucket_name) > 63:
                raise ValueError('Bucket names must contain 3 to 63 letters.')
            else:
                name_OK = True
        
        return name_OK
  
        
    def _xml_tostring(self, root_elem):
        '''
            Converts an xml.etree.ElementTree to string.
            @param root_elem: An xml.etree.ElementTree object.
            @return: A string representation of the XML.
        '''
        body = xml.tostring(root_elem, 'utf-8')
        body = '<?xml version="1.0" encoding="UTF-8"?>' + body
        return body

    
    def _get_location_xml(self, bucket_location):
        '''
            Create the XML document for the bucket location request.
            @param param: bucket_location: The location of the bucket (EU or US).
            @return: The string XML representation of the location.
        '''
        bucket_config_elem = xml.Element('CreateBucketConfiguration')
        location_elem = xml.SubElement(bucket_config_elem, 'LocationConstraint')
        location_elem.text = bucket_location
        return self._xml_tostring(bucket_config_elem)
    
    
    def _get_acls_email_body(self, permission, scope, email):
        '''
            Create the XML document for the ACL request.
            @param permission: The access permission to assign to the email.
            @param scope: The scope for the ACL.
            @param email: The email for which to create the ACL.
            @return: The string XML representation of the ACL body.
        '''
        acls_config_elem = xml.Element('AccessControlList')
        acls_elem = xml.SubElement(acls_config_elem, 'Entries')   
        
        acl_elem =  xml.SubElement(acls_elem, 'Entry')
        
        acl_perm = xml.SubElement(acl_elem, 'Permission')     
        acl_perm.text = permission
    
        acl_scope = xml.SubElement(acl_elem, 'Scope')     
        acl_scope.set('type', scope)
        
        acl_email = xml.SubElement(acl_scope, 'EmailAddress') 
        acl_email.text = email
        
        return self._xml_tostring(acls_config_elem)        
  
                   
    def _get_cors_body(self, origins, methods, response_headers, max_age_secs):
        '''
            Create the XML document for the CORS request.
            @param origins: List of string origins.
            @param methods: List of string methods (GET, POST, etc).
            @param response_headers: List of string response headers.
            @param max_age_secs: Maximum age in seconds.
            @return: The string XML representation of the CORS body.
        '''
    
        cors_config_elem = xml.Element('CorsConfig')
        cors_elem = xml.SubElement(cors_config_elem, 'Cors')    
    
        origins_elem = xml.SubElement(cors_elem, 'Origins')
        for origin in origins:
            origin_elem = xml.SubElement(origins_elem, 'Origin')
            origin_text = origin.strip()
            origin_elem.text = origin_text
    
        methods_elem = xml.SubElement(cors_elem, 'Methods')
        for method in methods:
            method_elem = xml.SubElement(methods_elem, 'Method')
            method_text = method.strip()
            method_elem.text = method_text

        response_headers_elem = xml.SubElement(cors_elem, 'ResponseHeaders')
        for response_header in response_headers:
            response_header_elem = xml.SubElement(response_headers_elem, 'ResponseHeader')
            response_header_text = response_header.strip()
            response_header_elem.text = response_header_text
        
        max_age_sec_elem = xml.SubElement(cors_elem, 'MaxAgeSec')
        if type(max_age_secs) is int:
            max_age_sec_elem.text = '%d' % max_age_secs
        elif type(max_age_secs) is float:
            max_age_sec_elem.text = '%f' % max_age_secs
        else:
            max_age_sec_elem.text = max_age_secs
    
        return self._xml_tostring(cors_config_elem)

      
class GCS_Error(Exception):
    '''
        Handle exception raised when API call does not return an 
        HTTP 20x status.
        Attributes:
            status: The string status of the HTTP response.
            message: A string message explaining the error.
      '''

    def __init__(self, status, message):
        '''
            Initializes GCS_Error with status and message.
            @param status: HTTP response status.
            @param message: Message explaining the error.
        '''
        self.status = status
        self.message = message

    def __str__(self):
        '''
            Displays the error as <status>: <error message>.
            @return: The string representation of the error.
        '''
        return '%s: %s' % (repr(self.status), repr(self.message))
    
  
     