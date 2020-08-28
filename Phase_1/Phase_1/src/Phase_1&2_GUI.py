from PyQt5 import QtCore, QtGui, QtWidgets
import operator
from bitstring import BitArray

mnemonic_fmt = {
    'lb':['I', '0000011', '000'],
    'lh':['I', '0000011', '001'],
    'lw':['I', '0000011', '010'],
    'ld':['I', '0000011', '011'],
    'lbu':['I', '0000011', '100'],
    'lhu':['I', '0000011', '101'],
    'lwu':['I', '0000011', '110'],
    'fence':['I', '0001111', '000'],
    'fence.i':['I', '0001111', '001'],
    'addi':['I', '0010011', '000'],
    'slli':['I', '0010011', '001', '0000000'],
    'slti':['I', '0010011', '010'],
    'sltiu':['I', '0010011', '011'],
    'xori':['I', '0010011', '100'],
    'srli':['I', '0010011', '101', '0000000'],
    'srai':['I', '0010011', '101', '0100000'],
    'ori':['I', '0010011', '110'],
    'andi':['I', '0010011', '111'],
    'auipc':['U', '0010111'],
    'addiw':['I', '0011011', '000'],
    'slliw':['I', '0011011', '001', '0000000'],
    'srliw':['I', '0011011', '101', '0000000'],
    'sraiw':['I', '0011011', '101', '0100000'],
    'sb':['S', '0100011', '000'],
    'sh':['S', '0100011', '001'],
    'sw':['S', '0100011', '010'],
    'sd':['I', '0100011', '011'],
    'add':['R', '0110011', '000', '0000000'],
    'sub':['R', '0110011', '000', '0100000'],
    'mul':['R', '0110011', '000', '0000001'],
    'div':['R', '0110011', '100', '0000001'],
    'sll':['R', '0110011', '001', '0000000'],
    'slt':['R', '0110011', '010', '0000000'],
    'sltu':['R', '0110011', '011', '0000000'],
    'xor':['R', '0110011', '100', '0000000'],
    'srl':['R', '0110011', '101', '0000000'],
    'sra':['R', '0110011', '101', '0100000'],
    'or':['R', '0110011', '110', '0000000'],
    'and':['R', '0110011', '111', '0000000'],
    'lui':['U', '0110111'],
    'addw':['R', '0111011', '000', '0000000'],
    'subw':['R', '0111011', '000', '0100000'],
    'sllw':['R', '0111011', '001', '0000000'],
    'srlw':['R', '0111011', '101', '0000000'],
    'sraw':['R', '0111011', '101', '0100000'],
    'beq':['SB', '1100011', '000'],
    'bne':['SB', '1100011', '001', ],
    'blt':['SB', '1100011', '100'],
    'bge':['SB', '1100011', '101'],
    'bltu':['SB', '1100011', '110'],
    'bgeu':['SB', '1100011', '111'],
    'jalr':['I', '1100111', '000'],
    'jal':['UJ', '1101111'],
    'ecall':['I', '1110011', '000', '000000000000'],
    'ebreak':['I', '1110011', '000', '000000000001'],
    'CSRRW':['I', '1110011', '001'],
    'CSRRS':['I', '1110011', '010'],
    'CSRRC':['I', '1110011', '011'],
    'CSRRWI':['I', '1110011', '101'],
    'CSRRSI':['I', '1110011', '110'],
    'CSRRCI':['I', '1110011', '111'],
}

class riscVGui(QtWidgets.QWidget):
    
    def settingWidgets(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit_as = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_as.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_as.setSizePolicy(sizePolicy)
        self.plainTextEdit_as.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.plainTextEdit_as.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit_as.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit_as.setPlainText("")
        self.plainTextEdit_as.setObjectName("plainTextEdit_as")
        self.highlight = self.plainTextEdit_as.document()
        MainWindow.setStyleSheet('''QPlainTextEdit{font-size: 20px;font-weight: 400;}''')
        self.gridLayout.addWidget(self.plainTextEdit_as, 2, 2, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 3, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_2.setContentsMargins(-1, -1, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.step = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step.sizePolicy().hasHeightForWidth())
        self.step.setSizePolicy(sizePolicy)
        self.step.setObjectName("step")
        self.gridLayout_2.addWidget(self.step, 0, 4, 1, 1)
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset.sizePolicy().hasHeightForWidth())
        self.reset.setSizePolicy(sizePolicy)
        self.reset.setObjectName("reset")
        self.gridLayout_2.addWidget(self.reset, 0, 5, 1, 1)
        self.run = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run.sizePolicy().hasHeightForWidth())
        self.run.setSizePolicy(sizePolicy)
        self.run.setObjectName("run")
        self.gridLayout_2.addWidget(self.run, 0, 3, 1, 1)
        self.as_assemble = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.as_assemble.sizePolicy().hasHeightForWidth())
        self.as_assemble.setSizePolicy(sizePolicy)
        self.as_assemble.setObjectName("as_assemble")
        self.gridLayout_2.addWidget(self.as_assemble, 0, 2, 1, 1)
        self.plainTextEdit_console = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_console.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_console.setSizePolicy(sizePolicy)
        self.plainTextEdit_console.setMinimumSize(QtCore.QSize(0, 100))
        self.plainTextEdit_console.setDocumentTitle("")
        self.plainTextEdit_console.setReadOnly(True)
        self.plainTextEdit_console.setPlainText("")
        self.plainTextEdit_console.setObjectName("plainTextEdit_console")
        self.gridLayout_2.addWidget(self.plainTextEdit_console, 1, 0, 2, 6)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 5, 2, 2, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setMidLineWidth(0)
        self.label.setIndent(5)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)
        self.plainTextEdit_mc = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_mc.setObjectName("plainTextEdit_mc")
        self.gridLayout.addWidget(self.plainTextEdit_mc, 2, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 8, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(378, 0))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView_2 = QtWidgets.QTableView(self.tab_2)
        self.tableView_2.setObjectName("tableView_2")
        self.verticalLayout_2.addWidget(self.tableView_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 8, 5, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 17))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_mc = QtWidgets.QAction(MainWindow)
        self.actionSave_mc.setObjectName("actionSave_mc")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuFIle.addAction(self.actionOpen)
        self.menuFIle.addAction(self.actionSave_as)
        self.menuFIle.addAction(self.actionSave_mc)
        self.menuFIle.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionHelp)
        self.menubar.addAction(self.menuFIle.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RISC-V Simulator"))
        self.label_2.setText(_translate("MainWindow", "Machine Code"))
        self.step.setText(_translate("MainWindow", "Step"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.run.setText(_translate("MainWindow", "Run"))
        self.label_3.setText(_translate("MainWindow", "Output"))
        self.label.setText(_translate("MainWindow", "Assembly Code"))
        self.as_assemble.setText(_translate("MainWindow", "Assemble"))
        self.comboBox.setItemText(0, _translate("MainWindow", "HEX"))
        self.comboBox.setItemText(1, _translate("MainWindow", "DECIMAL"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Register"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Memory"))
        self.menuFIle.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave_as.setText(_translate("MainWindow", "Save .asm"))
        self.actionSave_mc.setText(_translate("MainWindow", "Save .mc"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.comboIndex = 0
        self.pc_temp = 0
        self.Execute = execute()
        self.populate()
        self.run.clicked.connect(self.Run)
        self.as_assemble.clicked.connect(self.assemble_as)
        self.reset.clicked.connect(self.assemble_mc)
        self.actionExit.triggered.connect(self.exit)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave_as.triggered.connect(self.saveFile_as)
        self.actionSave_mc.triggered.connect(self.saveFile_mc)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.step.clicked.connect(self.Step)

    def openFile(self, MainWindow):
        dlg = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '',"Assembly files (*.asm)")
        if (dlg[0]!=""):
            f = open(dlg[0], 'r')
            data = f.read()
            print(data)
            self.plainTextEdit_as.setPlainText(data)

    def exit(self):
        sys.exit()

    def saveFile_as(self, MainWindow):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', "", "Assembly files (*.asm)")
        if (name[0]!=""):
            file = open(name[0],'w')
            text = self.plainTextEdit_as.toPlainText()
            file.write(text)
            file.close()

    def saveFile_mc(self, MainWindow):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', "", "Machine Code (*.mc)")
        if (name[0]!=""):
            file = open(name[0],'w')
            text = self.plainTextEdit_mc.toPlainText()
            file.write(text)
            file.close()

    def populate(self):
        regs = self.Execute.returnRegisters()
        reglist = []
        for i in range(len(regs)):
            value = regs['{0:05b}'.format(i)]
            if self.comboIndex == 0:
                b = BitArray(int = value, length=32)
                value = '0x' + b.hex
            reglist.append(["x"+str(i),value])

        if len(reglist)>0:
            table_model = MyTableModel(self, reglist, ["Register",'value'])
            self.tableView.setModel(table_model)
            header = self.tableView.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        mem = self.Execute.returnMemory()
        memlist = []
        for key, value in mem.items():
            if key %4 == 0:
                content = ["0x"+'{:08x}'.format(key),self.Execute.readbyteMemory(key),
                self.Execute.readbyteMemory(key+1),
                self.Execute.readbyteMemory(key+2),
                self.Execute.readbyteMemory(key+3)]
                if self.comboIndex == 0:
                    content = ["0x"+'{:08x}'.format(key),
                        BitArray(int=self.Execute.readbyteMemory(key+3), length = 8).hex,
                        BitArray(int=self.Execute.readbyteMemory(key+2), length = 8).hex,
                        BitArray(int=self.Execute.readbyteMemory(key+1), length = 8).hex,
                        BitArray(int=self.Execute.readbyteMemory(key), length = 8).hex]
                memlist.append(content)

        if len(memlist)>0:
            table_model = MyTableModel(self, memlist, ["Address",'+0','+1','+2','+3'])
            self.tableView_2.setModel(table_model)
            header = self.tableView_2.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        
        self.highlightline(self.Execute.PC/4,True)
    
    def assemble_mc(self):
        self.highlightline(self.pc_temp,False)
        mc_code = self.plainTextEdit_mc.toPlainText()
        self.Execute.assemble(mc_code)
        self.populate()
        self.run.setEnabled(True)
        self.step.setEnabled(True)
        self.plainTextEdit_console.setPlainText("")

    def assemble_as(self):
        try:
            as_code = self.plainTextEdit_as.toPlainText()
            if(as_code!=""):
                mc_code = mc_generator(as_code)
                self.plainTextEdit_mc.setPlainText(mc_code)
                self.Execute.assemble(mc_code)
                self.populate()
                self.run.setEnabled(True)
                self.step.setEnabled(True)
                self.plainTextEdit_console.setPlainText("")
            else:
                self.plainTextEdit_console.setPlainText("Enter valid assembly code")
        except:
            self.plainTextEdit_console.setPlainText("Enter valid assembly code")

    def Run(self):
        try:
            if(self.plainTextEdit_mc.toPlainText()!=""):
                self.Execute.run()
                self.populate()
                self.run.setEnabled(False)
                self.step.setEnabled(False)
                self.plainTextEdit_console.setPlainText("No. of Cycles taken to execute : "+str(self.Execute.cycle))
            else:
                self.plainTextEdit_console.setPlainText("Run the assembler first")
        except:
            self.plainTextEdit_console.setPlainText("Run the assembler first")

    def Step(self):
        try:
            if(self.plainTextEdit_mc.toPlainText()!=""):
                self.highlightline(self.Execute.PC/4,False)
                self.Execute.fetch()
                self.populate()
                self.plainTextEdit_console.setPlainText("")
                if self.Execute.nextIR() == 0:
                    self.run.setEnabled(False)
                    self.step.setEnabled(False)
                    self.plainTextEdit_console.setPlainText("No. of Cycles taken to execute : "+str(self.Execute.cycle))
                
                self.pc_temp = self.Execute.PC/4
            else:
                self.plainTextEdit_console.setPlainText("Run the assembler first")
        except:
            self.plainTextEdit_console.setPlainText("Run the assembler first")

    def on_combobox_changed(self, value):
        self.comboIndex = value
        self.populate()

    def highlightline(self,linino,color):
        fmt = QtGui.QTextCharFormat()
        if color:
            fmt.setBackground(QtCore.Qt.blue)
            fmt.setForeground(QtCore.Qt.white)
        else:
            fmt.setBackground(QtCore.Qt.white)

        block = self.plainTextEdit_mc.document().findBlockByLineNumber(int(linino))
        blockPos = block.position()

        cursor = QtGui.QTextCursor(self.plainTextEdit_mc.document())
        cursor.setPosition(blockPos)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.setCharFormat(fmt)

class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        self.emit(QtWidgets.SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(QtWidgets.SIGNAL("layoutChanged()"))

class execute:
    def __init__(self):
        self.RegisterFile = register()
        self.Memory = memory()
        self.sp=0x7ffffffc
        self.PC = 0
        self.IR = 0

    def assemble(self,mc_code):
        self.RegisterFile.flush()
        self.Memory.flush()
        self.PC = 0
        self.cycle = 0
        self.RegisterFile.writeC("00010", self.sp)
        if (mc_code == None):
            return "fail"
        mc_code = mc_code.splitlines()
        for line in mc_code:
            try:
                address,value = line.split()
                address = int(address,16)
                value = BitArray(hex = value).int
                self.Memory.writeWord(address,value)
            except:
                return "fail"

    def run(self):
        self.printRegisters()
        while self.nextIR() != 0:
            self.fetch()

    def fetch(self): 
        self.cycle += 1
        self.IR = self.nextIR()
        self.IR = BitArray(int = self.IR, length = 32).bin
        print("IR:"+str(self.IR))
        self.PC = self.PC + 4
        self.decode()
    
    def decode(self):
        self.opcode = self.IR[25:32]
        print("opcode:"+self.opcode)
        self.memory_enable = False
        self.write_enable = True
        self.muxY = 0
        self.RZ = 0
        format = self.checkFormat()
        print("format:"+format)
        if format == "r":
            self.decodeR()
        elif format == "iORs":
            self.RS1 = self.IR[12:17]
            print("RS1:"+self.RS1)
            self.RA = self.RegisterFile.readA(self.RS1)
            print("RA:"+str(self.RA))
            self.funct3 = self.IR[17:20]
            print("funct3:"+self.funct3)
            if self.opcode == "0100011" and self.funct3 != "011":
                self.decodeS()
            else:
                self.decodeI()
        elif format == "sb":
            self.decodeSB()
        elif format == "u":
            self.decodeU()
        elif format == "uj":
            self.decodeUJ()
    
    def alu(self,operation):
        print("OP:",operation)
        if operation == "add":
            if self.muxB == 0:
                self.RZ = self.RA + self.RB
            if self.muxB == 1:
                self.RZ = self.RA + self.imm
        elif operation == "mul":
            self.RZ = self.RA * self.RB
        elif operation == "div":
            self.RZ = self.RA // self.RB
        elif operation == "rem":
            self.RZ = self.RA % self.RB
        elif operation == "beq":
            if self.RA == self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "bne":
            if self.RA != self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "bge":
            if self.RA >= self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "blt":
            if self.RA < self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "auipc":
            self.RZ = self.PC - 4 + self.imm
        elif operation == "jal":
            self.PC_temp = self.PC
            self.PC = self.PC - 4 + self.imm 
        elif operation == "jalr":
            self.PC_temp = self.PC
            self.PC = self.RA + self.imm
        elif operation == "slli":
            self.RZ = BitArray(int=self.RA, length=32) << self.imm
            self.RZ = self.RZ.int
        elif operation == "srli":
            self.RZ = BitArray(int=self.RA, length=32) >> self.imm
            self.RZ = self.RZ.int
        elif operation == "srai":
            self.RZ = self.RA >> self.imm
        elif operation == "or":
            if self.muxB == 0:
                self.RZ = self.RA | self.RB
            elif self.muxB == 1:
                self.RZ = self.RA | self.imm
        elif operation == "and":
            if self.muxB == 0:
                self.RZ = self.RA & self.RB
            elif self.muxB == 1:
                self.RZ = self.RA & self.imm
        elif operation == "xor":
            if self.muxB == 0:
                self.RZ = self.RA ^ self.RB
            elif self.muxB == 1:
                self.RZ = self.RA ^ self.imm
        elif operation == "sub":
            self.RZ = self.RA - self.RB
        elif operation == "sll":
            self.RZ = BitArray(int=self.RA, length=32) << self.RB
            self.RZ = self.RZ.int
        elif operation == "srl":
            self.RZ = BitArray(int=self.RA, length=32) >> self.RB
            self.RZ = self.RZ.int
        elif operation == "sra":
            self.RZ = self.RA >> self.RB
        elif operation == "slt":
            if self.muxB == 0:
                self.RZ = 1 if self.RA < self.RB else 0                 #slt
            elif self.muxB == 1:
                self.RZ = 1 if self.RA < self.imm else 0                #slti
        elif operation == "sltu":
            if self.muxB == 0:
                self.RA = BitArray(int = self.RA, length = 32).uint
                self.RB = BitArray(int = self.RB, length = 32).uint
                self.RZ = 1 if self.RA < self.RB else 0                 #sltu
            elif self.muxB == 1:
                self.RA = BitArray(int = self.RA, length = 32).uint
                self.imm = BitArray(int = self.imm, length = 32).uint
                self.RZ = 1 if self.RA < self.imm else 0                #sltiu
            
        self.memAccess()
        
    def memAccess(self):
        if self.memory_enable:
            if self.muxY == 1:
                if self.funct3 == "010":
                    self.data = self.Memory.readWord(self.RZ)   #lw
                elif self.funct3 == "000":
                    self.data = self.Memory.readByte(self.RZ)   #lb
                elif self.funct3 == "001":
                    self.data = self.Memory.readDoubleByte(self.RZ)   #lh
                elif self.funct3 == "100":
                    self.data = self.Memory.readUnsignedByte(self.RZ)   #lbu
                elif self.funct3 == "101":
                    self.data = self.Memory.readUnsignedDoubleByte(self.RZ)     #lhu
            else:    
                if self.funct3 == "010":                        #sw
                    self.Memory.writeWord(self.RZ,self.RM)
                elif self.funct3 == "000":                      #sb
                    self.Memory.writeByte(self.RZ,self.RM)
                elif self.funct3 == "001":                      #sh
                    self.Memory.writeDoubleByte(self.RZ, self.RM)
        #writing in  muxY
        if self.muxY == 0:
            self.RY = self.RZ
        elif self.muxY == 1:
            self.RY = self.data
        elif self.muxY == 2:
            self.RY = self.PC_temp
        self.writeReg()

    def writeReg(self):
        if self.write_enable:
            self.RegisterFile.writeC(self.RD, self.RY)
            print("RY:"+str(self.RY))

    def checkFormat(self):
        iORs = "0000011 0001111 0010011 0011011 0100011 1100111 1110011".split()
        r = "0110011 0111011".split()
        u = "0010111 0110111".split()
        sb = "1100011"
        uj = "1101111"
        for c in r:
            if self.opcode == c:
                return "r"
        for c in u:
            if self.opcode == c:
                return "u"
        if self.opcode == sb:
            return "sb"
        if self.opcode == uj:
            return "uj"
        for c in iORs:
            if self.opcode == c:
                return "iORs"
        return "none"

    def decodeR(self):
        self.RS1 = self.IR[12:17]
        print("RS1:"+self.RS1)
        self.RS2 = self.IR[7:12]
        print("RS2:"+self.RS2)
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        self.RA = self.RegisterFile.readA(self.RS1)
        print("RA:"+str(self.RA))
        self.RB = self.RegisterFile.readB(self.RS2)
        print("RB:"+str(self.RB))
        self.muxB = 0
        self.funct3 = self.IR[17:20]
        self.funct7 = self.IR[0:7]
        self.muxY=0
        if self.funct3 == "000" and self.funct7 == "0000000":
            self.alu("add")                 #add
        elif self.funct3 == "000" and self.funct7 == "0000001":
            self.alu("mul")                 #mul
        elif self.funct3 == "110" and self.funct7 == "0000000":
            self.alu("or")                  #or
        elif self.funct3 == "111" and self.funct7 == "0000000":
            self.alu("and")                 #and
        elif self.funct3 == "100" and self.funct7 == "0000000":
            self.alu("xor")                 #xor
        elif self.funct3 == "000" and self.funct7 == "0100000":
            self.alu("sub")                 #sub
        elif self.funct3 == "001" and self.funct7 == "0000000":
            self.alu("sll")                 #sll
        elif self.funct3 == "010" and self.funct7 == "0000000":
            self.alu("slt")                 #slt
        elif self.funct3 == "011" and self.funct7 == "0000000":
            self.alu("sltu")                #sltu
        elif self.funct3 == "101" and self.funct7 == "0000000":
            self.alu("srl")                 #srl
        elif self.funct3 == "101" and self.funct7 == "0100000":
            self.alu("sra")                 #sra
        elif self.funct3 == "100" and self.funct7 == "0000001":
            self.alu("div")                 #div
        elif self.funct3 == "110" and self.funct7 == "0000001":
            self.alu("rem")                 #rem


    def decodeI(self):
        print("I-format")
        self.imm = BitArray(bin = self.IR[0:12]).int
        print("imm:"+str(self.imm))
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        self.muxB = 1
        if self.opcode == "0010011" and self.funct3 == "000":
            self.muxY = 0
            self.alu("add")                 #addi
        elif self.opcode == "0000011" and (self.funct3 == "010" or self.funct3 == "000" or self.funct3 == "001" or self.funct3 == "100" or self.funct3 == "101"):
            self.muxY = 1
            self.memory_enable = True
            self.alu("add")                 #all load instructions - lb, lh, lw, lbu, lhu
        elif self.opcode == "1100111" and self.funct3 == "000":
            self.muxY = 2
            self.alu("jalr")                #jalr 
        elif self.opcode == "0010011":
            if self.funct3 == "001":
                self.funct7 = self.IR[0:7]
                self.imm = BitArray(bin = self.IR[7:12]).uint
                if self.funct7 == "0000000":
                    self.muxY = 0
                    self.alu("slli")            #slli
            elif self.funct3 == "101":
                self.funct7 = self.IR[0:7]
                self.imm = BitArray(bin = self.IR[7:12]).uint
                if self.funct7 == "0000000":
                    self.muxY = 0
                    self.alu("srli")            #srli
                if self.funct7 == "0100000":
                    self.muxY = 0
                    self.alu("srai")            #srai (arithmetic right shift)
            elif self.funct3 == "010":
                self.muxY = 0
                self.alu("slt")             #slti
            elif self.funct3 == "011":
                self.muxY = 0
                self.alu("sltu")            #sltiu 
            elif self.funct3 == "100":
                self.muxY = 0
                self.alu("xor")             #xori
            elif self.funct3 == "110":
                self.muxY = 0
                self.alu("or")             #ori
            elif self.funct3 == "111":
                self.muxY = 0
                self.alu("and")             #andi
    
    def decodeS(self):
        print("S-format")
        self.RS2 = self.IR[7:12]
        print("RS2:"+self.RS2)
        self.RB = self.RegisterFile.readB(self.RS2)
        print("RB:"+str(self.RB))
        imm1 = self.IR[0:7]
        imm2 = self.IR[20:25]
        self.write_enable = False
        self.imm = BitArray(bin = imm1+imm2).int
        if self.funct3 == "010" or self.funct3 == "000" or self.funct3 == "001":
            self.RM = self.RB
            self.muxB = 1
            self.memory_enable = True
            self.alu("add")                 #sw or sb or sh

    def decodeSB(self):
        self.RS1 = self.IR[12:17]
        print("RS1:"+self.RS1)
        self.RS2 = self.IR[7:12]
        print("RS2:"+self.RS2)
        self.RA = self.RegisterFile.readA(self.RS1)
        print("RA:"+str(self.RA))
        self.RB = self.RegisterFile.readB(self.RS2)
        print("RB:"+str(self.RB))
        self.muxB = 0
        self.funct3 = self.IR[17:20]
        imm1 = self.IR[0]
        imm2 = self.IR[24]
        imm3 = self.IR[1:7]
        imm4 = self.IR[20:24]
        self.write_enable = False
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int
        if self.funct3 == "000":
            print("going to beq")
            self.alu("beq")                 #beq
        elif self.funct3 == "101":
            self.alu("bge")                 #bge
        elif self.funct3 == "100":
            self.alu("blt")                 #blt    
        elif self.funct3 == "001":
            self.alu("bne")                 #bne
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").uint             #for unsigned operations
        print(str(self.imm))
        if self.funct3 == "111":
            self.alu("bge")                 #bgeu
        elif self.funct3 == "110":
            self.alu("blt")                 #bltu

        
    def decodeU(self):
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        imm1 = self.IR[0:20]
        imm2 = "000000000000"
        self.imm = BitArray(bin = imm1 + imm2).int
        if self.opcode == "0110111":
            self.RA = 0
            self.muxB = 1
            self.alu("add")                 #lui
        else:
            self.alu("auipc")               #auipc

    def decodeUJ(self):
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        imm1 = self.IR[0]
        imm2 = self.IR[12:20]
        imm3 = self.IR[11]
        imm4 = self.IR[1:11]
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int
        self.muxY = 2
        self.alu("jal")                     #jal
        

    def printRegisters(self):
        self.RegisterFile.printall()

    def printMemory(self):
        self.Memory.printall()

    def returnRegisters(self):
        return self.RegisterFile.returnAll()

    def returnMemory(self):
        return self.Memory.returnAll()

    def readbyteMemory(self,address):
        return self.Memory.readByte(address)

    def nextIR(self):
        return self.Memory.readWord(self.PC)
    
class memory:
    def __init__(self):
        self.memory = {}
    
    def readWord(self,address):
        b = ""
        for i in range(4):
            if address+i in self.memory:
                b = self.memory[address+i] + b
            else:
                b = "00000000" + b
        return BitArray(bin = b).int

    def readByte(self,address):
        if address in self.memory:
            return BitArray(bin = self.memory[address]).int
        else:
            return 0

    def readDoubleByte(self, address):
        b = ""
        for i in range(2):
            if address+i in self.memory:
                b = self.memory[address+i] + b
            else:
                b = "00000000" + b
        return BitArray(bin = b).int

    def readUnsignedByte(self,address):
        if address in self.memory:
            return BitArray(bin = self.memory[address]).uint
        else:
            return 0

    def readUnsignedDoubleByte(self, address):
        b = ""
        for i in range(2):
            if address+i in self.memory:
                b = self.memory[address+i] + b
            else:
                b = "00000000" + b
        return BitArray(bin = b).uint
    
    def writeWord(self,address,value):
        if address%4 != 0:
            address_to_be_written = address - address%4
            if not address_to_be_written in self.memory:
                self.memory[address_to_be_written] = "00000000"         #for gui purpose
                
        value = BitArray(int = value, length = 32).bin
        b3 = value[0:8]
        b2 = value[8:16]
        b1 = value[16:24]
        b0 = value[24:32]
        self.memory[address] = b0
        self.memory[address+1] = b1
        self.memory[address+2] = b2
        self.memory[address+3] = b3

    def writeByte(self,address,value):
        if address%4 != 0:
            address_to_be_written = address - address%4
            if not address_to_be_written in self.memory:
                self.memory[address_to_be_written] = "00000000"           #for gui purpose

        value = BitArray(int = value, length = 8).bin
        self.memory[address] = value

    def writeDoubleByte(self,address,value):
        if address%4 != 0:
            address_to_be_written = address - address%4
            if not address_to_be_written in self.memory:
                self.memory[address_to_be_written] = "00000000"           #for gui purpose

        value = BitArray(int = value, length = 32).bin
        b1 = value[16:24]
        b0 = value[24:32]
        self.memory[address] = b0
        self.memory[address+1] = b1

    def printall(self):
        print(self.memory)

    def returnAll(self):
        return self.memory

    def flush(self):
        self.memory.clear()

class register:
    def __init__(self):
        self.registers = {}
        for i in range(32):
            self.registers['{0:05b}'.format(i)] = 0
    def readA(self,address):
        return self.registers[address]

    def readB(self,address):
        return self.registers[address]
    
    def writeC(self,address,value):
        if not address=="00000":
            self.registers[address] = value

    def printall(self):
        print(self.registers)

    def returnAll(self):
        return self.registers

    def flush(self):
        for i in range(32):
            self.registers['{0:05b}'.format(i)] = 0

def R_type(words):
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    funct7=mnemonic_fmt[words[0]][3]

    try:
        rd='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rd\' in R_type in ',words)
    try:
        rs1='{0:05b}'.format(int(words[2][1:]))
    except:
        print('problem in getting \'rs1\' in R_type in ',words)
    try:
        rs2='{0:05b}'.format(int(words[3][1:]))
    except:
        print('problem in getting \'rs2\' in R_type in ',words)
    try:
        machine_code=funct7 + rs2 + rs1 + funct3 + rd + opcode
        return machine_code
    except:
        print('problem in generating machine_code in R_type in ',words)

def I_type(words):
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    try:
        rd='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rd\' in I_type in ',words)
    try:
        rs1='{0:05b}'.format(int(words[2][1:]))
    except:
        print('problem in getting \'rd\' in I_type in ',words)
    imm=''

    if(words[3][0:2] == '0x'):
        try:
            imm='{0:012b}'.format(int(words[3][2:], 16))
        except:
            print('problem in getting hexadecimal immediate value in I_type in ',words)

    elif(words[3][0:2] == '0b'):
        try:
            imm='{0:012b}'.format(int(words[3][2:], 2))
        except:
            print('problem in getting binary immediate value in I_type in ',words)

    else:
        try:
            imm=BitArray(int=int(words[3]), length=12).bin
        except:
            print('problem in getting other type of immediate value in I_type in ',words)

    try:
        machine_code = imm + rs1 + funct3 + rd + opcode
        return machine_code
    except:
        print('problem in generating machine code in I_type in ',words)

def S_type(words):
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    try:
        rs2='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rs2\' in S_type in ',words)

    temp_str=''
    # third word should be in the format like 986(x7)
    for i in range(2, len(words)):
        temp_str += words[i]

    offset = temp_str[0:temp_str.find('(')]
    # handling of -ve offset left
    try:
        rs1=int(temp_str[temp_str.find('(')+2:temp_str.find(')')])
        rs1='{0:05b}'.format(rs1)
    except:
        print('problem in getting \'rs1\' in S_type in ',words)

    imm=''
    if(offset[0:2] == '0x'):
        try:
            imm='{0:012b}'.format(int(offset[2:], 16))
        except:
            print('problem in getting hexadecimal immediate value in S_type in ',words)

    elif(offset[0:2] == '0b'):
        try:
            imm='{0:012b}'.format(int(offset[2:], 2))
        except:
            print('problem in getting binary immediate value in S_type in ',words)
        
    else:
        try:
            imm=BitArray(int=int(offset), length=12).bin
        except:
            print('problem in getting other type of immediate value in S_type in ',words)

    try:
        machine_code = imm[0:7] + rs2 + rs1 + funct3 + imm[7:12] + opcode
        return machine_code
    except:
        print('problem in generating machine_code in S_type in ',words)


def SB_type(words, label_offset):
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    try:
        rs1='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rs1\' in SB_type in ',words)

    try:
        rs2='{0:05b}'.format(int(words[2][1:]))
    except:
        print('problem in getting \'rs2\' in SB_type in ',words)

    try:
        imm=BitArray(int=label_offset, length=12).bin
    except:
        print('problem in generating immediate in SB_type in ',words)

    print(label_offset, imm[0] + imm[2:8] + rs2 + rs1 + funct3 + imm[8:12] + imm[1] + opcode)
    try:
        machine_code = imm[0] + imm[2:8] + rs2 + rs1 + funct3 + imm[8:12] + imm[1] + opcode
        return machine_code
    except:
        print('problem in generating machine_code in SB_type in ',words)

def U_type(words):
    opcode=mnemonic_fmt[words[0]][1]
    try:
        rd='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rd\' in U_type in ',words)
    var_address = ''
    
    if(words[2][0:2] == '0x'):
        try:
            var_address='{0:020b}'.format(int(words[2][2:], 16))
        except:
            print('problem in getting hexadecimal var_address in U_type in ',words)

    elif(words[2][0:2] == '0b'):
        try:
            var_address='{0:020b}'.format(int(words[2][2:], 2))
        except:
            print('problem in getting binary var_address in U_type in ',words)
        
    else:
        try:
            var_address=BitArray(int=int(words[2]), length=20).bin
        except:
            print('problem in getting other type of var_address in U_type in ',words)

    try:
        machine_code = var_address + rd + opcode
        return machine_code
    except:
        print('problem in generating machine_code in U_type in ',words)

def UJ_type(words, label_address):
    opcode=mnemonic_fmt[words[0]][1]
    try:
        rd='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rd\' in UJ_type in ',words)

    try:
        label_address=BitArray(int=label_address, length=21).bin
    except:
        print('problem in getting label_address in UJ_type in ',words)
    try:
        machine_code = label_address[0] + label_address[10:20] + label_address[9] + label_address[1:9] + rd + opcode
        return machine_code
    except:
        print('problem in generating machine_code in UJ_type in ',words)
def mc_generator(asm_text=""):
    file_write= open("write_file.mc","w")
    
    return_txt=''
    if asm_text=="":
        file_read = open("read_file.asm","r")
        if file_read.mode=='r':
            asm_code=file_read.read()
        # .data and .text part of the code can come in any order
    else:
        asm_code=asm_text
    dictionary = {}                                                                 #Declaration of a dictionary(to be used later as reference to memory addresses)
    if(asm_code.find('.data') >= 0):
        data = ''
        text = ''
        
        if asm_code.find(".data") < asm_code.find('.text') :
            data = asm_code[asm_code.find(".data")+5:asm_code.find(".text")].strip()
            text = asm_code[asm_code.find('.text')+5:].strip()
        else:
            text = asm_code[asm_code.find('.text')+5:asm_code.find('.data')].strip()
            data = asm_code[asm_code.find('.data')+5:].strip()

        #Handling of data part of code starts here
        instructions = data.split('\n')
        data_address = int("0x10000000", 16)
        for i in range(len(instructions)):
            if(instructions[i]==''):                                                    #removal of '\n's
                del instructions[i]
            else:
                dictionary[instructions[i][:instructions[i].find(':')].strip()] = hex(data_address)
                if instructions[i].find('.word')>=0:
                    for word in (instructions[i][instructions[i].find('.word'):].strip()).split():
                        try:
                            #return_txt+=str(hex(data_address))+' '+str(hex(int(word)))+'\n'
                            return_txt+=str(hex(data_address))+' 0x' + BitArray(int=int(word), length=32).hex + '\n'
                            data_address=data_address+4
                        except: pass
                if instructions[i].find('.byte')>=0:
                    for byte in (instructions[i][instructions[i].find('.byte'):].strip()).split():
                        try:
                            #return_txt+=str(hex(data_address))+' '+str(hex(int(byte)))+'\n'
                            return_txt+=str(hex(data_address))+' 0x' + BitArray(int=int(byte), length=32).hex + '\n'
                            data_address=data_address+1
                        except: pass
                #file_write.write(hex(data_address)+' \n')
        print("Instructions", instructions)
        print("Dictionary", dictionary)

        # Handling of data part ends here
        #registers = {'x0':0, 'x1':0, 'x2':2147483632, 'x3':268435456, 'x4':0, 'x5':0, 'x6':0, 'x7':0, 'x8':0, 'x9':0, 'x10':0, 'x11':0, 'x12':0, 'x13':0, 'x14':0, 'x15':0, 'x16':0, 'x17':0, 'x18':0, 'x19':0, 'x20':0, 'x21':0, 'x22':0, 'x23':0, 'x24':0, 'x25':0, 'x26':0, 'x27':0, 'x28':0, 'x29':0, 'x30':0, 'x31':0}
        #print(len(registers))
        #print(registers)
    if(asm_code.find('.data') == -1):
        text=asm_code
    instructions = list(filter(bool, text.splitlines()))
    # Assuming there is no extra '\n' in the text part of the code
    n=len(instructions)
    i=0
    
    label_position={}
    while(i<n):
        instructions[i]=instructions[i].strip()
        a=instructions[i].find('#')
        if(a==0):
            del instructions[i]
            n=n-1
            continue
        elif(a>0):
            instructions[i]=instructions[i][0:a]

        k=instructions[i].find(':')
        if (k > 0):
            instructions[i]=instructions[i].strip()
            label=instructions[i][:k]
            label_position[label]=i
            if(len(instructions[i][k+1:]) > 0):
                instructions[i]=instructions[i][k+1:]
            else:
                del instructions[i]
                i=i-1
                n=n-1
            print(instructions[i-1], instructions[i])
        i=i+1

    pc=0
    print(label_position)

    for i in range(0, n):
        instructions[i]=instructions[i].replace(',', ' ')
        words=instructions[i].split()

        if(mnemonic_fmt[words[0]][0] == 'R'):
            return_txt+=hex(pc)+' '
            return_txt+='0x' + '{0:08x}'.format(int(R_type(words), 2)) + '\n'
        elif(mnemonic_fmt[words[0]][0] == 'I'):
            return_txt+=hex(pc)+' '
            if(words[0] == 'lb' or words[0] == 'lw' or words[0] == 'jalr'):
                if words[2] in dictionary:
                    words_extra=['auipc',words[1],'0b00010000000000000000']
                    return_txt+='0x' + '{0:08x}'.format(int(U_type(words_extra), 2)) + '\n'
                    new_offset=BitArray(int=int(dictionary[words[2]], 16)-int('0x10000000', 16)-pc, length=12).bin
                    words[2]=words[1]
                    words.append('0b'+new_offset)
                    pc=pc+4
                    return_txt+=hex(pc)+' '
                    return_txt+='0x' + '{0:08x}'.format(int(I_type(words), 2)) + '\n'
                else:
                    temp_str=''
                    # third word should be in the format like 986(x7)
                    for i in range(2, len(words)):
                        temp_str += words[i]
                    offset = temp_str[0:temp_str.find('(')]
                    # handling of -ve offset left
                    rs2=temp_str[(temp_str.find('(')+1):temp_str.find(')')]
                    words=[words[0],words[1],rs2,offset]
                    return_txt+='0x' + '{0:08x}'.format(int(I_type(words), 2))+'\n'
            else:
                return_txt+='0x' + '{0:08x}'.format(int(I_type(words), 2))+'\n'
        elif(mnemonic_fmt[words[0]][0] == 'S'):
            return_txt+=hex(pc)+' '
            return_txt+='0x' + '{0:08x}'.format(int(S_type(words), 2))+'\n'
        elif(mnemonic_fmt[words[0]][0] == 'SB'):
            var=int(((label_position[words[3]])*4-pc)/2)
            print('var   ', words[3], var)
            return_txt+=hex(pc)+' '+'0x' + '{0:08x}'.format(int(SB_type(words, var), 2))+'\n'
        elif(mnemonic_fmt[words[0]][0] == 'U'):
            return_txt+=hex(pc)+' '+'0x' + '{0:08x}'.format(int(U_type(words), 2))+'\n'
        elif(mnemonic_fmt[words[0]][0] == 'UJ'):
            temp_var=(label_position[words[2]])*4-pc
            return_txt+=hex(pc)+' '+'0x' + '{0:08x}'.format(int(UJ_type(words, temp_var), 2))+'\n'
        pc=pc+4
    file_write.write(return_txt)
    if(asm_text==''):
        file_write.write(return_txt)
    else:
        return return_txt


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = riscVGui()
    ui.settingWidgets(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
