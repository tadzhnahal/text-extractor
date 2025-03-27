import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, 
    QVBoxLayout, QHBoxLayout, QFileDialog, QWidget, QSplitter, 
    QSizePolicy, QStatusBar, QStyle
)
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont
from PyQt5.QtCore import Qt, QSize
from PIL import Image
import pytesseract
import pyperclip


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='rus+eng')
        return text.strip()
    except Exception as e:
        return f"Ошибка: {str(e)}"


class TextExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextExtractor Pro")
        self.setMinimumSize(1280, 720)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #6200ea;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font: 12pt 'Segoe UI';
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #3700b3;
            }
            QPushButton:pressed {
                background-color: #03dac6;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px;
                font: 12pt 'Segoe UI';
            }
            QLabel {
                border: 2px dashed #e0e0e0;
                background-color: #fafafa;
                min-height: 200px;
                border-radius: 8px;
            }
            QSplitter::handle {
                background-color: #e0e0e0;
                width: 2px;
            }
        """)
        
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.SP_FileIcon)))
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Верхняя панель кнопок
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        
        self.open_btn = QPushButton("Загрузить изображение")
        self.open_btn.setIcon(QIcon.fromTheme("document-open"))
        self.open_btn.clicked.connect(self.open_image)
        self.open_btn.setIconSize(QSize(24, 24))
        top_layout.addWidget(self.open_btn)
        
        self.copy_btn = QPushButton("Копировать текст")
        self.copy_btn.setIcon(QIcon.fromTheme("edit-copy"))
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        top_layout.addWidget(self.copy_btn)
        
        self.exit_btn = QPushButton("Выход")
        self.exit_btn.setIcon(QIcon.fromTheme("application-exit"))
        self.exit_btn.clicked.connect(self.close)
        top_layout.addWidget(self.exit_btn)
        
        main_layout.addLayout(top_layout)

        # Основной контент
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        
        # Левая панель с изображением
        self.image_preview = QLabel("Перетащите изображение\nили нажмите 'Загрузить'")
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setStyleSheet("font: 14pt; color: #616161;")
        splitter.addWidget(self.image_preview)
        
        # Правая панель с текстом
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Здесь появится распознанный текст...")
        splitter.addWidget(self.text_area)
        
        splitter.setSizes([500, 700])
        main_layout.addWidget(splitter)

        # Статусная строка
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Готов к работе")
        main_layout.addWidget(self.status_bar)

        self.setCentralWidget(main_widget)

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите изображение", 
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.tiff);;Все файлы (*)",
            options=options
        )
        
        if file_path:
            self.status_bar.showMessage("Обработка изображения...")
            QApplication.processEvents()
            
            text = extract_text_from_image(file_path)
            self.text_area.setText(text)
            
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.image_preview.size() * 0.9,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_preview.setPixmap(scaled_pixmap)
                self.image_preview.setAlignment(Qt.AlignCenter)
            else:
                self.image_preview.setText("Ошибка загрузки изображения")
            
            self.status_bar.showMessage("Готово")

    def copy_to_clipboard(self):
        text = self.text_area.toPlainText()
        if text:
            try:
                pyperclip.copy(text)
                self.status_bar.showMessage("Текст скопирован в буфер обмена")
            except Exception as e:
                self.status_bar.showMessage(f"Ошибка копирования: {str(e)}")
        else:
            self.status_bar.showMessage("Нет текста для копирования")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.image_preview.pixmap():
            pixmap = self.image_preview.pixmap()
            scaled_pixmap = pixmap.scaled(
                self.image_preview.size() * 0.9,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_preview.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = TextExtractorApp()
    window.show()
    
    sys.exit(app.exec_())