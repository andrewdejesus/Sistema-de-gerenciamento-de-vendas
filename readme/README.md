<h1> 
    <img src="./rsz_2linha_alliance__divulgaÇÃo__mercedes-benz.png">
    <p>Sistema de controle de vendas 📈</p>
</h1>

## 📖 Indíce
    -[About](#📕-about)
    -[Ferramentas](#🔨-ferramentas)
    -[Tela de Login](#tela-de-login)
    -[Tela Principal](#tela-principal-main)
    -[Importar](#importar)
    -[Tabela Estoque](#tabelas-estoque)
    -[Tabela Cliente](#tabelas-clientes)
    -[Tabela Fornecedor](#tabelas-fornecedor)
    -[Tabela Venda](#tabelas-vendas)
    -[Carrinho](#carrinho)
    -[Contatos](#contato)

## 📕 About
É um projeto para auxiliar o usuário, dono de loja, no gerencimento das vendas, do estoque, dos clientes e fornecedores.

## 🔨 Ferramentas
    - Python
    - PostegreSQL
    - [API receitaws](https://receitaws.com.br/)

# Tela de Login
<img src="./Captura de Tela (2).png">
    A tela de login recebe um usuário e uma senha e compara com as informações da tabela vendedor no banco de dados. O programa verifica se as informações existem e caso existam permite que abra a janela principal. É possível errar as informações até 3 vezes, após isso o programa fecha e é preciso abri-lo novamente.

#  Tela Principal (Main)
<img src="./captura de tela (3).png">
    Após o processo de validação na tela de login, abrirá a janela principal. Na parte superior é possivel identificar 5 áreas. A área HOME é a primeira a aparecer juntamente com uma notificação do sistema dizendo que o acesso foi concedido.

# IMPORTAR
<img src="./captura de tela (29).png">
    Clicando em IMPORTAR, abrirá uma área onde é possível inserir uma NFe(Nota Fiscal Eletrônica) referente à uma venda, o sistema lê as informações da nota e insere na tabela venda. O sistema também verifica se existe um cliente cadastrado no banco de dados e caso não exista, cria um cliente com as informações provenientes da NFe, atribuindo essa venda a esse cliente.

# TABELAS: ESTOQUE
<img src="./captura de tela (31).png">
    A tabela de estoque, além das funções de adicionar ao carrinho, adicionar remover e alterar produto, também possui a funcionalidade de gerar um gráfico que auxilia na visualização da quantidade de produtos que tem em estoque e na necessidade de produtos a serem repostos. Além disso, é possível ver todas essas informações em um arquivo Excel, clicando em "Gerar Excel".

### Gráfico de Estoque x Necessidade
<img src="./captura de tela (35).png">

# TABELAS: CLIENTES
<img src="./captura de tela (36).png">
    A tabela Clientes possui as informações necessárias para que se faça uma venda, no entanto, ao cadastrar, as informações não são obrigatórias.

### Cadastro de Clientes
<img src="./captura de tela (37).png">

# TABELAS: FORNECEDOR
<img src ="./captura de tela (40).png">
    A tabela fornecedor é associada a um produto da tabela estoque como FOREIGN KEY e caso haja necessidade de trocar algum produto, as informações contidas nela são de extrema importância.

### Cadastro de Fornecedor
<img src ="./captura de tela (39).png">
    No cadastro de fornecedores há uma função para pesquisar o CPF do fornecedor usando a API receitaws, as informação necessárias são autocompletadas na tela de cadastro, sendo possível alterá-las e incluir informações que não foram encontradas antes de finalizar o cadastro.

# TABELAS: VENDAS
<img src ="./captura de tela (43).png">
    Na tabela de vendas existem as funções de gerar planilha e gráfico, assim como na tabela estoque, mas nesse caso, o gráfico gerado é para que o usuário observe, de maneira rápida, os meses que suas vendas foram melhores ou piores. Ao clicar em gerar gráfico no exemplo acima, teremos a seguinte resposta do sistema:
<img src ="./captura de tela (44).png"> 
    É possível ver que os meses de Março e Dezembro foram os melhores em vendas no ano, nesse exemplo

# CARRINHO
Após clicar em adicionar ao carrinho na tabela estoque, o item selecionado é visto na área 'Carrinho' e as informações ficam salvas até que a venda seja realizada ou que clique em limpar venda. A quantidade incial de cada produto adicionada é definida em 1, se alterar a quantidade será preciso clicar em atualizar valor para que o valor total seja atualizado. Vejamos o exemplo a seguir:
<img src ="./captura de tela (33).png">

### CONTATO
<img src ="./captura de tela (28).png">
    Ao clicar nos botões uma página do navegador abrirá e o usuário será redirecionado para os seguintes links:
    -[Instagram](https://www.instagram.com/_andrewjesus/)
    -[Linkedin](https://www.linkedin.com/in/andrew-machado-dias-de-jesus-22420a18b/)
    -[Github](https://github.com/andrewdejesus)