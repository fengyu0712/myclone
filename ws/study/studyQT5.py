import sys
from PyQt5.QtWidgets import QApplication, QWidget,QLabel,QVBoxLayout,QPushButton

if __name__ == '__main__':
    app = QApplication([])

    w = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QPushButton("top"))
    layout.addWidget(QPushButton("Bottom"))
    w.setLayout(layout)
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    #
    # label = QLabel('Hello World!')
    # label.show()
    sys.exit(app.exec_())