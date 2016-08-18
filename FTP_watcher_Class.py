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
        self.checkDelay = 2 # default checking delay is 2 seconds
        self.configuredDatabase = False
        self.listofConnectedServers = []
        self.serverDirectoryDictionary = defaultdict(list)
        self.keyIDs = []
        self.cnnct, self.databaseCursor, self.user, self.password, self.host, self.databaseName = False, False, False, False, False, False
        self.cnnct = None
        self.databaseCursor = None
        self.reportFileNames = ["DatabaseReports.txt", "ServerReports.txt", "DirectoryReports.txt", "FTPReports.txt", "IndexReports.txt"]

    def checkServerExistence(self, serverName):
        if serverName in self.listofConnectedServers:
            return True
        else:
            return False
    def getDatabaseStatus(self):
        return self.configuredDatabase
    def initiator(self):
        while (self.configuredDatabase == False):
            time.sleep(2)
            print("Trying to Connect to Database")
            self.checkFirstRunFile()

        self.reportToFile(self.reportFileNames[0], "Successfully Connected to " + self.databaseName + "\n")
        self.FTP_Checker()


    def checkFirstRunFile(self):
        if (os.path.isfile("./firstrun.txt") == True):
            fileExists = open("firstrun.txt", "r")
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

            try:
                self.cnnct = mysql.connector.connect(
                    user  = dbUsername,
                    password = dbPassword,
                    host = dbURLHost,
                    database = dbName
                )
            except mysql.connector.Error as e:
                reportMessage = "Couldnt Connect to database with Name " + str(dbUsername) + "\n" + str(e) + "\n"
                self.reportToFile(self.reportFileNames[0], reportMessage)
                self.configuredDatabase = False
                return

            self.databaseCursor = self.cnnct.cursor(buffered= True)
            self.user = dbUsername
            self.password = dbPassword
            self.host = dbURLHost
            self.databaseName = dbName
            self.configuredDatabase = True
        else:
            self.reportToFile(self.reportFileNames[0], "No Database Found\n")


    def FTP_Checker(self):
        try:
            while (self.configuredDatabase == True):
                time.sleep(self.checkDelay)
                #INsert Garbage Collector
                self.garbageCollector()
                #Check how many Servers are there.
                try:
                    self.databaseCursor.execute(
                        "SELECT COUNT(*) FROM server"
                    )
                    self.cnnct.commit()
                    self.fetchedNumberOfServers = self.databaseCursor.fetchall()
                    # print(self.fetchedNumberOfServers)
                except mysql.connector.Error as e:
                    reportMessage = "Error Getting Number of Servers : " + str(e.msg)
                    self.reportToFile(self.reportFileNames[1], reportMessage)
                    self.resetAll()

                if(self.fetchedNumberOfServers[0][0] > 0):
                    self.reportToFile(self.reportFileNames[1], "Found " + str(self.fetchedNumberOfServers[0][0]) + " Servers, Proceeding...\n")
                    # print(self.fetchedNumberOfServers[0][0])

                    #Getting all Unactivated Directories.
                    try:
                        self.databaseCursor.execute(
                            "SELECT serverid, directoryName, Activated FROM directory WHERE Activated LIKE '0'"
                        )
                        self.cnnct.commit()
                        self.fetchedUnactivatedDirectories = self.databaseCursor.fetchall()
                    except mysql.connector.Error as e:
                        reportMessage = "Error getting Unactivated Directories from Database : \n" + str(e) + "\n"
                        self.reportToFile(self.reportFileNames[2], reportMessage)
                        self.resetAll()

                    #Getting all activated Directories
                    try:
                        self.databaseCursor.execute(
                            "SELECT serverid, directoryName, Activated FROM directory WHERE Activated LIKE '1'"
                        )
                        self.cnnct.commit()
                        self.fetchedActivatedDirectories = self.databaseCursor.fetchall()
                    except mysql.connector.Error as e:
                        reportMessage = "Error getting Activated Directories from Database : \n" + str(e) + "\n"
                        self.reportToFile(self.reportFileNames[2], reportMessage)
                        self.resetAll()
                    try:
                        self.databaseCursor.execute(
                            "SELECT serverName from server"
                        )
                        self.cnnct.commit()
                        self.fetchedServerNames = self.databaseCursor.fetchall()
                        self.listofConnectedServers=[]
                        for counter in range(len(self.fetchedServerNames)):
                            self.listofConnectedServers.append(self.fetchedServerNames[counter][0])
                    except mysql.connector.Error as e:
                        reportMessage = "Error getting server Names from Database : \n" + str(e) + "\n"
                        self.reportToFile(self.reportFileNames[1], reportMessage)
                        self.resetAll()

                    #Start Filling the Dictionary
                    # print(len(self.fetchedUnactivatedDirectories))
                    if(len(self.fetchedUnactivatedDirectories) > 0):
                        self.directoryFiller(self.fetchedUnactivatedDirectories)
                        self.UnactivatedToActivated()

                    self.garbageCollector()

                    if(len(self.fetchedActivatedDirectories) > 0):
                        self.directoryFiller(self.fetchedActivatedDirectories)
                        self.checkActivated()

                    # print(self.listofConnectedServers)

                    self.garbageCollector()


                elif (self.fetchedNumberOfServers[0][0] == 0):
                    self.reportToFile(self.reportFileNames[1], "There are no Servers in the database...")
        except IndexError:
            reportMessage = "Index Error 2"
            self.reportToFile(self.reportFileNames[4], reportMessage)
            self.resetAll()



    def checkActivated(self):
        try:
            for counter in range(len(self.serverDirectoryDictionary)):
                try:
                    self.databaseCursor.execute(
                        "SELECT serverName, host, userName, port FROM server WHERE id LIKE " + "'" + str(self.keyIDs[counter]) + "'"
                    )
                    self.cnnct.commit()
                    self.serverInformation = self.databaseCursor.fetchall()
                except mysql.connector.Error as e:
                    reportMessage = "Error getting Activated Servers \n" + str(e.msg) + "\n"
                    self.reportToFile(self.reportFileNames[0], reportMessage)
                    self.resetAll()

                try:
                    serverName = self.serverInformation[0][0]
                    hostURL = self.serverInformation[0][1]
                    userName = self.serverInformation[0][2]
                    serverPort = self.serverInformation[0][3]
                except ValueError:
                    reportMessage = "Faield to assign fetched information from Activated servers :\n" + str(e.msg) + "\n"
                    self.reportToFile(self.reportFileNames[1], reportMessage)
                    self.resetAll()

                try:
                    self.databaseCursor.execute(
                        "SELECT password FROM server WHERE  id LIKE " + "'" + str(self.keyIDs[counter]) + "'"
                    )
                    self.cnnct.commit()
                    fetchedServerPassword = self.databaseCursor.fetchall()
                    userPassword = self.Parent.decrypt_server_password(fetchedServerPassword[0])
                except mysql.connector.Error as e:
                    reportMessage = "Failed to fetch Password from Activated server from DB : \n" + str(e) + "\n"
                    self.reportToFile(self.reportFileNames[0], reportMessage)
                    self.resetAll()

                try:
                    ftp = ftplib.FTP()
                    ftp.connect(host = hostURL, port = serverPort)
                    ftp.login(user = userName, passwd= userPassword)

                    for serverCounter in range(len(self.serverDirectoryDictionary[self.keyIDs[counter]])):
                        try:  # Change to Currect Working Directory
                            ftp.cwd(str(self.serverDirectoryDictionary[self.keyIDs[counter]][serverCounter]))
                            listofFTPfiles = []
                            ftp.dir(listofFTPfiles.append)
                            splittedFiles = []
                        except ftplib.all_errors as directoryError:
                            reportMessage = "Failed to CWD inside Activated FTP server \n" + str(directoryError) + "\n"
                            self.reportToFile(self.reportFileNames[3], reportMessage)
                            self.resetAll()

                        for splittedCounter in range(len(listofFTPfiles)):
                            splittedFiles.append(self.splitClearer(listofFTPfiles[splittedCounter].split(" ")))

                        try:
                            self.databaseCursor.execute("SELECT file, ModifiedTime FROM file WHERE directoryName LIKE " +"'" + self.serverDirectoryDictionary[self.keyIDs[counter]][serverCounter] + "'")
                            self.cnnct.commit()
                            fetchedFileNames = self.databaseCursor.fetchall()
                        except mysql.connector.Error as e:
                            reportMessage = "Failed to fetch files and modified Time from Activated server File table : \n" + str(e.msg) + "\n"
                            self.reportToFile(self.reportFileNames[0], reportMessage)
                            self.resetAll()

                        self.checkIteration(fetchedFileNames, splittedFiles, serverCounter, counter)
                        self.CheckExistenceDbToServer(fetchedFileNames, splittedFiles, serverCounter, counter)
                        self.CheckExistenceServerToDb(fetchedFileNames, splittedFiles, serverCounter, counter)

                except ftplib.all_errors as ftpErr:
                    reportMessage = "Failed to Connect to FTP server : \n" + str(ftpErr) + "\n"
                    self.reportToFile(self.reportFileNames[3], reportMessage)
                    self.resetAll()
        except IndexError:
            reportMessage = "Index Error 1"
            self.reportToFile(self.reportFileNames[4], reportMessage)
            self.resetAll()


    def CheckExistenceServerToDb(self, listOne, listTwo, serverCounter, maincounter):
        try:
            for counter in range(len(listTwo)):
                found = False
                try:
                    for counterTwo in range(len(listOne)):
                        if(listTwo[counter][8] == listOne[counterTwo][0]):
                            found = True
                            break
                except IndexError:
                    self.resetAll()

                if(found == False):

                    self.Parent.popupAnnouncer("File Has Been Added To " + self.serverInformation[0][0] + " At " + str(
                        self.serverDirectoryDictionary[self.keyIDs[maincounter]][serverCounter]), listTwo[counter][8])

                    try:
                        currentYear = datetime.datetime.now().year
                        currentMinutes = datetime.datetime.now().minute
                        currentHours = datetime.datetime.now().hour
                        currentSeconds = datetime.datetime.now().second
                        FTPserverDateTime = datetime.datetime(int(currentYear), int(
                            self.listOfMonths[str(listTwo[counterTwo][5])]),
                                                              int(listTwo[counterTwo][6]), int(currentHours),
                                                              int(currentMinutes), currentSeconds)
                        self.databaseCursor.execute("INSERT INTO file VALUES (%s,%s,%s)", ((str(self.serverDirectoryDictionary[self.keyIDs[maincounter]][serverCounter])),
                                                                                           (str(listTwo[counter][8])),(FTPserverDateTime)))
                    except mysql.connector.Error as e:
                        reportMessage = ("Failed to Add Activated Directory To File \n" + str(e.msg) + "\n")
                        self.reportToFile(self.reportFileNames[0], reportMessage)
                        self.resetAll()
                    try:  # insert into the log the information about the file addition.
                        self.databaseCursor.execute(
                            """
                            INSERT INTO log
                            VALUES(%s,%s,%s,%s)
                            """,
                            (self.keyIDs[maincounter],
                             str(self.serverDirectoryDictionary[self.keyIDs[maincounter]][serverCounter]),
                             ("New File Has Been Added: " + "'" + str(listTwo[counter][8])) + "'",
                             FTPserverDateTime))
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        reportMessage = ("Failed to Add Activated Directory To Log \n" + str(e.msg) + "\n")
                        self.reportToFile(self.reportFileNames[0], reportMessage)
                        self.resetAll()
        except IndexError:
            reportMessage = "Index Error 3"
            self.reportToFile(self.reportFileNames[4], reportMessage)
            self.resetAll()




    def CheckExistenceDbToServer(self, listOne, listTwo, serverCounter, maincounter):
        try:
            for counter in range(len(listOne)):
                found = False
                for counterTwo in range(len(listTwo)):
                    if(listOne[counter][0] == listTwo[counterTwo][8]):
                        found = True
                        break
                if(found == False):
                    try:
                        self.Parent.popupAnnouncer("File Has Been Removed from " + self.serverInformation[0][0] + " At " + str(
                            self.serverDirectoryDictionary[self.keyIDs[maincounter]][serverCounter]), listOne[counter][0])
                    except IndexError:
                        self.resetAll()
                    try:
                        currentYear = datetime.datetime.now().year
                        currentMinutes = datetime.datetime.now().minute
                        currentHours = datetime.datetime.now().hour
                        currentSeconds = datetime.datetime.now().second
                        FTPserverDateTime = datetime.datetime(int(currentYear), int(
                            self.listOfMonths[str(listTwo[counterTwo][5])]),
                                                              int(listTwo[counterTwo][6]), int(currentHours),
                                                              int(currentMinutes), currentSeconds)
                        self.databaseCursor.execute(
                            """
                            INSERT INTO log
                            VALUES(%s,%s,%s,%s)
                            """,
                            (self.keyIDs[maincounter],
                             str(self.serverDirectoryDictionary[self.keyIDs[maincounter]][serverCounter]),
                             ("File Has Been Removed: " + "'" + str(listOne[counter][0])) + "'",
                             FTPserverDateTime))
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        reportMessage = ("Failed to insert Activated item Deleted into LOG \n" + str(e.msg) + "\n")
                        self.reportToFile(self.reportFileNames[0], reportMessage)
                        self.resetAll()
                    try:
                        self.databaseCursor.execute(
                            "DELETE FROM file WHERE file = " + "'" + (
                                str(listOne[counter][0])) + "'")
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        reportMessage = ("Failed to Delete Activated Directory From File \n" + str(e.msg) + "\n")
                        self.reportToFile(self.reportFileNames[0], reportMessage)
                        self.resetAll()
        except IndexError:
            reportMessage = "Index Error 4"
            self.reportToFile(self.reportFileNames[4], reportMessage)
            self.resetAll()

    def checkIteration(self, listOne, listTwo, serverCounter, maincounter):
        try:
            for counter in range(len(listOne)):
                for counterTwo in range(len(listTwo)):
                    if(listOne[counter][0] == listTwo [counterTwo][8]):
                        itemFound = True
                        if(":" in listTwo[counterTwo][7]):
                            currentYear = datetime.datetime.now().year
                            currentHour, currentMinutes = self.HourMinuteSplitter(listTwo[counterTwo][7])
                            FTPserverDateTime = datetime.datetime(int(currentYear), int(
                                self.listOfMonths[str(listTwo[counterTwo][5])]),
                                                                  int(listTwo[counterTwo][6]), int(currentHour),
                                                                  int(currentMinutes), int(00))
                            if(listOne[counter][1] < FTPserverDateTime):
                                try:
                                    self.Parent.popupAnnouncer("New Iteration Of an Item at "+  self.serverInformation[0][0] +" At "+str(self.serverDirectoryDictionary[self.keyIDs[maincounter]][serverCounter]),
                                                               listOne[counter][0])
                                except IndexError:
                                    self.resetAll()
                                try:
                                    self.databaseCursor.execute(
                                        """
                                        INSERT INTO log
                                        VALUES(%s,%s,%s,%s)
                                        """,
                                        (self.keyIDs[maincounter],
                                         str(self.serverDirectoryDictionary[self.keyIDs[maincounter]][serverCounter]),
                                         ("New Iteration Of " + str(listOne[counter][0])),
                                         FTPserverDateTime))
                                    self.cnnct.commit()
                                except mysql.connector.Error as e:
                                    reportMessage = ("Failed to insert Activated new Interation into LOG \n" + str(e.msg) + "\n")
                                    self.reportToFile(self.reportFileNames[0], reportMessage)
                                    self.resetAll()

                                try:
                                    self.databaseCursor.execute(
                                        """
                                        UPDATE file
                                        SET ModifiedTime=%s
                                        WHERE file LIKE %s
                                        """,
                                        (FTPserverDateTime, str(listOne[counter][0])))
                                    self.cnnct.commit()
                                except mysql.connector.Error as e:
                                    reportMessage = ("Failed to Update Activated = 1new Interation into LOG \n" + str(e.msg) + "\n")
                                    self.reportToFile(self.reportFileNames[0], reportMessage)
                                    self.resetAll()
                            elif(":" not in listTwo[counterTwo][7]):
                                pass
        except IndexError:
            reportMessage = "Index Error 5"
            self.reportToFile(self.reportFileNames[4], reportMessage)
            self.resetAll()



    def UnactivatedToActivated(self):
        try:
            for counter in range(len(self.keyIDs)):
                try:#fetch all server information EXEPT PASSWORD
                    self.databaseCursor.execute(
                        "SELECT serverName, host, userName, port FROM server WHERE id LIKE " + "'" + str(self.keyIDs[counter]) + "'"
                    )
                    self.cnnct.commit()
                    self.serverInformation = self.databaseCursor.fetchall()
                except mysql.connector.Error as e:
                    reportMessage = "Failed to fetch Unactivated server Information from DB : \n" + str(e.msg) + "\n"
                    self.reportToFile(self.reportFileNames[1], reportMessage)
                    self.resetAll()

                try:#assign the information to variables
                    serverName = self.serverInformation[0][0]
                    hostURL = self.serverInformation[0][1]
                    userName = self.serverInformation[0][2]
                    serverPort = self.serverInformation[0][3]
                except ValueError:
                    reportMessage = "Failed to assign Fetched Information From unactivated servers : \n" + str(e.msg) +"\n"
                    self.reportToFile(self.reportFileNames[1], reportMessage)
                    self.resetAll()

                try:#fetch the password from the db
                    self.databaseCursor.execute(
                        "SELECT password FROM server WHERE id LIKE "+ "'" + str(self.keyIDs[counter]) + "'"
                    )
                    self.cnnct.commit()
                    fetchedServerPassword = self.databaseCursor.fetchall()
                    userPassword = self.Parent.decrypt_server_password(fetchedServerPassword[0])
                except mysql.connector.Error as e:
                    reportMessage = "Failed to fetch Password from Unactivated server from DB : \n" + str(e) + "\n"
                    self.reportToFile(self.reportFileNames[1], reportMessage)
                    self.resetAll()

                try:#Connect to FTP to get all the data
                    ftp = ftplib.FTP()
                    ftp.connect(host = hostURL, port = serverPort)
                    ftp.login(user = userName, passwd= userPassword)

                    for directoryCounter in range(len(self.serverDirectoryDictionary[self.keyIDs[counter]])):
                        try:#Change to Currect Working Directory
                            ftp.cwd(str(self.serverDirectoryDictionary[self.keyIDs[counter]][directoryCounter]))
                            listofFTPfiles = []
                            ftp.dir(listofFTPfiles.append)
                        except ftplib.all_errors as directoryError:
                            reportMessage = "Failed to CWD inside Unactivated FTP server \n" + str(directoryError) + "\n"
                            self.reportToFile(self.reportFileNames[3], reportMessage)
                            self.resetAll()

                        for splitFileCounter in range(len(listofFTPfiles)):
                            splittedFiles = self.splitClearer(listofFTPfiles[splitFileCounter].split(" "))
                            # print(splittedFiles)

                            if(":" in splittedFiles[7]):
                                currentYear = datetime.datetime.now().year
                                currentHour, currentMinute = self.HourMinuteSplitter(splittedFiles[7])
                                ModifiedTime = str(currentYear) + "-" + str(
                                    self.listOfMonths[str(splittedFiles[5])]) + "-" + str(splittedFiles[6]) + " " + str(
                                    currentHour) + ":" + str(currentMinute) + ":" + str(00)
                                try:
                                    self.databaseCursor.execute("INSERT INTO file VALUES(%s,%s,%s)", (
                                        (str(self.serverDirectoryDictionary[self.keyIDs[counter]][directoryCounter])),
                                        (str(splittedFiles[8])),
                                        (str(ModifiedTime))))
                                    self.cnnct.commit()
                                except mysql.connector.Error as e:
                                    reportMessage = "Failed to Insert Values into Unactivated File Table \n" + str(e.msg) + "\n"
                                    self.reportToFile(self.reportFileNames[0], reportMessage)
                                    self.resetAll()
                            elif(":" not in splittedFiles[7]):
                                currentYear = splittedFiles[7]
                                currentHour, currentMinute = "00", "00"
                                ModifiedTime = str(currentYear) + "-" + str(
                                    self.listOfMonths[str(splittedFiles[5])]) + "-" + str(splittedFiles[6]) + " " + str(
                                    currentHour) + ":" + str(currentMinute) + ":" + str(00)
                                try:
                                    self.databaseCursor.execute("INSERT INTO file VALUES(%s,%s,%s)", (
                                        (str(self.serverDirectoryDictionary[self.keyIDs[counter]][directoryCounter])),
                                        (str(splittedFiles[8])),
                                        (str(ModifiedTime))))
                                    self.cnnct.commit()
                                except mysql.connector.Error as e:
                                    reportMessage = "Failed to Insert Values into Unactivated File Table \n" + str(
                                        e.msg) + "\n"
                                    self.reportToFile(self.reportFileNames[0], reportMessage)
                                    self.resetAll()

                    for activateCounter in range(len(self.serverDirectoryDictionary[self.keyIDs[counter]])):
                        try:
                            self.databaseCursor.execute(
                                "UPDATE directory SET Activated=%s WHERE directoryName LIKE %s", (1, str(self.serverDirectoryDictionary[self.keyIDs[counter]][activateCounter]))
                            )
                        except mysql.connector.Error as e:
                            reportMessage = "Failed to Update from Unactivated to Activated :\n" + str(e.msg) + "\n"
                            self.reportToFile(self.reportFileNames[0], reportMessage)
                            self.resetAll()
                    ftp.close()

                except ftplib.all_errors as ftpErr:
                    reportMessage = "Failed to Connect to FTP server : \n" + str(ftpErr) + "\n"
                    self.reportToFile(self.reportFileNames[3], reportMessage)
                    self.resetAll()
        except IndexError:
            reportMessage = "Index Error 6"
            self.reportToFile(self.reportFileNames[4], reportMessage)
            self.resetAll()


    def HourMinuteSplitter(self, currentHourMinute):
        try:
            currentHour = str(currentHourMinute[0]) + str(currentHourMinute[1])
            currentSecond = str(currentHourMinute[3]) + str(currentHourMinute[4])
            return currentHour, currentSecond
        except IndexError:
            self.resetAll()

    def splitClearer(self, listOfFiles):
        try:
            listcounter = 0
            while listcounter in range(len(listOfFiles)):
                if(listOfFiles[listcounter] == ""):
                    del listOfFiles[listcounter]
                    listcounter-=1
                listcounter+=1
            return listOfFiles
        except IndexError:
            self.resetAll()

    def directoryFiller(self, listofDirectories):
        try:
            for counter in range(len(listofDirectories)):
                self.serverDirectoryDictionary[listofDirectories[counter][0]].append(
                    listofDirectories[counter][1])

            for counter in range(len(listofDirectories)):
                if ((listofDirectories[counter][0]) not in self.keyIDs):
                    self.keyIDs.append(listofDirectories[counter][0])
        except IndexError:
            self.resetAll()




    def reportToFile(self, fileName, Message):
        reportFile = open(fileName, "a")
        reportFile.write(Message)
        reportFile.close()

    def garbageCollector(self):

        del self.serverDirectoryDictionary
        self.serverDirectoryDictionary = defaultdict(list)
        del self.keyIDs
        self.keyIDs = []

    def resetAll(self):
        time.sleep(2)
        self.configuredDatabase = False
        self.serverDirectoryDictionary = defaultdict(list)
        self.keyIDs = []
        self.cnnct, self.databaseCursor, self.user, self.password, self.host, self.databaseName = False, False, False, False, False, False
        self.cnnct = None
        self.databaseCursor = None
        self.initiator()

