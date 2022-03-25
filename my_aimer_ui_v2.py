import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from PySide2 import QtGui

import maya.OpenMayaUI as omui
import maya.cmds as mc


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class OpenSliderDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(OpenSliderDialog, self).__init__(parent)

        self.setWindowTitle("I was born to Slide")
        self.setMinimumSize(340, 200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.my_locator = None
        self.temp_slider_locators = None
        self.temp_loc_list = []
        self.aim_rig = None

    def create_widgets(self):
        #Locator Slider
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 50)
        self.slider.setValue(5)
        print(self.slider.value())

        self.val_line_edit = QtWidgets.QLineEdit()
        self.val_line_edit.setFixedWidth(40)
        self.val_line_edit.setText("5")
        self.val_line_edit.setFont(QtGui.QFont("Sanserif", 10))

        self.make_loc_btn = QtWidgets.QPushButton()
        self.make_loc_btn.setIcon(QtGui.QIcon(":locator.png"))


        #Selection Widgets
        self.sel_line_edit = QtWidgets.QLineEdit()
        self.store_sel_btn = QtWidgets.QPushButton("")
        self.store_sel_btn.setIcon(QtGui.QIcon(":selectByObject.png"))

        self.world_cb = QtWidgets.QCheckBox("World")
        self.world_cb.setChecked(True)
        self.space_sel_line_edit = QtWidgets.QLineEdit()
        self.space_sel_line_edit.setStyleSheet("QLineEdit { background-color: gray }")
        self.store_space_btn = QtWidgets.QPushButton("")
        self.store_space_btn.setIcon(QtGui.QIcon(":selectByObject.png"))

        #Axis Selection
        self.axis_x_btn = QtWidgets.QRadioButton("x")
        self.axis_y_btn = QtWidgets.QRadioButton("y")
        self.axis_z_btn = QtWidgets.QRadioButton("z")
        self.axis_mx_btn = QtWidgets.QRadioButton("-x")
        self.axis_my_btn = QtWidgets.QRadioButton("-y")
        self.axis_mz_btn = QtWidgets.QRadioButton("-z")

        self.axis_z_btn.setChecked(True)

        self.axis_btn_group = QtWidgets.QButtonGroup()
        self.axis_btn_group.addButton(self.axis_x_btn)
        self.axis_btn_group.addButton(self.axis_y_btn)
        self.axis_btn_group.addButton(self.axis_z_btn)
        self.axis_btn_group.addButton(self.axis_mx_btn)
        self.axis_btn_group.addButton(self.axis_my_btn)
        self.axis_btn_group.addButton(self.axis_mz_btn)

        self.axis_groupbox = QtWidgets.QGroupBox("")

        # Offset Widgets
        self.offset_label = QtWidgets.QLabel("Exponent:")
        self.offset_cb = QtWidgets.QCheckBox("")
        self.offset_line_edit = QtWidgets.QLineEdit()
        self.offset_line_edit.setText("1")
        self.offset_line_edit.setFixedWidth(35)

        self.expo_cb = QtWidgets.QCheckBox("")

        self.expo_line_edit = QtWidgets.QLineEdit()
        self.expo_line_edit.setFixedWidth(35)
        self.expo_line_edit.setEnabled(False)
        self.expo_line_edit.setStyleSheet("QLineEdit { background-color: gray }")


        #Standard Buttons
        self.build_btn = QtWidgets.QPushButton("Build")
        self.delete_btn = QtWidgets.QPushButton("Delete")
        self.offset_btn = QtWidgets.QPushButton("Offset")
        self.close_btn = QtWidgets.QPushButton("Close")

        # Seperator line
        self.sep_line = QtWidgets.QFrame()
        self.sep_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.sep_line.setLineWidth(2)


    def create_layout(self):
        # Locator Slider Layout
        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.addWidget(self.val_line_edit)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.make_loc_btn)

        # Selection Chain Layout
        sel_layout = QtWidgets.QHBoxLayout()
        sel_layout.addWidget(self.sel_line_edit)
        sel_layout.addWidget(self.store_sel_btn)

        # Selection Space Layout
        space_layout = QtWidgets.QHBoxLayout()
        space_layout.addWidget(self.world_cb)
        space_layout.addWidget(self.space_sel_line_edit)
        space_layout.addWidget(self.store_space_btn)

        # Axis Select Layout
        axis_select_layout = QtWidgets.QHBoxLayout()
        axis_select_layout.addWidget(self.axis_groupbox)

        mirco_layout = QtWidgets.QHBoxLayout()
        mirco_layout.addWidget(self.axis_x_btn)
        mirco_layout.addWidget(self.axis_y_btn)
        mirco_layout.addWidget(self.axis_z_btn)
        mirco_layout.addWidget(self.axis_mx_btn)
        mirco_layout.addWidget(self.axis_my_btn)
        mirco_layout.addWidget(self.axis_mz_btn)

        self.axis_groupbox.setLayout(mirco_layout)

        # Offset Layout
        offset_layout = QtWidgets.QGridLayout()


        offset_layout.addWidget(self.offset_cb, 0, 0, 2, 1)
        offset_layout.addWidget(self.offset_line_edit, 0, 1, 2, 1)
        offset_layout.addWidget(self.offset_label, 0, 3, 2, 1)
        offset_layout.addWidget(self.expo_cb, 0, 4, 2, 1)
        offset_layout.addWidget(self.expo_line_edit, 0, 5, 2, 1)

        offset_layout.setColumnStretch(2, 1)
        offset_layout.setColumnStretch(6, 1)
        #offset_layout.setSpacing(0)
        #offset_layout.setContentsMargins(0, 0, 0, 0)


        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Selection Chain:", sel_layout)
        form_layout.addRow("Space Selection:", space_layout)
        form_layout.addRow("Axis Selection:", axis_select_layout)
        form_layout.addRow("Locator Distance:", slider_layout)



        btn_layout1 = QtWidgets.QHBoxLayout()
        btn_layout1.addStretch()
        btn_layout1.addWidget(self.build_btn)
        btn_layout1.addWidget(self.delete_btn)


        seperator_layout = QtWidgets.QHBoxLayout()
        seperator_layout.addWidget(self.sep_line)
        seperator_layout.setMargin(15)

        form_layout2 = QtWidgets.QFormLayout()
        form_layout2.addRow("Anim Offset:", offset_layout)


        btn_layout2 = QtWidgets.QHBoxLayout()
        btn_layout2.addStretch()
        btn_layout2.addWidget(self.offset_btn)
        btn_layout2.addWidget(self.close_btn)


        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(7)
        main_layout.addLayout(btn_layout1)
        main_layout.addLayout(seperator_layout)
        main_layout.addLayout(form_layout2)
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout2)



    def create_connections(self):
        self.store_sel_btn.clicked.connect(self.get_sel)

        self.world_cb.toggled.connect(self.toggle_manuel_space)
        self.store_space_btn.clicked.connect(self.toggle_world_cb)
        self.store_space_btn.clicked.connect(self.get_space_sel)


        # Locator slider and button
        self.make_loc_btn.clicked.connect(self.get_ui_input)
        self.make_loc_btn.clicked.connect(self.check_sel_exists)
        self.make_loc_btn.clicked.connect(self.make_axis_matrix)
        self.make_loc_btn.clicked.connect(self.make_locators)
        # Slider
        self.slider.valueChanged.connect(self.update_line_edit_from_slider)
        self.val_line_edit.textChanged.connect(self.update_slider_from_line_edit)


        self.build_btn.clicked.connect(self.get_ui_input)
        self.build_btn.clicked.connect(self.check_sel_exists)
        self.build_btn.clicked.connect(self.make_rig)
        self.delete_btn.clicked.connect(self.delete_rig_stuff)

        self.expo_cb.toggled.connect(self.update_expo_cb)
        self.offset_btn.clicked.connect(self.get_offset_input)
        self.offset_btn.clicked.connect(self.offset_locs)
        self.close_btn.clicked.connect(self.close)

    def check_sel_exists(self):
        if not self.sel_line_edit.text():
            self.warning = QtWidgets.QMessageBox.warning(self, "Need selection", "Need selection")
        else:
            return

    def get_sel(self):
        selection = mc.ls(sl=1)
        self.sel_line_edit.setText(str(selection))
        self.sel_line_edit.setStyleSheet("QLineEdit { background-color: Sienna }")

    def get_space_sel(self):
        space_selection = mc.ls(sl=1)[0]
        self.space_sel_line_edit.setText(str(space_selection))
        self.space_sel_line_edit.setStyleSheet("QLineEdit { background-color: Saddlebrown }")

    def toggle_world_cb(self):
        self.world_cb.setChecked(False)

    def toggle_manuel_space(self):
        if self.world_cb.isChecked():
            self.space = False
            self.space_sel_line_edit.setEnabled(False)
            self.space_sel_line_edit.setStyleSheet("QLineEdit { background-color: gray }")
        else:
            self.space_sel_line_edit.setEnabled(True)
            self.space_sel_line_edit.setStyleSheet("")



    def update_line_edit_from_slider(self):
        # /2 to have finer increment
        self.slider_val = float(self.slider.value())/2
        self.val_line_edit.setText(str(self.slider_val))


    def update_slider_from_line_edit(self):
        #Update slider UI
        self.line_edit_value = self.val_line_edit.text()
        # x2 to counter the halving from slider function
        self.line_edit_float = float(self.line_edit_value)*2

        self.slider.setValue(float(self.line_edit_float))

        #Run if locator exists
        if self.temp_slider_locators:
            for temp_loc in self.temp_loc_list:
                self.offset_value = [i * self.slider_val for i in self.axis_matrix]
                mc.xform(temp_loc, objectSpace=1, translation=self.offset_value)

        else:
            pass


    def get_offset_input(self):
        self.offset_multi = float(self.offset_line_edit.text())
        self.exponent = float(self.expo_line_edit.text())

    def update_expo_cb(self):
        print ("update_expo stuff:")
        if self.expo_cb.isChecked():
            self.expo_line_edit.setEnabled(True)
            self.expo_line_edit.setText("0.1")
            self.expo_line_edit.setStyleSheet("")
        else:
            self.exponent = 0
            self.expo_line_edit.setEnabled(False)
            self.expo_line_edit.setStyleSheet("QLineEdit { background-color: gray }")


    def get_ui_input(self):

        print ("Getting UI Input Now")

        self.chain_ctrls = self.sel_line_edit.text()
        print("chain_ctrls: {0}".format(self.chain_ctrls))
        # Convert line edit strings to lists
        self.chain_ctrls = list(map(str.strip, self.chain_ctrls.strip('][').replace("'", '').split(',')))

        # If space is False world cb is clicked

        if self.world_cb.isChecked():
            self.space = False
        else:
            self.space = self.space_sel_line_edit.text()
            self.space = list(map(str.strip, self.space.strip('][').replace('"', '').split(',')))


        # Get slider value
        self.make_axis_matrix()


    def make_axis_matrix(self):

        self.axis = {
            "x": (1, 0, 0),
            "-x": (-1, 0, 0),
            "y": (0, 1, 0),
            "-y": (0, -1, 0),
            "z": (0, 0, 1),
            "-z": (0, 0, -1),
        }

        self.axis_sel = self.axis_btn_group.checkedButton().text()
        self.axis_matrix = self.axis[self.axis_sel]

        self.slider_val = float(self.slider.value())/2

        self.offset_value = [i * self.slider_val for i in self.axis_matrix]

        # Get appropriate up vector
        self.up_vector = (0, 0, 1)
        self.world_up_vector = (0, 0, 1)

        if self.axis_matrix in ("z", "-z"):
            self.up_vector = (0, 1, 0)
            self.world_up_vector = (0, 1, 0)

        return self.axis_matrix


    # Slider temp locators
    def make_locators(self):

        # Check if locators already exist
        print ("temp_slider_locators: {0}".format(self.temp_slider_locators))
        print ("temp_loc_list out here: {0}".format(self.temp_loc_list))

        # Check if build rig has been run
        if self.aim_rig:
            return

        # Check for selection in line edit
        if not self.sel_line_edit.text():
            return

        # Delete temp locators if they exist
        if self.temp_slider_locators:
            try:
                mc.delete(self.temp_loc_list)
            except:
                pass

        # set temp loc check to True and reset temp loc list
        self.temp_slider_locators = True
        self.temp_loc_list = []


        for ctrl in self.chain_ctrls:
            temp_loc = mc.spaceLocator(n=ctrl + "temp_aim_target")

            self.temp_loc_list.append(temp_loc[0])

            # Position locators to ctrls
            mc.parent(temp_loc, ctrl)
            mc.xform(temp_loc, t=(0, 0, 0))

            # Multiply slider value by axis matrix
            self.offset_value = [i * self.slider_val for i in self.axis_matrix]
            mc.xform(temp_loc, relative=1, objectSpace=1, translation=self.offset_value)


##################################################################################
############################# Building Rig Stuff #################################
##################################################################################

    def check_if_rig_exists(self):
        if mc.objExists('collection_Aim_Loc_Grp'):
            mc.delete('collection_Aim_Loc_Grp')
        else:
            pass

    def myBake(self, bakee, space_obj=None):
        minTime = mc.playbackOptions(q=1, minTime=1)
        maxTime = mc.playbackOptions(q=1, maxTime=1)

        timeSliderRange = minTime, maxTime

        # Find first and last keys
        try:
            # Use existing Key Range for Bake
            # fullKeyList = sorted(mc.keyframe(space_obj, q=1))
            # firstLastKeys = fullKeyList[0], fullKeyList[-1]
            print ("RUNNING BAKE")
            mc.bakeResults(bakee, time=timeSliderRange, preserveOutsideKeys=1)

            print ("bakees: {0}".format(bakee))

        except:
            print("No keys?")
            pass


    def make_rig(self):
        print("make_rig is now")
        self.check_if_rig_exists()
        self.aim_rig = True

        self.offsetLocList = []
        self.rootLocList = []
        self.targetLocList = []

        self.bakees = []
        tempConstraints = []

        # Delete guide locators
        print("temp_loc_list {0}".format(self.temp_loc_list))
        if self.temp_loc_list:
            try:
                mc.delete(self.temp_loc_list)
            except:
                pass
            self.temp_slider_locators = False

        # Get space info from ui
        self.set_space()

        self.hooked_up_grp = mc.group(name="hooked_up_Aim_Loc_Grp", empty=1)

        for obj in self.chain_ctrls:
            # Make the 3 Locators
            offsetLoc = mc.spaceLocator(n=obj + "aim_offset")
            rootLoc = mc.spaceLocator(n=obj + "aim_root")
            targetLoc = mc.spaceLocator(n=obj + "aim_target")

            # Make sub group for organisation
            # Parent locs to group (controlled by space input)
            mc.parent(offsetLoc, rootLoc, self.hooked_up_grp)
            mc.parent(self.hooked_up_grp, targetLoc, self.rooter_grp)


            # Sort target locators into list for later Offsetting
            self.targetLocList.append(targetLoc[0])
            self.offsetLocList.append(offsetLoc[0])
            self.rootLocList.append(rootLoc[0])


            # Build AimConstraint setup
            mc.parent(offsetLoc, rootLoc)

            tempRootCon = mc.parentConstraint(obj, rootLoc, mo=0)

            # Align target locator, then offset it in selected axis
            tempCon = mc.parentConstraint(obj, targetLoc, mo=0)
            mc.xform(targetLoc, relative=1, objectSpace=1, translation=self.offset_value)
            mc.delete(tempCon)

            tempCon2 = mc.parentConstraint(obj, targetLoc, mo=1)

            self.bakees.append(rootLoc[0])
            self.bakees.append(targetLoc[0])

            tempConstraints.append(tempCon[0])
            tempConstraints.append(tempCon2[0])
            tempConstraints.append(tempRootCon[0])

        # Baking
        print("Baking from make_rig")
        self.myBake(self.bakees, space_obj=obj)

        # Deleting, now baked, Root and Target locator's constraints
        mc.delete(tempConstraints)

        # Setting Aim Constraints
        self.make_aim_constraints()

    def set_space(self):
        # Check if world space, make constraint and bake if not
        self.rooter_grp = mc.group(name="collection_Aim_Loc_Grp", empty=1)

        if self.space:
            print ("self.space: {0}".format(self.space))

            tempCon = mc.parentConstraint(self.space, self.rooter_grp)
            self.myBake(bakee=self.rooter_grp)
            mc.delete(tempCon)
        else:
            pass


    def make_aim_constraints(self):

        #Setting the pointCon for rootLocs (to lock ctrls in place), and Aim constraints

        print ("chain_ctrls: {0}". format(self.chain_ctrls))
        print ("rootLocList: {0}". format(self.rootLocList))
        print ("targetLocList: {0}". format(self.targetLocList))
        print ("offsetLocList: {0}". format(self.offsetLocList))

        for i in range(len(self.chain_ctrls)):
            #mc.pointConstraint(self.chain_ctrls[i], self.rootLocList[i], mo=0)

            mc.aimConstraint(self.targetLocList[i], self.offsetLocList[i], mo=1, weight=1, aimVector=self.axis_matrix,
                             upVector=self.up_vector, worldUpType="objectrotation",
                             worldUpObject=self.rootLocList[i], worldUpVector=self.world_up_vector)

            mc.orientConstraint(self.offsetLocList[i], self.chain_ctrls[i], mo=0)

        mc.select(clear=True)


    def delete_rig_stuff(self):

        # Delete nodes made by script

        try:
            mc.delete(self.rooter_grp)
        except:
            pass
        try:
            print ("temp_sliders: {0}".format(self.temp_loc_list))
            mc.delete(self.temp_loc_list)
        except:
            pass

        self.aim_rig = False

    def axis_to_skip_if_locked(self):

        sel, tar = mc.ls(sl=1)

        xyz_skip_list = []

        for axis in ['.rotateX', '.rotateY', '.rotateZ']:
            its_locked = mc.getAttr(tar + axis, lock=1)
            if its_locked:
                xyz_skip_list.append(axis[-1].lower())

        mc.orientConstraint(sel, tar, skip=xyz_skip_list)

    def offset_locs(self):
        i = 0
        for loc in self.targetLocList:
            animCurves = mc.listConnections(loc, t="animCurve")
            mc.keyframe(animCurves, edit=1, relative=1, timeChange=i)

            i = i + self.offset_multi + (self.offset_multi * self.exponent)


        # # Baking
            # myBake(obj, bakees)
            #
            # # Deleting, now baked, Root and Target locator's constraints
            # mc.delete(tempConstraints)
            #
            # # Setting the pointCon for rootLocs (to lock ctrls in place), and Aim constraints
            # for i in range(len(self.chain_ctrls)):
            #     mc.pointConstraint(self.chain_ctrls[i], rootLocList[i], mo=0)
            #
            #     mc.aimConstraint(targetLocList[i], offsetLocList[i], mo=1, weight=1, aimVector=axis[axisSel],
            #                      upVector=getAxis.upVec, worldUpType="objectrotation",
            #                      worldUpObject=rootLocList[i], worldUpVector=getAxis.worldUpVec)
            #
            #     mc.orientConstraint(offsetLocList[i], self.chain_ctrls[i], mo=0)
            #
            # # Clean usless keys on Target locators
            # mc.cutKey(targetLocList, clear=1, attribute=["rotateX", "rotateY", "rotateZ",
            #                                              "translate{0}".format(axisSel[1])],
            #           time=(None, None), option="keys")
            # # Lock unused translate axis
            # for loc in targetLocList:
            #     mc.setAttr("{0}.translate{1}".format(loc, axisSel[1]), lock=True)





if __name__ == "__main__":

    try:
        open_slider_dialog.close() # pylint: disable=E0601
        open_slider_dialog.deleteLater()
    except:
        pass

    open_slider_dialog = OpenSliderDialog()
    open_slider_dialog.show()
