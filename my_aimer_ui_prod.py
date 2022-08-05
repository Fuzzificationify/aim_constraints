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


###  Collapsable Stuff ###

class CollapsibleHeader(QtWidgets.QWidget):

    COLLAPSED_PIXMAP = QtGui.QPixmap(":teRightArrow.png")
    EXPANCED_PIXMAP = QtGui.QPixmap(":teDownArrow.png")

    clicked = QtCore.Signal()

    def __init__(self, text, parent=None):
        super(CollapsibleHeader, self).__init__(parent)

        self.setAutoFillBackground(True)
        self.set_background_color(QtCore.Qt.darkCyan)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedWidth(self.COLLAPSED_PIXMAP.width())

        self.text_label = QtWidgets.QLabel()
        self.text_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addWidget(self.text_label)

        self.set_text(text)
        self.set_expanded(False)

    def set_text(self, text):
        self.text_label.setText("<b>{0}</b>".format(text))
        self.text_label.setStyleSheet("QLabel {color: thistle}")

    def set_background_color(self, color):
        if not color:
            color = QtWidgets.QPushButton().palette().color(QtGui.QPalette.Button)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)

    def is_expanded(self):
        return self._expanded

    def set_expanded(self, expanded):
        self._expanded = expanded

        if(self._expanded):
            self.icon_label.setPixmap(self.EXPANCED_PIXMAP)
        else:
            self.icon_label.setPixmap(self.COLLAPSED_PIXMAP)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

class CollapsibleWidget(QtWidgets.QWidget):

    def __init__(self, text, parent=None):
        super(CollapsibleWidget, self).__init__(parent)

        self.header_wdg = CollapsibleHeader(text)
        self.header_wdg.clicked.connect(self.on_header_clicked)

        self.body_wdg = QtWidgets.QWidget()

        self.body_layout = QtWidgets.QVBoxLayout(self.body_wdg)
        self.body_layout.setContentsMargins(4, 2, 4, 2)
        self.body_layout.setSpacing(3)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.header_wdg)
        self.main_layout.addWidget(self.body_wdg)

        self.set_expanded(False)

    def add_widget(self, widget):
        self.body_layout.addWidget(widget)

    def add_layout(self, layout):
        self.body_layout.addLayout(layout)

    def set_expanded(self, expanded):
        self.header_wdg.set_expanded(expanded)
        self.body_wdg.setVisible(expanded)

    def on_header_clicked(self):
        self.set_expanded(not self.header_wdg.is_expanded())
        if self.header_wdg.is_expanded():
            open_slider_dialog.adjustSize()
        else:
            for i in range(10):
                QtCore.QCoreApplication.processEvents()

            open_slider_dialog.resize(open_slider_dialog.minimumSizeHint())


    def set_header_background_color(self, color):
        self.header_wdg.set_background_color(color)


### Collapsable Stuff End ###


class customBut(QtWidgets.QPushButton):

    def __init__(self, text='', parent=None):
        super(customBut, self).__init__(text, parent)

    def mousePressEvent(self, event):

        if (event.button() == QtCore.Qt.MouseButton.LeftButton):
            open_slider_dialog.get_sel()
            open_slider_dialog.make_menus()

        elif (event.button() == QtCore.Qt.MouseButton.RightButton):
            if open_slider_dialog.selection:
                mc.select(open_slider_dialog.selection)


class context_menu(QtWidgets.QWidget):
    def __init__(self, widg, parent=None):
        super(context_menu, self).__init__(parent)

        self.widg = widg
        self.checked_tup_dic = {}

    def conjure_menu(self, selection):
        self.popMenu = QtWidgets.QMenu(self)
        try:
            # Dictionary of actions (which are the Checkboxes in practise) from the Qmenu
            self.menu_actions = {}
            for i, item in enumerate(selection):
                self.menu_actions[i] = (QtWidgets.QAction(item, self, checkable=True))
                self.popMenu.addAction(self.menu_actions[i])
        except:
            pass

    def classy_menu(self):
        # show context menu
        pos = self.widg1.rect().bottomLeft()
        self.popMenu.exec_(self.widg1.mapToGlobal(pos))

        # The [0] is to get the True / False return
        if self.check_if_check(self)[0]:
            self.widg1.setStyleSheet("QRadioButton { font-weight: bold; color: orange }")

            self.check_if_exclusive_check(self)

        else:
            self.widg1.setStyleSheet("QRadioButton { font-weight: ; color:  }")

        # Forces colour resets
        open_slider_dialog.generate_full_checked_list()


    def connect_menu(self, widg1):
        self.widg1 = widg1
        widg1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        widg1.customContextMenuRequested.connect(self.classy_menu)


    def get_inside(self, menu, widg):
        menu_actions = menu.menu_actions

        self.checked_action = []
        self.checked_tups = []

        for i, each in enumerate(menu_actions):
            if menu_actions[i].isChecked():
                self.checked_tup = (widg.text(), menu_actions[i].text())

                self.checked_action.append(widg.text())
                self.checked_tups.append(self.checked_tup)
            else:
                self.checked_tup = None


        return self.checked_tups


    def check_if_check(self, menu):
        # Get the actions (which are the Checkboxes in practise) from the Qmenu
        self.menu_actions = menu.menu_actions
        action_list = []

        self.widg_action_isChecked_list = []
        self.action_QTnodes_list = []

        for i, action in enumerate(self.menu_actions):
            checked = self.menu_actions[i].isChecked()
            action_list.append(checked)

            self.widg_action_isChecked_list.append(checked)
            self.action_QTnodes_list.append(self.menu_actions[i])


        if any(action_list):
            return True, self.widg_action_isChecked_list, self.action_QTnodes_list

        else:
            return False, self.widg_action_isChecked_list, self.action_QTnodes_list

    def check_if_exclusive_check(self, menus):
        # Get active (checked) box from click (active menu)
        for i, action in enumerate(self.widg_action_isChecked_list):
            if action == True:
                active_box = i

        # Finds all the checked boxes
        open_slider_dialog.generate_full_checked_list()

        curated_action_list = []

        # Make list of actions with correct active box (dic key)
        for i in open_slider_dialog.action_QTnodes_dic:
            # dic[i] is for looping, [active_box] is to access item from the list inside
            curated_action_list.append(open_slider_dialog.action_QTnodes_dic[i][active_box])

        # Compare newly made list to "current" (self) Qmenu Actions
        # And remove the current QActions
        for i in curated_action_list:
            if i in self.action_QTnodes_list:
                curated_action_list.remove(i)

        for i, each in enumerate(open_slider_dialog.checked_dic):

            if open_slider_dialog.checked_dic[i][active_box] == True:
                # Uncheck repeated action
                for action in curated_action_list:
                    action.setChecked(False)


    def reset_text_color(self, menu):
        if type(menu) is list:
            for each in menu:
                each.widg1.setStyleSheet("QRadioButton { font-weight: ; color: }")
        else:
            menu.widg1.setStyleSheet("QRadioButton { font-weight: ; color: }")


### Context Menu Stuff End ###
##############################


class OpenSliderDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(OpenSliderDialog, self).__init__(parent)

        self.setWindowTitle("I was born to Slide")
        self.setMinimumSize(340, 200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.selection = None
        self.my_locator = None
        self.temp_slider_locators = None
        self.temp_loc_list = []
        self.aim_rig = None
        self.ctrl_constraints = []
        self.exponent = 0

        # Context menu dictionaries
        self.tup_list = []
        self.checked_dic = {}
        self.action_QTnodes_dic = {}

    def create_widgets(self):
        # Locator Slider
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 50)
        self.slider.setValue(5)

        self.val_line_edit = QtWidgets.QLineEdit()
        self.val_line_edit.setFixedWidth(40)
        self.val_line_edit.setText("5")
        self.val_line_edit.setFont(QtGui.QFont("Sanserif", 10))

        self.make_loc_btn = QtWidgets.QPushButton()

        self.make_loc_btn.setIcon(QtGui.QIcon(":locator.png"))

        # Selection Widgets
        self.sel_line_edit = QtWidgets.QLineEdit()
        self.sel_line_edit.setEnabled(False)
        # self.store_sel_btn = QtWidgets.QPushButton("")
        self.store_sel_btn = customBut(self, "")
        self.store_sel_btn.setIcon(QtGui.QIcon(":selectByObject.png"))

        self.world_cb = QtWidgets.QCheckBox("World")
        self.world_cb.setChecked(True)
        self.space_sel_line_edit = QtWidgets.QLineEdit()
        self.space_sel_line_edit.setEnabled(False)
        self.space_sel_line_edit.setStyleSheet("QLineEdit { color: white; background-color: gray }")
        self.store_space_btn = QtWidgets.QPushButton("")
        self.store_space_btn.setIcon(QtGui.QIcon(":selectByObject.png"))

        # Axis Selection
        self.axis_x_btn = QtWidgets.QRadioButton("x")
        self.axis_y_btn = QtWidgets.QRadioButton("y")
        self.axis_z_btn = QtWidgets.QRadioButton("z")
        self.axis_mx_btn = QtWidgets.QRadioButton("-x")
        self.axis_my_btn = QtWidgets.QRadioButton("-y")
        self.axis_mz_btn = QtWidgets.QRadioButton("-z")

        self.axis_z_btn.setChecked(True)

        self.radio_btn_context_menus_instanes()

        self.axis_btn_group = QtWidgets.QButtonGroup()
        self.axis_btn_group.addButton(self.axis_x_btn)
        self.axis_btn_group.addButton(self.axis_y_btn)
        self.axis_btn_group.addButton(self.axis_z_btn)
        self.axis_btn_group.addButton(self.axis_mx_btn)
        self.axis_btn_group.addButton(self.axis_my_btn)
        self.axis_btn_group.addButton(self.axis_mz_btn)

        self.axis_groupbox = QtWidgets.QGroupBox("")

        # Offset Widgets
        self.offset_label = QtWidgets.QLabel("Anim Offset:")
        self.offset_expo_label = QtWidgets.QLabel("Exponent:")
        self.offset_line_edit = QtWidgets.QLineEdit()
        self.offset_line_edit.setText("1")
        self.offset_line_edit.setFixedWidth(35)

        self.expo_cb = QtWidgets.QCheckBox("")

        self.expo_line_edit = QtWidgets.QLineEdit()
        self.expo_line_edit.setFixedWidth(35)
        self.expo_line_edit.setEnabled(False)
        self.expo_line_edit.setStyleSheet("QLineEdit { background-color: gray }")

        self.include_frist_cb = QtWidgets.QCheckBox("Include 1st control")

        self.offset_btn = QtWidgets.QPushButton("Offset")
        self.offset_btn.setMaximumWidth(80)
        self.offset_btn.setMinimumHeight(25)

        self.undo_offset_btn = QtWidgets.QPushButton("Undo Offset")
        self.undo_offset_btn.setMaximumWidth(70)
        self.undo_offset_btn.setMinimumHeight(25)

        # Bake Widgets
        self.bake_btn = QtWidgets.QPushButton("Bake")
        self.stay_constrained_cb = QtWidgets.QCheckBox("Stay Constrained")
        self.anim_layer_cb = QtWidgets.QCheckBox("To AnimLayer")
        self.timeline_range_cb = QtWidgets.QCheckBox("Use Timeline Range")

        # Collapsible Widget Stuff
        self.collapsible_wdg_offset = CollapsibleWidget("Offset")

        offset_grid_layout = QtWidgets.QGridLayout()
        offset_grid_layout.addWidget(self.offset_label, 0, 0, 2, 1)
        offset_grid_layout.addWidget(self.offset_line_edit, 0, 1, 2, 1)
        offset_grid_layout.addWidget(self.offset_expo_label, 0, 3, 2, 1)
        offset_grid_layout.addWidget(self.expo_cb, 0, 4, 2, 1)
        offset_grid_layout.addWidget(self.expo_line_edit, 0, 5, 2, 1)

        offset_grid_layout.setSpacing(12)
        offset_grid_layout.setColumnStretch(2, 1)
        offset_grid_layout.setColumnStretch(6, 1)

        offset_btns_layout = QtWidgets.QHBoxLayout()
        offset_btns_layout.addStretch()
        offset_btns_layout.addWidget(self.include_frist_cb)
        offset_btns_layout.addWidget(self.offset_btn)
        offset_btns_layout.addWidget(self.undo_offset_btn, alignment=QtCore.Qt.AlignRight)

        offset_v_layout = QtWidgets.QVBoxLayout()
        offset_v_layout.addLayout(offset_grid_layout)
        offset_v_layout.addSpacing(7)
        offset_v_layout.addLayout(offset_btns_layout)
        offset_v_layout.setSpacing(10)

        self.collapsible_wdg_offset.add_layout(offset_v_layout)

        # Collapsible Bake Widget
        self.collapsible_wdg_bake = CollapsibleWidget("Bake")

        bake_h_layout = QtWidgets.QHBoxLayout()
        bake_h_layout.setContentsMargins(40, 1, 1, 1)
        bake_h_layout.addWidget(self.stay_constrained_cb)

        bake_v_layout = QtWidgets.QVBoxLayout()
        bake_v_layout.addLayout(bake_h_layout)
        bake_v_layout.addSpacing(7)
        bake_v_layout.addWidget(self.bake_btn)

        self.collapsible_wdg_bake.add_layout(bake_v_layout)

        self.spheres_cb = QtWidgets.QCheckBox('Distance locking')

        # Standard Buttons
        self.build_btn = QtWidgets.QPushButton("Build")
        self.delete_btn = QtWidgets.QPushButton("Delete")
        self.close_btn = QtWidgets.QPushButton("Close")


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

        self.mirco_layout = QtWidgets.QHBoxLayout()
        self.mirco_layout.addWidget(self.axis_x_btn)
        self.mirco_layout.addWidget(self.axis_y_btn)
        self.mirco_layout.addWidget(self.axis_z_btn)
        self.mirco_layout.addWidget(self.axis_mx_btn)
        self.mirco_layout.addWidget(self.axis_my_btn)
        self.mirco_layout.addWidget(self.axis_mz_btn)

        self.axis_groupbox.setLayout(self.mirco_layout)

        # Offset Layout
        self.offset_body_wdg = QtWidgets.QWidget()
        self.offset_layout = QtWidgets.QVBoxLayout(self.offset_body_wdg)
        self.offset_layout.setContentsMargins(1, 2, 1, 2)
        self.offset_layout.setSpacing(3)
        self.offset_layout.setAlignment(QtCore.Qt.AlignTop)

        self.offset_layout.addWidget(self.collapsible_wdg_offset)

        # Bake Layout
        self.bake_body_wdg = QtWidgets.QWidget()
        self.bake_layout = QtWidgets.QVBoxLayout(self.bake_body_wdg)
        self.bake_layout.setContentsMargins(1, 2, 1, 2)
        self.bake_layout.setSpacing(3)
        self.bake_layout.setAlignment(QtCore.Qt.AlignTop)

        self.bake_layout.addWidget(self.collapsible_wdg_bake)


        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Selection Chain:", sel_layout)
        form_layout.addRow("Space Selection:", space_layout)
        form_layout.addRow("Axis Selection:", axis_select_layout)
        form_layout.addRow("Locator Distance:", slider_layout)

        btn_layout1 = QtWidgets.QHBoxLayout()
        btn_layout1.addStretch()
        btn_layout1.addWidget(self.spheres_cb)
        btn_layout1.addWidget(self.build_btn)
        btn_layout1.addWidget(self.delete_btn)

        btn_layout2 = QtWidgets.QHBoxLayout()
        btn_layout2.addStretch()
        btn_layout2.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(7)
        main_layout.addLayout(btn_layout1)
        main_layout.addWidget(self.offset_body_wdg)
        main_layout.addWidget(self.bake_body_wdg)


    def create_connections(self):
        self.store_sel_btn.clicked.connect(self.get_sel)
        self.store_sel_btn.clicked.connect(self.make_menus)

        self.world_cb.toggled.connect(self.toggle_manuel_space)
        self.store_space_btn.clicked.connect(self.toggle_world_cb)
        self.store_space_btn.clicked.connect(self.get_space_sel)

        # Locator slider and button
        self.make_loc_btn.clicked.connect(self.get_ui_input)
        self.make_loc_btn.clicked.connect(self.check_sel_exists)
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
        self.undo_offset_btn.clicked.connect(self.undo_offset)

        self.bake_btn.clicked.connect(self.bake_all)

        self.close_btn.clicked.connect(self.close)


    def radio_btn_context_menus_instanes(self):
        self.cb_menu = context_menu(self.axis_x_btn)
        self.cb_menu.connect_menu(self.axis_x_btn)

        self.cb2_menu = context_menu(self.axis_y_btn)
        self.cb2_menu.connect_menu(self.axis_y_btn)

        self.cb3_menu = context_menu(self.axis_z_btn)
        self.cb3_menu.connect_menu(self.axis_z_btn)

        self.cb4_menu = context_menu(self.axis_mx_btn)
        self.cb4_menu.connect_menu(self.axis_mx_btn)

        self.cb5_menu = context_menu(self.axis_my_btn)
        self.cb5_menu.connect_menu(self.axis_my_btn)

        self.cb6_menu = context_menu(self.axis_mz_btn)
        self.cb6_menu.connect_menu(self.axis_mz_btn)

        self.cb_widg_list = [self.axis_x_btn, self.axis_y_btn, self.axis_z_btn, self.axis_mx_btn, self.axis_my_btn, self.axis_mz_btn]
        self.cb_menu_list = [self.cb_menu, self.cb2_menu, self.cb3_menu, self.cb4_menu, self.cb5_menu, self.cb6_menu]


    def generate_full_checked_list(self):
        for i, menu in enumerate(self.cb_menu_list):
            any_checked, self.checked_dic[i], self.action_QTnodes_dic[i] = menu.check_if_check(menu)

            if any_checked == False:
                # Reset highlight if there's nothing checked in menu
                menu.reset_text_color(menu)


    def check_sel_exists(self):
        if not self.sel_line_edit.text():
            self.warning = QtWidgets.QMessageBox.warning(self, "Need selection", "Need selection")
        else:
            return

    def get_sel(self):
        self.selection = mc.ls(sl=1)
        self.sel_line_edit.setText(str(self.selection))
        self.sel_line_edit.setStyleSheet("QLineEdit { color: white; background-color: Sienna }")


    def make_menus(self):
        for cb in self.cb_menu_list:
            cb.conjure_menu(self.selection)

        # Reset highlights
        for menu in self.cb_menu_list:
            menu.reset_text_color(menu)


    def get_space_sel(self):
        space_selection = mc.ls(sl=1)[0]
        self.space_sel_line_edit.setText(str(space_selection))
        self.space_sel_line_edit.setStyleSheet("QLineEdit { color: white; background-color: Saddlebrown }")

    def toggle_world_cb(self):
        self.world_cb.setChecked(False)

    def toggle_manuel_space(self):
        if self.world_cb.isChecked():
            self.space = False
            self.space_sel_line_edit.setEnabled(False)
            self.space_sel_line_edit.setStyleSheet("QLineEdit { background-color: gray }")
        else:
            # self.space_sel_line_edit.setEnabled(True)
            self.space_sel_line_edit.setStyleSheet("QLineEdit { color: white; background-color: Saddlebrown }")


    def update_line_edit_from_slider(self):
        # /2 to have finer increment
        self.slider_val = float(self.slider.value())/2
        self.val_line_edit.setText(str(self.slider_val))


    def update_slider_from_line_edit(self):
        # Update slider UI
        self.line_edit_value = self.val_line_edit.text()
        # x2 to counter the halving from slider function
        self.line_edit_float = float(self.line_edit_value)*2

        self.slider.setValue(float(self.line_edit_float))

        # Run if locator exists
        if self.temp_slider_locators:

            for i, ctrl in enumerate(self.chain_ctrls):
                # Find the overrides
                if ctrl in self.chain_ctrl_override:
                    ctrl_index = self.chain_ctrl_override.index(ctrl)
                    ctrl_axis = self.chain_ctrl_axis_override[ctrl_index]

                    self.offset_override_value = [x * self.slider_val for x in ctrl_axis]
                    mc.xform(self.temp_loc_list[i], objectSpace=1, translation=self.offset_override_value)

                else:
                    self.offset_value = [x * self.slider_val for x in self.axis_matrix]
                    mc.xform(self.temp_loc_list[i], objectSpace=1, translation=self.offset_value)

        else:
            pass


    def get_offset_input(self):
        self.offset_multi = float(self.offset_line_edit.text())
        # Converting text unless it's empty
        if self.expo_line_edit.text():
            self.exponent = float(self.expo_line_edit.text())
        self.include_first = self.include_frist_cb.isChecked()


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
        self.chain_ctrls = self.sel_line_edit.text()

        # Remove 'u' if in earlier version of Maya
        if sys.version_info.major >= 3:
            # Convert line edit strings to lists
            self.chain_ctrls = list(map(str.strip, self.chain_ctrls.strip('][').replace("'", '').split(',')))
        else:
            self.chain_ctrls = self.chain_ctrls.strip('][').replace("'", '').split(', ')
            self.chain_ctrls = [x[1:] for x in self.chain_ctrls]

        # If space is False world cb is clicked
        if self.world_cb.isChecked():
            self.space = False
        else:
            self.space = self.space_sel_line_edit.text()
            # self.space = list(map(str.strip, self.space.strip('][').replace('"', '').split(',')))

        self.custom_axis_override()

        # Get slider value
        axis_sel = self.axis_btn_group.checkedButton().text()
        self.make_axis_matrix(axis_sel)


    def make_axis_matrix(self, axis_input):

        self.axis = {
            "x": (1, 0, 0),
            "-x": (-1, 0, 0),
            "y": (0, 1, 0),
            "-y": (0, -1, 0),
            "z": (0, 0, 1),
            "-z": (0, 0, -1),
        }

        self.axis_matrix = self.axis[axis_input]

        self.slider_val = float(self.slider.value())/2

        self.offset_value = [x * self.slider_val for x in self.axis_matrix]

        # Get appropriate up vector
        self.up_vector = (0, 0, 1)
        self.world_up_vector = (0, 0, 1)

        if self.axis_matrix in ("z", "-z"):
            self.up_vector = (0, 1, 0)
            self.world_up_vector = (0, 1, 0)

        return self.axis_matrix

    def custom_axis_override(self):
        tup_list = []
        for i, menu in enumerate(self.cb_menu_list):
            tup = menu.get_inside(self.cb_menu_list[i], self.cb_widg_list[i])
            if tup != []:
                tup_list.append(tup)

        # Remove nested lists
        tup_clean = [val for sublist in tup_list for val in sublist]

        self.chain_ctrl_override = [name[1] for name in tup_clean]
        self.chain_ctrl_key_override = [name[0] for name in tup_clean]

        self.chain_ctrl_axis_override = []
        # GET THE LETTER (X,Y,Z)
        for pair in tup_clean:
            axis = self.make_axis_matrix(pair[0])
            self.chain_ctrl_axis_override.append(axis)

        if self.chain_ctrl_axis_override != []:
            print("chain_ctrl_axis_override ", self.chain_ctrl_axis_override)

    # Slider temp locators
    def make_locators(self):
        # Check if locators already exist

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

        # Set temp loc check to True and reset temp loc list
        self.temp_slider_locators = True
        self.temp_loc_list = []


        for ctrl in self.chain_ctrls:
            temp_loc = mc.spaceLocator(n=ctrl + "temp_aim_target")
            self.temp_loc_list.append(temp_loc[0])

            # Position locators to ctrls
            mc.parent(temp_loc, ctrl)
            mc.makeIdentity(temp_loc, apply=0, t=1, r=1, s=1)

            # Multiply slider value by axis matrix
            if ctrl in self.chain_ctrl_override:
                ctrl_index = self.chain_ctrl_override.index(ctrl)
                ctrl_axis = self.chain_ctrl_axis_override[ctrl_index]

                offset_value = [x * self.slider_val for x in ctrl_axis]
                mc.xform(temp_loc, relative=1, objectSpace=1, translation=offset_value)

            else:
                self.offset_value = [x * self.slider_val for x in self.axis_matrix]
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
            mc.bakeResults(bakee, time=timeSliderRange, preserveOutsideKeys=1)

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
        if self.temp_loc_list:
            try:
                mc.delete(self.temp_loc_list)
            except:
                pass
            self.temp_slider_locators = False

        # Get space info from ui
        self.set_space()

        self.hooked_up_grp = mc.group(name="hooked_up_Aim_Loc_Grp", empty=1)
        mc.setAttr(self.hooked_up_grp + ".visibility", 0)
        mc.parent(self.hooked_up_grp, self.rooter_grp)

        for obj in self.chain_ctrls:
            # Make the 3 Locators
            offsetLoc = mc.spaceLocator(n=obj + "aim_offset")
            rootLoc = mc.spaceLocator(n=obj + "aim_root")
            targetLoc = mc.spaceLocator(n=obj + "aim_target")

            # Make sub group for organisation
            # Parent locs to group (controlled by space input)
            mc.parent(offsetLoc, rootLoc, self.hooked_up_grp)
            mc.parent(targetLoc, self.rooter_grp)

            # Sort target locators into list for later Offsetting
            self.targetLocList.append(targetLoc[0])
            self.offsetLocList.append(offsetLoc[0])
            self.rootLocList.append(rootLoc[0])

            # Build AimConstraint setup
            mc.parent(offsetLoc, rootLoc)

            tempRootCon = mc.parentConstraint(obj, rootLoc, mo=0)

            # Align target locator, then offset it in selected axis
            tempCon = mc.parentConstraint(obj, targetLoc, mo=0)

            if obj in self.chain_ctrl_override:
                ctrl_index = self.chain_ctrl_override.index(obj)
                ctrl_axis = self.chain_ctrl_axis_override[ctrl_index]

                offset_value = [x * self.slider_val for x in ctrl_axis]
                mc.xform(targetLoc, relative=1, objectSpace=1, translation=offset_value)
            else:
                mc.xform(targetLoc, relative=1, objectSpace=1, translation=self.offset_value)
            mc.delete(tempCon)

            tempCon2 = mc.parentConstraint(obj, targetLoc, mo=1)

            self.bakees.append(rootLoc[0])
            self.bakees.append(targetLoc[0])

            tempConstraints.append(tempCon[0])
            tempConstraints.append(tempCon2[0])
            tempConstraints.append(tempRootCon[0])

        # Baking
        self.myBake(self.bakees, space_obj=obj)

        # Deleting, now baked, Root and Target locator's constraints
        mc.delete(tempConstraints)

        # Setting Aim Constraints
        self.make_aim_constraints()

        #Spheres
        if self.spheres_cb.isChecked():
            self.make_spheres()

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
        # Setting the pointCon for rootLocs (to lock ctrls in place), and Aim constraints

        for i in range(len(self.chain_ctrls)):
            mc.pointConstraint(self.chain_ctrls[i], self.rootLocList[i], mo=0)

            if self.chain_ctrls[i] in self.chain_ctrl_override:
                ctrl_index = self.chain_ctrl_override.index(self.chain_ctrls[i])
                ctrl_axis = self.chain_ctrl_axis_override[ctrl_index]

                self.offset_override_value = [x * self.slider_val for x in ctrl_axis]

                mc.aimConstraint(self.targetLocList[i], self.offsetLocList[i], mo=1, weight=1,
                                 aimVector=ctrl_axis,
                                 upVector=self.up_vector, worldUpType="objectrotation",
                                 worldUpObject=self.rootLocList[i], worldUpVector=self.world_up_vector)

            else:
                mc.aimConstraint(self.targetLocList[i], self.offsetLocList[i], mo=1, weight=1, aimVector=self.axis_matrix,
                                 upVector=self.up_vector, worldUpType="objectrotation",
                                 worldUpObject=self.rootLocList[i], worldUpVector=self.world_up_vector)

            self.axis_to_skip_if_locked(self.chain_ctrls[i], self.offsetLocList[i])
            ctrl_con = mc.orientConstraint(self.offsetLocList[i], self.chain_ctrls[i], mo=0)[0]

            self.ctrl_constraints.append(ctrl_con)

        mc.select(clear=True)


    def make_spheres(self):
        #create nurbs Spheres
        self.sphere_grp = mc.group(name="sphere_grp", empty=1)
        mc.parent(self.sphere_grp, self.rooter_grp)
        mc.setAttr(self.sphere_grp + ".visibility", 0)
        mc.reorder(self.sphere_grp, front=1)
        for index, ctrl in enumerate(self.chain_ctrls):
            sphere = mc.sphere(radius=self.slider_val, n=ctrl + "_sphere", ch=0)
            mc.parent(sphere, self.sphere_grp)
            mc.pointConstraint(ctrl, sphere, mo=0)
            mc.geometryConstraint(sphere, self.targetLocList[index])
        mc.select(clear=1)

    def delete_rig_stuff(self):
        # Delete nodes made by script
        try:
            mc.delete(self.rooter_grp)
        except:
            pass
        try:
            mc.delete(self.temp_loc_list)
        except:
            pass

        self.aim_rig = False

    def axis_to_skip_if_locked(self, ctrl, loc):
        xyz_skip_list = []

        for axis in ['.rotateX', '.rotateY', '.rotateZ']:
            its_locked = mc.getAttr(ctrl + axis, lock=1)
            if its_locked:
                xyz_skip_list.append(axis[-1].lower())

        mc.orientConstraint(loc, ctrl, skip=xyz_skip_list, mo=0)

        if xyz_skip_list != []:
            print("Skip List: ", xyz_skip_list)

    def offset_locs(self):
        # make starting i val equal to offset if 'include first' check box is ticked
        if self.include_first == True:
            i = self.offset_multi + (self.offset_multi * self.exponent)
        else:
            i = 0
        for loc in self.targetLocList:
            animCurves = mc.listConnections(loc, t="animCurve")
            mc.keyframe(animCurves, edit=1, relative=1, timeChange=i)

            i = i + self.offset_multi + (self.offset_multi * self.exponent)

    def undo_offset(self):
        # make starting i val equal to offset if 'include first' check box is ticked
        if self.include_first == True:
            i = self.offset_multi + (self.offset_multi * self.exponent)
        else:
            i = 0
        for loc in self.targetLocList:
            animCurves = mc.listConnections(loc, t="animCurve")
            mc.keyframe(animCurves, edit=1, relative=1, timeChange=-i)

            i = i + self.offset_multi + (self.offset_multi * self.exponent)


    #Bakeing
    def bake_all(self):

        sel = self.selection
        animLayer_name = sel[0] + "_base"

        minTime = mc.playbackOptions(q=1, minTime=1)
        maxTime = mc.playbackOptions(q=1, maxTime=1)
        time_range = minTime, maxTime

        # Extract base animation to new layer
        extract_lyr = mc.animLayer(animLayer_name, override=1, addSelectedObjects=1, extractAnimation="BaseAnimation")

        mc.bakeResults(sel, time=time_range, bakeOnOverrideLayer=True, preserveOutsideKeys=True)
        bake_container = mc.ls(sl=1, type="container")[0]

        if mc.animLayer(sel, q=1, affectedLayers=1) and mc.animLayer('BakeResults', q=1, exists=1):
            mc.rename('BakeResults', "AimTail_offset{0}_bk_lyr".format(int(self.offset_multi)))

        # Copy anim back to Base layer and delete
        mc.animLayer('BaseAnimation', e=1, copyAnimation=extract_lyr)
        mc.delete(extract_lyr)

        # Delete Asset Container (made from baking)
        mc.select(bake_container)
        mc.DeleteSelectedContainers()

        if self.stay_constrained_cb.isChecked() == False:
            self.delete_constraints()
            self.delete_rig_stuff()

    def delete_constraints(self):
        mc.delete(self.ctrl_constraints, constraints=True)



if __name__ == "__main__":
    #     open_slider_dialog.close() # pylint: disable=E0601

    try:
        open_slider_dialog.show()
    except:
        open_slider_dialog = OpenSliderDialog()
        open_slider_dialog.show()


# if __name__ == "__main__":
#
#     try:
#         open_slider_dialog.close() # pylint: disable=E0601
#         open_slider_dialog.deleteLater()
#     except:
#         pass
#
#     open_slider_dialog = OpenSliderDialog()
#     open_slider_dialog.show()
