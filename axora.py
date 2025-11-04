#!/usr/bin/env python3
"""
Axora - Utility Bill Organizer
Professional desktop application for organizing utility bills
"""

import os
import re
import json
import shutil
import sys
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QProgressBar,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QFrame,
    QGroupBox,
    QTabWidget,
    QListWidget,
    QListWidgetItem,
    QRadioButton,
    QButtonGroup,
    QStatusBar,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

import pandas as pd

HISTORY_FILE = "axora_history.json"


# ------------------------------ Worker Thread ------------------------------

class FileOrganizerWorker(QThread):
    """Worker thread for file organization"""
    progress_updated = pyqtSignal(str)
    progress_percent = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, organizer, source_path, dest_root):
        super().__init__()
        self.organizer = organizer
        self.source_path = source_path
        self.dest_root = dest_root

    def run(self):
        try:
            self.progress_updated.emit("Initializing...")
            
            # Handle source as file or folder
            pdf_files = []
            if os.path.isfile(self.source_path):
                if self.source_path.lower().endswith('.pdf'):
                    pdf_files = [(os.path.dirname(self.source_path) or ".", os.path.basename(self.source_path))]
            elif os.path.isdir(self.source_path):
                files = [f for f in os.listdir(self.source_path) if os.path.isfile(os.path.join(self.source_path, f))]
                pdf_files = [(self.source_path, f) for f in files if f.lower().endswith('.pdf')]
            
            total = len(pdf_files)
            if total == 0:
                self.error_occurred.emit("No PDF files found in source.")
                return
            
            moved = 0
            skipped = 0
            not_found = 0
            
            for idx, (source_dir, file_name) in enumerate(pdf_files, start=1):
                percent = int((idx - 1) / total * 100)
                self.progress_percent.emit(percent)
                self.progress_updated.emit(f"Processing file {idx} of {total}: {file_name}")
                
                try:
                    result, message = self.organizer.process_single_file(source_dir, self.dest_root, file_name)
                    if result:
                        moved += 1
                        # message contains the hierarchy path
                        self.progress_updated.emit(f"✅ MOVED '{file_name}' -> {message}")
                    elif message == "not_found":
                        not_found += 1
                        self.progress_updated.emit(f"NOT FOUND '{file_name}': Account not found in Excel")
                    else:
                        skipped += 1
                        self.progress_updated.emit(f"SKIPPED '{file_name}': Target already exists")
                except Exception as ex:
                    skipped += 1
                    self.progress_updated.emit(f"SKIPPED '{file_name}': {ex}")
            
            self.progress_percent.emit(100)
            self.finished.emit({
                "moved": moved,
                "skipped": skipped,
                "not_found": not_found,
                "total": total
            })
            
        except Exception as e:
            self.error_occurred.emit(str(e))


# ------------------------------ Main App ------------------------------

class AxoraApp(QMainWindow):
    """Axora - Utility Bill Organizer"""

    def __init__(self):
        super().__init__()
        self.mapping = {}
        self.worker_thread = None
        self.is_dark = True
        self.history_items = []

        self.setup_ui()
        self.apply_dark_style()
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

        # Source mode selection (File or Folder)
        source_mode_group = QButtonGroup(self)
        self.source_file_radio = QRadioButton("File")
        self.source_folder_radio = QRadioButton("Folder")
        self.source_folder_radio.setChecked(True)
        source_mode_group.addButton(self.source_file_radio)
        source_mode_group.addButton(self.source_folder_radio)

        source_mode_layout = QHBoxLayout()
        source_mode_layout.addWidget(QLabel("Mode:"))
        source_mode_layout.addWidget(self.source_file_radio)
        source_mode_layout.addWidget(self.source_folder_radio)
        source_mode_layout.addStretch()
        source_layout.addLayout(source_mode_layout)

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
        self.organize_btn.setEnabled(False)
        
        # Enable button when all fields are filled
        self.excel_path_edit.textChanged.connect(self.update_execute_enabled)
        self.source_path_edit.textChanged.connect(self.update_execute_enabled)
        self.dest_path_edit.textChanged.connect(self.update_execute_enabled)
        
        button_progress_layout.addWidget(self.organize_btn, 0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setFixedHeight(26)
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setFormat("%p%")
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
            
            QRadioButton { color: #e5e7eb; spacing: 5px; }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #334155;
                background: #111827;
            }
            QRadioButton::indicator:checked {
                background: #3b82f6;
                border: 2px solid #3b82f6;
            }
            
            QTabWidget::pane { border: 1px solid #334155; background-color: #0f172a; }
            QTabBar::tab {
                background-color: #111827;
                color: #e5e7eb;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
                color: #0b1220;
            }
            QTabBar::tab:hover {
                background-color: #1f2937;
            }
        """)


    # ---------- File pickers ----------

    def browse_excel_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Excel File", "", "Excel files (*.xlsx *.xls);;All files (*.*)"
        )
        if file_path:
            # Show just filename
            self.excel_path_edit.setText(os.path.basename(file_path))
            self.excel_path_edit.setToolTip(file_path)
            self.load_excel_data(file_path)

    def browse_source_folder(self):
        if self.source_file_radio.isChecked():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select source file", "", "PDF Files (*.pdf);;All Files (*.*)"
            )
            if file_path:
                self.source_path_edit.setText(os.path.basename(file_path))
                self.source_path_edit.setToolTip(file_path)
        else:
            folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
            if folder:
                self.source_path_edit.setText(os.path.basename(folder) if os.path.basename(folder) else folder)
                self.source_path_edit.setToolTip(folder)

    def browse_dest_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Utilities Folder")
        if folder:
            self.dest_path_edit.setText(os.path.basename(folder) if os.path.basename(folder) else folder)
            self.dest_path_edit.setToolTip(folder)

    def update_execute_enabled(self):
        self.organize_btn.setEnabled(
            bool(self.excel_path_edit.text().strip()) and
            bool(self.source_path_edit.text().strip()) and
            bool(self.dest_path_edit.text().strip())
        )

    # ---------- Excel / Organizer ----------

    def load_excel_data(self, file_path):
        try:
            excel_path = self.excel_path_edit.toolTip() or file_path
            self.mapping = self.build_mapping_from_excel(excel_path)
            self.add_result(f"✅ Loaded mapping entries: {len(self.mapping)}")
            self.statusBar().showMessage(f"Excel data loaded: {len(self.mapping)} entries")
        except Exception as e:
            error_msg = f"Error loading Excel file: {str(e)}"
            self.add_result(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def build_mapping_from_excel(self, excel_path: str) -> dict:
        df = pd.read_excel(excel_path, header=None)

        mapping = {}
        current_provider = None

        for _, row in df.iterrows():
            cell0 = str(row[0]).strip() if not pd.isna(row[0]) else ""
            cell1 = str(row[1]).strip() if len(row) > 1 and not pd.isna(row[1]) else ""
            cell2 = str(row[2]).strip() if len(row) > 2 and not pd.isna(row[2]) else ""

            if cell0.upper() in ("BELL", "TELUS", "ROGERS"):
                if (cell1 == "" or cell1 == "nan" or pd.isna(row[1])) and (cell2 == "" or cell2 == "nan" or pd.isna(row[2])):
                    current_provider = cell0.upper()
                    continue

            if current_provider is None:
                continue

            if cell1 == "" or cell1 == "nan" or pd.isna(row[1]):
                continue
            if cell2 == "" or cell2 == "nan" or pd.isna(row[2]):
                continue

            corp = cell1
            account_str = cell2

            # First, extract extension
            ext = ""
            ext_match = re.search(r"\(([^)]+)\)", account_str)
            if ext_match:
                ext_str = ext_match.group(1).strip()
                if re.match(r"^[\dA-Za-z]{2,6}$", ext_str):
                    ext = ext_str
                    account_str = re.sub(r"\([^)]+\)", "", account_str)
            else:
                space_ext = re.search(r"\s+(\d{3,4})\s*$", account_str)
                if space_ext:
                    ext = space_ext.group(1)
                    account_str = re.sub(r"\s+" + re.escape(ext) + r"\s*$", "", account_str)

            # Extract last4
            phone_match = re.search(r"(\d{3}[-\s]?\d{3}[-\s]?\d{4})", account_str)
            if phone_match:
                phone_digits = re.sub(r"\D", "", phone_match.group(1))
                if len(phone_digits) == 10:
                    last4 = phone_digits[-4:]
                else:
                    all_digits = re.sub(r"\D", "", account_str)
                    last4 = all_digits[-4:] if len(all_digits) >= 4 else ""
            else:
                all_digits = re.sub(r"\D", "", account_str)
                last4 = all_digits[-4:] if len(all_digits) >= 4 else ""

            entry = {
                "provider": current_provider,
                "corp": corp,
                "account_last4": last4,
                "account_ext": ext,
            }

            if last4:
                mapping[(current_provider, last4)] = entry
            if ext:
                mapping[(current_provider, ext)] = entry

        return mapping

    # ---------- Processing ----------

    def process_single_file(self, source_dir: str, dest_root: str, file_name: str) -> tuple[bool, str]:
        """Process a single file. Returns (success: bool, skip_reason: str)"""
        src_path = os.path.join(source_dir, file_name)

        # Extract account identifiers from filename
        last4, ext = self.extract_account_tokens(file_name)
        if not last4 and not ext:
            return False, "not_found"

        # Try matching: first last4, then extension
        map_entry = None
        matched_token = None

        if last4:
            for prov in ("BELL", "TELUS", "ROGERS"):
                key = (prov, last4)
                if key in self.mapping:
                    map_entry = self.mapping[key]
                    matched_token = last4
                    break

        if map_entry is None and ext:
            for prov in ("BELL", "TELUS", "ROGERS"):
                key = (prov, ext)
                if key in self.mapping:
                    map_entry = self.mapping[key]
                    matched_token = ext
                    break

        if map_entry is None:
            return False, "not_found"

        provider = map_entry["provider"]
        corp = str(map_entry["corp"]).strip()

        # Extract date from filename
        date_str, year_folder, final_name = self.extract_date_targets(file_name)
        if not date_str:
            return False, "not_found"

        # Build destination path
        account_folder_name = matched_token
        corp_dir = os.path.join(dest_root, corp)
        provider_dir = os.path.join(corp_dir, provider.capitalize())
        account_dir = os.path.join(provider_dir, account_folder_name)

        os.makedirs(account_dir, exist_ok=True)

        # Ensure account organized by year
        self.ensure_year_organized(account_dir)

        year_dir = os.path.join(account_dir, year_folder)
        os.makedirs(year_dir, exist_ok=True)

        dest_file_path = os.path.join(year_dir, final_name)
        if os.path.exists(dest_file_path):
            return False, "skipped"

        shutil.move(src_path, dest_file_path)
        # Return hierarchy path for display
        hierarchy_path = f"{corp} -> {provider.capitalize()} -> {account_folder_name} -> {year_folder} -> {final_name}"
        return True, hierarchy_path

    def extract_account_tokens(self, file_name: str) -> tuple[str, str]:
        base = os.path.splitext(file_name)[0]

        # Extract extension first
        ext = ""
        ext_match = re.search(r"\(([^)]+)\)", base)
        if ext_match:
            ext_candidate = ext_match.group(1).strip()
            if re.match(r"^[\dA-Za-z]{2,6}$", ext_candidate):
                ext = ext_candidate
        else:
            space_ext = re.search(r"\s+(\d{3,4})\s*$", base)
            if space_ext:
                ext = space_ext.group(1)

        # Remove date patterns
        base_for_last4 = re.sub(r"_\d{4}-\d{2}-\d{2}", "", base)
        base_for_last4 = re.sub(r"_\d{2}-\d{2}-\d{2}", "", base_for_last4)
        base_for_last4 = re.sub(r"\d{4}-\d{2}-\d{2}", "", base_for_last4)
        base_for_last4 = re.sub(r"\d{2}-\d{2}-\d{2}", "", base_for_last4)

        if ext:
            base_for_last4 = re.sub(r"\([^)]+\)", "", base_for_last4)
            base_for_last4 = re.sub(r"\s+" + re.escape(ext) + r"\s*", "", base_for_last4)

        # Find phone numbers
        phone_patterns = [
            r"(\d{3}\s+\d{3}\s+\d{4})",
            r"(\d{3}-\d{3}-\d{4})",
            r"(\d{10})",
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, base_for_last4)
            if phone_match:
                phone_str = phone_match.group(1)
                phone_digits = re.sub(r"\D", "", phone_str)
                if len(phone_digits) == 10:
                    match_start = phone_match.start()
                    if match_start == 0 or not base_for_last4[match_start - 1].isalnum():
                        return phone_digits[-4:], ext

        # Find account numbers
        digit_sequences = re.finditer(r"(\d{7,10})", base_for_last4)
        candidates = []
        for match in digit_sequences:
            seq = match.group(1)
            start_pos = match.start()
            if start_pos > 0 and base_for_last4[start_pos - 1].isalpha():
                continue
            if start_pos > 0 and base_for_last4[start_pos - 1].upper() == 'X':
                continue
            seq_len = len(seq)
            if 7 <= seq_len <= 10:
                candidates.append((seq, start_pos))

        if candidates:
            best = max(candidates, key=lambda x: (len(x[0]), x[1]))
            return best[0][-4:], ext

        # Fallback
        digit_sequences = re.finditer(r"(\d{4,})", base_for_last4)
        candidates = []
        for match in digit_sequences:
            seq = match.group(1)
            start_pos = match.start()
            if len(seq) == 4 and (seq.startswith("19") or seq.startswith("20")):
                continue
            if start_pos > 0 and base_for_last4[start_pos - 1].isalpha():
                continue
            candidates.append((seq, start_pos))

        if candidates:
            best = max(candidates, key=lambda x: x[1])
            return best[0][-4:], ext

        return "", ext

    def extract_date_targets(self, file_name: str) -> tuple[str, str, str]:
        name, ext = os.path.splitext(file_name)

        m_full = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
        if m_full:
            yyyy, mm, dd = m_full.group(1), m_full.group(2), m_full.group(3)
        else:
            m_short = re.search(r"(\d{2})-(\d{2})-(\d{2})", name)
            if not m_short:
                return "", "", ""
            yy, mm, dd = m_short.group(1), m_short.group(2), m_short.group(3)
            yyyy = f"20{yy}"

        final_name = f"{yyyy[2:]}-{mm}-{dd}{ext}"
        return f"{yyyy}-{mm}-{dd}", yyyy, final_name

    def ensure_year_organized(self, account_dir: str) -> None:
        entries = [e for e in os.listdir(account_dir) if os.path.isdir(os.path.join(account_dir, e))]
        if any(re.fullmatch(r"\d{4}", e) for e in entries):
            return

        files = [f for f in os.listdir(account_dir) if os.path.isfile(os.path.join(account_dir, f))]
        for f in files:
            date_str, year_folder, _ = self.extract_date_targets(f)
            if not date_str:
                continue
            year_dir = os.path.join(account_dir, year_folder)
            os.makedirs(year_dir, exist_ok=True)
            try:
                shutil.move(os.path.join(account_dir, f), os.path.join(year_dir, f))
            except Exception:
                pass

    # ---------- Run & Progress ----------

    def start_organization(self):
        excel_tooltip = self.excel_path_edit.toolTip()
        excel_path = excel_tooltip if excel_tooltip else self.excel_path_edit.text().strip()

        source_tooltip = self.source_path_edit.toolTip()
        source_path = source_tooltip if source_tooltip else self.source_path_edit.text().strip()

        dest_tooltip = self.dest_path_edit.toolTip()
        dest_root = dest_tooltip if dest_tooltip else self.dest_path_edit.text().strip()

        if not excel_path or not source_path or not dest_root:
            QMessageBox.warning(self, "Missing Information",
                                "Please select Excel file, source folder, and destination folder")
            return

        if not self.mapping:
            self.load_excel_data(excel_path)
            if not self.mapping:
                return

        # Disable controls
        self.organize_btn.setEnabled(False)
        self.organize_btn.setText("Processing...")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.results_text.clear()

        # Start worker thread
        self.worker_thread = FileOrganizerWorker(self, source_path, dest_root)
        self.worker_thread.progress_updated.connect(self.update_progress_text)
        self.worker_thread.progress_percent.connect(self.update_progress_bar)
        self.worker_thread.finished.connect(self.organization_finished)
        self.worker_thread.error_occurred.connect(self.organization_error)
        self.worker_thread.start()

        self.add_result("🚀 Starting file organization...")

    def update_progress_text(self, message):
        self.add_result(message)

    def update_progress_bar(self, value):
        self.progress_bar.setValue(max(0, min(100, int(value))))

    def organization_finished(self, results):
        self.organize_btn.setEnabled(True)
        self.organize_btn.setText("Execute")
        self.progress_bar.setValue(100)

        moved = results.get('moved', 0)
        skipped = results.get('skipped', 0)
        not_found = results.get('not_found', 0)
        total = results.get('total', 0)

        # Show totals at the top
        totals_msg = f"Moved: {moved} | Skipped: {skipped} | Not Found: {not_found}"
        current_text = self.results_text.toPlainText()
        self.results_text.setPlainText(totals_msg + "\n" + "=" * 50 + "\n" + current_text)

        self.statusBar().showMessage(f"Completed. Moved: {moved}, Skipped: {skipped}, Not Found: {not_found}")
        QMessageBox.information(self, "Success", f"Files have been successfully organized!\n\nMoved: {moved}\nSkipped: {skipped}\nNot Found: {not_found}")

        # Log to history
        self.append_history_entry(results)

    def organization_error(self, error_message):
        self.organize_btn.setEnabled(True)
        self.organize_btn.setText("Execute")
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
        total = results.get('total', 0)
        moved = results.get('moved', 0)
        skipped = results.get('skipped', 0)
        not_found = results.get('not_found', 0)
        failed = skipped + not_found
        summary = (f"{timestamp}  |  Total: {total}  |  "
                   f"✓ {moved}  |  ✗ {failed}")
        item = QListWidgetItem(summary)
        self.history_list.insertItem(0, item)

        # Save to disk
        self.history_items.insert(0, {
            "timestamp": timestamp,
            "total": total,
            "successful": moved,
            "failed": failed,
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
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history_items = json.load(f)
                # Populate UI
                for rec in reversed(self.history_items):
                    summary = (f"{rec['timestamp']}  |  Total: {rec['total']}  |  "
                               f"✓ {rec['successful']}  |  ✗ {rec['failed']}")
                    self.history_list.addItem(summary)
        except Exception:
            pass

    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history_items, f, indent=2)
        except Exception:
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
