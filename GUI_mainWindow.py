import sys
import GUI_new_server_Window
import GUI_new_database_Window
import GUI_new_Directory_Window
import FTP_checker_Class
import GUI_check_frequency_Window
import mysql.connector
from PyQt4 import QtCore, QtGui
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import PyInstaller
import os
import winsound

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtGui.QMenu(parent)
        self.setContextMenu(self.menu)





class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):#Initialization of the GUI.
        super(QtGui.QMainWindow, self).__init__()
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.configured_Database = False
        self.databaseCursor = None
        self.cnnct = None
        self.firstRunChecker()
        self.start_file_checker()
        self.fetchedLogs = 0
        self.icon = QtGui.QIcon("FTPimage.png")
        self.menu = QtGui.QMenu()
        self.exitAction = self.menu.addAction("exit")
        self.exitAction.triggered.connect(sys.exit)
        self.tray = QtGui.QSystemTrayIcon()
        self.traysignal = "activated(QSystemTrayIcon::ActivationReason)"
        QtCore.QObject.connect(self.tray, QtCore.SIGNAL(self.traysignal), self.hideShowTray)
        self.tray.setIcon(self.icon)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.tray.setToolTip("FTP File Checker")





    def setupUi(self, MainWindow):#initialize the ui
        MainWindow.setObjectName(_fromUtf8("FTP File Checker"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.server_info_Frame = QtGui.QFrame(self.centralwidget)
        self.server_info_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.server_info_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.server_info_Frame.setObjectName(_fromUtf8("server_info_Frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.server_info_Frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.server_Directory_Tree = QtGui.QTreeWidget(self.server_info_Frame)
        self.server_Directory_Tree.setAlternatingRowColors(True)
        self.server_Directory_Tree.setObjectName(_fromUtf8("server_Directory_Tree"))
        self.horizontalLayout_2.addWidget(self.server_Directory_Tree)
        self.log_LV = QtGui.QListWidget(self.server_info_Frame)
        self.log_LV.setObjectName(_fromUtf8("log_LV"))
        self.horizontalLayout_2.addWidget(self.log_LV)
        self.verticalLayout.addWidget(self.server_info_Frame)
        self.server_buttons_Frame = QtGui.QFrame(self.centralwidget)
        self.server_buttons_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.server_buttons_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.server_buttons_Frame.setObjectName(_fromUtf8("server_buttons_Frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.server_buttons_Frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Add_Directory = QtGui.QPushButton(self.server_buttons_Frame)
        self.Add_Directory.setObjectName(_fromUtf8("Add_Directory"))
        self.horizontalLayout.addWidget(self.Add_Directory)
        self.Remove_Directory_BTN = QtGui.QPushButton(self.server_buttons_Frame)
        self.Remove_Directory_BTN.setObjectName(_fromUtf8("Remove_Directory_BTN"))
        self.horizontalLayout.addWidget(self.Remove_Directory_BTN)
        self.delete_server_BT = QtGui.QPushButton(self.server_buttons_Frame)
        self.delete_server_BT.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.delete_server_BT.setObjectName(_fromUtf8("delete_server_BT"))
        self.horizontalLayout.addWidget(self.delete_server_BT)
        self.Popup_Notification_CB = QtGui.QCheckBox(self.server_buttons_Frame)
        self.Popup_Notification_CB.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Popup_Notification_CB.setObjectName(_fromUtf8("Popup Notification"))
        self.sound_Notifification_CB = QtGui.QCheckBox(self.server_buttons_Frame)
        self.sound_Notifification_CB.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.sound_Notifification_CB.setObjectName(_fromUtf8("sound_Notifification_CB"))
        self.horizontalLayout.addWidget(self.Popup_Notification_CB)
        self.horizontalLayout.addWidget(self.sound_Notifification_CB)
        self.verticalLayout.addWidget(self.server_buttons_Frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuAdd_Configure_DB = QtGui.QMenu(self.menuFile)
        self.menuAdd_Configure_DB.setObjectName(_fromUtf8("menuAdd_Configure_DB"))
        self.menuNew_Server = QtGui.QMenu(self.menuFile)
        self.menuNew_Server.setObjectName(_fromUtf8("menuNew_Server"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionView_DB_info = QtGui.QAction(MainWindow)
        self.actionView_DB_info.setObjectName(_fromUtf8("actionView_DB_info"))
        self.actionView_Check_Frequency = QtGui.QAction(MainWindow)
        self.actionView_Check_Frequency.setObjectName(_fromUtf8("actionView_Check_Frequency"))
        self.actionAdd_Configure_DB = QtGui.QAction(MainWindow)
        self.actionAdd_Configure_DB.setObjectName(_fromUtf8("actionAdd_Configure_DB"))
        self.actionAdd_Configure_server = QtGui.QAction(MainWindow)
        self.actionAdd_Configure_server.setObjectName(_fromUtf8("actionAdd_Configure_server"))
        self.menuAdd_Configure_DB.addAction(self.actionView_DB_info)
        self.menuAdd_Configure_DB.addAction(self.actionAdd_Configure_DB)
        self.menuNew_Server.addAction(self.actionView_Check_Frequency)
        self.menuNew_Server.addAction(self.actionAdd_Configure_server)
        self.menuFile.addAction(self.menuNew_Server.menuAction())
        self.menuFile.addAction(self.menuAdd_Configure_DB.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        #Clickable events of the menu bar.
        self.actionView_Check_Frequency.triggered.connect(self.check_Frequency)
        self.actionView_DB_info.triggered.connect(self.resetAllSettings)
        self.actionAdd_Configure_DB.triggered.connect(self.to_new_database_Window)
        self.actionAdd_Configure_server.triggered.connect(self.to_new_server_Window)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.show()





    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("FTP File Checker", "FTP File Checker", None))
        MainWindow.setWindowIcon(QtGui.QIcon("FTPimage.png"))
        self.server_Directory_Tree.headerItem().setText(0, _translate("MainWindow", "Servers/Directories", None))
        __sortingEnabled = self.server_Directory_Tree.isSortingEnabled()
        self.server_Directory_Tree.setSortingEnabled(False)
        self.server_Directory_Tree.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.log_LV.isSortingEnabled()
        self.log_LV.setSortingEnabled(False)
        self.log_LV.setSortingEnabled(__sortingEnabled)
        self.Add_Directory.setText(_translate("MainWindow", "Add Directory", None))
        self.Remove_Directory_BTN.setText(_translate("MainWindow", "Remove Directory", None))
        self.delete_server_BT.setText(_translate("MainWindow", "Delete Server", None))
        self.sound_Notifification_CB.setText(_translate("MainWindow", "Sound Notification Enabled", None))
        self.Popup_Notification_CB.setText(_translate("MainWindow", "Popup Notification Enables", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuAdd_Configure_DB.setTitle(_translate("MainWindow", "Database Options", None))
        self.menuNew_Server.setTitle(_translate("MainWindow", "Server Options", None))
        self.actionView_DB_info.setText(_translate("MainWindow", "Reset All Information", None))
        self.actionView_Check_Frequency.setText(_translate("MainWindow", "Set Check Frequency", None))
        self.actionAdd_Configure_DB.setText(_translate("MainWindow", "Add/Configure DB", None))
        self.actionAdd_Configure_server.setText(_translate("MainWindow", "Add/Configure Server", None))

    def resetAllSettings(self):
        reply = QtGui.QMessageBox.question(self, "Reset Checker", "Are you sure you want to Reset? you will lose all your infomartion. however database wont be removed"
                                           , QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if (reply == QtGui.QMessageBox.Yes):
            self.resetChecker()
            filelist = [f for f in os.listdir(".") if f.endswith(".txt")]
            for f in filelist:
                os.remove(f)
            self.server_Directory_Tree.clear()
        else:
            pass

    def popupAnnouncer(self, Title, Message):
        if(self.Popup_Notification_CB.isChecked() == True):
            self.tray.showMessage(Title, Message)
        if(self.sound_Notifification_CB.isChecked() == True):
            winsound.PlaySound("workwork.wav", winsound.SND_FILENAME)

    def hideShowTray(self):
        if(self.isHidden() == False):
            self.hide()
        else:
            self.show()

    def firstRunChecker(self):
        if ((os.path.isfile("./firstrun.txt")) == True):
            fileExists = open("firstrun.txt", 'r')
            encryptedFileName = fileExists.readline()
            self.decrypt_password(self.getKey("mGDfJpfDsQ6651fsf!@$^!@$*!@#fwefgax6qNY2"),
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
            if(db_Existence == True):
                QtGui.QMessageBox.warning(self, "Connected to DB.",
                                          "Connected to: \n" + str(dbName) + " at " + str(dbURLHost))
            else:
                QtGui.QMessageBox.warning(self, "DB doesnt exist","Database doesn't Exist: \n" + str(dbName) + " at " + str(dbURLHost))
                return
        else:
            QtGui.QMessageBox.warning(self, "DB not Configured.",
                                      "Steps:\n 1-Configure Database Using Xammp and phpMyAdmin \n 2-Add FTP servers and Directories")
            return

        self.refreshServerList()

    def resetChecker(self):
        self.filechecker.setConfiguredDB()

    def start_file_checker(self):
        self.thread = QtCore.QThread()
        self.filechecker = FTP_checker_Class.FTP_checker(self)
        self.filechecker.moveToThread(self.thread)
        self.filechecker.finished.connect(self.thread.quit)
        # self.thread.started.connect(self.filechecker.infin)
        self.thread.started.connect(self.filechecker.initiator)
        self.thread.start()


    def decrypt_password(self, key, fileName):#function that decrypts the file
        chunkSize = 64 * 1024
        outputFile = fileName[11:]
        with open(fileName, 'rb') as infile:
            fileSize = int(infile.read(16))
            IV = infile.read(16)

            decryptor = AES.new(key, AES.MODE_CBC, IV)

            with open(outputFile, 'wb') as outputFile:
                while True:
                    chunk = infile.read(chunkSize)

                    if (len(chunk) == 0):
                        break
                    outputFile.write(decryptor.decrypt(chunk))
                outputFile.truncate(fileSize)

    def to_new_server_Window(self):#checks if the database is configured first then start the add new server GUI window.
        if(self.configured_Database == False):
            QtGui.QMessageBox.warning(self, "Please Configure Database", "Please Add/Configure your databse First!")
        else:
            self.newuser = GUI_new_server_Window.Ui_new_server_Frame(self)
            self.newuser.show()

    def to_new_database_Window(self):#starts the GUI window that adds a new server
        self.newDB = GUI_new_database_Window.Ui_new_Database_Frame(self)
        self.newDB.show()
        self.configured_Database=True

    def set_Database_Cursor(self, userName, password, URLHost, dataBaseName):#Function that sets the cursor, links it to the DB
        try:#connect to the database with the provided information
            self.cnnct = mysql.connector.connect(
                user=userName,
                password=password,
                host=URLHost,
                database=dataBaseName)
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "DB connection Error.", str(e.msg))
            return False

        self.databaseCursor = self.cnnct.cursor(buffered=True)
        self.user = userName
        self.password = password
        self.host = URLHost
        self.databaseName = dataBaseName
        self.configured_Database = True
        return True

    def sew(self):#Test Function
        print("banana milkshake")

    def getKey(self, password):#Pass in the password and return the hash value of it to use it as a key for the decryption.
        hasher = SHA256.new(password.encode("utf-8"))
        return hasher.digest()


    def refreshServerList(self):#function that refreshes the list of server/directories
        self.server_Directory_Tree.clear()

        try:#Get number of Servers in Database
            query = "SELECT COUNT(*) FROM server"
            self.databaseCursor.execute(query)
            self.cnnct.commit()
            fetched_Size = self.databaseCursor.fetchall()
            numberOfServers = int(fetched_Size[0][0])
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Getting number of servers Error", str(e.msg))
            return


        try:#Get number of Directories in Database
            query = "SELECT COUNT(*) FROM directory"
            self.databaseCursor.execute(query)
            self.cnnct.commit()
            fetched_Size = self.databaseCursor.fetchall()
            numberofDirectories = int(fetched_Size[0][0])
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Getting number of directories Error", str(e.msg))
            return

        #Initialize list of servers and list of Directories
        self.listOfServers = [QtGui.QTreeWidgetItem(self.server_Directory_Tree) for counter in range(numberOfServers)]
        self.listOfDirectories = [QtGui.QTreeWidgetItem() for counter in range(numberofDirectories)]

        #Initialize the flags for each server Index of listofserver
        for counter in range(numberOfServers):
            self.listOfServers[counter].setFlags(
                QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
            )

        #Get names and ID of each server in Database
        try:
            query = "SELECT id , serverName FROM server"
            self.databaseCursor.execute(query)
            self.cnnct.commit()
            serverNameAndID = self.databaseCursor.fetchall()
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Inserting FTP Error", str(e.msg))
            return

        #Assign Server Names to the GUI Tree list
        for serverCounter in range(len(serverNameAndID)):
            self.server_Directory_Tree.topLevelItem(serverCounter).setText(0, _translate("MainWindow", str(serverNameAndID[serverCounter][1]), None))
        # print(numberOfServers)
        # print(serverNameAndID[0][1])
        upperDirCounter = 0
        for counter in range(numberOfServers):
            # print(counter)
            try:
                query = "SELECT directoryName FROM directory WHERE serverid LIKE "+ "'" + str(serverNameAndID[counter][0]) + "'"
                self.databaseCursor.execute(query)
                self.cnnct.commit()
                directoryNames = self.databaseCursor.fetchall()
                # print(str(directoryNames[2][0]))
            except mysql.connector.Error as e:
                QtGui.QMessageBox.warning(self, "Getting Directory Names Error", str(e.msg))
                return

            for lowerDirCounter in range(len(directoryNames)):
                self.listOfDirectories[upperDirCounter] = QtGui.QTreeWidgetItem(self.listOfServers[counter])
                self.listOfDirectories[upperDirCounter].setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
                )
                self.server_Directory_Tree.topLevelItem(counter).child(lowerDirCounter).setText(0, _translate("MainWindow", directoryNames[lowerDirCounter][0], None))
                upperDirCounter+=1
        self.connect(self.server_Directory_Tree, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.populateLogs)

    def populateLogs(self):#function that populate the log of modifications that happened to selected directory.
        self.log_LV.clear()
        for counter in range(len(self.listOfDirectories)):#loop that goes through the list of directories to see which element is currently selected in order to populate its log.
            if (self.listOfDirectories[counter].isSelected() == True):
                try:#get the log message and time stamp of each modification/addition/removal of items inside that specific directory
                    self.databaseCursor.execute(
                        "SELECT logMessage, timeStamp FROM log WHERE directoryName LIKE " + "'" +
                        str(self.listOfDirectories[counter].text(0)) + "'")
                    self.cnnct.commit()
                    self.fetchedLogs = self.databaseCursor.fetchall()
                except mysql.connector.Error as e:
                    QtGui.QMessageBox.warning(self, "Error getting File Names", str(e.msg))
                    return
                if (len(self.fetchedLogs) > 0):#populate the log with logs fetched from the Database
                    for smallcounter in range(len(self.fetchedLogs)):
                        self.log_LV.addItem(self.fetchedLogs[smallcounter][0] + str(" at Time: ") + str(self.fetchedLogs[smallcounter][1]))
                        self.log_LV.addItem("---------------------------------------------------------------------")
                break

    @QtCore.pyqtSignature("on_Add_Directory_clicked()")
    def add_Directory(self):#function that adds directory to selected server
        itemFound = False
        for counter in range(len(self.listOfServers)):# loop that goes through the list of servers to see which element is currently selected in order to add directory to it.
            if(self.listOfServers[counter].isSelected() == True):
                self.addDirectory = GUI_new_Directory_Window.Ui_new_directory_Form(self, self.listOfServers[counter].text(0))#starts the GUI window of add new directory
                self.addDirectory.show()
                itemFound= True
                break
        if (itemFound == False):
            QtGui.QMessageBox.warning(self, "Server Not Found", "Please click on the Server you want to add Directory to")


    @QtCore.pyqtSignature("on_Remove_Directory_BTN_clicked()")
    def remove_Directory(self):#function that deletes the selected directory
        itemFound = False
        for counter in range(len(self.listOfDirectories)):# loop that goes through the list of directories to see which element is currently selected in order to set it for delition
            print(counter)
            if(self.listOfDirectories[counter].isSelected() == True):
                reply = QtGui.QMessageBox.question(self, "Delete Directory Checker",
                                                   "Are you sure you want to Delete this Directory? "
                                                   , QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if (reply == QtGui.QMessageBox.Yes):
                    try:
                        self.databaseCursor.execute(
                            "DELETE FROM log WHERE directoryName LIKE " + "'" + str((self.listOfDirectories[counter].text(0))) + "'")
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        QtGui.QMessageBox.warning(self, "DELETING Directory Errors", str(e.msg))
                        return
                    try:
                        self.databaseCursor.execute(
                            "DELETE FROM file WHERE directoryName LIKE " + "'" + str((self.listOfDirectories[counter].text(0)) + "'"))
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        QtGui.QMessageBox.warning(self, "DELETING Directory Errora", str(e.msg))
                        return
                    try:  # delete the directory and all thats related to it. NOT THE SERVER. the files and logs only.
                        self.databaseCursor.execute(
                            "DELETE FROM directory WHERE directoryName LIKE " + "'" + str((self.listOfDirectories[counter].text(0)) + "'"))
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        QtGui.QMessageBox.warning(self, "DELETING Directory Errorb", str(e.msg))
                        return

                    self.refreshServerList()  # call the refresh list function inside the parent to refresh the list of servers/Directories.
                    itemFound = True
                    break
            else:
                pass

        if (itemFound == False):
            QtGui.QMessageBox.warning(self, "Directory Not Found", "Please click on the Directory you want to remove")


    @QtCore.pyqtSignature("on_delete_server_BT_clicked()")
    def deleteServer(self):#Function that deletes the selected server.
        itemFound = False
        for counter in range(len(self.listOfServers)):# loop that goes through the list of servers to see which element is currently selected in order to set it for delition
            if(self.listOfServers[counter].isSelected() == True):
                reply = QtGui.QMessageBox.question(self, "Delete Server Checker",
                                                   "Are you sure you want to Delete this server? "
                                                   , QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if (reply == QtGui.QMessageBox.Yes):
                    try:  # get the id of the server to delete
                        self.databaseCursor.execute(
                            "SELECT id FROM server WHERE serverName LIKE " + "'" + (str(self.listOfServers[counter].text(0))) + "'")
                        self.cnnct.commit()
                        serverid = self.databaseCursor.fetchall()
                    except mysql.connector.Error as e:
                        QtGui.QMessageBox.warning(self, "Getting id Error", str(e.msg))
                        return
                    try:  # delete the logs linked to the server
                        self.databaseCursor.execute(
                            "DELETE FROM log WHERE serverid LIKE " + "'" + (str(serverid[0][0])) + "'")
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        QtGui.QMessageBox.warning(self, "Deleting log Error", str(e.msg))
                        return
                    try:  # delete the directory linked to the server
                        self.databaseCursor.execute(
                            "DELETE FROM Directory WHERE serverid LIKE " + (str(serverid[0][0])))
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        QtGui.QMessageBox.warning(self, "Deleting Directory Error", str(e.msg))
                        return

                    try:  # delete the server and all thats related to it from the database.
                        self.databaseCursor.execute(
                            "DELETE FROM server WHERE serverName LIKE " + "'" + (str(self.listOfServers[counter].text(0))) + "'")
                        self.cnnct.commit()
                    except mysql.connector.Error as e:
                        QtGui.QMessageBox.warning(self, "Deleting Server Error", str(e.msg))
                        return

                    self.refreshServerList()  # call the refresh list function inside the parent to refresh the list of servers/Directories.
                else:
                    pass
                itemFound = True
                break
        if (itemFound == False):
            QtGui.QMessageBox.warning(self, "Server Not Found", "Please click on the server you want to remove")

    def check_Frequency(self):#function that activates the GUI window to set the frequency by which the program checks the DB and FTP for changes.
        self.checkFrequency = GUI_check_frequency_Window.Ui_check_Frequency_Form(self)
        self.checkFrequency.show()

    def get_configuredDatabase(self):#Function that returns the current state of the Database whether its configured or no.
        return self.configured_Database

    def set_FTP_Frequency(self, delayValue):#Function that calls the set frequency by which the FTP checker checks the DB and FTP. Used by GUI_check_frequency.py -> Here -> FTP_checker_class.py
        self.filechecker.setCheckDelay(delayValue)

    def closeEvent(self, event):#over ride the close function when X is clicked instead of closing the program. hide it.
        event.ignore()
        self.hide()

    def decrypt_server_password(self, password):#Function that decrypts the password based on the key from our specific value J3bVC5aPeHz#%!@$!^*#%$#@FVWsaga@!#uHdzV can be changed.
        key = self.getKey("J3bVC5aPeHz#%!@$!^*#%$#@FVWsaga@!#uHdzV")
        cipher = AES.new(key)
        dec = cipher.decrypt(password[0]).decode('utf-8')
        l = dec.count("{")
        return dec[:len(dec)-l]

if __name__ == '__main__':
    mainapp = QtGui.QApplication([])
    ex = Ui_MainWindow()
    mainapp.exec_()



