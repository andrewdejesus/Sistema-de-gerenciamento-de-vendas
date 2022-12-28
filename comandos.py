import psycopg2 as db
from senha import senha



#Configurações
class Config:
    def __init__(self):

        self.config = {
            "postgres":{
                "user": "postgres",
                "password": senha,
                "host": "localhost",
                "database": "LojaAuto"
            }
        }



#Conectando ao banco de dados
class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        try:
            self.conn = db.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()
        except Exception as e:
            return e

    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        return self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()



#Tabela itens
class itens(Connection):
    def __init__(self):
        Connection.__init__(self)


    def insert(self, *args):
        try:
            sql = f"INSERT INTO itens (nome,custo,preço,quantidade_estoque,quantidade_ideal,id_fornecedor) VALUES {args}"
            self.execute(sql, args)
            self.commit()
            return "Dados Inseridos com sucesso na tabela itens"
        except Exception as e:
            return "Erro ao inserir: ", e
    

    def insert_prod(self, *args):
        try:
            sql = f"INSERT INTO itens (nome,custo,preço,quantidade_estoque,id_fornecedor) VALUES {args}"
            self.execute(sql, args)
            self.commit()
            return "Dados Inseridos com sucesso na tabela itens"
        except:
            return "Erro ao inserir"


    def delete(self, id):
        try:
            sqls = f"select * from itens where id_itens = {id}"
            if not self.query(sqls):
                return "Registro não encontrado"
            sqld = f"delete from itens where id_itens = {id}"
            self.execute(sqld)
            self.commit()
            return "Deletado com sucesso"
        except Exception as e:
            return "Erro ao deletar: ", e


    def update(self, fulldataset):
        self.fornecedor = fornecedor()
        forn= self.fornecedor.search(fulldataset[6])
        
        
        try:
            sql = (f"""update itens set
            id_itens = '{fulldataset[0]}',
            nome = '{fulldataset[1]}',
            custo = '{fulldataset[2]}',
            preço = '{fulldataset[3]}',
            quantidade_estoque = '{fulldataset[4]}',
            quantidade_ideal = '{fulldataset[5]}',
            id_fornecedor= '{int(forn[0][0])}'
            where id_itens = '{fulldataset[0]}' """)

            self.execute(sql)
            self.commit()
            return f"Porduto atualizado com sucesso"
        except Exception as e:
            return f"Erro ao atualizar Produto"


    def search (self, *args, types='nome'):
        sql = "select * from itens where nome like %s"
        
        if types != "nome":
            sql = f"select * from itens where {types} = %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"
            


#Tabela Fornecedor
class fornecedor(Connection):
    def __init__(self):
        Connection.__init__(self)


    def insert(self, *args):
        try:
            sql = f"INSERT INTO fornecedor (nome,cnpj,telefone,email,website) VALUES {args}"
            self.execute(sql, args)
            self.commit()
            return "Dados Inseridos com sucesso na tabela fornecedor"
        except Exception as e:
            return "Erro ao inserir"


    def delete(self, id):
        try:
            sqls = f"select * from fornecedor where id_fornecedor = {id}"
            if not self.query(sqls):
                return "Registro não encontrado"
            sqld = f"delete from fornecedor where id_fornecedor = {id}"
            self.execute(sqld)
            self.commit()
            return f"id {id} deletado com sucesso"
        except Exception as e:
            return "Erro ao deletar: ", e


    def update(self, fulldataset):
        try:
            sql = (f"""update fornecedor set
            id_fornecedor = '{int(fulldataset[0])}',
            nome = '{fulldataset[1]}',
            cnpj = '{fulldataset[2]}',
            telefone = '{fulldataset[3]}',
            email = '{fulldataset[4]}',
            website = '{fulldataset[5]}'
            where id_fornecedor = '{int(fulldataset[0])}' """)

            self.execute(sql)
            self.commit()
            return f"Fornecedor atualizado com sucesso"
        except Exception as e:
            return f"Erro ao atualizar fornecedor"

    def search (self, *args, types='nome'):
        sql = "select * from fornecedor where nome = %s"
        
        if types != "nome":
            sql = f"select * from fornecedor where {types} = %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"



class cliente(Connection):
    def __init__(self):
        Connection.__init__(self)


    def insert(self,nome,telefone,email,endereco,municipio,bairro,cpf):
        try:
            sql = f"INSERT INTO cliente (nome,telefone,email,endereço,município,bairro,cpf) VALUES ('{nome}','{telefone}','{email}','{endereco}','{municipio}','{bairro}','{cpf}')"
            self.execute(sql)
            self.commit()
            return "Dados Inseridos com sucesso na tabela cliente"
        except Exception as e:
            return "Erro ao inserir: ", e


    def insert_xml(self,nome,endereco,municipio,bairro,cpf):
        try:
            sql = f"INSERT INTO cliente (nome,endereço,município,bairro,cpf) VALUES ('{nome}','{endereco}','{municipio}','{bairro}','{cpf}')"
            self.execute(sql)
            self.commit()
            return "Dados Inseridos com sucesso na tabela cliente"
        except Exception as e:
            return "Erro ao inserir: ", e
    

    def delete(self, id):
        try:
            sqls = f"select * from cliente where id_cliente = {id}"
            if not self.query(sqls):
                return "Registro não encontrado"
            sqld = f"delete from cliente where id_cliente = {id}"
            self.execute(sqld)
            self.commit()
            return f"Deletado com sucesso"
        except Exception as e:
            return "Erro ao deletar"


    def update(self, fulldataset):
        try:
            sql = (f"""update cliente set
            id_cliente = {int(fulldataset[0])},
            nome = '{fulldataset[1]}',
            telefone = '{fulldataset[2]}',
            email = '{fulldataset[3]}',
            endereço = '{fulldataset[4]}',
            município = '{fulldataset[5]}',
            bairro = '{fulldataset[6]}',
            cpf = '{fulldataset[7]}'
            where id_cliente = {int(fulldataset[0])} """)

            self.execute(sql)
            self.commit()
            return f"Cliente alterado com sucesso"
        except:
            return f"Erro ao atualizar cliente"


    def search (self, *args, types='nome'):
        sql = "select * from cliente where nome like %s"
        
        if types != "nome":
            sql = f"select * from cliente where {types} = %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"



#Tabela Venda
class venda(Connection):
    def __init__(self):
        Connection.__init__(self)


    def insert(self, *args):
        try:
            sql = f"INSERT INTO venda (data,valor,forma_pagamento,id_cliente,id_vendedor) VALUES {args}"
            self.execute(sql, args)
            self.commit()
            return "Dados Inseridos com sucesso na tabela venda"
        except Exception as e:
            return "Erro ao inserir:", e


    def delete(self, id):
        try:
            sqls = f"select * from venda where id_venda = {id}"
            if not self.query(sqls):
                return "Registro não encontrado"
            sqld = f"delete from venda where id_venda = {id}"
            self.execute(sqld)
            self.commit()
            return f"id {id} deletado com sucesso"
        except Exception as e:
            return "Erro ao deletar:", e


    def update(self, fulldataset):
        try: 
            sql = (f"""update venda set
            id_venda = {int(fulldataset[0])},
            descrição = '{fulldataset[1]}',
            id_cliente = {fulldataset[2]},
            id_vendedor = {fulldataset[3]},
            qntd = '{fulldataset[4]}',
            valor_prod = '{fulldataset[5]}',
            data_emissao = '{fulldataset[6]}'
            where id_venda = {int(fulldataset[0])} """)

            self.execute(sql)
            self.commit()
            return f"Venda alterada com sucesso"
        except:
            return f"Erro ao atualizar Venda"


    def search (self, *args, types='nome'):
        sql = "select * from venda where nome = %s"
        
        if types != "nome":
            sql = f"select * from venda where {types} = %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"


    def insert_xml(self, nota):
        
        try:
            camposdatabela = "(id_cliente,id_vendedor,nfe,serie,data_emissao,chave,cnpj_emitente,nome_emitente,valornfe,item_nota,cod,qntd,descrição,valor_prod,data_importacao)"
            for fulldataset in nota:
                
                sql = f"INSERT INTO venda {camposdatabela} VALUES ({int(fulldataset[0])},{int(fulldataset[1])},'{str(fulldataset[2])}','{str(fulldataset[3])}','{str(fulldataset[4])}','{str(fulldataset[5])}','{str(fulldataset[6])}','{str(fulldataset[7])}','{str(fulldataset[8])}','{str(fulldataset[9])}','{str(fulldataset[10])}','{str(fulldataset[11])}','{str(fulldataset[12])}','{str(fulldataset[13])}','{str(fulldataset[14])}')"
                self.execute(sql)
                self.commit()
        except:
            return "Nota já existe"


    def check(self,fulldataset):
        
        for chave in fulldataset:
            sql = f"select * from venda"
            data = self.query(sql)
            for linha in data:
                if str(linha[6]).split() == str(fulldataset[0][5]).split() and str(linha[11]).split() == str(fulldataset[0][10]).split():
                    return "Essa nota já existe"

        return "Nota adicionada com sucesso"



class venda_itens(Connection):
    def __init__(self):
        Connection.__init__(self)


    def insert(self, *args):
        try:
            sql = f"INSERT INTO venda_itens (id_itens,id_venda) VALUES {args}"
            self.execute(sql, args)
            self.commit()
            return "Dados Inseridos com sucesso na tabela venda_itens"
        except Exception as e:
            return "Erro ao inserir:", e


    def delete(self, id):
        try:
            sqls = f"select * from venda_itens where id_venda_itens = {id}"
            if not self.query(sqls):
                return "Registro não encontrado"
            sqld = f"delete from venda_itens where id_venda_itens = {id}"
            self.execute(sqld)
            self.commit()
            return f"id {id} deletado com sucesso"
        except Exception as e:
            return "Erro ao deletar:", e


    def search (self, *args, types='id_venda_itens'):
        sql = f"select * from venda_itens where {types} = %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"



#Tabela Vendedor
class vendedor(Connection):
    def __init__(self):
        Connection.__init__(self)


    def insert(self, *args):
        try:
            sql = f"INSERT INTO vendedor (nome,password) VALUES {args}"
            self.execute(sql, args)
            self.commit()
            return "Dados Inseridos com sucesso na tabela vendedor"
        except Exception as e:
            return "Erro ao inserir:", e
    

    def delete(self, id):
        try:
            sqls = f"select * from vendedor where id_vendedor = {id}"
            if not self.query(sqls):
                return "Registro não encontrado"
            sqld = f"delete from vendedor where id_vendedor = {id}"
            self.execute(sqld)
            self.commit()
            return f"id {id} deletado com sucesso"
        except Exception as e:
            return "Erro ao deletar:", e


    def update(self, id, coluna,*args):
        try:
            sql = f"update vendedor set {coluna} = %s where id_vendedor = {id}"
            self.execute(sql, args)
            self.commit()
        except Exception as e:
            return "Erro ao atualizar:", e


    def search (self, *args, types='nome'):
        sql = "select * from vendedor where nome like %s"
        
        if types == "id_vendedor":
            sql = f"select * from vendedor where id_vendedor = %s"
        data = self.query(sql, args)
        if data:
            return data
        return "Registro não encontrado"


    def check(self,nome,password):
        try:
            sql = f"select * from vendedor"
            data = self.query(sql)
            for linha in data:
                if str(linha[1]).split() == str(nome).split() and str(linha[2]).split() == str(password).split():
                    return "Acesso concedido"
            return "Acesso negado"
        except:
            return "Erro ao fazer Login, verifique sua conexão com a internet"


