def run():
    from PySide2 import QtWidgets
    from modbus_tcp.main_window import MainWindow

    app = QtWidgets.QApplication()

    # create, populate and show main window
    main_window = MainWindow()
    main_window.show()

    return app.exec_()
