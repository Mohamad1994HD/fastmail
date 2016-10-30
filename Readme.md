#A simple command line tool for sending email via SMTP

### Modules:

  *  **_cli.py_**  which is responsible for command line interfacing
  
  *  **_email_sender.py_** which is responsible for handling the sending request
 
 
### Tool options:
  * **Config**: Set the configurations ( used only once unless you want to change the configs )
    * **--port**: Port number (e.g. 469)

    * **--host**: Host service (e.g. smtp.gmail.com)

    * **--email**: User email

    * **--password**: User password

    * **--layer**: Use tls | ssl 
  
  * **init**: Initialize the tool (used only once after installation)
  
  * **send**: Send the email message
    * **--t/--n**: To use a predefined (t)emplate or (n)ot
        The user will be prompted to enter the template file location (full path) - its better to have admin authorization
        when open the cli window-
        
        The user will be prompted to enter key:value pairs of template keys as __JSON notation__ (easier for developers :D) in order to             substitute them accordingly
        as well as the indicator of the keys to  be detected will be required. (e.g. & or > or #) any symbol prefered to 
        mark a key.
  * **info**: Displayes the user configurations info
  
 
 
###Usage:
  
  **1. ```fastmail init```**
  
  **2. ```fastmail config --port XXX --host XXX --email XXX --password XXX --layer XXX```**
  
  **3. ```fastmail send --t\--n```**    
  then the user will be prompted to enter reciever email, subject & message body
  
  

###You can find compiled binary of the tool for windows

  <a href="https://sourceforge.net/projects/fastmail-sender/files/latest/download" rel="nofollow"><img alt="Download fastmail sender" src="https://a.fsdn.com/con/app/sf-download-button"></a>

###Screenshots

![image1](images/1.png)
![image2](images/2.png)
![image3](images/3.png)
![image4](images/4.png)
