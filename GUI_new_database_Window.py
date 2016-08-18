from PyQt4 import QtCore, QtGui
import mysql.connector
from mysql.connector import errorcode
from Crypto.Cipher import AES
from Crypto import Random
import os

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

class Ui_new_Database_Frame(QtGui.QWidget):
    def __init__(self, Parent):#Initialization of the GUI. taking in the Parent in order to use the cursor to the database instead of reconnecting with different cursor.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.Parent = Parent

    def setupUi(self, new_DB_Frame):
        new_DB_Frame.setObjectName(_fromUtf8("new_DB_Frame"))
        new_DB_Frame.resize(577, 484)
        self.verticalLayout = QtGui.QVBoxLayout(new_DB_Frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.username_Frame = QtGui.QFrame(new_DB_Frame)
        self.username_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.username_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.username_Frame.setObjectName(_fromUtf8("username_Frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.username_Frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.username_TV = QtGui.QLabel(self.username_Frame)
        self.username_TV.setObjectName(_fromUtf8("username_TV"))
        self.horizontalLayout.addWidget(self.username_TV)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.username_TE = QtGui.QLineEdit(self.username_Frame)
        self.username_TE.setObjectName(_fromUtf8("username_TE"))
        self.horizontalLayout.addWidget(self.username_TE)
        self.verticalLayout.addWidget(self.username_Frame)
        self.password_Frame = QtGui.QFrame(new_DB_Frame)
        self.password_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.password_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.password_Frame.setObjectName(_fromUtf8("password_Frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.password_Frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.password_TV = QtGui.QLabel(self.password_Frame)
        self.password_TV.setObjectName(_fromUtf8("password_TV"))
        self.horizontalLayout_2.addWidget(self.password_TV)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.password_TE = QtGui.QLineEdit(self.password_Frame)
        self.password_TE.setEchoMode(QtGui.QLineEdit.Password)
        self.password_TE.setObjectName(_fromUtf8("password_TE"))
        self.horizontalLayout_2.addWidget(self.password_TE)
        self.verticalLayout.addWidget(self.password_Frame)
        self.server_URL_Frame = QtGui.QFrame(new_DB_Frame)
        self.server_URL_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.server_URL_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.server_URL_Frame.setObjectName(_fromUtf8("server_URL_Frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.server_URL_Frame)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.server_URL_TV = QtGui.QLabel(self.server_URL_Frame)
        self.server_URL_TV.setObjectName(_fromUtf8("server_URL_TV"))
        self.horizontalLayout_3.addWidget(self.server_URL_TV)
        spacerItem2 = QtGui.QSpacerItem(50, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.server_URL_TE = QtGui.QLineEdit(self.server_URL_Frame)
        self.server_URL_TE.setObjectName(_fromUtf8("server_URL_TE"))
        self.horizontalLayout_3.addWidget(self.server_URL_TE)
        self.verticalLayout.addWidget(self.server_URL_Frame)
        self.frame = QtGui.QFrame(new_DB_Frame)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.db_Name_TV = QtGui.QLabel(self.frame)
        self.db_Name_TV.setObjectName(_fromUtf8("db_Name_TV"))
        self.horizontalLayout_5.addWidget(self.db_Name_TV)
        self.db_Name_TE = QtGui.QLineEdit(self.frame)
        self.db_Name_TE.setObjectName(_fromUtf8("db_Name_TE"))
        self.horizontalLayout_5.addWidget(self.db_Name_TE)
        self.verticalLayout.addWidget(self.frame)
        self.buttons_Frame = QtGui.QFrame(new_DB_Frame)
        self.buttons_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.buttons_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.buttons_Frame.setObjectName(_fromUtf8("buttons_Frame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.buttons_Frame)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.new_DB_BTN = QtGui.QPushButton(self.buttons_Frame)
        self.new_DB_BTN.setObjectName(_fromUtf8("new_DB_BTN"))
        self.horizontalLayout_4.addWidget(self.new_DB_BTN)
        self.existing_DB_BTN = QtGui.QPushButton(self.buttons_Frame)
        self.existing_DB_BTN.setObjectName(_fromUtf8("existing_DB_BTN"))
        self.horizontalLayout_4.addWidget(self.existing_DB_BTN)
        self.verticalLayout.addWidget(self.buttons_Frame)

        self.retranslateUi(new_DB_Frame)
        QtCore.QMetaObject.connectSlotsByName(new_DB_Frame)

    def retranslateUi(self, new_DB_Frame):
        new_DB_Frame.setWindowTitle(_translate("new_DB_Frame", "Form", None))
        self.username_TV.setText(_translate("new_DB_Frame", "Username", None))
        self.password_TV.setText(_translate("new_DB_Frame", "Password", None))
        self.server_URL_TV.setText(_translate("new_DB_Frame", "Host", None))
        self.db_Name_TV.setText(_translate("new_DB_Frame", "Database Name", None))
        self.new_DB_BTN.setText(_translate("new_DB_Frame", "New Database", None))
        self.existing_DB_BTN.setText(_translate("new_DB_Frame", "Existing Database", None))


    @QtCore.pyqtSignature("on_new_DB_BTN_clicked()")
    def create_Database(self):
        #Get all the information from the text edits
        userName = self.username_TE.text()
        password = self.password_TE.text()
        URLHost = self.server_URL_TE.text()
        databaseName = self.db_Name_TE.text()
        #Check if there are empty fields. password is the only field allowed to be empty
        if not userName:
            QtGui.QMessageBox.warning(self, "Please Enter Username",
                                      "please fill in all information before proceeding ")
        elif not URLHost:
            QtGui.QMessageBox.warning(self, "Please Enter URL", "please fill in all information before proceeding ")
        elif not databaseName:
            QtGui.QMessageBox.warning(self, "Please Enter dbName",
                                      "please fill in all information before proceeding ")
        #try to connect to the server with the provided information
        else:
            try:#connect to the database with the provided information
                cnnct = mysql.connector.connect(
                    user = userName,
                    password = password,
                    host = URLHost
                )
            except mysql.connector.Error as ERR:
                QtGui.QMessageBox.warning(self, "database Connection Error", str(ERR.msg))
                return

            try:#set the cursor and the database name to the cnnct variable.
                cursor = cnnct.cursor()
                cnnct.database = databaseName
            except mysql.connector.Error as ERR:
                if ERR.errno == errorcode.ER_BAD_DB_ERROR:
                    try:#if database of this name doesnt exist the create it and set the format.
                        cursor.execute(
                            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(databaseName)
                        )
                    except mysql.connector.Error as ERR2:
                        QtGui.QMessageBox.warning(self, "General DBname Error", str(ERR2.msg))
                        return
                    cnnct.database = databaseName
                else:
                    QtGui.QMessageBox.warning(self, "General DBname Error", str(ERR.msg))
                    print(ERR.msg)
                    return

            try:# after connecting to the database run multiple queries to create the tables if they don't exist
                #create the server Table
                cursor.execute("""CREATE TABLE IF NOT EXISTS Server(id INTEGER AUTO_INCREMENT, serverName TEXT, host TEXT, port INTEGER,
                            userName TEXT, password LONGBLOB, PRIMARY KEY(id))""")
                #create the directory table
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Directory(serverid INTEGER, directoryName VARCHAR(200),
                    Activated INTEGER ,PRIMARY KEY(directoryName), FOREIGN KEY(serverid) REFERENCES Server(id) ON DELETE CASCADE)""")
                #create the log table
                cursor.execute("""CREATE TABLE IF NOT EXISTS Log(serverid INTEGER, directoryName VARCHAR(200),
                 logMessage TEXT,timeStamp DATETIME, FOREIGN KEY(serverid) REFERENCES Server(id) ON DELETE CASCADE,
                        FOREIGN KEY(directoryName) REFERENCES Directory(directoryName))""")
                #create the file table
                cursor.execute("""CREATE TABLE IF NOT EXISTS file(directoryName VARCHAR(200),
                 file VARCHAR(200),ModifiedTime DATETIME ,FOREIGN KEY(directoryName) REFERENCES Directory(directoryName)  ON DELETE CASCADE)""")

                self.Parent.set_Database_Cursor(userName, password, URLHost, databaseName)#set the cursor of the parent

            except mysql.connector.Error as ERR:
                QtGui.QMessageBox.warning(self, "Error Creating Tables", str(ERR.msg))
                return

            #create a file and store all the DB information inside it as well as encrypting.
            fName = str(databaseName)
            fName = fName.replace(".", "")
            fName = str(fName) +".txt"
            creatFile = open(fName, "w")
            creatFile.write(userName + "\n" + password + "\n" + URLHost + "\n" + databaseName)
            creatFile.close()
            self.encrypt_file(self.Parent.getKey("mGDfJpfDsQ6651fsf!@$^!@$*!@#fwefgax6qNY2"), fName)
            cnnct.close()

            self.Parent.refreshServerList()#call the refresh list function inside the parent to refresh the list of servers/Directories.
            # self.Parent.resetChecker()
            self.close()#close this window.


    def encrypt_file(self, key, filename):#encrypts the file
        chunkSize = 64*1024
        outputFile = "(encrypted)" + filename
        fileSize = str(os.path.getsize(filename)).zfill(16)
        IV = Random.new().read(16)

        encryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(filename, 'rb') as infile:
            with open(outputFile, 'wb') as outputFile:
                outputFile.write(fileSize.encode("utf-8"))
                outputFile.write(IV)

                while True:
                    chunk = infile.read(chunkSize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 !=0:
                        chunk += b" " * (16 - (len(chunk) %16))
                    outputFile.write(encryptor.encrypt(chunk))

        continueFile = open("firstrun.txt", 'w')
        continueFile.write(filename)
        continueFile.close()




    @QtCore.pyqtSignature("on_existing_DB_BTN_clicked()")
    def Connect_Existing_Database(self):#Connects into an existing database
        #get all the information from the text editor and store it into variables
        userName = self.username_TE.text()
        password = self.password_TE.text()
        URLHost = self.server_URL_TE.text()
        dataBaseName = self.db_Name_TE.text()
        #if any of the text editor fields are empty then throw an error
        if not userName:
            QtGui.QMessageBox.warning(self, "Please Enter Username", "please fill in all information before proceeding")
        elif not URLHost:
            QtGui.QMessageBox.warning(self, "Please Enter URL", "please fill in all information before proceeding")
        elif not dataBaseName:
            QtGui.QMessageBox.warning(self, "Please Enter dbName", "please fill in all information before proceeding")
        else:
            try:#connect to the database with the provided information
                cnnct = mysql.connector.connect(
                    user=userName,
                    password=password,
                    host=URLHost,
                    database=dataBaseName)
            except mysql.connector.Error as e:
                if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    QtGui.QMessageBox.warning(self, "ERROR ACCESS DENIED","Access denied, Check Username and Password.\n"+ str(e.msg))
                    return
                elif e.errno == errorcode.ER_BAD_DB_ERROR:
                    QtGui.QMessageBox.warning(self, "Database Doesnt Exist", "Databse Doesnt exist.\n" + str(e.msg))
                    return
                else:
                    QtGui.QMessageBox.warning(self, "Other Error.", str(e.msg))
                    return

            cursor = cnnct.cursor()# set the cursor and create the missing tables if any
            #create server table
            cursor.execute("""CREATE TABLE IF NOT EXISTS Server(id INTEGER AUTO_INCREMENT, serverName TEXT, host TEXT, port INTEGER,
                        userName TEXT, password LONGBLOB, PRIMARY KEY(id))""")
            # create the directory table
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS Directory(serverid INTEGER, directoryName VARCHAR(200),
                Activated INTEGER ,PRIMARY KEY(directoryName), FOREIGN KEY(serverid) REFERENCES Server(id) ON DELETE CASCADE)""")
            # create the log table
            cursor.execute("""CREATE TABLE IF NOT EXISTS Log(serverid INTEGER, directoryName VARCHAR(200),
                 logMessage TEXT,timeStamp DATETIME, FOREIGN KEY(serverid) REFERENCES Server(id) ON DELETE CASCADE,
                        FOREIGN KEY(directoryName) REFERENCES Directory(directoryName))""")
            # create the file table
            cursor.execute("""CREATE TABLE IF NOT EXISTS file(directoryName VARCHAR(200),
             file VARCHAR(200),ModifiedTime DATETIME ,FOREIGN KEY(directoryName) REFERENCES Directory(directoryName)  ON DELETE CASCADE)""")
            cnnct.close()
            self.Parent.set_Database_Cursor(userName, password, URLHost, dataBaseName)#set the cursor of the parent.
            self.Parent.refreshServerList()##all the refresh list function inside the parent to refresh the list of servers/Directories.
            self.close()#close this window.

