import sys
import sqlite3

from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, \
    QVBoxLayout, QMessageBox

class GerenciamentoContatos(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('APP | GERENCIAR CONTATOS')
        self.setWindowIcon(QtGui.QIcon('images/icone.png'))
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("background-color: #EAECEE;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        self.lbl_nome = QLabel('NOME')
        self.lbl_nome.setStyleSheet("font-weight: bold;"
                                    "color: #2C3E50;")
        self.txt_nome = QLineEdit()
        self.lbl_sobrenome = QLabel('SOBRENOME')
        self.lbl_sobrenome.setStyleSheet("font-weight: bold;"
                                         "color: #2C3E50;")
        self.txt_sobrenome = QLineEdit()
        self.lbl_email = QLabel('E-MAIL')
        self.lbl_email.setStyleSheet("font-weight: bold;"
                                     "color: #2C3E50;")
        self.txt_email = QLineEdit()

        self.lbl_telefone = QLabel('TELEFONE')
        self.lbl_telefone.setStyleSheet("font-weight: bold;"
                                        "color: #2C3E50;")
        self.txt_telefone = QLineEdit()

        self.btn_salvar = QPushButton('Adicionar contato')
        self.btn_salvar.setStyleSheet("background-color: #A9DFBF;"
                                      "border-radius: 4px;"
                                      "border: 1px solid black;"
                                      "font-weight: bold;")
        self.btn_editar = QPushButton('Editar contato')
        self.btn_editar.setStyleSheet("background-color: #FFBD67;"
                                      "border-radius: 4px;"
                                      "border: 1px solid black;"
                                      "font-weight: bold")
        self.btn_remover = QPushButton('Excluir contato')
        self.btn_remover.setStyleSheet("background-color: #F5B7B1;"
                                       "border-radius: 4px;"
                                       "border: 1px solid black;"
                                       "font-weight: bold")
        self.btn_limpar_campos = QPushButton('Limpar campos')
        self.btn_limpar_campos.setStyleSheet("background-color: #A9CCE3;"
                                             "border-radius: 4px;"
                                             "border: 1px solid black;"
                                             "font-weight: bold")

        self.lst_contatos = QListWidget()
        self.lst_contatos.setStyleSheet("background-color: #F9F9F9;"
                                        "opacity: 0.5;")

        self.lst_contatos.itemClicked.connect(self.selecionar_contato)
        self.btn_editar.clicked.connect(self.editar_contato)
        self.btn_remover.clicked.connect(self.validar_remocao)
        self.btn_limpar_campos.clicked.connect(self.limpar_campos)

        self.layout.addWidget(self.lbl_nome)
        self.layout.addWidget(self.txt_nome)
        self.layout.addWidget(self.lbl_sobrenome)
        self.layout.addWidget(self.txt_sobrenome)
        self.layout.addWidget(self.lbl_email)
        self.layout.addWidget(self.txt_email)
        self.layout.addWidget(self.lbl_telefone)
        self.layout.addWidget(self.txt_telefone)
        self.layout.addWidget(self.lst_contatos)
        self.layout.addWidget(self.btn_salvar)
        self.layout.addWidget(self.btn_editar)
        self.layout.addWidget(self.btn_remover)
        self.layout.addWidget(self.btn_limpar_campos)

        self.criar_banco()
        self.carregar_contatos()
        self.contato_selecionado = None
        self.btn_salvar.clicked.connect(self.salvar_contato)


    def criar_banco(self):
        conexao = sqlite3.connect('contatos.db')
        cursor = conexao.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS contatos (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         nome TEXT,
                         sobrenome TEXT,
                         email TEXT,
                         telefone TEXT
                         )
        ''')
        conexao.close()


    def salvar_contato(self):
        nome = self.txt_nome.text()
        sobrenome = self.txt_sobrenome.text()
        email = self.txt_email.text()
        telefone = self.txt_telefone.text()
        if nome and sobrenome and email and telefone:
            conexao = sqlite3.connect('contatos.db')
            cursor = conexao.cursor()
            if self.contato_selecionado is None:
                cursor.execute('''
                    INSERT INTO contatos (nome, sobrenome, email, telefone)
                    VALUES (?, ?, ?, ?)
                ''', (nome, sobrenome, email, telefone))
            else:
                cursor.execute('''
                    UPDATE contatos SET nome = ?, sobrenome = ?, email = ?, telefone = ? WHERE ID = ?
                ''', (nome, sobrenome, email, telefone, self.contato_selecionado['id']))
            conexao.commit()
            conexao.close()

            self.carregar_contatos()
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.txt_telefone.clear()
            self.contato_selecionado = None

        else:
            QMessageBox().warning(self,'Aviso','Preencha todos os dados!')


    def carregar_contatos(self):
        self.lst_contatos.clear()
        conexao = sqlite3.connect('contatos.db')
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT id, nome, sobrenome, email, telefone FROM contatos ORDER BY nome ASC
        ''')
        contatos = cursor.fetchall()
        conexao.close()

        for contato in contatos:
            id_contato, nome, sobrenome, email, telefone = contato
            self.lst_contatos.addItem(f'{id_contato} | {nome} {sobrenome} | {email} | {telefone}')


    def selecionar_contato(self, item):
        if self.btn_editar.text() == 'Cancelar':
            self.btn_editar.setText('Editar contato')
            self.btn_salvar.setText('Adicionar contato')

        self.contato_selecionado = {
            'id' : item.text().split()[0],
            'nome' : self.txt_nome.text(),
            'sobrenome' : self.txt_sobrenome.text(),
            'email' : self.txt_email.text(),
            'telefone': self.txt_telefone.text()
        }
        conexao = sqlite3.connect('contatos.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT nome, sobrenome, email, telefone FROM contatos'
                       ' WHERE id = ?', [self.contato_selecionado['id']])
        contato = cursor.fetchone()
        conexao.close()

        if contato:
            nome, sobrenome, email, telefone = contato
            self.txt_nome.setText(nome)
            self.txt_sobrenome.setText(sobrenome)
            self.txt_email.setText(email)
            self.txt_telefone.setText(telefone)


    def editar_contato(self):
        if self.btn_editar.text() == 'Editar contato':
            if self.contato_selecionado is not None:
                conexao = sqlite3.connect('contatos.db')
                cursor = conexao.cursor()
                cursor.execute('SELECT nome, sobrenome, email, telefone FROM contatos'
                               ' WHERE id = ?', [self.contato_selecionado['id']])
                contato = cursor.fetchone()
                conexao.close()

                if contato:
                    nome, sobrenome, email, telefone = contato
                    self.txt_nome.setText(nome)
                    self.txt_sobrenome.setText(sobrenome)
                    self.txt_email.setText(email)
                    self.txt_telefone.setText(telefone)
                    self.btn_editar.setText('Cancelar')
                    self.btn_salvar.setText('Atualizar contato')

        else:
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.txt_telefone.clear()
            self.btn_editar.setText('Editar contato')
            self.btn_salvar.setText('Adicionar contato')
            self.contato_selecionado = None


    def validar_remocao(self):
        if self.contato_selecionado is None:
            QMessageBox().warning(self, 'Aviso', 'Selecione um contato!')
        else:
                mensagem = QMessageBox()
                mensagem.setWindowTitle('Atenção')
                mensagem.setWindowIcon(QtGui.QIcon('images/alerta.png'))
                mensagem.setText('Tem certeza que deseja remover o contato?')
                botao_sim = mensagem.addButton('Sim', QMessageBox.YesRole)
                botao_nao = mensagem.addButton('Não', QMessageBox.NoRole)
                mensagem.setIcon(QMessageBox.Question)
                mensagem.exec()

                if mensagem.clickedButton() == botao_sim:
                    self.remover_contato()


    def remover_contato(self):
        if self.contato_selecionado is not None:
            conexao = sqlite3.connect('contatos.db')
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM contatos WHERE id = ?', [self.contato_selecionado['id']])
            conexao.commit()
            conexao.close()
            self.carregar_contatos()
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.txt_telefone.clear()
            self.contato_selecionado = None


    def limpar_campos(self):
        if self.btn_editar.text() == 'Cancelar':
            self.btn_editar.setText('Editar contato')
            self.btn_salvar.setText('Adicionar contato')

        self.txt_nome.clear()
        self.txt_sobrenome.clear()
        self.txt_email.clear()
        self.txt_telefone.clear()
        self.contato_selecionado = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GerenciamentoContatos()
    window.show()
    sys.exit(app.exec())