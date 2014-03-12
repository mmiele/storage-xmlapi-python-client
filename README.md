storage-xmlapi-python-client
============================
<h1>Using XML API</h1>
Google Cloud Storage supports a RESTful API, with payload in XML format, to allow programmatic 
access to the service.
	
<h2>Summary</h2>
This command line application shows how to programmatically interact with Google Cloud Storage through the 
<a href="https://developers.google.com/storage/docs/xml-api-overview" target="_blank">XML API</a>. 
It uses a simple interface which allows you to perform tasks such as: list the buckets in a project, 
list objects in a bucket, create a bucket, create an object and so on. 
The intent of the application is educational and should help you to understand the API syntanx (and semantics) 
when interacting with Google Cloud Storage. 

<h3>Background</h3>
Before running the application, assure that you satisfy the following prerequisites:
<ol>
  <li>Install the required software as listed next.</li>
  <li>Update the information contained in the <i>client_secrets.json</i> file.
      Use your client id and secret available in the 
      <a href="https://code.google.com/apis/console#access" target="_blank">Google API Console</a>.</li>	
</ol>	
	 
The first time you run the application, you will be asked to authenticate it. The application uses OAuth2.0 and stores
the credentials in a local file called <i>stored_credentials.json</i>. 
Also, the user will be asked to enter the project ID which is stored in a local file called <i>project.dat</i>.
	
<h2>Usage</h2>
In a terminal window activate the program as follows:<br/> 

<pre>  
  <i>python main.py  --logging_level ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] </i> 
</pre>

You can find more details on how to build the application and run it in Eclipse (or in a Terminal window) here: 
<a href="http://www.acloudysky.com" target="_blank">acloudysky.com</a>.

