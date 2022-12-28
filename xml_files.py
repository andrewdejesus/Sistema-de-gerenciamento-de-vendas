import os
import xml.etree.ElementTree as Et
from datetime import date
from comandos import *




#Classe que faz a Leitura do XML
class read_xml():
    def __init__(self, directory) -> None:
        self.directory = directory


    def all_files(self):
        return [os.path.join(self.directory, arq) for arq in os.listdir(self.directory) if arq.lower().endswith(".xml")]


    def check_none(self,var):
        if var == None:
            return ""
        else:
            try:
                return var.text.replace(".",",")
            except:
                return "var.text"


    #Função que pega os dados da NFe
    def nfe_data(self,xml):
        root = Et.parse(xml).getroot()
        nsNFE = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

        #Dados NFE
        NFe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF", nsNFE))
        serie = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:serie", nsNFE))
        data_emissao = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi", nsNFE))
        data_emissao = F"{data_emissao[8:10]}/{data_emissao[5:7]}/{data_emissao[:4]}"

        #Dados Emitente
        chave = self.check_none(root.find("./ns:protNFe/ns:infProt/ns:chNFe", nsNFE))
        cnpj_emitente = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ", nsNFE))
        nome_emitente = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:emit/ns:xNome", nsNFE))
        cnpj_emitente = self.format_cnpj(cnpj_emitente)
        valorNFe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF", nsNFE))

        #Formatação da data que a nota foi importada para o sistema
        data_importacao = date.today()
        data_importacao = data_importacao.strftime('%d/%m/%Y')

        #ID do vendedor 'ADMIN'
        id_vendedor = 2

        #Dados do Cliente
        cpf = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:dest/ns:CPF", nsNFE))
        self.cliente = cliente()
        id_cliente = self.cliente.search(cpf, types='cpf')
        if id_cliente == "Registro não encontrado":
            telefone = ''
            email = ''
            nome = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:dest/ns:xNome", nsNFE))
            endereço = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xLgr", nsNFE))
            bairro = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xBairro", nsNFE))
            municipio = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xMun", nsNFE))
            self.cliente.insert(nome,telefone,email,endereço,municipio,bairro,cpf)
            id_cliente = self.cliente.search(cpf, types='cpf')

        #Pegar informações dos itens na nota
        item_nota = 1
        notas = []
        for item in root.findall("./ns:NFe/ns:infNFe/ns:det", nsNFE):
            cod = self.check_none(item.find("./ns:prod/ns:cProd", nsNFE))
            qntd = self.check_none(item.find("./ns:prod/ns:qCom", nsNFE))
            desc = self.check_none(item.find("./ns:prod/ns:xProd", nsNFE))
            valor_prod = self.check_none(item.find("./ns:prod/ns:vProd", nsNFE))
            qntd = qntd.replace(",","").replace("0","")
            dados_prod = [int(id_cliente[0][0]),int(id_vendedor),NFe,serie,data_emissao,chave,cnpj_emitente,nome_emitente,valorNFe,item_nota,cod,qntd,desc,valor_prod,data_importacao]
            notas.append(dados_prod)
            item_nota += 1
        
        return notas


    #Função para colocar a formatação padrão no CNPJ encontrado
    def format_cnpj(self,cnpj):
        try:
            cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}.'
            return cnpj
        
        except:
            return ""


