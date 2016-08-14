from PyQt4 import QtCore, QtGui #Create a new Server
import mysql.connector
import ftplib
from Crypto.Cipher import AES

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

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

class Ui_new_server_Frame(QtGui.QWidget):
    def __init__(self, Parent):#Initialization of the GUI. taking in the Parent in order to use the cursor to the database instead of reconnecting with different cursor.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.Parent = Parent

    def setupUi(self, new_server_Frame):
        new_server_Frame.setObjectName(_fromUtf8("new_server_Frame"))
        new_server_Frame.resize(577, 484)
        self.verticalLayout = QtGui.QVBoxLayout(new_server_Frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.username_Frame = QtGui.QFrame(new_server_Frame)
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
        self.password_Frame = QtGui.QFrame(new_server_Frame)
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
        self.server_URL_Frame = QtGui.QFrame(new_server_Frame)
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
        self.root_Directory_Frame = QtGui.QFrame(new_server_Frame)
        self.root_Directory_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.root_Directory_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.root_Directory_Frame.setObjectName(_fromUtf8("root_Directory_Frame"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.root_Directory_Frame)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.root_Directory_TV = QtGui.QLabel(self.root_Directory_Frame)
        self.root_Directory_TV.setObjectName(_fromUtf8("root_Directory_TV"))
        self.horizontalLayout_5.addWidget(self.root_Directory_TV)
        self.root_Directory_TE = QtGui.QLineEdit(self.root_Directory_Frame)
        self.root_Directory_TE.setObjectName(_fromUtf8("root_Directory_TE"))
        self.horizontalLayout_5.addWidget(self.root_Directory_TE)
        self.verticalLayout.addWidget(self.root_Directory_Frame)
        self.serverName_Frame = QtGui.QFrame(new_server_Frame)
        self.serverName_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.serverName_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.serverName_Frame.setObjectName(_fromUtf8("serverName_Frame"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.serverName_Frame)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.serverName_TV = QtGui.QLabel(self.serverName_Frame)
        self.serverName_TV.setObjectName(_fromUtf8("serverName_TV"))
        self.horizontalLayout_6.addWidget(self.serverName_TV)
        self.serverName_TE = QtGui.QLineEdit(self.serverName_Frame)
        self.serverName_TE.setObjectName(_fromUtf8("serverName_TE"))
        self.horizontalLayout_6.addWidget(self.serverName_TE)
        self.verticalLayout.addWidget(self.serverName_Frame)
        self.buttons_Frame = QtGui.QFrame(new_server_Frame)
        self.buttons_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.buttons_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.buttons_Frame.setObjectName(_fromUtf8("buttons_Frame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.buttons_Frame)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.new_server_Button = QtGui.QPushButton(self.buttons_Frame)
        self.new_server_Button.setObjectName(_fromUtf8("new_server_Button"))
        self.horizontalLayout_4.addWidget(self.new_server_Button)
        self.cancel_Button = QtGui.QPushButton(self.buttons_Frame)
        self.cancel_Button.setObjectName(_fromUtf8("cancel_Button"))
        self.horizontalLayout_4.addWidget(self.cancel_Button)
        self.verticalLayout.addWidget(self.buttons_Frame)

        self.retranslateUi(new_server_Frame)
        QtCore.QMetaObject.connectSlotsByName(new_server_Frame)

    def retranslateUi(self, new_server_Frame):
        new_server_Frame.setWindowTitle(_translate("new_server_Frame", "Form", None))
        self.username_TV.setText(_translate("new_server_Frame", "Username", None))
        self.password_TV.setText(_translate("new_server_Frame", "Password", None))
        self.server_URL_TV.setText(_translate("new_server_Frame", "Host", None))
        self.root_Directory_TV.setText(_translate("new_server_Frame", "Root Directory", None))
        self.serverName_TV.setText(_translate("new_server_Frame", "Server Name", None))
        self.new_server_Button.setText(_translate("new_server_Frame", "New FTP Server", None))
        self.cancel_Button.setText(_translate("new_server_Frame", "Cancel", None))


    def pad(self, parameter):#Pad function for the encryption/decryption Function
        return parameter + ((16-len(parameter) % 16) * "{")

    def encrypt(self, password):#Set value as a key which can be changed, Encrypt the password
        key = self.Parent.getKey("J3bVC5aPeHz#%!@$!^*#%$#@FVWsaga@!#uHdzV")
        cipher = AES.new(key)
        return cipher.encrypt(self.pad(password))

    def decrypt(self, password):#decrypt the password using the hash value of the same key we used to encrypt.
        key = self.Parent.getKey("J3bVC5aPeHz#%!@$!^*#%$#@FVWsaga@!#uHdzV")
        cipher = AES.new(key)
        dec = cipher.decrypt(password).decode('utf-8')
        l = dec.count("{")
        return dec[:len(dec)-l]



    @QtCore.pyqtSignature("on_new_server_Button_clicked()")
    def new_server(self):#Run this function when the button New server is clicked.
        #Get all the information from the text Editors and save them into variables
        userName = self.username_TE.text()
        password = self.password_TE.text()
        URLHost = self.server_URL_TE.text()
        rootDirectory = self.root_Directory_TE.text()
        serverName = self.serverName_TE.text()
        #Checker to make sure that none of the Text edits are empty.
        if ((not userName) or (not password) or (not URLHost) or (not rootDirectory) or (not serverName)):
            QtGui.QMessageBox.warning(self, "Please Enter Username", "please fill in all information before proceeding")
        else:#pass in all the information into the login Function
            self.attemptLogin(userName, password, URLHost, serverName, rootDirectory)

    def attemptLogin(self, userName, password, URLHost, serverName, rootDirectory):#Attempt login function with multiple Checks before creation.
        try:#Get the number of servers that has the name Host name if Exists
            self.Parent.databaseCursor.execute("SELECT COUNT(*) FROM server WHERE host LIKE " + "'" + str(URLHost) + "'")
            self.Parent.cnnct.commit()
            fetched_Size = self.Parent.databaseCursor.fetchall()
            occurences_Of_Host = int(fetched_Size[0][0])
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Selecting Number of Servers with HostName.", str(e.msg))

        try:#Get the number of servers that has the same server name (Nick Name) if Exists.
            self.Parent.databaseCursor.execute("SELECT COUNT(*) FROM server WHERE serverName LIKE " + "'" + str(serverName) + "'")
            self.Parent.cnnct.commit()
            fetched_Size = self.Parent.databaseCursor.fetchall()
            occurences_Of_ServerName = int(fetched_Size[0][0])
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Selecting Number of Servers with ServerName", str(e.msg))

        if(occurences_Of_Host > 0):#Check if there are any servers with the same Host or Server Names. if Exists then throw an error.
            QtGui.QMessageBox.warning(self, "Server Host Already Exists.", "You already Added this URL server! " + str(URLHost))
            return
        elif(occurences_Of_ServerName > 0):
            QtGui.QMessageBox.warning(self, "Server Name Already Exists.","You are already using This name for another Server! " + str(userName))
            return

        else:#Try to connect to FTP server with the information given if they pass all the checks.
            try:#change the working directory to the given Root Directory.
                ftp = ftplib.FTP(URLHost)
                ftp.login(user = userName, passwd= password)
                ftp.cwd(rootDirectory)
            except ftplib.all_errors as ERR:
                QtGui.QMessageBox.warning(self, "FTP Connection ERROR", str(ERR))
                return
            ftp.close()

            try:#If the connection + root directory went well then insert all the information into our Database in the Server Table. *We encrypt the password and insert the encrypted value into DB
                self.Parent.databaseCursor.execute("INSERT INTO server (serverName, host, username, password) VALUES(%s,%s,%s,%s)", (serverName, URLHost, userName, self.encrypt(password)))
                self.Parent.cnnct.commit()
            except mysql.connector.Error as e:
                QtGui.QMessageBox.warning(self, "Inserting server Information into DB Error", str(e.msg))

            try:#Get the id of the server from the database in order to add the directory in its designated DB Table. (Directory Table.)
                self.Parent.databaseCursor.execute("SELECT id FROM server WHERE host LIKE " + "'" + str(URLHost) + "'")
                self.Parent.cnnct.commit()
                fetchedvalue = self.Parent.databaseCursor.fetchall()
                itemLocation = fetchedvalue[0][0]
            except mysql.connector.Error as e:
                QtGui.QMessageBox.warning(self, "Selecting ID from Server Error", str(e.msg))

            try:#Insert the root directory into the database inside the designated Table (directory Table)
                self.Parent.databaseCursor.execute("INSERT INTO directory VALUES(%s,%s,%s)", (itemLocation, rootDirectory, 0))
                self.Parent.cnnct.commit()
            except mysql.connector.Error as e:
                QtGui.QMessageBox.warning(self, "Inserting Directory into DB Error", str(e.msg))

            self.Parent.refreshServerList()#call the refresh list function inside the parent to refresh the list of servers/Directories.
            self.close()#close this window.


    @QtCore.pyqtSignature("on_cancel_Button_clicked()")
    def cancel_new_server(self):#Run this function if cancel button is clicked. and close this window.
        self.close()
