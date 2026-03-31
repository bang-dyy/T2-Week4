#---------------------------------------------------------------- #
# NAMA  : [Didy Ardiyanto]
# NIM   : [F1D02310046]
# KELAS : [C]
#---------------------------------------------------------------- #
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence


class KalkulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator")
        self.setFixedSize(400, 420)
        self.setStyleSheet(self._main_style())
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        body = QWidget()
        body.setObjectName("body")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(24, 20, 24, 20)
        body_layout.setSpacing(8)

        body_layout.addWidget(self._label("Angka Pertama"))
        self.input_a = QLineEdit()
        self.input_a.setObjectName("inputField")
        body_layout.addWidget(self.input_a)

        self.err_a = QLabel("⚠ Input harus berupa angka")
        self.err_a.setObjectName("errorMsg")
        self.err_a.hide()
        body_layout.addWidget(self.err_a)

        body_layout.addSpacing(4)

        body_layout.addWidget(self._label("Operasi"))
        self.combo = QComboBox()
        self.combo.setObjectName("operasiCombo")
        self.combo.addItems(["+ Tambah", "− Kurang", "× Kali", "÷ Bagi"])
        body_layout.addWidget(self.combo)

        body_layout.addSpacing(4)

        body_layout.addWidget(self._label("Angka Kedua"))
        self.input_b = QLineEdit()
        self.input_b.setObjectName("inputField")
        body_layout.addWidget(self.input_b)

        self.err_b = QLabel("⚠ Input harus berupa angka")
        self.err_b.setObjectName("errorMsg")
        self.err_b.hide()
        body_layout.addWidget(self.err_b)

        body_layout.addSpacing(10)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.btn_hitung = QPushButton("Hitung (Enter)")
        self.btn_hitung.setObjectName("btnHitung")
        self.btn_hitung.setEnabled(False)
        self.btn_hitung.setShortcut(QKeySequence(Qt.Key_Return))

        self.btn_clear = QPushButton("Clear (Esc)")
        self.btn_clear.setObjectName("btnClear")
        self.btn_clear.setShortcut(QKeySequence(Qt.Key_Escape))

        btn_row.addWidget(self.btn_hitung)
        btn_row.addWidget(self.btn_clear)
        body_layout.addLayout(btn_row)

        body_layout.addSpacing(10)

        self.result_label = QLabel("Hasil: —")
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignCenter)
        body_layout.addWidget(self.result_label)

        self.err_global = QLabel("⚠ Input tidak valid")
        self.err_global.setObjectName("errorGlobal")
        self.err_global.hide()
        body_layout.addWidget(self.err_global)

        body_layout.addStretch()
        root.addWidget(body)

    def _label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("fieldLabel")
        return lbl

    def _connect_signals(self):
        self.input_a.textChanged.connect(self._validate)
        self.input_b.textChanged.connect(self._validate)
        self.btn_hitung.clicked.connect(self._hitung)
        self.btn_clear.clicked.connect(self._clear)

    def _is_valid_number(self, text):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def _validate(self):
        a_text = self.input_a.text().strip()
        b_text = self.input_b.text().strip()

        a_empty = not bool(a_text)
        b_empty = not bool(b_text)

        a_ok = self._is_valid_number(a_text) if not a_empty else True
        b_ok = self._is_valid_number(b_text) if not b_empty else True

        self._set_field_state(self.input_a, a_ok)
        self._set_field_state(self.input_b, b_ok)

        self.err_a.setVisible(not a_empty and not a_ok)
        self.err_b.setVisible(not b_empty and not b_ok)

        both_valid = (not a_empty and not b_empty and
                      self._is_valid_number(a_text) and
                      self._is_valid_number(b_text))
        self.btn_hitung.setEnabled(both_valid)

        any_input = not a_empty or not b_empty
        self.err_global.setVisible(any_input and not both_valid)

    def _set_field_state(self, field, valid):
        field.setProperty("invalid", not valid)
        field.style().unpolish(field)
        field.style().polish(field)

    def _hitung(self):
        try:
            a = float(self.input_a.text().strip())
            b = float(self.input_b.text().strip())
            op = self.combo.currentText()

            if "+" in op:
                result, sym = a + b, "+"
            elif "−" in op:
                result, sym = a - b, "−"
            elif "×" in op:
                result, sym = a * b, "×"
            elif "÷" in op:
                if b == 0:
                    QMessageBox.critical(self, "Error", "Tidak dapat membagi dengan nol!")
                    return
                result, sym = a / b, "÷"
            else:
                return

            result_str = str(int(result)) if result == int(result) else f"{result:g}"
            self.result_label.setText(f"Hasil: {a:g} {sym} {b:g} = {result_str}")
        except Exception:
            pass

    def _clear(self):
        self.input_a.clear()
        self.input_b.clear()
        self.combo.setCurrentIndex(0)
        self.result_label.setText("Hasil: —")
        self.err_a.hide()
        self.err_b.hide()
        self.err_global.hide()
        self._set_field_state(self.input_a, True)
        self._set_field_state(self.input_b, True)
        self.btn_hitung.setEnabled(False)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Konfirmasi Keluar",
            "Apakah Anda yakin ingin menutup aplikasi?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        event.accept() if reply == QMessageBox.Yes else event.ignore()

    def _main_style(self):
        return """
        QMainWindow {
            background-color: #f0f2f5;
        }

        QWidget#body {
            background-color: #ffffff;
            border: 1px solid #d0d7de;
            border-radius: 8px;
        }

        QLabel#fieldLabel {
            color: #24292f;
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 500;
        }

        QLineEdit#inputField {
            border: 1.5px solid #d0d7de;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
            color: #24292f;
        }
        QLineEdit#inputField:focus {
            border: 1.5px solid #0969da;
        }
        QLineEdit#inputField[invalid="true"] {
            border: 1.5px solid #cf222e;
            background-color: #fff8f8;
        }

        QComboBox#operasiCombo {
            border: 1.5px solid #d0d7de;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }

        QLabel#errorMsg, QLabel#errorGlobal {
            color: #cf222e;
            font-size: 11.5px;
        }

        QPushButton#btnHitung {
            border-radius: 6px;
            padding: 10px;
            font-weight: 600;
        }
        QPushButton#btnHitung:enabled {
            background-color: #1a2e4a;
            color: white;
        }
        QPushButton#btnHitung:disabled {
            background-color: #8b9299;
            color: #d8dde2;
        }

        QPushButton#btnClear {
            background-color: #cf222e;
            color: white;
            border-radius: 6px;
            padding: 10px;
        }

        QLabel#resultLabel {
            color: #1a2e4a;
            font-size: 15px;
            font-weight: bold;
            padding-top: 10px;
            border-top: 1px solid #eaeef2;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = KalkulatorApp()
    window.show()
    sys.exit(app.exec_())