# sanctuary
#### Intro
I wanted a simple webapp to serve static files and is themed after an old terminal. Files in the `/content` folder may then be accessed via the URL.

While this website may feel bland to some, it is exactly what I had in mind before making it and I am personally quite happy with the outcome.

#### Security
Web security for this app was approached in the following way: 
- The webapp should not be able to write/store information on the server. (This nullifies any potential injections)
- As such, all changes to the files must be done through the terminal. (I edit things with VIM through SSH, which works great for me)
- URL sanitation is done with the Werkzeug module's `secure_filename()` function. 
The only file the app may write to is the log file. Care should be taken if parsing this file with a program.

I think I did an okay job at locking this down, but please contact me if you find any security problems with this app before I do.

Thank-you :)
