# sanctuary
#### Intro
I wanted a simple website which is themed after an old terminal, to serve static files. Content goes in a folder called /content which can then be accessed via the URL.

While this website may feel bland to some, it is exactly what I had in mind before making it so I actually feel quite accomplished with it.

#### Security
Security was approached in the following way: 
- The webapp itself has no write access to anything on the site. 
- The only data a client can provide is the URL, HTTP headers, and I guess their IP. All this is strictly formatted and printed to screen. This output is redirected to a log file using bash redirection. 

This way, I can have my site call Bash or Python scripts without fear that someone will take control of them.
My URL sanitation is done with the Werkzeug module's `secure_filename()` function. 

I'm interested in security, so please contact me if you find any problems with this app before I do.

Thank-you :)
