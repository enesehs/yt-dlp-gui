from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                               QTextEdit, QPushButton, QLabel, QCheckBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class LogViewer(QDialog):
    _instance = None
    _log_buffer = []
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Logs")
        self.setMinimumSize(600, 400)
        self.setModal(False)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        header_layout = QHBoxLayout()
        title = QLabel("Terminal Output")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #fafafa;")
        
        self.auto_scroll_cb = QCheckBox("Auto-scroll")
        self.auto_scroll_cb.setChecked(True)
        self.auto_scroll_cb.setStyleSheet("color: #888;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.auto_scroll_cb)
        layout.addLayout(header_layout)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("monospace", 11))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #0a0a0a;
                border: 1px solid #1a1a1a;
                border-radius: 8px;
                padding: 12px;
                color: #00ff00;
                font-family: "JetBrains Mono", "Fira Code", "Consolas", monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_text)
        
        btn_layout = QHBoxLayout()
        
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setObjectName("secondary")
        self.btn_clear.clicked.connect(self.clear_logs)
        
        self.btn_close = QPushButton("Close")
        self.btn_close.setObjectName("secondary")
        self.btn_close.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)
        
        self.log_text.setPlainText("\n".join(LogViewer._log_buffer))
        self._scroll_to_bottom()
    
    def _scroll_to_bottom(self):
        if self.auto_scroll_cb.isChecked():
            scrollbar = self.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def append_log(self, text):
        LogViewer._log_buffer.append(text)
        if len(LogViewer._log_buffer) > 1000:
            LogViewer._log_buffer = LogViewer._log_buffer[-500:]
        
        self.log_text.append(text)
        self._scroll_to_bottom()
    
    def clear_logs(self):
        LogViewer._log_buffer.clear()
        self.log_text.clear()
    
    @classmethod
    def log(cls, text):
        cls._log_buffer.append(text)
        if len(cls._log_buffer) > 1000:
            cls._log_buffer = cls._log_buffer[-500:]
    
    @classmethod
    def get_instance(cls, parent=None):
        if cls._instance is None or not cls._instance.isVisible():
            cls._instance = cls(parent)
        return cls._instance
