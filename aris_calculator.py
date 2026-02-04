#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARIS CALCULATOR
Une calculatrice complète avec interface graphique moderne.
Développée pour GitHub.
Auteur: [Votre nom]
"""

import tkinter as tk
from tkinter import font, ttk, messagebox
import math
import sys
import os

class ArisCalculator:
    """Classe principale de la calculatrice ARIS"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("ARIS CALCULATOR")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Configuration des couleurs
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#34495E',
            'accent': '#1ABC9C',
            'accent_hover': '#16A085',
            'text': '#ECF0F1',
            'text_dark': '#2C3E50',
            'display_bg': '#1A252F',
            'display_text': '#ECF0F1',
            'button_bg': '#34495E',
            'button_hover': '#4A6278',
            'operator_bg': '#1ABC9C',
            'operator_hover': '#16A085',
            'special_bg': '#E74C3C',
            'special_hover': '#C0392B'
        }
        
        # Variables
        self.current_input = ""
        self.result = ""
        self.history = []
        self.last_operation = ""
        self.is_result_displayed = False
        
        # Initialisation de l'interface
        self.setup_ui()
        
        # Bind des touches du clavier
        self.bind_keyboard()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        
        # Configuration de la fenêtre
        self.root.configure(bg=self.colors['primary'])
        
        # Création d'un style personnalisé
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cadre principal
        main_frame = tk.Frame(self.root, bg=self.colors['primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # En-tête avec le nom ARIS CALCULATOR
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame, 
            text="ARIS CALCULATOR", 
            font=('Helvetica', 28, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['primary']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Calculatrice scientifique complète",
            font=('Helvetica', 12),
            fg=self.colors['text'],
            bg=self.colors['primary']
        )
        subtitle_label.pack()
        
        # Cadre d'affichage
        display_frame = tk.Frame(main_frame, bg=self.colors['display_bg'], relief=tk.FLAT, height=100)
        display_frame.pack(fill=tk.X, pady=(0, 20))
        display_frame.pack_propagate(False)
        
        # Affichage de l'historique
        self.history_label = tk.Label(
            display_frame,
            text="",
            font=('Helvetica', 12),
            fg=self.colors['text'],
            bg=self.colors['display_bg'],
            anchor=tk.E,
            padx=20
        )
        self.history_label.pack(fill=tk.X, pady=(10, 0))
        
        # Affichage principal
        self.display_label = tk.Label(
            display_frame,
            text="0",
            font=('Helvetica', 32, 'bold'),
            fg=self.colors['display_text'],
            bg=self.colors['display_bg'],
            anchor=tk.E,
            padx=20,
            pady=(0, 10)
        )
        self.display_label.pack(fill=tk.X, expand=True)
        
        # Cadre des boutons
        buttons_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuration des boutons
        buttons_layout = [
            [
                ('C', self.clear_all, 'special'),
                ('CE', self.clear_entry, 'special'),
                ('⌫', self.backspace, 'special'),
                ('÷', lambda: self.add_operator('/'), 'operator')
            ],
            [
                ('x²', self.square, 'function'),
                ('√', self.square_root, 'function'),
                ('%', self.percentage, 'function'),
                ('×', lambda: self.add_operator('*'), 'operator')
            ],
            [
                ('7', lambda: self.add_digit('7'), 'digit'),
                ('8', lambda: self.add_digit('8'), 'digit'),
                ('9', lambda: self.add_digit('9'), 'digit'),
                ('-', lambda: self.add_operator('-'), 'operator')
            ],
            [
                ('4', lambda: self.add_digit('4'), 'digit'),
                ('5', lambda: self.add_digit('5'), 'digit'),
                ('6', lambda: self.add_digit('6'), 'digit'),
                ('+', lambda: self.add_operator('+'), 'operator')
            ],
            [
                ('1', lambda: self.add_digit('1'), 'digit'),
                ('2', lambda: self.add_digit('2'), 'digit'),
                ('3', lambda: self.add_digit('3'), 'digit'),
                ('=', self.calculate, 'equals')
            ],
            [
                ('±', self.negate, 'function'),
                ('0', lambda: self.add_digit('0'), 'digit'),
                ('.', self.add_decimal, 'digit'),
                ('π', self.add_pi, 'function')
            ]
        ]
        
        # Création des boutons
        for row_idx, row in enumerate(buttons_layout):
            row_frame = tk.Frame(buttons_frame, bg=self.colors['primary'])
            row_frame.pack(fill=tk.BOTH, expand=True, pady=2)
            
            for col_idx, (text, command, btn_type) in enumerate(row):
                # Détermination de la couleur en fonction du type de bouton
                if btn_type == 'digit':
                    bg_color = self.colors['button_bg']
                    hover_color = self.colors['button_hover']
                elif btn_type == 'operator':
                    bg_color = self.colors['operator_bg']
                    hover_color = self.colors['operator_hover']
                elif btn_type == 'function':
                    bg_color = self.colors['secondary']
                    hover_color = self.colors['button_hover']
                elif btn_type == 'special':
                    bg_color = self.colors['special_bg']
                    hover_color = self.colors['special_hover']
                else:  # equals
                    bg_color = self.colors['accent']
                    hover_color = self.colors['accent_hover']
                
                # Création du bouton
                btn = tk.Button(
                    row_frame,
                    text=text,
                    font=('Helvetica', 18, 'bold'),
                    bg=bg_color,
                    fg=self.colors['text'],
                    activebackground=hover_color,
                    activeforeground=self.colors['text'],
                    relief=tk.FLAT,
                    borderwidth=0,
                    command=command,
                    cursor='hand2'
                )
                btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
                
                # Effet de survol
                self.bind_hover_effect(btn, bg_color, hover_color)
        
        # Cadre des fonctions avancées
        advanced_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        advanced_frame.pack(fill=tk.X, pady=(15, 0))
        
        advanced_label = tk.Label(
            advanced_frame,
            text="Fonctions scientifiques :",
            font=('Helvetica', 10, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['primary']
        )
        advanced_label.pack(anchor=tk.W)
        
        # Boutons des fonctions scientifiques
        sci_buttons = [
            ('sin', self.sine),
            ('cos', self.cosine),
            ('tan', self.tangent),
            ('log', self.logarithm),
            ('ln', self.natural_log),
            ('x!', self.factorial),
            ('(', lambda: self.add_parenthesis('(')),
            (')', lambda: self.add_parenthesis(')')),
            ('x^y', self.power),
            ('1/x', self.reciprocal)
        ]
        
        sci_frame = tk.Frame(advanced_frame, bg=self.colors['primary'])
        sci_frame.pack(fill=tk.X, pady=(5, 0))
        
        for i, (text, command) in enumerate(sci_buttons):
            btn = tk.Button(
                sci_frame,
                text=text,
                font=('Helvetica', 10),
                bg=self.colors['secondary'],
                fg=self.colors['text'],
                activebackground=self.colors['button_hover'],
                activeforeground=self.colors['text'],
                relief=tk.FLAT,
                borderwidth=0,
                command=command,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
            self.bind_hover_effect(btn, self.colors['secondary'], self.colors['button_hover'])
        
        # Barre de statut
        status_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="ARIS CALCULATOR - Prêt",
            font=('Helvetica', 9),
            fg=self.colors['text'],
            bg=self.colors['secondary']
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Menu
        self.create_menu()
    
    def bind_hover_effect(self, widget, normal_color, hover_color):
        """Ajoute un effet de survol aux boutons"""
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_color))
    
    def create_menu(self):
        """Crée le menu de l'application"""
        menubar = tk.Menu(self.root, bg=self.colors['secondary'], fg=self.colors['text'])
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['button_bg'], fg=self.colors['text'])
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau calcul", command=self.clear_all, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Historique", command=self.show_history)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Menu Édition
        edit_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['button_bg'], fg=self.colors['text'])
        menubar.add_cascade(label="Édition", menu=edit_menu)
        edit_menu.add_command(label="Copier", command=self.copy_result, accelerator="Ctrl+C")
        edit_menu.add_command(label="Coller", command=self.paste_from_clipboard, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Effacer l'historique", command=self.clear_history)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['button_bg'], fg=self.colors['text'])
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=self.show_about)
        help_menu.add_command(label="Raccourcis clavier", command=self.show_shortcuts)
    
    def bind_keyboard(self):
        """Lie les touches du clavier aux fonctions"""
        self.root.bind('<Key>', self.key_press)
        
        # Raccourcis spécifiques
        self.root.bind('<Control-n>', lambda e: self.clear_all())
        self.root.bind('<Control-N>', lambda e: self.clear_all())
        self.root.bind('<Control-c>', lambda e: self.copy_result())
        self.root.bind('<Control-C>', lambda e: self.copy_result())
        self.root.bind('<Control-v>', lambda e: self.paste_from_clipboard())
        self.root.bind('<Control-V>', lambda e: self.paste_from_clipboard())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-Q>', lambda e: self.root.quit())
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
    
    def key_press(self, event):
        """Gère les touches du clavier"""
        key = event.char
        
        if key.isdigit():
            self.add_digit(key)
        elif key == '.':
            self.add_decimal()
        elif key in '+-*/':
            self.add_operator(key)
        elif key == '(' or key == ')':
            self.add_parenthesis(key)
        elif key == '\r':  # Enter
            self.calculate()
    
    def update_display(self):
        """Met à jour l'affichage"""
        display_text = self.current_input if self.current_input else "0"
        
        # Limite la longueur de l'affichage
        if len(display_text) > 30:
            display_text = display_text[:27] + "..."
        
        self.display_label.config(text=display_text)
        
        # Met à jour l'historique
        if self.last_operation:
            self.history_label.config(text=self.last_operation)
    
    def add_digit(self, digit):
        """Ajoute un chiffre à l'entrée actuelle"""
        if self.is_result_displayed:
            self.current_input = ""
            self.is_result_displayed = False
        
        if digit == '0' and (not self.current_input or self.current_input == '0'):
            return
            
        if self.current_input == '0':
            self.current_input = digit
        else:
            self.current_input += digit
        
        self.update_display()
        self.status_label.config(text=f"Saisie: {self.current_input}")
    
    def add_decimal(self):
        """Ajoute un point décimal"""
        if self.is_result_displayed:
            self.current_input = ""
            self.is_result_displayed = False
        
        if not self.current_input:
            self.current_input = "0."
        elif '.' not in self.current_input:
            self.current_input += '.'
        
        self.update_display()
    
    def add_operator(self, operator):
        """Ajoute un opérateur"""
        if self.is_result_displayed:
            self.current_input = self.result
            self.is_result_displayed = False
        
        if not self.current_input:
            self.current_input = "0"
        
        # Remplacer le dernier opérateur si nécessaire
        if self.current_input and self.current_input[-1] in '+-*/':
            self.current_input = self.current_input[:-1]
        
        # Remplacer l'opérateur d'affichage
        display_operator = operator
        if operator == '*':
            display_operator = '×'
        elif operator == '/':
            display_operator = '÷'
        
        self.current_input += operator
        self.update_display()
    
    def add_parenthesis(self, parenthesis):
        """Ajoute une parenthèse"""
        if self.is_result_displayed:
            self.current_input = ""
            self.is_result_displayed = False
        
        self.current_input += parenthesis
        self.update_display()
    
    def calculate(self):
        """Effectue le calcul"""
        if not self.current_input:
            return
        
        try:
            # Prépare l'expression pour l'évaluation
            expression = self.current_input
            
            # Remplace les symboles d'affichage
            expression = expression.replace('×', '*').replace('÷', '/')
            
            # Évalue l'expression
            result = eval(expression, {"__builtins__": None}, {
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log10,
                'ln': math.log,
                'pi': math.pi,
                'e': math.e
            })
            
            # Formate le résultat
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    # Limite les décimales
                    result = round(result, 10)
            
            self.result = str(result)
            self.last_operation = f"{self.current_input} = {self.result}"
            self.history.append(self.last_operation)
            
            self.current_input = self.result
            self.is_result_displayed = True
            
            self.update_display()
            self.status_label.config(text=f"Résultat: {self.result}")
            
        except ZeroDivisionError:
            messagebox.showerror("Erreur", "Division par zéro impossible!")
            self.status_label.config(text="Erreur: Division par zéro")
        except Exception as e:
            messagebox.showerror("Erreur", f"Expression invalide: {str(e)}")
            self.status_label.config(text=f"Erreur: Expression invalide")
    
    def clear_all(self):
        """Efface tout"""
        self.current_input = ""
        self.result = ""
        self.last_operation = ""
        self.is_result_displayed = False
        self.update_display()
        self.history_label.config(text="")
        self.status_label.config(text="ARIS CALCULATOR - Prêt")
    
    def clear_entry(self):
        """Efface l'entrée actuelle"""
        self.current_input = ""
        self.is_result_displayed = False
        self.update_display()
    
    def backspace(self):
        """Efface le dernier caractère"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.update_display()
    
    def negate(self):
        """Change le signe du nombre actuel"""
        if self.current_input:
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def percentage(self):
        """Calcule le pourcentage"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                self.current_input = str(value / 100)
                self.update_display()
            except:
                pass
    
    def square(self):
        """Calcule le carré"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                self.current_input = str(value ** 2)
                self.update_display()
            except:
                pass
    
    def square_root(self):
        """Calcule la racine carrée"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                if value >= 0:
                    self.current_input = str(math.sqrt(value))
                    self.update_display()
                else:
                    messagebox.showerror("Erreur", "Racine carrée d'un nombre négatif impossible!")
            except:
                pass
    
    def add_pi(self):
        """Ajoute π à l'entrée"""
        if self.is_result_displayed:
            self.current_input = ""
            self.is_result_displayed = False
        
        self.current_input += str(math.pi)
        self.update_display()
    
    # Fonctions scientifiques
    def sine(self):
        """Calcule le sinus"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                # Conversion en radians si nécessaire
                result = math.sin(math.radians(value))
                self.current_input = str(round(result, 10))
                self.update_display()
            except:
                pass
    
    def cosine(self):
        """Calcule le cosinus"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                result = math.cos(math.radians(value))
                self.current_input = str(round(result, 10))
                self.update_display()
            except:
                pass
    
    def tangent(self):
        """Calcule la tangente"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                result = math.tan(math.radians(value))
                self.current_input = str(round(result, 10))
                self.update_display()
            except:
                pass
    
    def logarithm(self):
        """Calcule le logarithme base 10"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                if value > 0:
                    result = math.log10(value)
                    self.current_input = str(round(result, 10))
                    self.update_display()
                else:
                    messagebox.showerror("Erreur", "Logarithme d'un nombre ≤ 0 impossible!")
            except:
                pass
    
    def natural_log(self):
        """Calcule le logarithme naturel"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                if value > 0:
                    result = math.log(value)
                    self.current_input = str(round(result, 10))
                    self.update_display()
                else:
                    messagebox.showerror("Erreur", "Logarithme d'un nombre ≤ 0 impossible!")
            except:
                pass
    
    def factorial(self):
        """Calcule la factorielle"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                if value.is_integer() and value >= 0:
                    result = math.factorial(int(value))
                    self.current_input = str(result)
                    self.update_display()
                else:
                    messagebox.showerror("Erreur", "Factorielle d'un nombre non-entier ou négatif impossible!")
            except:
                pass
    
    def power(self):
        """Ajoute l'opérateur de puissance"""
        self.add_operator('**')
    
    def reciprocal(self):
        """Calcule l'inverse"""
        if self.current_input:
            try:
                value = float(eval(self.current_input))
                if value != 0:
                    self.current_input = str(1 / value)
                    self.update_display()
                else:
                    messagebox.showerror("Erreur", "Division par zéro!")
            except:
                pass
    
    # Fonctions du menu
    def copy_result(self):
        """Copie le résultat dans le presse-papier"""
        if self.result:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.result)
            self.status_label.config(text="Résultat copié dans le presse-papier")
    
    def paste_from_clipboard(self):
        """Colle depuis le presse-papier"""
        try:
            clipboard_content = self.root.clipboard_get()
            # Vérifie si le contenu est un nombre
            try:
                float(clipboard_content)
                self.current_input = clipboard_content
                self.update_display()
                self.status_label.config(text="Contenu collé depuis le presse-papier")
            except:
                messagebox.showerror("Erreur", "Le presse-papier ne contient pas un nombre valide!")
        except:
            messagebox.showerror("Erreur", "Impossible de lire le presse-papier!")
    
    def show_history(self):
        """Affiche l'historique des calculs"""
        if not self.history:
            messagebox.showinfo("Historique", "Aucun calcul dans l'historique.")
            return
        
        history_text = "Historique des calculs:\n\n"
        for i, calc in enumerate(self.history[-10:]):  # 10 derniers calculs
            history_text += f"{i+1}. {calc}\n"
        
        messagebox.showinfo("Historique", history_text)
    
    def clear_history(self):
        """Efface l'historique"""
        self.history = []
        self.status_label.config(text="Historique effacé")
    
    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        about_text = """
ARIS CALCULATOR
Version 1.0

Une calculatrice complète avec fonctions scientifiques.
Développée en Python avec Tkinter.

Fonctionnalités:
- Opérations basiques (+, -, ×, ÷)
- Fonctions scientifiques (sin, cos, tan, log, ln, etc.)
- Historique des calculs
- Raccourcis clavier
- Interface moderne et élégante

Développée pour GitHub.
© 2023 - Tous droits réservés.
        """
        messagebox.showinfo("À propos d'ARIS CALCULATOR", about_text)
    
    def show_shortcuts(self):
        """Affiche les raccourcis clavier"""
        shortcuts = """
RACCOURCIS CLAVIER:

Basiques:
  Chiffres (0-9) : Saisie des chiffres
  . : Point décimal
  + - * / : Opérateurs
  ( ) : Parenthèses
  Entrée : Calculer
  Échap : Effacer tout
  Retour arrière : Effacer dernier caractère

Contrôle:
  Ctrl+N : Nouveau calcul
  Ctrl+C : Copier le résultat
  Ctrl+V : Coller depuis le presse-papier
  Ctrl+Q : Quitter l'application
        """
        messagebox.showinfo("Raccourcis clavier", shortcuts)


def main():
    """Fonction principale"""
    root = tk.Tk()
    
    # Centrer la fenêtre
    window_width = 500
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Création de l'application
    app = ArisCalculator(root)
    
    # Lancement de la boucle principale
    root.mainloop()


if __name__ == "__main__":
    main()
