import ftplib
import time
from multiprocessing import Process
import winsound
from PyQt4 import QtCore, QtGui
import mysql.connector
from mysql.connector import errorcode
import sys
import ftplib
import time

from multiprocessing import Process
import winsound
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from datetime import datetime
import base64
import os
import sys
import socket
import warnings
import datetime

from socket import _GLOBAL_DEFAULT_TIMEOUT
# INSERT INTO `files` (`directoryName`, `files`, `ModifiedTime`) VALUES ('/downloads/', 'dada', '2016-08-11 00:00:00');

def clear_Meta(Files_In_Dir):
    counter = 0
    while counter in range(len(Files_In_Dir)):
        if (".meta" in (Files_In_Dir[counter])):
            del Files_In_Dir[counter]
            counter -= 1
        counter += 1
    return Files_In_Dir





def Main():
    now = datetime.datetime.now()
    print(int(now.year)%100)

    usr = "knox"
    pss= "ARO0Ry1F8faooR8B"
    hst = "red.seedhost.eu"
    rd = "/downloads/"
    nana = "seed03.my-seedbox.com"
    try:
        UserName, UserPassword, Root_Directiory = "201_asgard", "Nu66et$","/Media/"
        UserName = "demo-user"
        UserPassword ="demo-user"
        Root_Directiory = rd
        ftp = ftplib.FTP("demo.wftpserver.com")#Give it the website
        ftp.login(user=UserName, passwd=UserPassword)
        # ftp.cwd("/Media/xml/")
        ftp.dir()
        print(ftp.pwd())
        # Files_in_Dir = ftp.nlst()
        # Files_in_Dir = clear_Meta(Files_in_Dir)
        # #print(Files_in_Dir)
        # # a= []
        # # ftp.dir(a.append)
        # # print(a[0].split("\t"))
        # b =[]
        # ftp.cwd("/downloads/")
        # ftp.transfercmd("SITE watch")



        # print(ftp.sendcmd("MLSD watch"))

       # print(ftp.nlst())
        # b = open("sasa.txt", "w")
        # b.write(a)
        # b.close()
        # c = open("sasa.txt", "r")
        # x = c.read()
        # print(x)
        # print(ftp.rmd("/Media/xml/mods"))
        # ftp.sendcmd("MDMT mods")
        # for counter in range(len(Files_in_Dir)):
        #     print(ftp.sendcmd("MDMT " + str(Files_in_Dir[counter])))

        # print(len(Files_in_Dir))

        ftp.close()
    # except ftplib.error_perm:
    #     print("error Permission, user name is : ", UserName, " Password is: ", UserPassword)
    # except ftplib.error_temp:
    #     print("Temporary error, Response codes in range 400-499")
    # except ftplib.error_reply:
    #     print("unexpected reply is recieved from server")
    except ftplib.error_proto:
        print("Reply recieved from server doesnot fit the response specification of the file transpere protocol")

if __name__ == '__main__':
    Main()