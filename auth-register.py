# -*- coding: utf-8 -*-

import sys
import psycopg2
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                            QMessageBox, QFrame, QGraphicsDropShadowEffect,
                            QFormLayout)
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPen, QPainterPath
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt, QRectF

class RoundedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            border: none;
            background-color: transparent;
            color: #2c3e50;
            padding: 8px;
        """)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Créer un chemin arrondi pour le fond
        path = QPainterPath()
        # Utiliser QRectF au lieu de QRect
        rect = QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, 10, 10)
        
        # Dessiner le fond
        painter.fillPath(path, QColor("#ffffff"))
        
        # Dessiner la bordure
        pen = QPen(QColor("#c8d6e1"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Appeler la méthode paintEvent de QLineEdit pour dessiner le texte
        super().paintEvent(event)

class StyledPushButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.lighter_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darker_color(color)};
            }}
        """)
        
        # Ajouter une ombre
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
    def lighter_color(self, color):
        """Retourne une version plus claire de la couleur"""
        # Couleur un peu plus claire pour hover
        if color == "#4CA1AF":  # Bleu principal
            return "#5DBBCC"
        elif color == "#e74c3c":  # Rouge pour reset
            return "#f15849"
        return color
    
    def darker_color(self, color):
        """Retourne une version plus foncée de la couleur"""
        # Couleur un peu plus foncée pour pressed
        if color == "#4CA1AF":  # Bleu principal
            return "#3A8A98"
        elif color == "#e74c3c":  # Rouge pour reset
            return "#d44231"
        return color


class CashierRegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Configuration de la fenêtre
        self.setWindowTitle("Centre Médical - Inscription Caissier")
        self.setMinimumSize(1000, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                color: #34495e;
                font-size: 14px;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #c8d6e5;
                border-radius: 8px;
                background-color: white;
                min-height: 25px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CA1AF;
            }
            #headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CA1AF, stop:1 #2C3E50);
                color: white;
                border-bottom: 1px solid #3A8A98;
            }
            #titleLabel {
                color: white;
                font-size: 26px;
                font-weight: bold;
            }
            #subtitleLabel {
                color: #b3d9e0;
                font-size: 16px;
            }
            #leftPanel {
                background-color: #34495e;
                border-radius: 8px;
                margin: 15px;
                padding: 15px;
            }
            #infoCard {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
            #formTitle {
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
                padding: 10px 0;
            }
            #noteLabel {
                color: #7f8c8d;
                font-style: italic;
                padding: 10px 0;
                font-size: 13px;
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # En-tête
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setMinimumHeight(100)
        header_layout = QVBoxLayout(header_frame)
        
        # Icône et titre dans un layout horizontal
        title_layout = QHBoxLayout()
        
        # Icône pour le titre (simulation)
        icon_label = QLabel()
        icon_label.setPixmap(self.create_medical_icon())
        icon_label.setFixedSize(60, 60)
        title_layout.addWidget(icon_label)
        
        # Titre et sous-titre dans un layout vertical
        title_box = QVBoxLayout()
        
        title_label = QLabel("Centre Médical CMA")
        title_label.setObjectName("titleLabel")
        title_box.addWidget(title_label)
        
        subtitle_label = QLabel("Système de Gestion - Inscription du Personnel")
        subtitle_label.setObjectName("subtitleLabel")
        title_box.addWidget(subtitle_label)
        
        title_layout.addLayout(title_box)
        title_layout.addStretch()
        
        header_layout.addLayout(title_layout)
        header_layout.setContentsMargins(25, 20, 25, 20)
        
        main_layout.addWidget(header_frame)
        
        # Contenu - Utilisation d'un splitter pour diviser l'écran
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Panneau gauche - Information décorative
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_panel.setFixedWidth(280)
        
        left_layout = QVBoxLayout(left_panel)
        
        # Logo
        logo_label = QLabel()
        logo_label.setPixmap(self.create_health_logo())
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFixedHeight(120)
        left_layout.addWidget(logo_label)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #4CA1AF; margin: 15px 0;")
        left_layout.addWidget(separator)
        
        # Texte d'information
        welcome_label = QLabel("Bienvenue au Système de Gestion")
        welcome_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(welcome_label)
        
        info_text = QLabel(
            "Ce formulaire vous permet d'enregistrer un nouveau caissier dans le système. "
            "Tous les champs marqués d'un * sont obligatoires.\n\n"
            "Une fois l'inscription terminée, le caissier pourra se connecter "
            "au système avec son email et son mot de passe."
        )
        info_text.setStyleSheet("color: #b3d9e6; line-height: 1.5; margin-top: 15px;")
        info_text.setWordWrap(True)
        left_layout.addWidget(info_text)
        
        # Image décorative
        image_label = QLabel()
        image_label.setPixmap(self.create_medical_illustration())
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(180)
        image_label.setStyleSheet("margin-top: 20px;")
        left_layout.addWidget(image_label)
        
        left_layout.addStretch()
        
        # Section de contact
        contact_label = QLabel("Besoin d'aide ?")
        contact_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(contact_label)
        
        contact_info = QLabel("Contact technique: support@pharmaplus.com")
        contact_info.setStyleSheet("color: #b3d9e0;")
        left_layout.addWidget(contact_info)
        
        content_layout.addWidget(left_panel)
        
        # Panneau droit - Formulaire
        right_panel = QFrame()
        right_panel.setObjectName("infoCard")
        
        # Ajouter une ombre au panneau droit
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 2)
        right_panel.setGraphicsEffect(shadow)
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        
        # Titre du formulaire
        form_title = QLabel("Inscription d'un Nouveau Caissier")
        form_title.setObjectName("formTitle")
        right_layout.addWidget(form_title)
        
        # Description
        description = QLabel("Veuillez remplir tous les champs requis pour créer un nouveau compte caissier.")
        description.setStyleSheet("color: #b3d9e0; margin-bottom: 25px;")
        right_layout.addWidget(description)
        
        # Formulaire d'inscription
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(20)
        form_layout.setHorizontalSpacing(30)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # Matricule
        matricule_label = QLabel("Matricule* :")
        self.employee_id_edit = RoundedLineEdit()
        self.employee_id_edit.setPlaceholderText("Ex: CA2025001")
        form_layout.addRow(matricule_label, self.employee_id_edit)
        
        # Prénom
        first_name_label = QLabel("Prénom* :")
        self.first_name_edit = RoundedLineEdit()
        self.first_name_edit.setPlaceholderText("Entrez le prénom")
        form_layout.addRow(first_name_label, self.first_name_edit)
        
        # Nom
        last_name_label = QLabel("Nom* :")
        self.last_name_edit = RoundedLineEdit()
        self.last_name_edit.setPlaceholderText("Entrez le nom")
        form_layout.addRow(last_name_label, self.last_name_edit)
        
        # Email
        email_label = QLabel("Email* :")
        self.email_edit = RoundedLineEdit()
        self.email_edit.setPlaceholderText("exemple@centremedical.com")
        form_layout.addRow(email_label, self.email_edit)
        
        # Mot de passe
        password_label = QLabel("Mot de passe* :")
        self.password_edit = RoundedLineEdit()
        self.password_edit.setPlaceholderText("Mot de passe sécurisé")
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow(password_label, self.password_edit)
        
        # Confirmation du mot de passe
        confirm_password_label = QLabel("Confirmer* :")
        self.confirm_password_edit = RoundedLineEdit()
        self.confirm_password_edit.setPlaceholderText("Confirmer le mot de passe")
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow(confirm_password_label, self.confirm_password_edit)
        
        right_layout.addLayout(form_layout)
        
        # Remarque sur la date d'inscription
        note_label = QLabel("Note: La date d'inscription avec jour, mois et année sera automatiquement enregistrée.")
        note_label.setObjectName("noteLabel")
        right_layout.addWidget(note_label)
        
        # Boutons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        self.reset_button = StyledPushButton("Réinitialiser", "#e74c3c")
        self.reset_button.setFixedSize(150, 45)
        self.reset_button.clicked.connect(self.reset_form)
        
        self.submit_button = StyledPushButton("Enregistrer", "#4CA1AF")
        self.submit_button.setFixedSize(150, 45)
        self.submit_button.clicked.connect(self.submit_registration)
        
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.submit_button)
        
        right_layout.addLayout(button_layout)
        
        content_layout.addWidget(right_panel)
        
        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
    
    def create_medical_icon(self):
        """Crée une icône médicale (simple croix)"""
        pixmap = QPixmap(60, 60)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dessiner un cercle blanc
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 56, 56)
        
        # Dessiner une croix médicale
        painter.setBrush(QColor("#4CA1AF"))
        painter.drawRect(18, 10, 24, 40)  # Rectangle vertical
        painter.drawRect(10, 18, 40, 24)  # Rectangle horizontal
        
        painter.end()
        return pixmap
    
    def create_health_logo(self):
        """Crée un logo pour le centre de santé"""
        pixmap = QPixmap(120, 120)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dessiner un cercle de fond
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(10, 10, 100, 100)
        
        # Dessiner un caducée stylisé (symbole médical simplifié)
        painter.setPen(QPen(QColor("#4CA1AF"), 6))
        painter.drawLine(60, 35, 60, 85)  # Ligne verticale
        
        # Dessiner des "serpents" stylisés
        path1 = QPainterPath()
        path1.moveTo(60, 35)
        path1.cubicTo(40, 45, 80, 55, 60, 65)
        
        path2 = QPainterPath()
        path2.moveTo(60, 65)
        path2.cubicTo(40, 75, 80, 85, 60, 95)
        
        painter.drawPath(path1)
        painter.drawPath(path2)
        
        painter.end()
        return pixmap
    
    def create_medical_illustration(self):
        """Crée une illustration simple pour le panneau latéral"""
        pixmap = QPixmap(200, 180)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fond
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(20, 20, 160, 140, 10, 10)
        
        # Ligne de vie (électrocardiogramme)
        painter.setPen(QPen(QColor("#4CA1AF"), 3))
        points = [
            QPoint(30, 90), QPoint(50, 90), QPoint(60, 70), 
            QPoint(70, 110), QPoint(80, 70), QPoint(90, 90),
            QPoint(110, 90), QPoint(120, 50), QPoint(130, 130),
            QPoint(140, 90), QPoint(170, 90)
        ]
        
        for i in range(len(points)-1):
            painter.drawLine(points[i], points[i+1])
        
        # Quelques icônes médicales stylisées
        painter.setBrush(QColor("#e74c3c"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(40, 40, 20, 20)  # Point rouge
        
        painter.setBrush(QColor("#3498db"))
        painter.drawRoundedRect(150, 40, 20, 20, 5, 5)  # Carré bleu
        
        painter.end()
        return pixmap
    
    def reset_form(self):
        # Réinitialise tous les champs
        self.employee_id_edit.clear()
        self.first_name_edit.clear()
        self.last_name_edit.clear()
        self.email_edit.clear()
        self.password_edit.clear()
        self.confirm_password_edit.clear()
    
    def submit_registration(self):
        # Validation des champs
        if not self.employee_id_edit.text():
            QMessageBox.warning(self, "Champ manquant", "Veuillez entrer le matricule du caissier.")
            return
        
        if not self.first_name_edit.text() or not self.last_name_edit.text():
            QMessageBox.warning(self, "Champs manquants", "Veuillez entrer le prénom et le nom.")
            return
        
        if not self.email_edit.text() or '@' not in self.email_edit.text():
            QMessageBox.warning(self, "Email invalide", "Veuillez entrer une adresse email valide.")
            return
        
        if not self.password_edit.text():
            QMessageBox.warning(self, "Mot de passe manquant", "Veuillez entrer un mot de passe.")
            return
        
        if self.password_edit.text() != self.confirm_password_edit.text():
            QMessageBox.warning(self, "Erreur de mot de passe", "Les mots de passe ne correspondent pas.")
            return
        
        # Récupération des données
        employee_id = self.employee_id_edit.text()
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()  # Dans une application réelle, il faudrait hasher ce mot de passe
        
        # Date d'inscription automatique
        registration_date = datetime.now()
        reg_day = registration_date.day
        reg_month = registration_date.month
        reg_year = registration_date.year
        
        # Connexion à PostgreSQL
        try:
            # Remplacez ces paramètres par vos informations de connexion
            conn = psycopg2.connect(
            host="localhost",
            database="pharmacy_management",
            user="postgres",
            password="pmceohamdev"
            )
            conn.set_client_encoding('UTF8')
            # Création d'un curseur
            cur = conn.cursor()
            
            # Préparation de la requête SQL
            query = """
                INSERT INTO cashiers (
                    employee_id, first_name, last_name, email, password,
                    registration_date, reg_day, reg_month, reg_year
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Exécution de la requête
            cur.execute(query, (
                employee_id, first_name, last_name, email, password,
                registration_date, reg_day, reg_month, reg_year
            ))
            
            # Validation de la transaction
            conn.commit()
            
            # Fermeture du curseur et de la connexion
            cur.close()
            conn.close()
            
            # Message de confirmation avec style
            success_msg = QMessageBox(self)
            success_msg.setWindowTitle("Enregistrement réussi")
            success_msg.setText(f"<h3>Inscription Complétée</h3>")
            success_msg.setInformativeText(
                f"Le caissier <b>{first_name} {last_name}</b> a été enregistré avec succès.<br><br>"
                f"<b>Date d'inscription:</b> {registration_date.strftime('%d/%m/%Y')}<br>"
                f"<b>Matricule:</b> {employee_id}"
            )
            success_msg.setIconPixmap(self.create_success_icon())
            success_msg.setStandardButtons(QMessageBox.Ok)
            success_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                }
                QPushButton {
                    background-color: #4CA1AF;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5DBBCC;
                }
            """)
            success_msg.exec_()
            
            # Réinitialisation du formulaire après l'inscription
            self.reset_form()
            
        except Exception as e:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle("Erreur de base de données")
            error_msg.setText("<h3>Erreur lors de l'enregistrement</h3>")
            error_msg.setInformativeText(f"Une erreur s'est produite lors de l'enregistrement:<br><br>{str(e)}")
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setStandardButtons(QMessageBox.Ok)
            error_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f5f7fa;
                }
                QLabel {
                    color: #2c3e50;
                }
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #f15849;
                }
            """)
            error_msg.exec_()
    
    def create_success_icon(self):
        """Crée une icône de succès"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Cercle vert
        painter.setBrush(QColor("#2ecc71"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 60, 60)
        
        # Coche blanche
        painter.setPen(QPen(QColor("white"), 4))
        painter.drawLine(16, 34, 28, 46)
        painter.drawLine(28, 46, 48, 20)
        
        painter.end()
        return pixmap


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CashierRegistrationWindow()
    window.show()
    sys.exit(app.exec_())