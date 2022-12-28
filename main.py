from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QFileDialog, QMainWindow, QWidget, QMessageBox
from login import Ui_Login
from ui_main import Ui_MainWindow
import sys
import webbrowser
from comandos import *
from xml_files import *
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt





class login(QWidget, Ui_Login):
    def __init__(self) -> None:
        super(login, self).__init__()

        #Checa login e senha usando a tabela vendedor do bando de dados
        self.tentativas = 0
        self.setupUi(self)
        self.setWindowTitle("Login do Sistema")
        self.btn_login.clicked.connect(self.checklogin)
        

    def checklogin(self):
        try:
            self.users = vendedor()
            autenticado = self.users.check(self.txtuser.text(), self.txtpass.text())

            if autenticado == "Acesso concedido":
                self.w = MainWindow()
                self.w.show()
                self.close()

            if autenticado == "Acesso negado":
                if self.tentativas < 3:
                    msg = QMessageBox()
                    msg.setWindowTitle("Erro ao acessar")
                    msg.setText("Login ou senha incorretas")
                    msg.exec()
                    self.tentativas +=1

                if self.tentativas == 3:
                    msg = QMessageBox()
                    msg.setWindowTitle("Erro ao acessar")
                    msg.setText("Você atingiu ao máximo de tentativas")
                    msg.exec()
                    sys.exit(0)

            else:
                msg = QMessageBox()
                msg.setWindowTitle("Login")
                msg.setText(autenticado)
                msg.exec()

        except:
            pass



class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Sistema de Gerenciamento")


        #Botões que levam às páginas
        self.btn_home.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pag_home))
        self.btn_tabelas.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pag_table))
        self.btn_add_client.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pag_cadastro))
        self.btn_add_prod.clicked.connect(lambda:self.Pages.setCurrentWidget(self.page_cad_prod))
        self.btn_contato.clicked.connect(lambda:self.Pages.setCurrentWidget(self.page_contato))
        self.btnc_importar.clicked.connect(lambda:self.Pages.setCurrentWidget(self.page_xml))
        self.btn_add_forn.clicked.connect(lambda:self.Pages.setCurrentWidget(self.page))
        self.btn_carrinho.clicked.connect(lambda:self.Pages.setCurrentWidget(self.page_2))

        #Botões de cadastrar
        self.btn_cadastrar.clicked.connect(self.sub_cliente)
        self.btn_cad_prod.clicked.connect(self.cadastrar_produto)
        self.btn_cad_forn.clicked.connect(self.cadastar_fornecedor)

        #Botões de redirecionamento para rede sociais na página: Contato
        self.btn_insta.clicked.connect(self.redirect_insta)
        self.btn_github.clicked.connect(self.redirect_git)
        self.btn_linkedin.clicked.connect(self.redirect_linkedin)

        #Tabelas
        self.tabela_estoque()
        self.tabela_cliente()
        self.tabela_fornecedor()
        self.tabela_venda()
        self.tabela_carrinho()

        #Botões de Carrinho e realizar venda
        self.btn_add_carrinho.clicked.connect(self.adicionar_carrinho)
        self.btn_limpar_venda_carrinho.clicked.connect(self.limpar_carrinho)
        self.btn_realizar_venda_2.clicked.connect(self.realizar_venda)
        self.pushButton.clicked.connect(self.atualizar_valor)

        #Botões de remover
        self.btn_rem_prod.clicked.connect(self.deletar_prod)
        self.btn_remover_forn.clicked.connect(self.deletar_fornecedor)
        self.btn_remover_client.clicked.connect(self.deletar_cliente)
        self.btn_remover_venda.clicked.connect(self.deletar_venda)
        self.btn_rem_item_carrinho.clicked.connect(self.rem_item_carrinho)

        #Botões de alterar
        self.btn_alterar_venda.clicked.connect(self.alterar_venda)
        self.btn_alterar_prod.clicked.connect(self.alterar_produto)
        self.btn_alterar_forn.clicked.connect(self.alterar_fornecedor)
        self.btn_alterar_cliente.clicked.connect(self.alterar_cliente)

        #Botões da página IMPORTAR
        self.btn_open.clicked.connect(self.open_path)
        self.btn_importar_xml.clicked.connect(self.import_xml)
        self.progressBar.setValue(0)

        #Botões gerar Excel
        self.btn_gerar_excel.clicked.connect(self.gerar_excel_estoque)
        self.btn_gerarexcel_venda.clicked.connect(self.gerar_excel_venda)

        #Botões gerar gráfico
        self.btn_gerar_graf.clicked.connect(self.gerar_graf_estoque)
        self.btn_gerargraf_venda.clicked.connect(self.gerar_graf_venda)

        #Botão para pesquisar CNPJ
        self.btn_pes_cnpj.clicked.connect(self.pesq_cpnj)




    #Funcões de redirecionamento
    def redirect_insta(self):

        webbrowser.open("https://www.instagram.com/_andrewjesus/")


    def redirect_git(self):

        webbrowser.open("https://github.com/andrewdejesus")


    def redirect_linkedin(self):

        webbrowser.open("https://www.linkedin.com/in/andrew-machado-dias-de-jesus-22420a18b/")


    #Funções da página IMPORTAR
    def open_path(self):
        try:
            self.path = QFileDialog.getOpenFileName (parent=None , caption=""  , directory=""  , filter="XML files (*.xml)")

            self.txt_selecionar_xml.setText(self.path[0])



        except:
            pass
    

    def import_xml(self):
        try:
            xml = read_xml(os.getcwd())
            all = xml.all_files()

            self.progressBar.setMaximum(len(all))
            cont = 1
            self.venda = venda()

            self.progressBar.setValue(cont)
            fulldataset = xml.nfe_data(self.txt_selecionar_xml.text())
            check = self.venda.check(fulldataset)
            if check == "Nota adicionada com sucesso":
                self.venda.insert_xml(fulldataset)
                cont+=1

                msg = QMessageBox()
                msg.setWindowTitle("Importando XML")
                msg.setText(check)
                msg.exec()
                self.progressBar.setValue(0)
                self.table_cliente.reset()
                self.tabela_cliente()
                self.table_venda.reset()
                self.tabela_venda()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Importando XML")
                msg.setText(check)
                msg.exec()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Importando XML")
            msg.setText("Por favor, insira um arquivo XML")
            msg.exec()


    #Funções de carrinho e realizar venda
    def tabela_carrinho(self):
        try:
            self.cliente = cliente()
            result = self.cliente.query("Select * from carrinho")
            
            self.tableWidget.setRowCount(len(result))

            total = 0

            for row, text in enumerate(result):
                
                valor = str(text[2])
                valor = valor.replace("R","")
                valor = valor.replace("$","")
                valor = valor.replace(",00","")
                valor = int(valor)
                total += (valor * int(text[3])) 
                for column, data in enumerate(text):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(data)))

            self.lineEdit_2.setText(str(total))
        except Exception as e:
            print(e)
        

    def rem_item_carrinho(self):
        try:
            self.venda = venda()
            msg = QMessageBox()
            msg.setWindowTitle("Deletar item do carrinho")
            msg.setText("Este item será excluído")
            msg.setInformativeText("Você deseja realmente excluir este Item do carrinho?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                                QMessageBox.StandardButton.No)
            QBtn = msg.exec()

            if QBtn == QMessageBox.StandardButton.Yes:
                id = self.tableWidget.selectionModel().currentIndex().siblingAtColumn(0).data()
                self.venda.execute(f"delete from carrinho where id_carrinho = {id}")
                self.venda.commit()
                self.tableWidget.reset()
                self.tabela_carrinho()
                msg = QMessageBox()
                msg.setWindowTitle("Deletar item")
                msg.setText("Item Deletado com sucesso")
                msg.exec()
        except:
            pass


    def atualizar_valor(self):
        try:
            self.venda = venda()
            self.itens = itens()
            self.venda_itens = venda_itens()
            dados = []
            update_dados = []
            for row in range(self.tableWidget.rowCount()):
                for column in range(self.tableWidget.columnCount()):
                    dados.append(self.tableWidget.item(row,column).text())
                update_dados.append(dados)
                dados = []

                
                for emp in update_dados:
                    self.itens.execute(f"update carrinho set quantidade = '{emp[3]}' where id_carrinho = {int(emp[0])} ")
                    self.itens.commit()

            self.tableWidget.reset()
            self.tabela_carrinho()
        except:
            pass
        


    def realizar_venda(self):
        try:
            self.venda = venda()
            self.itens = itens()
            self.venda_itens = venda_itens()
            dados = []
            update_dados = []
            for row in range(self.tableWidget.rowCount()):
                for column in range(self.tableWidget.columnCount()):
                    dados.append(self.tableWidget.item(row,column).text())
                update_dados.append(dados)
                dados = []

                
                for emp in update_dados:
                    self.itens.execute(f"update carrinho set quantidade = '{emp[3]}' where id_carrinho = {int(emp[0])} ")
                    self.itens.commit()

            venda_dados = self.itens.query("select * from carrinho")

            data = date.today()
            data = data.strftime('%d/%m/%Y')
            
            for emp in venda_dados:
                if emp[0] != "":
                    self.venda.execute(f"insert into venda (id_carrinho,descrição,valor_prod, qntd,id_cliente,id_vendedor,data_emissao,data_importacao) values ({int(emp[0])},'{emp[1]}','{emp[2]}','{emp[3]}',{int(emp[5])},{int(emp[6])},'{data}','{data}')")
                    id_venda = self.venda.query(f"select id_venda from venda where id_carrinho = {emp[0]}")
                    self.venda.commit()
                    self.venda_itens.execute(f"insert into venda_itens(id_itens,id_venda) values ( {int(emp[7])} ,{int(id_venda[0][0])})")

                    self.itens.execute(f"update itens set quantidade_estoque = (quantidade_estoque - {int(emp[3])}) where id_itens = {int(emp[7])}")
                    self.venda.execute("delete from carrinho")
                    self.venda.commit()
                    self.itens.commit()
                    self.venda_itens.commit()
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Carrinho")
                    msg.setText("Carrinho está vazio, por favor, adicionar itens")
                    msg.exec()



            self.tableWidget.reset()
            self.tabela_carrinho()
            self.table_estoque.reset()
            self.tabela_estoque()
            self.table_venda.reset()
            self.tabela_venda()
            msg = QMessageBox()
            msg.setWindowTitle("Carrinho")
            msg.setText("Venda realizada com sucesso")
            msg.exec()
        except:
            pass
        
    
    def adicionar_carrinho(self):
        try:
            self.cliente = cliente()
            id = self.table_estoque.selectionModel().currentIndex().siblingAtColumn(0).data()
            prod = self.table_estoque.selectionModel().currentIndex().siblingAtColumn(1).data()
            preco = self.table_estoque.selectionModel().currentIndex().siblingAtColumn(3).data()
            qtd = 1
            fornecedor = self.table_estoque.selectionModel().currentIndex().siblingAtColumn(6).data()
            cliente_name = self.txt_cliente_carrinho.text() 
            if cliente_name == "":
                cliente_name = 18
            vendedor = self.txt_vendedor_carrinho.text()
            if vendedor == "":
                vendedor = 2

            self.cliente.execute(f"insert into carrinho (id_item, produto,preço,quantidade,fornecedor,cliente,vendedor) values ({int(id)}, '{prod}', '{preco}', '{qtd}','{fornecedor}','{cliente_name}','{vendedor}')")
            self.cliente.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Carrinho")
            msg.setText(f"Produto: {prod.split()} adicionado ao carrinho")
            msg.exec()
            self.tableWidget.reset()
            self.tabela_carrinho()
        except TypeError:
            msg = QMessageBox()
            msg.setWindowTitle("Carrinho")
            msg.setText("Por favor, selecione um item")
            msg.exec()
            pass
        except:
            pass


    def limpar_carrinho(self):
        try:
            self.itens = itens()
            msg = QMessageBox()
            msg.setWindowTitle("Apagar carrinho")
            msg.setText("Este carrinho será deletado")
            msg.setInformativeText("Todo o carrinho será apagado, deseja continuar?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                                QMessageBox.StandardButton.No)
            QBtn = msg.exec()

            if QBtn == QMessageBox.StandardButton.Yes:
                self.itens.execute("delete from carrinho")
                self.itens.commit()
                self.tableWidget.reset()
                self.tabela_carrinho()
                msg = QMessageBox()
                msg.setWindowTitle("Alteração de produto")
                msg.setText("Carrinho apagado com sucesso")
                msg.exec()
        except:
            pass


    #Funções da tabela: ESTOQUE
    def cadastrar_produto(self):
        try:
            nome = self.txt_nome_prod.text()
            custo = self.txt_custo.text()
            preco = self.txt_preco.text()
            qtd = self.txt_qtd.text()
            nome_fornecedor = self.txt_fornecedor.text()


            self.fornecedor = fornecedor()
            forn = self.fornecedor.search(nome_fornecedor)
            if forn == "Registro não encontrado":


                msg = QMessageBox()
                msg.setWindowTitle("Cadastro de Produto")
                msg.setText("Fornecedor não encontrado")
                msg.exec()
            for id in forn:
                id_fornecedor = id[0]




            try:
                self.itens = itens()
                item = self.itens.insert_prod(nome,int(custo),int(preco),int(qtd),int(id_fornecedor))

                if item == "Dados Inseridos com sucesso na tabela itens":
                    msg = QMessageBox()
                    msg.setWindowTitle("Cadastro de produto")
                    msg.setText("Produto Cadastrado com sucesso")
                    msg.exec()

                    self.txt_nome_prod.setText("")
                    self.txt_custo.setText("")
                    self.txt_preco.setText("")
                    self.txt_qtd.setText("")
                    self.txt_fornecedor.setText("")
                    self.table_estoque.reset()
                    self.tabela_estoque()
                    self.Pages.setCurrentWidget(self.pag_table)
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Cadastro de produto")
                    msg.setText("Erro ao cadastrar produto")
                    msg.exec()
            except:
                pass
        except:
            pass


    def alterar_produto(self):
        try:
            dados = []
            update_dados = []
            for row in range(self.table_estoque.rowCount()):
                for column in range(self.table_estoque.columnCount()):
                    dados.append(self.table_estoque.item(row,column).text())
                update_dados.append(dados)
                dados = []

            self.itens = itens()
            for emp in update_dados:
                a = self.itens.update(tuple(emp))


            msg = QMessageBox()
            msg.setWindowTitle("Alteração de produto")
            msg.setText(a)
            msg.exec()

            self.table_estoque.reset()
            self.tabela_estoque()
        except:
            pass

    

    def tabela_estoque(self):
        try:
            self.itens = itens()
            result = self.itens.query("Select * from itens")

            self.table_estoque.setRowCount(len(result))
            self.fornecedor = fornecedor()

            for row, text in enumerate(result):
                forn = self.fornecedor.search(int(text[6]), types='id_fornecedor')
                try:
                    necessidade = int(text[5]) - int(text[4])
                except:
                    necessidade = 0 - int(text[4])
                if necessidade < 0:
                    necessidade = 0

                for column, data in enumerate(text):
                    self.table_estoque.setItem(row, column, QTableWidgetItem(str(data)))
                    self.table_estoque.setItem(row, 6, QTableWidgetItem(str(forn[0][1])))
                    self.table_estoque.setItem(row,7, QTableWidgetItem(str(necessidade)))
        except:
            pass


    def deletar_prod(self):
        self.itens = itens()
        msg = QMessageBox()
        msg.setWindowTitle("Deletar Produto")
        msg.setText("Este produto será excluído")
        msg.setInformativeText("Você deseja realmente excluir esse produto?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        QBtn = msg.exec()

        if QBtn == QMessageBox.StandardButton.Yes:
            id = self.table_estoque.selectionModel().currentIndex().siblingAtColumn(0).data()
            result = self.itens.delete(int(id))
            msg = QMessageBox()
            msg.setWindowTitle("Deletar Produto")
            msg.setText(result)
            msg.exec()
            self.table_estoque.reset()
            self.tabela_estoque()



    def gerar_excel_estoque(self):
        dados = []
        all_dados = []

        for row in range(self.table_estoque.rowCount()):
            for column in range(self.table_estoque.columnCount()):
                dados.append(self.table_estoque.item(row, column).text())

            all_dados.append(dados)
            dados = []

        columns = ['ID','Nome','Custo','Preço','Qtd.Estoque', 'Qtd.Ideal', 'Fornecedor','Necessidade']
        pd.set_option("display.max_colwidth", 250)
        itensexcel = pd.DataFrame(all_dados, columns = columns)
        itensexcel.to_excel("Pedido_Fornecedor.xlsx", sheet_name='pedido', index=False)



        msg = QMessageBox()
        msg.setWindowTitle("Relatório Excel")
        msg.setText("Relatório gerado com sucesso")
        msg.exec()

    def gerar_graf_estoque(self):
        try:
            self.itens = itens()

            dados = []
            update_dados = []
            for row in range(self.table_estoque.rowCount()):
                for column in range(self.table_estoque.columnCount()):
                    dados.append(self.table_estoque.item(row,column).text())
                update_dados.append(dados)
                dados = []
                necessidade = 0
                for data in update_dados:
                    necessidade += int(data[7])

            estoque = self.itens.query("Select sum (quantidade_estoque) from itens")



            labels = "Estoque", "Reposição"
            sizes = [estoque[0][0], necessidade]
            fig1,axl = plt.subplots()
            axl.pie(sizes,labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
            axl.axis("equal")
            plt.show()
        except:
            pass


    #Funções da tabela: VENDA
    def tabela_venda(self):
        try:
            self.venda = venda()
            result = self.venda.query("select id_venda,descrição, id_cliente,id_vendedor, qntd, valor_prod, data_emissao from venda")
            self.table_venda.setRowCount(len(result))

            for row, text in enumerate(result):
                self.cliente = cliente()
                self.vendedor = vendedor()
                cliente_nome = self.cliente.search(text[2], types="id_cliente")
                vendedor_nome = self.vendedor.search(text[3], types="id_vendedor")
                for column, data in enumerate(text):
                    self.table_venda.setItem(row, column, QTableWidgetItem(str(data)))
                    self.table_venda.setItem(row,2,QTableWidgetItem(str(cliente_nome[0][1])))
                    self.table_venda.setItem(row,3,QTableWidgetItem(str(vendedor_nome[0][1])))
        except:
            pass


    def gerar_excel_venda(self):
        dados = []
        all_dados = []



        for row in range(self.table_venda.rowCount()):
            for column in range(self.table_venda.columnCount()):
                dados.append(self.table_venda.item(row, column).text())

            all_dados.append(dados)
            dados = []

        columns = ['ID','Produto','Cliente','Vendedor','Quantidade', 'Valor', 'Data']
        pd.set_option("display.max_colwidth", 250)
        itensexcel = pd.DataFrame(all_dados, columns = columns)
        itensexcel.to_excel("relatorio_venda.xlsx", sheet_name='Venda', index=False)



        msg = QMessageBox()
        msg.setWindowTitle("Relatório Excel")
        msg.setText("Relatório gerado com sucesso")
        msg.exec()


    def alterar_venda(self):

        try:
            dados = []
            update_dados = []
            for row in range(self.table_venda.rowCount()):
                for column in range(self.table_venda.columnCount()):
                    dados.append(self.table_venda.item(row,column).text())
                update_dados.append(dados)
                dados = []

            self.venda = venda()
            for emp in update_dados:
                self.cliente = cliente()
                self.vendedor = vendedor()
                cliente_id = self.cliente.search(emp[2])
                vendedor_id = self.vendedor.search(emp[3])
                emp[2] = int(cliente_id[0][0])
                emp[3] = int(vendedor_id[0][0])
                a = self.venda.update(tuple(emp))


            msg = QMessageBox()
            msg.setWindowTitle("Alteração de produto")
            msg.setText(a)
            msg.exec()

            self.table_estoque.reset()
            self.tabela_estoque()
        except Exception as e:
            pass


    def deletar_venda(self):
        try:
            self.venda = venda()
            msg = QMessageBox()
            msg.setWindowTitle("Deletar Venda")
            msg.setText("Esta venda será excluída")
            msg.setInformativeText("Você deseja realmente excluir essa venda?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                                QMessageBox.StandardButton.No)
            QBtn = msg.exec()

            if QBtn == QMessageBox.StandardButton.Yes:
                id = self.table_venda.selectionModel().currentIndex().siblingAtColumn(0).data()
                self.venda.delete(int(id))
                msg = QMessageBox()
                msg.setWindowTitle("Deletar venda")
                msg.setText("venda Deletada com sucesso")
                msg.exec()
                self.table_venda.reset()
                self.tabela_venda()
        except:
            pass


    def gerar_graf_venda(self):
        try:
            self.venda = venda()
            size = []
            labels = []
            estoque = self.venda.query("select extract (month from data_emissao) as mes, count(*) as quantidade from venda group by extract(month from data_emissao) order by extract(month from data_emissao)")


            for i in estoque:
                meses = str(i[0])
                if meses == "1":
                    meses = "Janeiro"
                    labels.append(meses)
                if meses == "2":
                    meses = "Fevereiro"
                    labels.append(meses)
                if meses == "3":
                    meses = "Março"
                    labels.append(meses)
                if meses == "4":
                    meses = "Abril"
                    labels.append(meses)
                if meses == "5":
                    meses = "Maio"
                    labels.append(meses)
                if meses == "6":
                    meses = "Junho"
                    labels.append(meses)
                if meses == "7":
                    meses = "Julho"
                    labels.append(meses)
                if meses == "8":
                    meses = "Agosto"
                    labels.append(meses)
                if meses == "9":
                    meses = "Setembro"
                    labels.append(meses)
                if meses == "10":
                    meses = "Outubro"
                    labels.append(meses)
                if meses == "11":
                    meses = "Novembro"
                    labels.append(meses)
                if meses == "12":
                    meses = "Dezembro"
                    labels.append(meses)


            for i in estoque:
                size.append(i[1])



            fig1,axl = plt.subplots()
            axl.pie(size,labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
            axl.axis("equal")
            plt.show()
        except:
            pass


    #Funções da tabela:CLIENTE
    def sub_cliente(self):
        try:
            nome = self.txt_nome.text()
            telefone = self.txt_telefone.text()
            email = self.txt_email.text()
            endereco = self.txt_endereco.text()
            municipio = self.txt_municipio.text()
            bairro = self.txt_bairro.text()
            cpf = self.lineEdit.text()
            self.cliente = cliente()
            data = self.cliente.insert(nome,telefone,email,endereco,municipio,bairro,cpf)

            if str(data) == "Dados Inseridos com sucesso na tabela cliente":


                msg = QMessageBox()
                msg.setWindowTitle("Cadastro de usuário")
                msg.setText("Cadastro realizado com sucesso")
                msg.exec()

                self.txt_nome.setText("")
                self.txt_telefone.setText("")
                self.txt_email.setText("")
                self.txt_endereco.setText("")
                self.txt_municipio.setText("")
                self.txt_bairro.setText("")
                self.lineEdit.setText("")
                self.table_cliente.reset()
                self.tabela_cliente()
                self.Pages.setCurrentWidget(self.pag_table)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Cadastro de usuário")
                msg.setText(f"Erro ao cadastrar usuário")
                msg.exec()
        except:
            pass


    def alterar_cliente(self):
        dados = []
        update_dados = []
        for row in range(self.table_cliente.rowCount()):
            for column in range(self.table_cliente.columnCount()):
                dados.append(self.table_cliente.item(row,column).text())
            update_dados.append(dados)
            dados = []

        self.cliente = cliente()
        for emp in update_dados:

            a = self.cliente.update(tuple(emp))


            msg = QMessageBox()
            msg.setWindowTitle("Alteração de Cliente")
            msg.setText(a)
            msg.exec()
            self.table_cliente.reset()
            self.tabela_cliente()


    def tabela_cliente(self):
        self.cliente = cliente()
        result = self.cliente.query("Select * from cliente")
        self.table_cliente.setRowCount(len(result))

        for row, text in enumerate(result):
            for column, data in enumerate(text):
                self.table_cliente.setItem(row, column, QTableWidgetItem(str(data)))


    def deletar_cliente(self):
        self.cliente = cliente()
        msg = QMessageBox()
        msg.setWindowTitle("Deletar Cliente")
        msg.setText("Este Cliente será excluído")
        msg.setInformativeText("Você deseja realmente excluir esse Cliente?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        QBtn = msg.exec()

        if QBtn == QMessageBox.StandardButton.Yes:
            id = self.table_cliente.selectionModel().currentIndex().siblingAtColumn(0).data()
            result = self.cliente.delete(int(id))
            msg = QMessageBox()
            msg.setWindowTitle("Deletar Cliente")
            msg.setText("Cliente Deletado com sucesso")
            msg.exec()
            self.table_cliente.reset()
            self.tabela_cliente()

    #Funções da tabela:FORNECEDOR
    def tabela_fornecedor(self):
        self.fornecedor = fornecedor()
        result = self.fornecedor.query("Select * from fornecedor")
        self.table_fornecedor.setRowCount(len(result))

        for row, text in enumerate(result):
            for column, data in enumerate(text):
                self.table_fornecedor.setItem(row, column, QTableWidgetItem(str(data)))


    def pesq_cpnj(self):
        try:
            cnpj = self.pes_cnpj_forn.text()
            newcnpj = cnpj.replace(".","").replace("/","").replace("-","")
            url = f'https://receitaws.com.br/v1/cnpj/{newcnpj}'
            response = requests.request('GET', url)

            resp = json.loads(response.text)
            self.txt_cad_nome.setText(str(resp['fantasia']))
            if str(resp['fantasia']) == '':
                self.txt_cad_nome.setText(str(resp['nome']))
            self.txt_cad_telefone.setText(str(resp['telefone']))
            self.txt_cad_email.setText(str(resp['email']))
            self.txt_cad_cnpj.setText(str(resp['cnpj']))
            msg = QMessageBox()
            msg.setWindowTitle("Cadastro de fornecedor")
            msg.setText("CNPJ encontrado")
            msg.exec()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Cadastro de fornecedor")
            msg.setText("CNPJ não encontrado")
            msg.exec()


    def cadastar_fornecedor(self):

        nome = self.txt_cad_nome.text()
        telefone = self.txt_cad_telefone.text()
        email = self.txt_cad_email.text()
        cnpj = self.txt_cad_cnpj.text()
        site = self.txt_cad_site.text()



        self.fornecedor = fornecedor()
        data = self.fornecedor.insert(nome,cnpj,telefone,email,site)
        if data == "Dados Inseridos com sucesso na tabela fornecedor":
            msg = QMessageBox()
            msg.setWindowTitle("Cadastro de fornecedor")
            msg.setText("Fornecedor Cadastrado com sucesso")
            msg.exec()

            self.txt_cad_nome.setText("")
            self.txt_cad_telefone.setText("")
            self.txt_cad_email.setText("")
            self.txt_cad_cnpj.setText("")
            self.txt_cad_site.setText("")

            self.table_fornecedor.reset()
            self.tabela_fornecedor()
            self.Pages.setCurrentWidget(self.pag_table)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Cadastro de fornecedor")
            msg.setText("Não foi possível cadastrar o fornecedor")
            msg.exec()


    def deletar_fornecedor(self):
        self.fornecedor = fornecedor()
        msg = QMessageBox()
        msg.setWindowTitle("Deletar Fornecedor")
        msg.setText("Este Fornecedor será excluído")
        msg.setInformativeText("Você deseja realmente excluir esse Fornecedor?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        QBtn = msg.exec()

        if QBtn == QMessageBox.StandardButton.Yes:
            id = self.table_fornecedor.selectionModel().currentIndex().siblingAtColumn(0).data()
            result = self.fornecedor.delete(int(id))
            msg = QMessageBox()
            msg.setWindowTitle("Deletar Fornecedor")
            msg.setText("Fornecedor Deletado com sucesso")
            msg.exec()
            self.table_fornecedor.reset()
            self.tabela_fornecedor()


    def alterar_fornecedor(self):
        dados = []
        update_dados = []
        for row in range(self.table_fornecedor.rowCount()):
            for column in range(self.table_fornecedor.columnCount()):
                dados.append(self.table_fornecedor.item(row,column).text())
            update_dados.append(dados)
            dados = []

        self.fornecedor = fornecedor()
        for emp in update_dados:
            a = self.fornecedor.update(tuple(emp))


        msg = QMessageBox()
        msg.setWindowTitle("Alteração de Fornecedor")
        msg.setText(a)
        msg.exec()
        self.table_fornecedor.reset()
        self.tabela_fornecedor()



if __name__=="__main__":
    app = QApplication(sys.argv)
    window = login()
    window.show()
    app.exec()



