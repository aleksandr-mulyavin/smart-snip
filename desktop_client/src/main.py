import sys

from desktop_client.src.ui import ScannerApp

# Точка запуска приложения
if __name__ == "__main__":
    app = ScannerApp(sys.argv)
    app.exec_()
