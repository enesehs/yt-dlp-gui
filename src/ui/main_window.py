import os
import tempfile
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QLabel, QComboBox, 
                               QProgressBar, QMessageBox, QFrame, QSizePolicy,
                               QFileDialog, QStyle)
from PySide6.QtCore import Qt, QSize, QThread
from PySide6.QtGui import QPixmap, QIcon

from src.logic.downloader import MetadataWorker, DownloadWorker, fetch_thumbnail, get_formats_list
from src.ui.log_viewer import LogViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.video_info = None
        self.formats_data = []
        self.metadata_thread = None
        self.download_thread = None
        self.download_worker = None
        self.output_dir = os.path.expanduser("~/Downloads")
        self.is_downloading = False

        self.setWindowTitle("yt-dlp-gui")
        
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "img", "logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setMinimumSize(650, 700)
        self.setMaximumSize(800, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.layout = QVBoxLayout(central_widget)
        self.layout.setSpacing(18)
        self.layout.setContentsMargins(28, 28, 28, 28)

        header_layout = QHBoxLayout()
        
        title_container = QVBoxLayout()
        title_label = QLabel("yt-dlp-gui")
        title_label.setObjectName("title")
        subtitle_label = QLabel("video downloader")
        subtitle_label.setObjectName("subtitle")
        logo_title_row = QHBoxLayout()
        logo_title_row.setSpacing(10)
        
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "img", "logo.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        logo_title_row.addWidget(logo_label)
        logo_title_row.addWidget(title_label)
        logo_title_row.addStretch()
        
        title_container.addLayout(logo_title_row)
        title_container.addWidget(subtitle_label)
        title_container.setSpacing(2)
        
        self.btn_about = QPushButton("i")
        self.btn_about.setObjectName("icon")
        self.btn_about.setFixedSize(40, 40)
        self.btn_about.setCursor(Qt.PointingHandCursor)
        self.btn_about.clicked.connect(self.show_about_dialog)
        
        self.btn_logs = QPushButton("#")
        self.btn_logs.setObjectName("icon")
        self.btn_logs.setFixedSize(40, 40)
        self.btn_logs.setCursor(Qt.PointingHandCursor)
        self.btn_logs.setToolTip("View Logs")
        self.btn_logs.clicked.connect(self.show_logs)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_logs)
        header_layout.addWidget(self.btn_about)
        self.layout.addLayout(header_layout)

        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste video URL here...")
        self.url_input.returnPressed.connect(self.check_link)
        
        self.btn_check = QPushButton("Fetch")
        self.btn_check.setObjectName("secondary")
        self.btn_check.setFixedWidth(90)
        self.btn_check.setFixedHeight(45)
        self.btn_check.setCursor(Qt.PointingHandCursor)
        self.btn_check.clicked.connect(self.check_link)

        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.btn_check)
        self.layout.addLayout(input_layout)

        self.thumbnail_label = QLabel("Enter a URL and click Fetch")
        self.thumbnail_label.setObjectName("thumbnail")
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.thumbnail_label.setFixedHeight(220)
        self.thumbnail_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(self.thumbnail_label)
        
        self.video_title_label = QLabel("")
        self.video_title_label.setAlignment(Qt.AlignCenter)
        self.video_title_label.setWordWrap(True)
        self.video_title_label.setStyleSheet("font-weight: 500; color: rgba(255,255,255,0.85);")
        self.layout.addWidget(self.video_title_label)

        options_layout = QHBoxLayout()
        format_label = QLabel("Format:")
        format_label.setStyleSheet("font-weight: 500;")
        self.format_combo = QComboBox()
        self.format_combo.addItem("Fetch a video first...")
        self.format_combo.setEnabled(False)
        
        options_layout.addWidget(format_label)
        options_layout.addWidget(self.format_combo, 1)
        self.layout.addLayout(options_layout)

        location_layout = QHBoxLayout()
        location_label = QLabel("Save to:")
        location_label.setStyleSheet("font-weight: 500;")
        self.location_input = QLineEdit()
        self.location_input.setText(self.output_dir)
        self.location_input.setReadOnly(True)
        
        self.btn_browse = QPushButton()
        self.btn_browse.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.btn_browse.setIconSize(QSize(24, 24))
        self.btn_browse.setObjectName("icon")
        self.btn_browse.setFixedSize(40, 40)
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.setToolTip("Browse folder")
        self.btn_browse.clicked.connect(self.browse_location)
        
        location_layout.addWidget(location_label)
        location_layout.addWidget(self.location_input, 1)
        location_layout.addWidget(self.btn_browse)
        self.layout.addLayout(location_layout)

        self.btn_download = QPushButton("Download")
        self.btn_download.setObjectName("primary")
        self.btn_download.setFixedHeight(52)
        self.btn_download.setCursor(Qt.PointingHandCursor)
        self.btn_download.setEnabled(False)
        self.btn_download.clicked.connect(self.toggle_download)
        self.layout.addWidget(self.btn_download)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        self.layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setObjectName("subtitle")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.layout.addStretch()

    def browse_location(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Download Folder", self.output_dir
        )
        if folder:
            self.output_dir = folder
            self.location_input.setText(folder)

    def check_link(self):
        url = self.url_input.text().strip()
        if not url:
            return
        
        self.status_label.setText("Fetching metadata...")
        self.btn_check.setEnabled(False)
        self.btn_download.setEnabled(False)
        self.format_combo.clear()
        self.format_combo.addItem("Loading...")
        
        self.metadata_thread = QThread()
        self.metadata_worker = MetadataWorker(url)
        self.metadata_worker.moveToThread(self.metadata_thread)
        
        self.metadata_thread.started.connect(self.metadata_worker.run)
        self.metadata_worker.finished.connect(self.on_metadata_received)
        self.metadata_worker.error.connect(self.on_metadata_error)
        self.metadata_worker.finished.connect(self.metadata_thread.quit)
        self.metadata_worker.error.connect(self.metadata_thread.quit)
        
        self.metadata_thread.start()

    def on_metadata_received(self, info):
        self.video_info = info
        self.btn_check.setEnabled(True)
        
        title = info.get('title', 'Unknown Title')
        self.video_title_label.setText(title[:80] + "..." if len(title) > 80 else title)
        
        thumbnail_url = info.get('thumbnail')
        if thumbnail_url:
            temp_path = os.path.join(tempfile.gettempdir(), "yt_thumb.jpg")
            if fetch_thumbnail(thumbnail_url, temp_path):
                pixmap = QPixmap(temp_path)
                scaled = pixmap.scaled(
                    self.thumbnail_label.width() - 10, 
                    self.thumbnail_label.height() - 10, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.thumbnail_label.setPixmap(scaled)
        
        self.formats_data = get_formats_list(info)
        self.format_combo.clear()
        for fmt in self.formats_data:
            self.format_combo.addItem(fmt['label'], fmt['id'])
        
        self.format_combo.setEnabled(True)
        self.btn_download.setEnabled(True)
        self.status_label.setText("Ready to download!")
        self.progress_bar.setValue(0)

    def on_metadata_error(self, error_msg):
        self.btn_check.setEnabled(True)
        self.status_label.setText(f"Error: {error_msg[:50]}...")
        self.thumbnail_label.setText("Failed to fetch video")
        self.format_combo.clear()
        self.format_combo.addItem("Fetch a video first...")

    def toggle_download(self):
        if self.is_downloading:
            self.cancel_download()
        else:
            self.start_download()

    def start_download(self):
        if not self.video_info:
            return
        
        format_id = self.format_combo.currentData()
        if not format_id:
            return
        
        self.is_downloading = True
        self.btn_download.setText("Cancel")
        self.btn_download.setObjectName("secondary")
        self.btn_download.style().unpolish(self.btn_download)
        self.btn_download.style().polish(self.btn_download)
        
        self.status_label.setText("Downloading...")
        self.progress_bar.setValue(0)
        
        self.download_thread = QThread()
        self.download_worker = DownloadWorker(self.url_input.text().strip(), format_id, self.output_dir)
        self.download_worker.moveToThread(self.download_thread)
        
        self.download_thread.started.connect(self.download_worker.run)
        self.download_worker.progress.connect(self.on_download_progress)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.error.connect(self.on_download_error)
        self.download_worker.log.connect(self.on_log_message)
        self.download_worker.finished.connect(self.download_thread.quit)
        self.download_worker.error.connect(self.download_thread.quit)
        
        self.download_thread.start()

    def cancel_download(self):
        if self.download_worker:
            self.download_worker.cancel()
            LogViewer.log("[USER] Cancellation requested...")
            
        if self.download_thread and self.download_thread.isRunning():
            if not self.download_thread.wait(2000):
                LogViewer.log("[WARN] Force terminating thread...")
                self.download_thread.terminate()
                self.download_thread.wait()
            
            self.is_downloading = False
            self.btn_download.setText("Download")
            self.btn_download.setObjectName("primary")
            self.btn_download.style().unpolish(self.btn_download)
            self.btn_download.style().polish(self.btn_download)
            
            self.status_label.setText("Download cancelled")
            self.progress_bar.setValue(0)
            LogViewer.log("[USER] Download cancelled by user")

    def on_download_progress(self, percent):
        self.progress_bar.setValue(percent)
        self.status_label.setText(f"Downloading... {percent}%")

    def on_download_finished(self, filepath):
        self.is_downloading = False
        self.btn_download.setText("Download")
        self.btn_download.setObjectName("primary")
        self.btn_download.style().unpolish(self.btn_download)
        self.btn_download.style().polish(self.btn_download)
        self.btn_download.setEnabled(True)
        
        self.progress_bar.setValue(100)
        self.status_label.setText("Download complete!")
        QMessageBox.information(self, "Download Complete", f"Saved to:\n{filepath}")

    def on_download_error(self, error_msg):
        self.is_downloading = False
        self.btn_download.setText("Download")
        self.btn_download.setObjectName("primary")
        self.btn_download.style().unpolish(self.btn_download)
        self.btn_download.style().polish(self.btn_download)
        self.btn_download.setEnabled(True)
        
        self.status_label.setText(f"Error: {error_msg[:50]}...")
        QMessageBox.critical(self, "Download Error", error_msg)

    def show_about_dialog(self):
        QMessageBox.about(self, "About yt-dlp-gui", 
                          "<h2 style='color: #fafafa; margin-bottom: 5px;'>yt-dlp-gui</h2>"
                          "<p style='color: #888; margin-top: 0;'>An open-source Qt 6-based graphical user interface for yt-dlp, "
                          "designed to make video downloading easier through a visual interface.</p>"
                          "<hr style='border-color: #333;'>"
                          "<p style='color: #666; font-size: 12px;'>made with love by <b>enesehs</b></p>"
                          "<p style='font-size: 12px;'><a href='https://enesehs.dev' style='color: #888;'>https://enesehs.dev</a></p>")
    
    def show_logs(self):
        log_viewer = LogViewer.get_instance(self)
        log_viewer.show()
        log_viewer.raise_()
    
    def on_log_message(self, message):
        LogViewer.log(message)
        if LogViewer._instance and LogViewer._instance.isVisible():
            LogViewer._instance.append_log(message)
