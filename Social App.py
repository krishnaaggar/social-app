import sys
import qtawesome as qta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, 
                             QScrollArea, QDialog, QLineEdit, QTextEdit, QMessageBox, QStackedWidget, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSlot, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont

class JobApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Job Board")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2C2F33; color: #FFFFFF;")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_page = QWidget()
        self.create_main_page()
        self.stacked_widget.addWidget(self.main_page)

    def create_main_page(self):
        main_layout = QVBoxLayout()

        # Scroll Area for Job Posts
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)

        # Adding some job posts
        job_posts = [
            {"title": "Need a Plumber urgently!", "author": "John Doe", "likes": 5, "time": "2m ago", "description": "Looking for an experienced plumber...", "tags": ["plumber"]},
            {"title": "Looking for a Cook", "author": "Jane Smith", "likes": 2, "time": "10m ago", "description": "Need a cook for my restaurant...", "tags": ["cook"]},
            {"title": "Electrician required", "author": "Mike Johnson", "likes": 3, "time": "1h ago", "description": "Need an electrician for home repairs...", "tags": ["electrician"]},
            {"title": "Gardener needed", "author": "Emily Davis", "likes": 4, "time": "3h ago", "description": "Looking for a gardener for my backyard...", "tags": ["gardener"]},
            {"title": "Cleaner wanted", "author": "Chris Brown", "likes": 1, "time": "5h ago", "description": "Need a cleaner for my apartment...", "tags": ["cleaner"]},
            {"title": "Carpenter job available", "author": "Anna White", "likes": 6, "time": "7h ago", "description": "Looking for a skilled carpenter...", "tags": ["carpenter"]},
            {"title": "Painter needed", "author": "David Wilson", "likes": 2, "time": "1d ago", "description": "Need a painter for house interior...", "tags": ["painter"]},
        ]

        self.job_posts = job_posts
        self.add_job_posts()

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # New Post Button
        new_post_button = QPushButton("New Post")
        new_post_button.setStyleSheet("background-color: #7289DA; color: #FFFFFF; padding: 10px; margin-top: 10px;")
        new_post_button.clicked.connect(self.new_post)
        main_layout.addWidget(new_post_button)

        self.main_page.setLayout(main_layout)

    def add_job_posts(self):
        for i, post in enumerate(self.job_posts):
            job_button = JobPostButton(post, self)
            job_button.clicked.connect(lambda checked, idx=i: self.show_job_details(idx))
            self.scroll_layout.addWidget(job_button)

    @pyqtSlot()
    def show_job_details(self, index):
        post = self.job_posts[index]
        details_page = JobDetailsPage(post, self)
        self.stacked_widget.addWidget(details_page)
        self.stacked_widget.setCurrentWidget(details_page)

    @pyqtSlot()
    def new_post(self):
        new_post_dialog = NewPostDialog(self)
        new_post_dialog.exec_()

class JobPostButton(QPushButton):
    def __init__(self, post, parent=None):
        super().__init__(parent)
        self.post = post
        self.setText(f"{post['title']} - {post['author']} - {post['time']}")
        self.setStyleSheet("""
            QPushButton {
                background-color: #4F545C; 
                color: #FFFFFF; 
                padding: 10px; 
                margin: 5px; 
                text-align: left;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5865F2;
            }
        """)
        self.setFont(QFont('Arial', 12))
        self.setCursor(Qt.PointingHandCursor)
        self.original_geometry = self.geometry()

        self.enterEvent = self.on_hover
        self.leaveEvent = self.on_leave

    def on_hover(self, event):
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(200)
        animation.setStartValue(self.geometry())
        animation.setEndValue(QRect(self.geometry().x() - 10, self.geometry().y() - 10, 
                                    self.geometry().width() + 20, self.geometry().height() + 20))
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start()

    def on_leave(self, event):
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(200)
        animation.setStartValue(self.geometry())
        animation.setEndValue(self.original_geometry)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start()

class JobDetailsPage(QWidget):
    def __init__(self, post, parent=None):
        super().__init__(parent)

        self.post = post
        self.parent = parent
        self.setStyleSheet("background-color: #2C2F33; color: #FFFFFF;")
        layout = QVBoxLayout()

        title = QLabel(post["title"])
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(title)

        description = QLabel(post["description"])
        description.setWordWrap(True)
        description.setStyleSheet("color: #BBBBBB; margin-top: 10px;")
        layout.addWidget(description)

        applicants_label = QLabel("Other Applicants:")
        applicants_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(applicants_label)

        # Placeholder for applicants list
        applicants = ["Alice Smith", "Bob Johnson", "Carol Williams"]
        for applicant in applicants:
            applicant_label = QLabel(applicant)
            applicant_label.setStyleSheet("color: #BBBBBB; margin-left: 10px;")
            layout.addWidget(applicant_label)

        message_label = QLabel("Message Employer:")
        message_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(message_label)

        self.message_input = QTextEdit()
        self.message_input.setStyleSheet("background-color: #23272A; color: #FFFFFF; padding: 10px;")
        layout.addWidget(self.message_input)

        send_button = QPushButton("Send")
        send_button.setStyleSheet("background-color: #7289DA; color: #FFFFFF; padding: 10px; margin-top: 10px;")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #7289DA; color: #FFFFFF; padding: 10px; margin-top: 10px;")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    @pyqtSlot()
    def send_message(self):
        message = self.message_input.toPlainText()
        print(f"Message sent to employer: {message}")
        QMessageBox.information(self, "Message Sent", "Your message has been sent to the employer.", QMessageBox.Ok)
        # Animation for message sent
        animation = QPropertyAnimation(self.message_input, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(QRect(self.message_input.geometry().x(), self.message_input.geometry().y(), 
                                      self.message_input.geometry().width(), self.message_input.geometry().height()))
        animation.setEndValue(QRect(self.message_input.geometry().x(), self.message_input.geometry().y(), 
                                    self.message_input.geometry().width(), 0))
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    @pyqtSlot()
    def go_back(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.main_page)

class NewPostDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("New Post")
        self.setGeometry(150, 150, 400, 300)
        self.setStyleSheet("background-color: #2C2F33; color: #FFFFFF;")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Job Title")
        self.title_input.setStyleSheet("background-color: #23272A; color: #FFFFFF; padding: 10px;")
        layout.addWidget(self.title_input)

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Your Name")
        self.author_input.setStyleSheet("background-color: #23272A; color: #FFFFFF; padding: 10px;")
        layout.addWidget(self.author_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Job Description")
        self.description_input.setStyleSheet("background-color: #23272A; color: #FFFFFF; padding: 10px;")
        layout.addWidget(self.description_input)

        post_button = QPushButton("Post")
        post_button.setStyleSheet("background-color: #7289DA; color: #FFFFFF; padding: 10px;")
        post_button.clicked.connect(self.post_job)
        layout.addWidget(post_button)

        self.setLayout(layout)

    @pyqtSlot()
    def post_job(self):
        title = self.title_input.text()
        author = self.author_input.text()
        description = self.description_input.toPlainText()

        if title and author and description:
            new_post = {"title": title, "author": author, "likes": 0, "time": "just now", "description": description, "tags": []}
            self.parent().job_posts.append(new_post)
            self.parent().add_job_posts()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "All fields are required.", QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JobApp()
    window.show()
    sys.exit(app.exec_())
