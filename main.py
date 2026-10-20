import sys
from pathlib import Path
from PySide6 import QtCore, QtWidgets, QtGui

class Window(QtWidgets.QWidget):
    def __init__(self):
        flags = (
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool |
            QtCore.Qt.WindowType.WindowDoesNotAcceptFocus
        )

        super().__init__(None, flags)
        
        self.anim = QtCore.QVariantAnimation(self)
        self.anim.valueChanged.connect(self.move)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

        imagePath = Path(__file__).parent / "assets" / "cat.png"
        self.sprite = QtGui.QPixmap(str(imagePath))
        self.sprite = self.sprite.scaled(200, 200)

        if self.sprite.isNull():
            raise FileNotFoundError(f"Could not load pet sprite: {imagePath}")

        self.resize(QtCore.QSize(200, 200))


        # Position above the taskbar on the primary display.
        screen = QtWidgets.QApplication.primaryScreen()
        area = screen.availableGeometry()

        self.move((area.right() - self.width()) / 2, area.bottom() - self.height())

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.sprite)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        startPosition = self.pos()
        endPosition = QtCore.QPoint(startPosition.x(), screen.bottom() - self.height())
        duration = (startPosition.y() - endPosition.y()) * -0.35
        duration = duration if duration > 0 else -duration

        self.anim.setStartValue(startPosition)
        self.anim.setEndValue(endPosition)
        self.anim.setDuration(duration)     # Animation duration
        self.anim.setEasingCurve(QtCore.QEasingCurve.Type.InQuad)
        self.anim.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Window()
    window.show()

    # add to the system tray
    icon = QtGui.QIcon("assets/poop.png")
    tray = QtWidgets.QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # system tray menu actions
    menu = QtWidgets.QMenu()

    quitAction = QtGui.QAction("Quit")
    quitAction.triggered.connect(app.quit)
    menu.addAction(quitAction)

    tray.setContextMenu(menu)

    sys.exit(app.exec())
