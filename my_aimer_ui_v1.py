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
        self.setMinimumSize(300, 80)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.my_locator = None
        self.temp_slider_locators = None
        self.temp_loc_list = []

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


        #Standard Buttons
        self.build_btn = QtWidgets.QPushButton("Build")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        #Locator Slider Layout
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


        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Selection Chain:", sel_layout)
        form_layout.addRow("Space Selection:", space_layout)
        form_layout.addRow("Axis Selection:", axis_select_layout)
        form_layout.addRow("Locator Distance:", slider_layout)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.build_btn)
        btn_layout.addWidget(self.close_btn)


        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)


    def create_connections(self):
        self.store_sel_btn.clicked.connect(self.get_sel)

        self.world_cb.toggled.connect(self.toggle_manuel_space)
        self.store_space_btn.clicked.connect(self.toggle_world_cb)
        self.store_space_btn.clicked.connect(self.get_space_sel)


        #Locator slider and button
        self.make_loc_btn.clicked.connect(self.get_ui_input)
        self.make_loc_btn.clicked.connect(self.check_sel_exists)
        self.make_loc_btn.clicked.connect(self.make_axis_matrix)
        self.make_loc_btn.clicked.connect(self.make_locators)
        self.slider.valueChanged.connect(self.update_result)
        self.val_line_edit.textChanged.connect(self.update_slider)

        self.build_btn.clicked.connect(self.get_ui_input)
        self.build_btn.clicked.connect(self.check_sel_exists)
        self.build_btn.clicked.connect(self.make_rig)
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

    # def get_axis_sel(self):
    #     self.axis_sel = self.axis_btn_group.checkedButton().text()


    def update_result(self):
        self.slider_val = self.slider.value()
        self.val_line_edit.setText(str(self.slider_val))


    def update_slider(self):
        #Update slider UI
        self.line_edit_value = self.val_line_edit.text()
        self.slider.setValue(int(self.line_edit_value))

        #Run if locator exists
        if self.temp_slider_locators:
            for temp_loc in self.temp_loc_list:
                self.offset_value = [i * self.slider_val for i in self.axis_matrix]
                print ("offset value: {0}".format(self.offset_value))
                mc.xform(temp_loc, objectSpace=1, translation=self.offset_value)
        else:
            pass





    def get_ui_input(self):

        print ("Getting UI Input Now")
        print(self.slider.value())
        print("1111slider.value: {0}".format(self.slider.value()))
        self.chain_ctrls = self.sel_line_edit.text()
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
        print("2222slider.value: {0}".format(self.slider.value()))
        self.slider_val = self.slider.value()


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

        self.slider_val = self.slider.value()
        print("2222slider.value: {0}".format(self.slider.value()))
        self.offset_value = [i * self.slider_val for i in self.axis_matrix]
        print("offset_value: {0}".format(self.offset_value))

        # Get appropriate up vector
        self.up_vector = (0, 0, 1)
        self.world_up_vector = (0, 0, 1)
        print ("axis_matrix: {0}".format(self.axis_matrix))
        if self.axis_matrix in ("z", "-z"):
            self.up_vector = (0, 1, 0)
            self.world_up_vector = (0, 1, 0)

        return self.axis_matrix


    # Slider temp locators
    def make_locators(self):

        # Check if locators already exist
        print ("temp_slider_locators: {0}".format(self.temp_slider_locators))
        print ("temp_loc_list: {0}".format(self.temp_loc_list))
        if self.temp_slider_locators:
            mc.delete(self.temp_loc_list)

        else:
            pass

        self.temp_slider_locators = True

        for ctrl in self.chain_ctrls:
            temp_loc = mc.spaceLocator(n=ctrl + "aim_target")

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

        self.offsetLocList = []
        self.rootLocList = []
        self.targetLocList = []

        self.bakees = []
        tempConstraints = []

        #Delete guide locators
        print("temp_loc_list {0}".format(self.temp_loc_list))
        if self.temp_loc_list:

            mc.delete(self.temp_loc_list)



        self.set_space()

        for obj in self.chain_ctrls:
            # Make the 3 Locators
            offsetLoc = mc.spaceLocator(n=obj + "aim_offset")
            rootLoc = mc.spaceLocator(n=obj + "aim_root")
            targetLoc = mc.spaceLocator(n=obj + "aim_target")

            # Parent them to group (controlled by Hips)
            mc.parent(offsetLoc, rootLoc, targetLoc, self.rooter_grp)

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
        if self.space:
            print ("self.space: {0}".format(self.space))
            self.rooter_grp = mc.group(name="collection_Aim_Loc_Grp", empty=1)
            tempCon = mc.parentConstraint(self.space, self.rooter_grp)
            self.myBake(bakee=self.rooter_grp)
            mc.delete(tempCon)
        else:
            self.rooter_grp = mc.group(name="collection_Aim_Loc_Grp", empty=1)


    def make_aim_constraints(self):

        #Setting the pointCon for rootLocs (to lock ctrls in place), and Aim constraints

        print ("chain_ctrls: {0}". format(self.chain_ctrls))
        print ("rootLocList: {0}". format(self.rootLocList))
        print ("targetLocList: {0}". format(self.targetLocList))
        print ("offsetLocList: {0}". format(self.offsetLocList))

        for i in range(len(self.chain_ctrls)):
            mc.pointConstraint(self.chain_ctrls[i], self.rootLocList[i], mo=0)

            mc.aimConstraint(self.targetLocList[i], self.offsetLocList[i], mo=1, weight=1, aimVector=self.axis_matrix,
                             upVector=self.up_vector, worldUpType="objectrotation",
                             worldUpObject=self.rootLocList[i], worldUpVector=self.world_up_vector)
            print("Or here???")
            mc.orientConstraint(self.offsetLocList[i], self.chain_ctrls[i], mo=0)
            print ("HERE--------")








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
