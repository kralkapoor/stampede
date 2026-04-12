"""Processing dialog with background worker thread.

Uses the Strategy pattern: accepts any callable (the strategy) and runs it in
a background QThread, keeping the GUI responsive while providing visual feedback.
The caller decides what work to do; this dialog only handles presentation.
"""

from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import QDialog, QLabel, QMessageBox, QVBoxLayout


class ProcessingWorker(QThread):
    """Runs a callback in a background thread, emitting signals on completion."""

    # Signals are used instead of returning from run() because Qt requires all
    # widget updates to happen on the main thread. Signals are automatically
    # marshalled across threads by Qt's event loop, making this thread-safe.
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def run(self):
        try:
            result = self.callback()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ProcessingDialog(QDialog):
    """Modal dialog that shows animated progress while a callback runs in a background thread."""

    def __init__(self, parent, title: str, message: str, callback):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(300, 100)
        self.setModal(True)

        # Stored on the dialog so the caller can inspect them after exec() returns,
        # since exec() only returns Accepted/Rejected — not the actual data.
        self.result = None
        self.error_message = None
        self._dot_count = 0

        layout = QVBoxLayout(self)

        self._message_label = QLabel(message)
        self._message_label.setStyleSheet("font-size: 12pt; color: blue;")
        layout.addWidget(self._message_label)

        self._progress_label = QLabel("Processing")
        self._progress_label.setStyleSheet("font-size: 10pt;")
        layout.addWidget(self._progress_label)

        # QTimer runs on the main thread's event loop, so it's safe to update
        # widgets directly. A second thread (like the old tkinter approach) would
        # need cross-thread synchronisation for something this simple.
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(500)

        self._worker = ProcessingWorker(callback)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _animate(self):
        self._dot_count = (self._dot_count + 1) % 4
        self._progress_label.setText("Processing" + "." * self._dot_count)

    def _on_finished(self, result):
        self._timer.stop()
        self.result = result
        self.accept()

    def _on_error(self, error_message: str):
        self._timer.stop()
        self.error_message = error_message
        self.reject()

    def closeEvent(self, event):
        if self._worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Processing in progress",
                "Processing is still running. Are you sure you want to close?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self._worker.wait()
                super().closeEvent(event)
            else:
                event.ignore()
        else:
            super().closeEvent(event)
