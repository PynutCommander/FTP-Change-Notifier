from PyQt4 import QtCore, QtGui
import mysql.connector
import ftplib

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

class Ui_new_directory_Form(QtGui.QWidget):
    def __init__(self, Parent, serverName):#Initialization of the GUI. taking in the Parent in order to use the cursor to the database instead of reconnecting with different cursor.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.Parent = Parent
        self.serverName = serverName
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(469, 400)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.Directory_Getter_Frame = QtGui.QFrame(Form)
        self.Directory_Getter_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Directory_Getter_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.Directory_Getter_Frame.setObjectName(_fromUtf8("Directory_Getter_Frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.Directory_Getter_Frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.DirectoryName_TV = QtGui.QLabel(self.Directory_Getter_Frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.DirectoryName_TV.setFont(font)
        self.DirectoryName_TV.setObjectName(_fromUtf8("DirectoryName_TV"))
        self.horizontalLayout_2.addWidget(self.DirectoryName_TV)
        self.directoryName_TE = QtGui.QLineEdit(self.Directory_Getter_Frame)
        self.directoryName_TE.setObjectName(_fromUtf8("directoryName_TE"))
        self.horizontalLayout_2.addWidget(self.directoryName_TE)
        self.verticalLayout.addWidget(self.Directory_Getter_Frame)
        self.DirectoryButtons_Frame = QtGui.QFrame(Form)
        self.DirectoryButtons_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.DirectoryButtons_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.DirectoryButtons_Frame.setObjectName(_fromUtf8("DirectoryButtons_Frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.DirectoryButtons_Frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.AddDirectory_BT = QtGui.QPushButton(self.DirectoryButtons_Frame)
        self.AddDirectory_BT.setObjectName(_fromUtf8("AddDirectory_BT"))
        self.horizontalLayout.addWidget(self.AddDirectory_BT)
        self.cancel_BT = QtGui.QPushButton(self.DirectoryButtons_Frame)
        self.cancel_BT.setObjectName(_fromUtf8("cancel_BT"))
        self.horizontalLayout.addWidget(self.cancel_BT)
        self.verticalLayout.addWidget(self.DirectoryButtons_Frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.DirectoryName_TV.setText(_translate("Form", "Directory Name", None))
        self.AddDirectory_BT.setText(_translate("Form", "Add Directory", None))
        self.cancel_BT.setText(_translate("Form", "Cancel", None))

    @QtCore.pyqtSignature("on_AddDirectory_BT_clicked()")
    def addDirectory(self):#Run this function if the add directory button is clicked.

        try:#get the ID of the server with the designated servername that we want to add the directory to.
            self.Parent.databaseCursor.execute("SELECT id FROM server WHERE serverName LIKE " + "'" + self.serverName + "'")
            self.Parent.cnnct.commit()
            serverID = self.Parent.databaseCursor.fetchall()
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Selecting ID from Server Error", str(e.msg))
            return

        directoryName = self.directoryName_TE.text()#get the chosen directory name from the text editor.
        if not directoryName:#if the text editor is empty throw an error.
            QtGui.QMessageBox.warning(self, "Please Enter Directory Name","please fill in all information before proceeding")

        try:#get the number of servers that share the same serverid and directory name. it should be 0
            self.Parent.databaseCursor.execute("SELECT COUNT(*) FROM directory WHERE serverid LIKE " + "'" + str(serverID[0][0]) +"'" +
                                                       " AND directoryName LIKE " + "'" + str(directoryName) + "'")
            self.Parent.cnnct.commit()
            occurencesOfName = self.Parent.databaseCursor.fetchall()
            if(int(occurencesOfName[0][0]) > 0):#if the number is not 0 means the directory already exists
                QtGui.QMessageBox.warning(self, "Directory Already Exists", "The directory you are trying to add already exists!")
                return
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Selecting number of directory with same server id and directory Name Error", str(e.msg))
            return

        try:#Get the password of the server from the DB
            self.Parent.databaseCursor.execute("SELECT password FROM server WHERE id LIKE " + "'" + str(serverID[0][0]) + "'")
            self.Parent.cnnct.commit()
            fetchecServerPassword = self.Parent.databaseCursor.fetchall()
            serverPassword= self.Parent.decrypt_server_password(fetchecServerPassword[0])
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Getting Directory Names Error", str(e.msg))
            return

        try:#get the host URL and username from the DB. the reason why i didnt get the password together with them is it was giving an error as it was storing the Byte value from the BLOB field in the DB
            # in the same array as the user name and host which were string. so the password needed to be stored in a seperate variable.
            self.Parent.databaseCursor.execute("SELECT host, userName FROM server WHERE id LIKE " + "'" + str(serverID[0][0]) + "'")
            self.Parent.cnnct.commit()
            serverInformation = self.Parent.databaseCursor.fetchall()
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Getting Directory Names Error", str(e.msg))
            return

        try:#connect to the FTP server and check that the directory exists before inserting it into the directory Table in the DB
            ftp = ftplib.FTP(serverInformation[0][0])
            ftp.login(user=str(serverInformation[0][1]), passwd=str(serverPassword))
            ftp.cwd(str(directoryName))
        except ftplib.all_errors:
            QtGui.QMessageBox.warning(self, "Directory Doesnt Exist ERROR", "This Directory Doesnt Exist")
            return
        ftp.close()

        try:#Directory exists therefore insert it into the database.
            self.Parent.databaseCursor.execute("INSERT INTO directory VALUES(%s,%s,%s)",((str(serverID[0][0])), str(directoryName), 0))
            self.Parent.cnnct.commit()
        except mysql.connector.Error as e:
            QtGui.QMessageBox.warning(self, "Inserting directory into the database Error", str(e.msg))
            return
        self.Parent.refreshServerList()#call the refresh list function inside the parent to refresh the list of servers/Directories.
        self.close()#close this window.


    @QtCore.pyqtSignature("on_cancel_BT_clicked()")
    def cancelOperation(self):  # Run this function if cancel button is clicked. and close this window.
        self.close()
