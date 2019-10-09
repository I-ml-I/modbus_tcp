def run():
    from PySide2 import QtWidgets
    from modbus_tcp.modbus_window import Ui_MainWindow

    app = QtWidgets.QApplication()

    # create, populate and show main window
    main_window = QtWidgets.QMainWindow(parent=None)
    Ui_MainWindow().setupUi(main_window)
    main_window.show()

    return app.exec_()
