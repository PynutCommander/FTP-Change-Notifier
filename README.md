# FTP-Change-Notifier
This is a program that watches the specified directories and inform the user if any changes has happened in these directories, changes include:
1) Adding New File/Folder.
2) Removal of an existing File/Folder.
3) Editing of an existing File/Folder. 
which would help the user keep track of these directories if he has shared them with other people without the need of logging in and checking it manually..
the program uses .wav in order to play the alert sound. the file is called workwork.wav, you can replace it with your own sound wav, i got the alert sound from: http://www.wavsource.com/sfx/sfx.htm At: http://www.wavsource.com/snds_2016-08-07_1461683041535257/sfx/buzzer3_x.wav.
I have attached the executable copy of the program aswell in the GUI MainWindow Folder.
UPDATED: multiple changes has happened, first a new feature of Mouse Over server that shows the user the information about that specific server such as: serve URL, Port used, and username. also next to each server name a small icon of On or OFF that indicates the status of the checker. whether it is connected or not to the servers, also added a new tab which allows the user to specify the port he wants to use in order to connect to his FTP server. if the tab is left BLANK it will automatically use PORT = 21. there is an issue with some servers that doesnt return in english language. the function used to get the information about the last modified date is FTP.dir(), so if the server doesnt return the dates in english (Such as Korean servers) it might cause an issue for now.
