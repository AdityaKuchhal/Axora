#!/usr/bin/env python3
"""
Axora - Utility Bill Organizer
Professional desktop application for organizing utility bills
"""

import os
import json
import sys
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QProgressBar, QTextEdit, QFileDialog,
    QMessageBox, QFrame, QGroupBox, QTabWidget, QListWidget, QListWidgetItem,
    QMenu, QToolButton
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QAction

from PyQt6.QtWidgets import QSizePolicy



# ------------------------------ Worker ------------------------------

class FileOrganizerWorker(QThread):
    """Worker thread for file organization"""
    progress_updated = pyqtSignal(str)
    progress_percent = pyqtSignal(int)   # 0..100
    finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, organizer, source_folder, utilities_folder):
        super().__init__()
        self.organizer = organizer
        self.source_folder = source_folder
        self.utilities_folder = utilities_folder

    def run(self):
        try:
            # Emit a starting tick so the UI can flip from indeterminate later
            self.progress_updated.emit("Initializing...")

            def progress_callback(message):
                """
                Expect either:
                - tuple(current, total)  -> we compute percentage
                - string                 -> we forward as log
                """
                if isinstance(message, tuple) and len(message) == 2:
                    current, total = message
                    total = max(int(total), 1)
                    current = max(min(int(current), total), 0)
                    percent = int((current / total) * 100)
                    self.progress_percent.emit(percent)
                    self.progress_updated.emit(f"Processing file {current} of {total}")
                else:
                    self.progress_updated.emit(str(message))

            success, results = self.organizer.organize_files(
                self.source_folder,
                self.utilities_folder,
                progress_callback
            )

            if success:
                # Ensure 100% at the end even if organizer didn't send tuples
                self.progress_percent.emit(100)
                self.finished.emit(results)
            else:
                self.error_occurred.emit(str(results))

        except Exception as e:
            self.error_occurred.emit(str(e))


# ------------------------------ Main App ------------------------------

class AxoraApp(QMainWindow):
    """Axora - Utility Bill Organizer"""

    def __init__(self):
        super().__init__()
        self.organizer = None
        self.worker_thread = None

        # Theme & history
        self.is_dark = False
        self.history_path = os.path.join(os.path.expanduser("~"), ".axora", "history.json")
        self.history_items = []

        self.setup_ui()
        self.apply_dark_style()  # default
        self.load_history()

    # ---------- UI Structure ----------

    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("Axora")
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header with title centered and menu button on the right
        self.create_header(main_layout)

        # Content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(content_layout)

        # Panels
        left_panel = self.create_controls_panel()
        right_panel = self.create_right_panel()

        content_layout.addWidget(left_panel, 1)
        content_layout.addWidget(right_panel, 1)

        self.statusBar().showMessage("Ready to organize utility bills")

    def create_header(self, parent_layout):
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(60)

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 10, 16, 10)

        # Left spacer
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        

        # Title (center)
        title_label = QLabel("Axora")
        title_label.setObjectName("titleLabel")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Right menu button
        self.menu_button = QToolButton()
        self.menu_button.setObjectName("menuButton")
        self.menu_button.setText("⋯")
        self.menu_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menu_button.setFixedWidth(36)
        self.menu_button.setCursor(Qt.CursorShape.PointingHandCursor)

        menu = QMenu(self)
        self.action_toggle_light = QAction("Light Mode Toggle", self, checkable=True)
        self.action_toggle_light.triggered.connect(self.toggle_light_mode)

        self.action_show_history = QAction("History Tab", self)
        self.action_show_history.triggered.connect(lambda: self.tabs.setCurrentWidget(self.history_tab))

        self.action_info = QAction("Info", self)
        self.action_info.triggered.connect(self.show_info)

        menu.addAction(self.action_toggle_light)
        menu.addAction(self.action_show_history)
        menu.addSeparator()
        menu.addAction(self.action_info)
        self.menu_button.setMenu(menu)

        # Assemble: spacer | title | spacer | menu
        header_layout.addWidget(left_spacer, 1)
        header_layout.addWidget(title_label, 0, Qt.AlignmentFlag.AlignHCenter)
        header_layout.addStretch(1)
        header_layout.addWidget(self.menu_button, 0, Qt.AlignmentFlag.AlignRight)

        parent_layout.addWidget(header_frame)

    def create_controls_panel(self):
        panel = QFrame()
        panel.setObjectName("controlsPanel")
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Excel file
        excel_group = QGroupBox("Excel File")
        excel_group.setObjectName("fileGroup")
        excel_layout = QVBoxLayout(excel_group)
        excel_layout.setSpacing(10)
        excel_layout.setContentsMargins(15, 15, 15, 15)

        self.excel_path_edit = QLineEdit()
        self.excel_path_edit.setPlaceholderText("Select Excel file...")
        self.excel_browse_btn = QPushButton("Browse")
        self.excel_browse_btn.clicked.connect(self.browse_excel_file)

        excel_input_layout = QHBoxLayout()
        excel_input_layout.addWidget(self.excel_path_edit, 1)
        excel_input_layout.addWidget(self.excel_browse_btn, 0)
        excel_layout.addLayout(excel_input_layout)
        layout.addWidget(excel_group)

        # Source folder
        source_group = QGroupBox("Source Folder")
        source_group.setObjectName("fileGroup")
        source_layout = QVBoxLayout(source_group)
        source_layout.setSpacing(10)
        source_layout.setContentsMargins(15, 15, 15, 15)

        self.source_path_edit = QLineEdit()
        self.source_path_edit.setPlaceholderText("Select source folder...")
        self.source_browse_btn = QPushButton("Browse")
        self.source_browse_btn.clicked.connect(self.browse_source_folder)

        source_input_layout = QHBoxLayout()
        source_input_layout.addWidget(self.source_path_edit, 1)
        source_input_layout.addWidget(self.source_browse_btn, 0)
        source_layout.addLayout(source_input_layout)
        layout.addWidget(source_group)

        # Destination folder
        dest_group = QGroupBox("Destination Folder")
        dest_group.setObjectName("fileGroup")
        dest_layout = QVBoxLayout(dest_group)
        dest_layout.setSpacing(10)
        dest_layout.setContentsMargins(15, 15, 15, 15)

        self.dest_path_edit = QLineEdit()
        self.dest_path_edit.setPlaceholderText("Select destination folder...")
        self.dest_browse_btn = QPushButton("Browse")
        self.dest_browse_btn.clicked.connect(self.browse_dest_folder)

        dest_input_layout = QHBoxLayout()
        dest_input_layout.addWidget(self.dest_path_edit, 1)
        dest_input_layout.addWidget(self.dest_browse_btn, 0)
        dest_layout.addLayout(dest_input_layout)
        layout.addWidget(dest_group)

        # Action
        action_group = QGroupBox("Action")
        action_group.setObjectName("actionGroup")
        action_layout = QVBoxLayout(action_group)
        action_layout.setSpacing(15)
        action_layout.setContentsMargins(15, 15, 15, 15)

        button_progress_layout = QHBoxLayout()
        button_progress_layout.setSpacing(15)

        self.organize_btn = QPushButton("Execute")
        self.organize_btn.setObjectName("organizeButton")
        self.organize_btn.clicked.connect(self.start_organization)
        self.organize_btn.setFixedSize(110, 36)
        button_progress_layout.addWidget(self.organize_btn, 0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setFixedHeight(26)
        self.progress_bar.setValue(0)
        # Start with determinate range; we flip to indeterminate before work
        self.progress_bar.setRange(0, 100)
        button_progress_layout.addWidget(self.progress_bar, 1)

        action_layout.addLayout(button_progress_layout)
        layout.addWidget(action_group)

        return panel

    def create_right_panel(self):
        panel = QFrame()
        panel.setObjectName("resultsPanel")
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tabs: Results | History
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabs")

        # Results tab
        self.results_tab = QWidget()
        results_layout = QVBoxLayout(self.results_tab)
        results_header = QLabel("Results")
        results_header.setObjectName("resultsHeader")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        results_header.setFont(header_font)
        results_layout.addWidget(results_header)

        self.results_text = QTextEdit()
        self.results_text.setObjectName("resultsText")
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Results will appear here...")
        results_layout.addWidget(self.results_text)

        # History tab
        self.history_tab = QWidget()
        history_layout = QVBoxLayout(self.history_tab)
        history_header = QLabel("History")
        history_header.setObjectName("historyHeader")
        history_header.setFont(header_font)
        history_layout.addWidget(history_header)

        self.history_list = QListWidget()
        self.history_list.setObjectName("historyList")
        history_layout.addWidget(self.history_list)

        self.tabs.addTab(self.results_tab, "Results")
        self.tabs.addTab(self.history_tab, "History")

        layout.addWidget(self.tabs)
        return panel

    # ---------- Theming ----------

    def apply_light_style(self):
        self.is_dark = False
        self.action_toggle_light.setChecked(False)
        self.setStyleSheet("""
            QMainWindow { background-color: #f8fafc; color: #0f172a; }
            QLabel, QLineEdit, QTextEdit, QPushButton, QGroupBox { font-size: 13px; }

            #headerFrame { background: #ffffff; border-bottom: 1px solid #e5e7eb; }
            #titleLabel { color: #0f172a; font-weight: 700; }
            #menuButton { background: transparent; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px 0; }
            #menuButton::menu-indicator { image: none; }

            #controlsPanel, #resultsPanel { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; }

            QGroupBox {
                font-weight: 600; color: #0f172a; border: 1px solid #e5e7eb; border-radius: 8px;
                margin-top: 10px; padding-top: 12px; background: #ffffff;
            }
            QGroupBox::title { left: 12px; padding: 0 6px; color: #334155; }

            QLineEdit {
                padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 6px;
                background: #ffffff; color: #0f172a;
            }
            QLineEdit:focus { border: 1px solid #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
            QLineEdit::placeholder { color: #94a3b8; }

            QPushButton { background: #2563eb; color: #fff; border: none; padding: 9px 14px; border-radius: 6px; font-weight: 600; }
            QPushButton:hover { background: #1d4ed8; }
            QPushButton:disabled { background: #93c5fd; color: #fff; }
            #organizeButton { background: #16a34a; }
            #organizeButton:hover { background: #15803d; }

            #progressBar { border: 1px solid #cbd5e1; border-radius: 6px; background: #f1f5f9; height: 26px; text-align: center; }
            #progressBar::chunk { background: #16a34a; border-radius: 6px; }

            #resultsHeader, #historyHeader { color: #0f172a; }
            #resultsText {
                border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px;
                background: #0b1220; color: #e5e7eb;
                font-family: Menlo, Consolas, "Courier New", monospace; font-size: 12px;
            }
            #resultsText::placeholder { color: #94a3b8; }

            #historyList { border: 1px solid #e5e7eb; border-radius: 8px; background: #ffffff; }

            QStatusBar { background: #0f172a; color: #e5e7eb; }
            QStatusBar::item { border: none; }
        """)

    def apply_dark_style(self):
        self.is_dark = True
        self.action_toggle_light.setChecked(True)
        self.setStyleSheet("""
            QMainWindow { background-color: #0b1220; color: #e5e7eb; }
            QLabel, QLineEdit, QTextEdit, QPushButton, QGroupBox { font-size: 13px; }

            #headerFrame { background: #0f172a; border-bottom: 1px solid #1f2937; }
            #titleLabel { color: #e5e7eb; font-weight: 700; }
            #menuButton { background: transparent; border: 1px solid #334155; border-radius: 6px; padding: 4px 0; }
            #menuButton::menu-indicator { image: none; }

            #controlsPanel, #resultsPanel { background: #0f172a; border: 1px solid #1f2937; border-radius: 8px; }

            QGroupBox {
                font-weight: 600; color: #e5e7eb; border: 1px solid #1f2937; border-radius: 8px;
                margin-top: 10px; padding-top: 12px; background: #0f172a;
            }
            QGroupBox::title { left: 12px; padding: 0 6px; color: #cbd5e1; }

            QLineEdit {
                padding: 10px 12px; border: 1px solid #334155; border-radius: 6px;
                background: #111827; color: #e5e7eb;
            }
            QLineEdit:focus { border: 1px solid #60a5fa; box-shadow: 0 0 0 3px rgba(96,165,250,0.2); }
            QLineEdit::placeholder { color: #94a3b8; }

            QPushButton { background: #3b82f6; color: #0b1220; border: none; padding: 9px 14px; border-radius: 6px; font-weight: 700; }
            QPushButton:hover { background: #2563eb; }
            QPushButton:disabled { background: #1e3a8a; color: #94a3b8; }
            #organizeButton { background: #10b981; color: #0b1220; }
            #organizeButton:hover { background: #059669; }

            #progressBar { border: 1px solid #334155; border-radius: 6px; background: #111827; height: 26px; text-align: center; }
            #progressBar::chunk { background: #10b981; border-radius: 6px; }

            #resultsHeader, #historyHeader { color: #e5e7eb; }
            #resultsText {
                border: 1px solid #334155; border-radius: 8px; padding: 12px;
                background: #0b1220; color: #e5e7eb;
                font-family: Menlo, Consolas, "Courier New", monospace; font-size: 12px;
            }
            #historyList { border: 1px solid #334155; border-radius: 8px; background: #0f172a; color: #e5e7eb; }

            QStatusBar { background: #0f172a; color: #e5e7eb; }
            QStatusBar::item { border: none; }
        """)

    def toggle_light_mode(self, checked: bool):
        if checked:
            self.apply_light_style()
        else:
            self.apply_dark_style()

    # ---------- File pickers ----------

    def browse_excel_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Excel File", "", "Excel files (*.xlsx *.xls);;All files (*.*)"
        )
        if file_path:
            self.excel_path_edit.setText(file_path)
            self.load_excel_data(file_path)

    def browse_source_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_path_edit.setText(folder)
            self.count_source_files(folder)

    def browse_dest_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Utilities Folder")
        if folder:
            self.dest_path_edit.setText(folder)

    # ---------- Excel / Organizer ----------

    def load_excel_data(self, file_path):
        try:
            # Import the organizer class the user already has
            from utility_bill_organizer import SimplifiedUtilitiesOrganizer
            self.organizer = SimplifiedUtilitiesOrganizer()
            success, message = self.organizer.load_excel_data(file_path)

            if success:
                self.add_result(f"✅ {message}")
                self.statusBar().showMessage(f"Excel data loaded: {message}")
            else:
                self.add_result(f"❌ {message}")
                QMessageBox.warning(self, "Excel Load Error", message)

        except Exception as e:
            error_msg = f"Error loading Excel file: {str(e)}"
            self.add_result(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def count_source_files(self, folder):
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            self.add_result(f"📁 Source folder: {len(files)} files found")
            self.statusBar().showMessage(f"Source folder selected: {len(files)} files")
        except Exception:
            self.add_result("📁 Source folder selected")

    # ---------- Run & Progress ----------

    def start_organization(self):
        excel_file = self.excel_path_edit.text().strip()
        source_folder = self.source_path_edit.text().strip()
        dest_folder = self.dest_path_edit.text().strip()

        if not excel_file or not source_folder or not dest_folder:
            QMessageBox.warning(self, "Missing Information",
                                "Please select Excel file, source folder, and destination folder")
            return

        if not self.organizer:
            self.load_excel_data(excel_file)
            if not self.organizer:
                return

        # Disable controls and set indeterminate progress
        self.organize_btn.setEnabled(False)
        self.organize_btn.setText("Processing...")
        self.progress_bar.setRange(0, 0)  # Indeterminate spinner
        self.progress_bar.setValue(0)

        # Start worker thread
        self.worker_thread = FileOrganizerWorker(self.organizer, source_folder, dest_folder)
        self.worker_thread.progress_updated.connect(self.update_progress_text)
        self.worker_thread.progress_percent.connect(self.update_progress_bar)
        self.worker_thread.finished.connect(self.organization_finished)
        self.worker_thread.error_occurred.connect(self.organization_error)
        self.worker_thread.start()

        self.add_result("🚀 Starting file organization...")

    def update_progress_text(self, message):
        self.add_result(message)

    def update_progress_bar(self, value):
        # When we receive a real percentage, flip to determinate mode
        if self.progress_bar.minimum() == 0 and self.progress_bar.maximum() == 0:
            self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(max(0, min(100, int(value))))

    def organization_finished(self, results):
        self.organize_btn.setEnabled(True)
        self.organize_btn.setText("Execute")
        # Ensure determinate & complete
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

        # Display results
        self.add_result("\n🎉 Organization completed successfully!")
        self.add_result(f"📊 Processed: {results['total_files']} files")
        self.add_result(f"✅ Successful: {len(results['successful'])} files")
        self.add_result(f"❌ Failed: {len(results['failed'])} files\n")

        self.add_result("📁 Organized Structure:")
        for corp, providers in results['organized_structure'].items():
            self.add_result(f"  Corporation {corp}:")
            for provider, accounts in providers.items():
                self.add_result(f"    {provider}:")
                for account, years in accounts.items():
                    self.add_result(f"      Account {account}:")
                    for year, files in years.items():
                        self.add_result(f"        {year}: {', '.join(files)}")

        if results['failed']:
            self.add_result("\n❌ Failed Files:")
            for failure in results['failed']:
                self.add_result(f"  • {failure['file']}: {failure['reason']}")

        self.statusBar().showMessage("Organization completed successfully!")
        QMessageBox.information(self, "Success", "Files have been successfully organized!")

        # Log to history
        self.append_history_entry(results)

    def organization_error(self, error_message):
        self.organize_btn.setEnabled(True)
        self.organize_btn.setText("Execute")
        # Flip back from indeterminate if needed
        if self.progress_bar.minimum() == 0 and self.progress_bar.maximum() == 0:
            self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.add_result(f"❌ Organization failed: {error_message}")
        self.statusBar().showMessage("Organization failed")
        QMessageBox.critical(self, "Error", f"File organization failed:\n{error_message}")

    # ---------- Results / History / Info ----------

    def add_result(self, message):
        self.results_text.append(message)
        cursor = self.results_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.results_text.setTextCursor(cursor)

    def append_history_entry(self, results: dict):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = (f"{timestamp}  |  Total: {results.get('total_files', 0)}  |  "
                   f"✓ {len(results.get('successful', []))}  |  ✗ {len(results.get('failed', []))}")
        item = QListWidgetItem(summary)
        self.history_list.insertItem(0, item)  # newest on top

        # Save to disk
        self.history_items.insert(0, {
            "timestamp": timestamp,
            "total": results.get('total_files', 0),
            "successful": len(results.get('successful', [])),
            "failed": len(results.get('failed', [])),
        })
        self.save_history()

    def show_info(self):
        QMessageBox.information(
            self,
            "About Axora",
            (
                "<b>Axora</b> — Utility Bill Organizer<br><br>"
                "• Reads your Excel mapping to route files into corporation/provider/account/year folders.<br>"
                "• Renames files in chronological formats where applicable.<br>"
                "• Shows progress, logs detailed results, and keeps a timestamped history.<br><br>"
                "Built with PyQt6."
            )
        )

    # ---------- History Persistence ----------

    def load_history(self):
        try:
            os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
            if os.path.exists(self.history_path):
                with open(self.history_path, "r", encoding="utf-8") as f:
                    self.history_items = json.load(f)
                # Populate UI
                for rec in reversed(self.history_items):
                    summary = (f"{rec['timestamp']}  |  Total: {rec['total']}  |  "
                               f"✓ {rec['successful']}  |  ✗ {rec['failed']}")
                    self.history_list.addItem(summary)
        except Exception:
            # Non-fatal
            pass

    def save_history(self):
        try:
            os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump(self.history_items, f, indent=2)
        except Exception:
            # Non-fatal
            pass


# ------------------------------ Entry ------------------------------

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Axora")
    app.setApplicationVersion("2.1")
    app.setOrganizationName("AK Realm")

    window = AxoraApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()