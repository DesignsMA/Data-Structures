from PySide6 import QtWidgets, QtGui, QtCore
import sys


class BlurredOverlay(QtWidgets.QWidget):
    closeRequested = QtCore.Signal()

    def __init__(self, parent=None, msg:str = ""):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(parent.rect())

        # Crea widget desenfocado
        self._blurred_background = QtWidgets.QWidget(self)
        self._blurred_background.setGeometry(self.rect())
        self.closeRequested.connect(self.close)
        blur_effect = QtWidgets.QGraphicsBlurEffect()
        blur_effect.setBlurRadius(8)
        self._blurred_background.setGraphicsEffect(blur_effect)

        # Popup central
        self.popup = QtWidgets.QFrame(self)
        self.popup.setObjectName("popup")
        self.popup.setFixedSize(320, 150)
        self.popup.move(
            self.width() // 2 - self.popup.width() // 2,
            self.height() // 2 - self.popup.height() // 2,
        )

        # Layout y contenido
        layout = QtWidgets.QVBoxLayout(self.popup)
        label = QtWidgets.QLabel(msg)
        label.setObjectName("label")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        close_btn = QtWidgets.QPushButton("Cerrar")
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.closeRequested.emit)
        layout.addWidget(close_btn)