'''
    Contains data shared by all the modules.
    @note: To access the data a module must use the 
    statement: import config.

'''
__author__ = 'mielem@gmail.com'

# Define allowed authentication scopes.
scope_choices = {
         'RW_SCOPE' : 'https://www.googleapis.com/auth/devstorage.read_write',
         'WO_SCOPE' : 'https://www.googleapis.com/auth/devstorage.write_only',
         'RO_SCOPE' : 'https://www.googleapis.com/auth/devstorage.read_only',
         'FC_SCOPE' : 'https://www.googleapis.com/auth/devstorage.full_control'
}


# Global application data.
app_data = {
                'project_id' : None,
                'scope' : None,
                'http_client' : None,
                'auth_http_client' : None
}

# Define the default HTTP verb.
DEFAULT_METHOD = 'GET'