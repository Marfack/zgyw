# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from multiprocessing import Queue
from PyQt6 import QtCore, QtGui, QtWidgets
from ui.add_user import Ui_Dialog

class Ui_MainWindow(QtCore.QObject):

    def timerEvent(self, a0):
        if not self.uiq.empty():
            self.refresh(self.uiq.get())

    def setupUi(self, MainWindow: QtWidgets.QMainWindow, uiq: Queue, ptq: Queue):
        self.startTimer(1000)
        self.uiq = uiq
        self.ptq = ptq
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setFixedSize(800, 600)
        qss = ''
        with open('resources/qss/main_window.qss', 'r', encoding='utf8') as f:
            for line in f:
                qss += line
        self.MainWindow.setStyleSheet(qss)
        self.data = dict[str|list[str]]()
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(30, 20, 741, 531))
        self.tableWidget.setMinimumSize(QtCore.QSize(741, 531))
        self.tableWidget.setMouseTracking(False)
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(17)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 180)
        self.tableWidget.setColumnWidth(3, 235)
        # 行
        for i in range(len(self.data)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        # 列
        for i in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
        # 单元格
        for i in range(len(self.data)):
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, j, item)
            item = QtWidgets.QProgressBar()
            self.tableWidget.setCellWidget(i, 3, item)
        self.tableWidget.itemClicked.connect(self.clicked_item)
        self.clicked_item_r = -1
        self.clicked_item_c = -1
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_User = QtGui.QAction(self.MainWindow)
        self.actionAdd_User.setObjectName("actionAdd_User")
        self.actionAdd_User.triggered.connect(self.add_user)
        self.actionDel_User = QtGui.QAction(self.MainWindow)
        self.actionDel_User.setObjectName("actionDel_User")
        self.actionDel_User.triggered.connect(self.del_user)
        self.menuMenu.addAction(self.actionAdd_User)
        self.menuMenu.addAction(self.actionDel_User)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "中国语文挂机控制台"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "账号"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "累计时长"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "进度"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        # 填写单元格内容
        idx = 0
        for k, v in self.data.items():
            self.tableWidget.item(idx, 0).setText(_translate("MainWindow", k))
            self.tableWidget.item(idx, 1).setText(_translate("MainWindow", v[0]))
            self.tableWidget.item(idx, 2).setText(_translate("MainWindow", v[1]))
            try:
                time = int(eval(v[1][:-3]) // 10)
                if time >= 100 and not self.ptq.full():
                    self.ptq.put([0, v[-1], v[1]])
            except:
                QtWidgets.QMessageBox().critical(self.MainWindow, '程序崩溃', '程序由于无法处理的异常而崩溃')
            if time >= 100:
                self.tableWidget.cellWidget(idx, 3).setStyleSheet('QProgressBar::chunk {background-color:rgba(128, 255, 192, 0.5);}')
                self.tableWidget.cellWidget(idx, 3).setValue(100)
            else:
                self.tableWidget.cellWidget(idx, 3).setValue(time)
            idx += 1
        if idx < 17:
            for i in range(idx, 17):
                item = self.tableWidget.item(i, 0)
                if item is None:
                    break
                self.tableWidget.removeRow(i)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.menuMenu.setTitle(_translate("MainWindow", "菜单"))
        self.actionAdd_User.setText(_translate("MainWindow", "添加用户"))
        self.actionDel_User.setText(_translate("MainWindow", "删除用户"))
    
    def add_user(self):
        dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(dialog, self.ptq)
        dialog.exec()

    def del_user(self):
        if self.clicked_item_r >= len(self.data):
            return
        r = QtWidgets.QMessageBox.warning(self.MainWindow, '确认', '确定要删除该用户信息吗？', QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
        if r == QtWidgets.QMessageBox.StandardButton.Yes:
            item = self.tableWidget.item(self.clicked_item_r, 0)
            if item is None:
                QtWidgets.QMessageBox.warning(self.MainWindow, '警告', '所选行数据为空')
                return
            id = item.text()
            self.ptq.put([2, self.data[id][-1]])
            self.data.pop(id)
            if len(self.data) > 17:
                self.tableWidget.setRowCount(len(self.data))
            self.retranslateUi(self.MainWindow)

    def refresh(self, data: list[str]):
        if len(data) < 4:
            QtWidgets.QMessageBox().warning(self.MainWindow, '警告', data[0])
            return
        if data[0] not in self.data:
            idx = len(self.data)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(idx, item)
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(idx, j, item)
            item = QtWidgets.QProgressBar()
            self.tableWidget.setCellWidget(idx, 3, item)
        self.data[data[0]] = data[1:]
        if len(self.data) > 17:
            self.tableWidget.setRowCount(len(self.data))
        self.retranslateUi(self.MainWindow)

    def clicked_item(self, item):
        # if item is None:
        #     return
        self.clicked_item_r = item.row()
        self.clicked_item_c = item.column()