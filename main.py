import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QVBoxLayout, QFileDialog, QWidget, QSplitter, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import pytesseract
import pyperclip


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='rus+eng')  # Поддержка русского и английского языков
        return text
    except Exception as e:
        return f"Ошибка при извлечении текста: {str(e)}"


class TextExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text extractor")
        self.setFixedSize(1280, 720)

        # Иконка приложения
        try:
            self.setWindowIcon(QIcon("assets/icon.ico"))
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")

        # Создание виджетов
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Кнопка открытия изображения
        self.open_button = QPushButton("Открыть изображение", self)
        self.open_button.clicked.connect(self.open_image)
        self.open_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font: 12pt 'Helvetica';")
        layout.addWidget(self.open_button)

        # Создаем QSplitter для разделения пространства между картинкой и текстом
        splitter = QSplitter(Qt.Horizontal)

        # Виджет для предпросмотра изображения
        self.preview_label = QLabel(self)
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Разрешаем растяжение
        splitter.addWidget(self.preview_label)

        # Текстовое поле для вывода
        self.output_text = QTextEdit(self)
        self.output_text.setStyleSheet("background-color: white; font: 12pt 'Arial';")
        splitter.addWidget(self.output_text)

        # Настроим растяжение элементов внутри сплиттера
        splitter.setStretchFactor(0, 1)  # Картинка будет занимать 1 часть
        splitter.setStretchFactor(1, 1)  # Текстовое поле будет занимать 1 часть

        # Установим минимальные размеры для элементов
        self.preview_label.setMinimumWidth(200)
        self.output_text.setMinimumWidth(200)

        # Добавляем QSplitter в основной layout
        layout.addWidget(splitter)

        # Кнопка копирования текста
        self.copy_button = QPushButton("Копировать текст", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font: 12pt 'Helvetica';")
        layout.addWidget(self.copy_button)

        # Кнопка выхода
        self.exit_button = QPushButton("Выход", self)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font: 12pt 'Helvetica';")
        layout.addWidget(self.exit_button)

        # Центральный виджет и layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Откройте изображение", "", "Все изображения (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        if file_path:
            text = extract_text_from_image(file_path)
            self.output_text.setText(text)

            # Предпросмотр изображения
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(self.preview_label.width(), self.preview_label.height(), Qt.KeepAspectRatio)
            self.preview_label.setPixmap(pixmap)

    def copy_to_clipboard(self):
        text = self.output_text.toPlainText()
        try:
            pyperclip.copy(text)  # Копируем в буфер обмена
        except Exception as e:
            self.output_text.append(f"Ошибка при копировании в буфер обмена: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextExtractorApp()
    window.show()
    sys.exit(app.exec_())
