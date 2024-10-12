import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

class QuizGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel('Bir tuşa basın...', self)
        self.label.setGeometry(100, 100, 200, 50)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Quiz Game Key Handler')
        self.show()

    def keyPressEvent(self, event):
        # Test için hangi tuşa bastığınızı görmek için
        print(f"Tuş Kodu: {event.key()}")
        
        if event.key() == Qt.Key_1:
            self.selectOption('A')
        elif event.key() == Qt.Key_2:
            self.selectOption('B')
        elif event.key() == Qt.Key_3:
            self.selectOption('C')
        elif event.key() == Qt.Key_4:
            self.selectOption('D')
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirmAnswer()
        elif event.key() == Qt.Key_Escape:
            self.rejectAnswer()
        elif event.key() == Qt.Key_A:
            self.useJoker('50/50')
        elif event.key() == Qt.Key_S:
            self.useJoker('seyirci')
        elif event.key() == Qt.Key_D:
            self.useJoker('çift cevap')
        elif event.key() == Qt.Key_Right:
            self.nextQuestion()

    def selectOption(self, option):
        self.label.setText(f'{option} şıkkı seçildi.')

    def confirmAnswer(self):
        self.label.setText('Son kararınız onaylandı.')

    def rejectAnswer(self):
        self.label.setText('Son kararınız reddedildi.')

    def useJoker(self, joker):
        self.label.setText(f'{joker} jokeri kullanıldı.')

    def nextQuestion(self):
        self.label.setText('Diğer soruya geçildi.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = QuizGame()
    sys.exit(app.exec_())
