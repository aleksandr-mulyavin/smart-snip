import sys

from ui.snipper_app import SnipperApp

# Точка запуска приложения
if __name__ == "__main__":
    app = SnipperApp(sys.argv)
    app.exec_()
