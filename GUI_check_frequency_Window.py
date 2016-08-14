from PyQt4 import QtCore, QtGui

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

class Ui_check_Frequency_Form(QtGui.QWidget):
    def __init__(self, Parent):  # Initialization of the GUI. taking in the Parent in order to use the cursor to the database instead of reconnecting with different cursor.
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.Parent = Parent

    def setupUi(self, check_Frequency_Window):
        check_Frequency_Window.setObjectName(_fromUtf8("check_Frequency_Window"))
        check_Frequency_Window.resize(400, 300)
        self.verticalLayout_3 = QtGui.QVBoxLayout(check_Frequency_Window)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.get_delay_Frame = QtGui.QFrame(check_Frequency_Window)
        self.get_delay_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.get_delay_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.get_delay_Frame.setObjectName(_fromUtf8("get_delay_Frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.get_delay_Frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.check_frequency_TV = QtGui.QLabel(self.get_delay_Frame)
        self.check_frequency_TV.setObjectName(_fromUtf8("check_frequency_TV"))
        self.horizontalLayout_2.addWidget(self.check_frequency_TV)
        self.check_frequency_TE = QtGui.QLineEdit(self.get_delay_Frame)
        self.check_frequency_TE.setObjectName(_fromUtf8("check_frequency_TE"))
        self.horizontalLayout_2.addWidget(self.check_frequency_TE)
        self.verticalLayout_3.addWidget(self.get_delay_Frame)
        self.set_delay_Frame = QtGui.QFrame(check_Frequency_Window)
        self.set_delay_Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.set_delay_Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.set_delay_Frame.setObjectName(_fromUtf8("set_delay_Frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.set_delay_Frame)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.accept_BTN = QtGui.QPushButton(self.set_delay_Frame)
        self.accept_BTN.setObjectName(_fromUtf8("accept_BTN"))
        self.horizontalLayout_3.addWidget(self.accept_BTN)
        self.cancel_BTN = QtGui.QPushButton(self.set_delay_Frame)
        self.cancel_BTN.setObjectName(_fromUtf8("cancel_BTN"))
        self.horizontalLayout_3.addWidget(self.cancel_BTN)
        self.verticalLayout_3.addWidget(self.set_delay_Frame)

        self.retranslateUi(check_Frequency_Window)
        QtCore.QMetaObject.connectSlotsByName(check_Frequency_Window)

    def retranslateUi(self, check_Frequency_Window):
        check_Frequency_Window.setWindowTitle(_translate("check_Frequency_Window", "Form", None))
        self.check_frequency_TV.setText(_translate("check_Frequency_Window", "Check Frequency in Seconds", None))
        self.accept_BTN.setText(_translate("check_Frequency_Window", "Accept", None))
        self.cancel_BTN.setText(_translate("check_Frequency_Window", "Cancel", None))

    @QtCore.pyqtSignature("on_cancel_BTN_clicked()")
    def cancelFrequency(self):
        self.close()#close this window.

    @QtCore.pyqtSignature("on_accept_BTN_clicked()")
    def set_Frequency(self):#sets the frequency of checking
        if(self.Parent.get_configuredDatabase() == True):
            delayValue = self.check_frequency_TE.text()#gets the value from the text editor
            try:
                delayValue = int(delayValue)#tries to convert it into int. if the user enters other values such as strings or !@$#^ it will throw an errror
            except ValueError:
                QtGui.QMessageBox.warning(self, "Please Enter Integer Values", "Please Enter integer Value of the check frequency. the program should check every how many seconds?")
                return
            self.Parent.filechecker.setCheckDelay(delayValue)#set the delay by which the functions checks the DB and FTP. THE DELAY IS IN SECONDS.
            self.close()#close this window.
        else:
            QtGui.QMessageBox.warning(self, "Please Configure Database", "You need to configure your database before setting the Frequency of checking.")