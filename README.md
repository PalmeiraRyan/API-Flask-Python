# API-Flask-Python
API em flask e python. Armazena e personaliza dados de personagens e lugares.

# instalação 

1- Instale o python em: https://www.python.org/downloads/
2-instale o Flask com o comando com o comando: pip intall flask
3- Instale o Flask Pydantic Spec com o comando: pip install flask-pydantic-spe
4- Instale o TinyDB com o comando: pip install tinydb

# Rodando a API no navegador

Abra o projeto no VS code já com as devidas extensões do python instaladas e inicie o projeto.
A API roda na url: http://localhost:5000//apidoc/swagger
Lá estarão definidas todas as operações que podemos realizar (as operações são as mesmas listadas mais abaixo). Basta clicar na operação que deseja realizar, clicar no botão "try it out" e executar a operação. 
Consultas podem ser feitas de modo geral ou a partir de um ID, incersões podem ser feitas no formato JSON e para deletar basta inserir o ID específico.

# Testando a API no Postman

Uma outra alternativa e utilizar o Postman para visualizar a API

Após iniciar o projeto use as seguintes urls para testar suas funcionalidades. 

GET | http://localhost:5000/personagens -> Ver a lista de todos os personagens que temos no banco.
GET | http://localhost:5000/local -> Ver a lista de todos os locais que temos no banco.
GET | http://localhost:5000/personagens/{id} -> Mostra um personagem em específico, ao passar o ID do personagem no final da url.
GET | http://localhost:5000/local/{id} -> Mostra um local em específico, ao passar o ID do local no final da url.

POST | http://localhost:5000/personagens -> Adiciona um novo personagem (é necessario inserir os dados em formato JSON).
POST | http://localhost:5000/local -> Adiciona um novo local (é necessario inserir os dados em formato JSON).

PUT | http://localhost:5000/personagens/{id} -> ALtera os dados de um personagem (é necessario inserir os dados em formato JSON).
PUT | http://localhost:5000/local/{id} -> ALtera os dados de um local (é necessario inserir os dados em formato JSON).

DELETE | http://localhost:5000/personagens/{id} -> Deleta o personagem especificado.
DELETE | http://localhost:5000/local/{id} -> Deleta o local especificado.

GET | http://localhost:5000/personagens_locais/{id} -> Mostra o personagem especificado, sua origem e sua localização atual.
GET | http://localhost:5000/local_atual/{id} -> Mostra o local especificado, e os personagens que  estão neste local atualmente. 
