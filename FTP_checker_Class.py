import mysql.connector
from PyQt4 import QtCore, QtGui
from Crypto.Cipher import AES
import os
import ftplib
from collections import defaultdict
import time
import datetime

class FTP_checker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    def __init__(self, Parent):
        super(FTP_checker, self).__init__()
        self.listOfMonths = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9,
                             "Oct": 10, "Nov": 11, "Dec": 12}
        self.Parent = Parent
        self.checkDelay=2
        self.configured_Database = False
        self.listOfConnectedServers = []

    def setConfiguredDB(self):
        self.configured_Database = False

    def initiator(self):#initiator creates the dictionary of server and their designated directories.
        self.serverIDictionary = defaultdict(list)
        self.keyIDs = []#key id to manage the dictionary. it has list of server IDS
        self.configureCursor()#configure the cursor. this class has its own cursor as its consistently checking the db
        self.starter()#call the starter class

    def configureCursor(self):#as long as there is no DB keep checking if one is configured.
        while (self.configured_Database == False):
            time.sleep(2)
            self.firstRunChecker()

    def firstRunChecker(self):#decrypt the file and get the information of the DB and try to connect to it.
        if ((os.path.isfile("./firstrun.txt")) == True):
            fileExists = open("firstrun.txt", 'r')
            encryptedFileName = fileExists.readline()
            self.Parent.decrypt_password(self.Parent.getKey("mGDfJpfDsQ6651fsf!@$^!@$*!@#fwefgax6qNY2"),
                                  "(encrypted)" + encryptedFileName)
            fileExists.close()
            dbInformation = open(encryptedFileName, 'r')
            dbUsername = str(dbInformation.readline())
            dbPassword = str(dbInformation.readline())
            dbURLHost = str(dbInformation.readline())
            dbName = str(dbInformation.readline())
            dbInformation.close()
            dbInformation = open(encryptedFileName, "w")
            dbInformation.write("brain Freeze")
            dbInformation.close()
            db_Existence = self.set_Database_Cursor(dbUsername, dbPassword, dbURLHost, dbName)
            if (db_Existence == True):
                self.Parent.refreshcaller()
                print("Connected to DB")
            else:
                print("couldnt find db")
                return False
        else:
            print("not configured DB")
            return False

    def starter(self):#sleep for checkdelay seconds then call garbage collector that resets the variables each run and check for changes.
        while True:
            time.sleep(self.checkDelay)
            self.garbageCollector()

            if(self.databaseCursor != None and self.configured_Database ==True):
                try:#get the number of servers
                    self.databaseCursor.execute(
                        "SELECT COUNT(*) FROM server"
                    )
                    self.cnnct.commit()
                    self.fetchedNumberOfServers = self.databaseCursor.fetchall()
                except mysql.connector.Error as e:
                    print(e.msg)
                    if (self.databaseCursor == None):
                        self.configureCursor()

                if(int(self.fetchedNumberOfServers[0][0]) > 0):#if the number of servers is more than 0 then initialize else retry.
                    serverChecker = self.checkServers()
                    # print(self.fetchedNumberOfServers)
                    if((serverChecker != None) and (serverChecker > 0)):
                        self.initialize()
                    else:
                        pass
            else:
                self.initiator()

    def initialize(self):
        try:#be4 checking for changes we get the list of directories with Activated = 0 which means we have never checked them be4 and they are not in our Database. so we insert them into our DB
            self.databaseCursor.execute(
                "SELECT serverid, directoryName, Activated FROM directory WHERE Activated LIKE '0'")
            self.cnnct.commit()
            self.fetchedUnactivatedDirectories = self.databaseCursor.fetchall()
        except mysql.connector.Error as e:
            print(str(e.msg))
            return

        if ((len(self.fetchedUnactivatedDirectories)) > 0):#if we have any directories that are new. we call serverUnactivatedDictionaryFiller Function then fromFTPtoDatabase
            self.garbageCollector()
            self.serverUnactivatedIDictionaryFiller(self.fetchedUnactivatedDirectories)
            self.fromFtptoDatabase()
        else:
            self.changeChecker()

    def serverUnactivatedIDictionaryFiller(self, listOfDirectories):#gets the list of unactivated directories. insert each server id with all of its designated directories as follows
        # SERVERID: DIRECTORIE1, DIRECTORY2, DIRECTORY3
        # so if we call server id 5, we get DIR1, DIR2, DIR3. when checking.
        for counter in range(len(listOfDirectories)):
            self.serverIDictionary[self.fetchedUnactivatedDirectories[counter][0]].append(
                self.fetchedUnactivatedDirectories[counter][1])

        for counter in range(len(listOfDirectories)):
            if ((self.fetchedUnactivatedDirectories[counter][0]) not in self.keyIDs):
                self.keyIDs.append(self.fetchedUnactivatedDirectories[counter][0])

    def fromFtptoDatabase(self):#function that takes the unactivated  directories and insert them into the database.
        for counter in range(len(self.keyIDs)):
            # -------------- GET USER NAMES AND PASSWOED
            try:#get the servername, and host, username of the selected server ID
                self.databaseCursor.execute("SELECT serverName, host, userName, port FROM server WHERE id LIKE " + "'" + str(
                    self.keyIDs[counter]) + "'")
                self.cnnct.commit()
                self.serverInformation = self.databaseCursor.fetchall()
                # print(self.serverInformation)

            except mysql.connector.Error as e:
                print(str(e.msg))
                return

            try:#we set the userName and Host from the selected values from the DB.
                userName = self.serverInformation[0][2]
                hostURL = self.serverInformation[0][1]
                serverPort = self.serverInformation[0][3]
                serverName = self.serverInformation[0][0]
                try:
                    serverPort = int(serverPort)
                except ValueError:
                    QtGui.QMessageBox.warning(self, "Wrong Port Type ", "Please type in integer value for port")
                    return
            except:
                return

            try:#get the password of the server and decrypt it.
                self.databaseCursor.execute(
                    "SELECT password FROM server WHERE id LIKE " + "'" + str(self.keyIDs[counter]) + "'")
                self.cnnct.commit()
                fetchecServerPassword = self.databaseCursor.fetchall()
                userPassword = self.Parent.decrypt_server_password(fetchecServerPassword[0])
            except mysql.connector.Error as e:
                print(str(e.msg))
                return

            # ----------------- END OF GET USERNAME AND PASSWORD

            # ----------------- START OF FTP CONNECTION
            try:#connect to the FTP servert
                ftp = ftplib.FTP()
                ftp.connect(host=hostURL, port=serverPort)
                ftp.login(user=userName, passwd=userPassword)
                self.listOfConnectedServers.append(serverName)

                for dirCounter in range(len(self.serverIDictionary[self.keyIDs[counter]])):#runs for the length of the number of directories in each server
                    ftp.cwd(str(self.serverIDictionary[self.keyIDs[counter]][dirCounter]))#change the directory to that specific directory
                    listofFTPfiles = []
                    ftp.dir(listofFTPfiles.append)#append the list of files and their information inside the List of FTP files.

                    for splitterCounter in range(len(listofFTPfiles)):#this is an issue with the function Dir(). it only returns the year if the folder is older than a year. so a checker that checks if
                        #it returned Timing or year. if  returned timing it means the folder is last updated this year. if not then sacrify timing for the year.
                        splittedFiles = self.splitClearer(listofFTPfiles[splitterCounter].split(" "))
                        if (":" in splittedFiles[7]):
                            currentYear = datetime.datetime.now()
                            currentYear = currentYear.year
                            currentHour, currentMinutes = self.HourMinuteSplitter(splittedFiles[7])

                            # print(currentHour, currentMinutes)
                            ModifiedTime = str(currentYear) + "-" + str(
                                self.listOfMonths[str(splittedFiles[5])]) + "-" + str(splittedFiles[6]) + " " + str(
                                currentHour) + ":" + str(currentMinutes) + ":" + str(00)
                            # print(ModifiedTime)
                            try:
                                self.databaseCursor.execute("INSERT INTO file VALUES(%s,%s,%s)", (
                                (str(self.serverIDictionary[self.keyIDs[counter]][dirCounter])), (str(splittedFiles[8])),
                                (str(ModifiedTime))))
                                self.cnnct.commit()
                            except mysql.connector.Error as e:
                                print(str(e.msg))
                                return
                        elif(":" not in splittedFiles[7]):
                            print("n")
                            currentYear = splittedFiles[7]
                            currentHour, currentMinutes = "00", "00"
                            ModifiedTime = str(currentYear) +"-" +str(self.listOfMonths[str(splittedFiles[5])]) + "-" + str(splittedFiles[6])+" " + str(currentHour) + ":" + str(currentMinutes) + ":" +str(00)
                            print(ModifiedTime)
                            try:
                                self.databaseCursor.execute("INSERT INTO file VALUES(%s,%s,%s)", (
                                    (str(self.serverIDictionary[self.keyIDs[counter]][dirCounter])),
                                    (str(splittedFiles[8])),
                                    (str(ModifiedTime))))
                                self.cnnct.commit()
                            except mysql.connector.Error as e:
                                print(str(e.msg))
                                return

                for activatedCounter in range(len(self.serverIDictionary[self.keyIDs[counter]])):
                    try:#update the directory information, Activaed = 1 which means we have all the information in our database now.
                        self.databaseCursor.execute(
                            """
                            UPDATE directory
                            SET Activated=%s
                            WHERE directoryName LIKE %s
                            """, (1, str(self.serverIDictionary[self.keyIDs[counter]][activatedCounter])))
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        print(str(e.msg))
                        return

                # print(ftp.nlst())

                ftp.close()
            except ftplib.all_errors as ERR:
                print(str(ERR))
                return

    def set_Database_Cursor(self, userName, password, URLHost, dataBaseName):
        try:#sets the cursor of this class.
            self.cnnct = mysql.connector.connect(
                user=userName,
                password=password,
                host=URLHost,
                database=dataBaseName)
        except mysql.connector.Error as e:
            #QtGui.QMessageBox.warning(self, "DB connection Error.", str(e.msg))
            print(str(e.msg))
            return False

        self.databaseCursor = self.cnnct.cursor(buffered=True)
        self.user = userName
        self.password = password
        self.host = URLHost
        self.databaseName = dataBaseName
        # self.cnnct.close
        self.configured_Database = True
        return True

    def changeChecker(self):#this is the function that runs if we already have the file information about the directory in our database in order to compare.
        try:#get the id of the server as well as directory name. only the ones that we have in our database.
            self.databaseCursor.execute("SELECT serverid, directoryName FROM directory WHERE Activated LIKE '1'")
            self.cnnct.commit()
            self.fetchedActivatedDirectories = self.databaseCursor.fetchall()
        except mysql.connector.Error as e:
            print(str(e.msg))
            return
        self.garbageCollector()
        self.serverActivatedIDictionaryFiller(self.fetchedActivatedDirectories)#fill the information into the dictionary of ID: DIR,DIR,DIR.

        # #---------connect to server to get the new Information
        for counter in range(len(self.serverIDictionary)):#runs for each server

            try:#get the server name of that dictionary in order to connect to the FTP.
                self.databaseCursor.execute(
                    "SELECT serverName, host, userName, port FROM server WHERE id LIKE " + "'" + str(self.keyIDs[counter]) + "'")
                self.cnnct.commit()
                self.serverInformation = self.databaseCursor.fetchall()
            except mysql.connector.Error as e:
                print(str(e.msg))
                return

            try:# set the username and password of the FTP server.
                userName = self.serverInformation[0][2]
                hostURL = self.serverInformation[0][1]
                serverPort = self.serverInformation[0][3]
                serverName = self.serverInformation[0][0]
                try:
                    serverPort = int(serverPort)
                except ValueError:
                    QtGui.QMessageBox.warning(self, "Wrong Port Type ", "FTP checker serverPort not integer Value")
                    return
            except :
                return

            try:#get the password of the FTP server
                self.databaseCursor.execute(
                    "SELECT password FROM server WHERE id LIKE " + "'" + str(self.keyIDs[counter]) + "'")
                self.cnnct.commit()
                fetchecServerPassword = self.databaseCursor.fetchall()
                userPassword = self.Parent.decrypt_server_password(fetchecServerPassword[0])
            except mysql.connector.Error as e:
                print(str(e.msg))
                return
            # ----------------- END OF GET USERNAME AND PASSWORD

            # ----------------- START OF FTP CONNECTION
            try:#set the ftp host and log in with username and apssword.
                ftp = ftplib.FTP()
                ftp.connect(host=hostURL, port=serverPort)
                ftp.login(user=userName, passwd=userPassword)
                if(serverName not in self.listOfConnectedServers):
                    self.listOfConnectedServers.append(serverName)
                for serverCounter in range(len(self.serverIDictionary[self.keyIDs[counter]])):#run for number of servers
                    ftp.cwd(str(self.serverIDictionary[self.keyIDs[counter]][serverCounter]))#move to the designated directory
                    listOfFTPFiles = []
                    ftp.dir(listOfFTPFiles.append)
                    splittedFiles = []
                    for splittedFilesCounter in range(len(listOfFTPFiles)):#split the list that we get from the Dir() function
                        splittedFiles.append(self.splitClearer(listOfFTPFiles[splittedFilesCounter].split(" ")))
                    try:#get the file and modified time from the database.
                        self.databaseCursor.execute("SELECT file, ModifiedTime FROM file WHERE directoryName LIKE " +"'" + self.serverIDictionary[self.keyIDs[counter]][serverCounter] + "'")
                        self.cnnct.commit()
                        fetchedFilesNames = self.databaseCursor.fetchall()
                    except mysql.connector.Error as e:
                        print(str(e.msg))
                        return

                    for itemadder in range(len(splittedFiles)):
                        adderFound = False
                        for databaseitemchecker in range(len(fetchedFilesNames)):
                            if(str(splittedFiles[itemadder][8]) == str(fetchedFilesNames[databaseitemchecker][0])):
                                adderFound=True
                                break

                        if(adderFound == False):#if the file is not found in the database means its new file that is added.
                            self.Parent.popupAnnouncer("New File Has Been Added to " +self.serverInformation[0][0] +" At "+(str(self.serverIDictionary[self.keyIDs[counter]][serverCounter])),
                                                       (str(splittedFiles[itemadder][8])))
                            currentYear = datetime.datetime.now()
                            currentYear = currentYear.year
                            currentHour, currentMinutes = self.HourMinuteSplitter(splittedFiles[itemadder][7])
                            FTPserverDateTime = datetime.datetime(int(currentYear), int(
                                self.listOfMonths[str(splittedFiles[itemadder][5])]),
                                                                  int(splittedFiles[itemadder][6]), int(currentHour),
                                                                  int(currentMinutes), int(00))
                            try:#insert into the database the new file.
                                self.databaseCursor.execute(
                                    """
                                    INSERT INTO file
                                    VALUES(%s,%s,%s)
                                    """,((str(self.serverIDictionary[self.keyIDs[counter]][serverCounter])),(str(splittedFiles[itemadder][8])),(FTPserverDateTime))
                                )
                                self.cnnct.commit()
                            except mysql.connector.Error as e:
                                print(str(e.msg))
                                return
                            try:#insert into the log the information about the file addition.
                                self.databaseCursor.execute(
                                    """
                                    INSERT INTO log
                                    VALUES(%s,%s,%s,%s)
                                    """,
                                    (self.keyIDs[counter],
                                     str(self.serverIDictionary[self.keyIDs[counter]][serverCounter]),
                                     ("New File Has Been Added: " +"'"+ str(splittedFiles[itemadder][8]))+"'",
                                     FTPserverDateTime))
                                self.cnnct.commit()
                            except mysql.connector.Error as e:
                                print(str(e.msg))
                                return



                    filefound = False
                    for itemsearcher in range(len(fetchedFilesNames)):#check if a file has been removed
                        for searchedlist in range(len(listOfFTPFiles)):
                            if(fetchedFilesNames[itemsearcher][0] == splittedFiles[searchedlist][8]):
                                filefound = True
                                # print(splittedFiles)
                                if (":" in splittedFiles[searchedlist][7]):
                                    currentYear = datetime.datetime.now()
                                    currentYear = currentYear.year
                                    currentHour, currentMinutes = self.HourMinuteSplitter(splittedFiles[searchedlist][7])
                                    FTPserverDateTime = datetime.datetime(int(currentYear), int(self.listOfMonths[str(splittedFiles[searchedlist][5])]),
                                                                          int(splittedFiles[searchedlist][6]), int(currentHour),int(currentMinutes), int(00))
                                    if(fetchedFilesNames[itemsearcher][1] < FTPserverDateTime):
                                        self.Parent.popupAnnouncer("New Iteration Of an Item at "+  self.serverInformation[0][0] +" At "+str(self.serverIDictionary[self.keyIDs[counter]][serverCounter]),
                                                                   fetchedFilesNames[itemsearcher][0])
                                        try:
                                            self.databaseCursor.execute(
                                                """
                                                INSERT INTO log
                                                VALUES(%s,%s,%s,%s)
                                                """,
                                                (self.keyIDs[counter],str(self.serverIDictionary[self.keyIDs[counter]][serverCounter]),("New Iteration Of " + str(fetchedFilesNames[itemsearcher][0])) ,
                                                 FTPserverDateTime))
                                            self.cnnct.commit()
                                        except mysql.connector.Error as e:
                                            print(str(e.msg))
                                            return
                                        try:
                                            self.databaseCursor.execute(
                                                """
                                                UPDATE file
                                                SET ModifiedTime=%s
                                                WHERE file LIKE %s
                                                """,
                                                (FTPserverDateTime, str(fetchedFilesNames[itemsearcher][0])))
                                            self.cnnct.commit()
                                        except mysql.connector.Error as e:
                                            print(str(e.msg))
                                            return
                                elif (":" not in splittedFiles[searchedlist][7]):
                                    pass
                        if(filefound == False):
                            self.Parent.popupAnnouncer("File Has Been Removed from "+  self.serverInformation[0][0] +" At "+str(self.serverIDictionary[self.keyIDs[counter]][serverCounter]), fetchedFilesNames[itemsearcher][0])
                            try:
                                self.databaseCursor.execute(
                                    """
                                    INSERT INTO log
                                    VALUES(%s,%s,%s,%s)
                                    """,
                                    (self.keyIDs[counter],
                                     str(self.serverIDictionary[self.keyIDs[counter]][serverCounter]),
                                     ("File Has Been Removed: " +"'"+ str(fetchedFilesNames[itemsearcher][0]))+"'",
                                     FTPserverDateTime))
                                self.cnnct.commit()
                            except mysql.connector.Error as e:
                                print(str(e.msg))
                                return
                            try:
                                self.databaseCursor.execute(
                                    "DELETE FROM file WHERE file = " + "'" + (
                                    str(fetchedFilesNames[itemsearcher][0])) + "'")
                                self.cnnct.commit()
                            except mysql.connector.Error as e:
                                print(str(e.msg))
                                return
                        filefound=False


                ftp.close()
            except ftplib.all_errors as ERR:
                print(str(ERR))

    def serverActivatedIDictionaryFiller(self, listOfDirectories):
        for counter in range(len(listOfDirectories)):
            self.serverIDictionary[self.fetchedActivatedDirectories[counter][0]].append(
                self.fetchedActivatedDirectories[counter][1])

        for counter in range(len(listOfDirectories)):
            if ((self.fetchedActivatedDirectories[counter][0]) not in self.keyIDs):
                self.keyIDs.append(self.fetchedActivatedDirectories[counter][0])

    def garbageCollector(self):
        del self.serverIDictionary
        self.serverIDictionary = defaultdict(list)
        del self.keyIDs
        self.keyIDs = []
        del self.listOfConnectedServers
        self.listOfConnectedServers = []


    def checkServers(self):
        try:
            query = "SELECT COUNT(*) FROM server"
            self.databaseCursor.execute(query)
            self.cnnct.commit()
            fetched_Size = self.databaseCursor.fetchall()
            numberOfServers = int(fetched_Size[0][0])
        except mysql.connector.Error as e:
            print(str(e.msg))
            return None
        return numberOfServers

            # -----------------END OF FTP CONNECTION
            # print(userName, hostURL, userPassword)

    def HourMinuteSplitter(self, currentHourMinute):
        currentHour = str(currentHourMinute[0]) + str(currentHourMinute[1])
        currentSecond = str(currentHourMinute[3]) + str(currentHourMinute[4])
        return currentHour, currentSecond

    def setCheckDelay(self, delayvalue):
        self.checkDelay = delayvalue
        # print(self.checkDelay)

    def splitClearer(self, listOfFiles):
        listcounter = 0
        while listcounter in range(len(listOfFiles)):
            if(listOfFiles[listcounter] == ""):
                del listOfFiles[listcounter]
                listcounter-=1
            listcounter+=1
        return listOfFiles

    def getCheckDelay(self):
        return self.checkDelay

    def getListOfConnectedServers(self):
        return self.listOfConnectedServers