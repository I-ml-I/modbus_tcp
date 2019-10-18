import traceback

def run():
    try:
        from PySide2 import QtWidgets
        from main_window import MainWindow

        app = QtWidgets.QApplication()

        # create, populate and show main window
        main_window = MainWindow()
        main_window.show()
        return app.exec_()
    except:
        traceback.print_exc()

    return 1

if __name__ == "__main__":
    run()