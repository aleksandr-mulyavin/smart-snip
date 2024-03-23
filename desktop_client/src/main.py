import sys

from .ui import SnipperApp

# Точка запуска приложения
if __name__ == "__main__":
    app = SnipperApp(sys.argv)
    app.exec_()
