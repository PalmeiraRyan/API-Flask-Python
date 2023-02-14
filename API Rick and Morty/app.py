from flask import Flask, jsonify, request, make_response
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request 
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query
from typing import Optional
from itertools import count
from datetime import date

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
spec = FlaskPydanticSpec('flask', title='API da Fanfic de Rick and Morty')
spec.register(app)
database = TinyDB('database/database.json', indent =4)
db = TinyDB('database/db.json', indent =4)

c = count()
class Personagem(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
    nome: str
    status: str
    species: str
    gender: str
    origin: object
    location: object
    created: str
    url: str

class Personagens(BaseModel):
    Personagens: list[Personagem]
    count: int

class Local(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
    nome: str
    dimension: str
    residents: str
    created: str
    url: str

class Locais(BaseModel):
    Locais: list[Local]
    count: int

class Locais_Personagens(BaseModel):
    Locais: list[Local]
    Personagens: list[Personagem]


@app.route('/personagens', methods=['GET'])
def buscar_personagem():
    """Mostra os Personagens que estão no Banco"""    
    return jsonify(
        Personagens(
            Personagens=database.all(),
            count=len(database.all())
        ).dict()
    )

#insere
@app.post('/personagens')
@spec.validate(body=Request(Personagem), resp=Response(HTTP_201=Personagem))
def inserir_personagem():
    """Insere um personagem no banco"""
    data = date.today()
    idsUser = len(database.all()) + 1
    idLocal = len(db.all()) + 1
    body = request.context.body.dict()
    body.update({'id': idsUser}) 
    body.update({'created': str(data)}) 
    body.update({'url': 'http://localhost:5000/personagens/'+str(idsUser)}) 
    insertLocation = body.get('location').lower()
    local = ""
    try:
        local = db.search(Query().nome == insertLocation)[0] 
    except:
        print('Já existe')    
    if local == "":
        quant = len(db.all()) + 1
        localCriacao = {"id": quant, "nome": insertLocation, "dimension": "uninformed ", "residents": "uninformed", "created": str(data), "url": 'http://localhost:5000/local/'+str(idLocal)}
        db.insert(localCriacao) 

    idLocal = len(db.all()) + 1
    insertOrigin = body.get('origin').lower()
    origin =""
    try:
        origin = db.search(Query().nome == insertOrigin)[0] 
    except:
        print('Já existe')    
    if origin == "":
        quant = len(db.all()) + 1
        localCriacao = {"id": quant, "nome": insertOrigin, "dimension": "uninformed ", "residents": "uninformed", "created": str(data), "url": 'http://localhost:5000/local/'+str(idLocal)}
        db.insert(localCriacao)    

    database.insert(body)
    return body

#Altera
@app.put('/personagens/<int:id>')
@spec.validate(body=Request(Personagem), resp=Response(HTTP_200=Personagem))
def altera_personagem(id):
    """Altera um Personagem no banco"""
    Personagem = Query()
    body = request.context.body.dict()
    database.update(body, Personagem.id == id)
    return jsonify(body)

#Retornar ID especifico
@app.route('/personagens/<int:id>', methods=['GET'])
def buscar_personagem_unico(id):
    """Mostra um Personagem por ID"""    
    try: 
        Personagem = database.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'Não tem esse ID no nosso banco!'}, 404    
    return jsonify(Personagem)

#DELETAR
@app.delete('/personagens/<int:id>')
@spec.validate(body=Request(Personagem), resp=Response('HTTP_204'))
def deleta_personagem(id):
    """DELETAR um Personagem no banco"""
    Personagem = Query()
    database.remove(Personagem.id == id)
    return jsonify('Deletado com sucesso')

#LOCAIS
@app.route('/local', methods=['GET'])
def buscar_local():
    """Mostra os locais que estão no Banco"""    
    return jsonify(
        Locais(
            Locais=db.all(),
            count=len(database.all())
        ).dict()
    )

#insere local
@app.post('/local')
@spec.validate(body=Request(Local), resp=Response(HTTP_201=Local))
def inserir_Local():
    """Insere um Local no banco"""
    data = date.today()
    idsUser = len(db.all()) + 1    
    body = request.context.body.dict()
    body.update({'id': idsUser}) 
    body.update({'created': str(data)}) 
    body.update({'url': 'http://localhost:5000/local/'+str(idsUser)})   
    body.update({'nome': body.get('nome').lower()})  
    db.insert(body)
    return body

#Altera local
@app.put('/local/<int:id>')
@spec.validate(body=Request(Local), resp=Response(HTTP_200=Local))
def altera_local(id):
    """Altera um local no banco"""
    Local = Query()
    body = request.context.body.dict()
    db.update(body, Local.id == id)
    return jsonify(body)

#Retornar ID especifico Local
@app.route('/local/<int:id>', methods=['GET'])
def buscar_loacl_unico(id):
    """Mostra um local por ID"""    
    try: 
        Local = db.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'Não tem esse ID no nosso banco!'}, 404    
    return jsonify(Local)

#DELETAR Local
@app.delete('/local/<int:id>')
@spec.validate(body=Request(Local), resp=Response('HTTP_204'))
def deleta_local(id):
    """Deleta um local do banco"""
    Local = Query()
    db.remove(Local.id == id)
    return jsonify({})

#Local + Personagem
@app.route('/personagens_locais/<int:id>', methods=['GET'])
def buscar_personagem_Local_unico(id):
    """Mostra determinado personagem, sua locaalização atual e sua origem"""    
    try: 
        Personagem = database.search(Query().id == id)[0]
        v = str(Personagem)
        list = v.split("'")
        l = list[25].lower()
        local = db.search(Query().nome == l)[0]
        
        o = list[21].lower()
        origin = db.search(Query().nome == o)[0]
    except IndexError:
        Personagem = database.search(Query().id == id)[0]
        v = str(Personagem)
        list = v.split("'")
        l = list[25].lower()
        print(l)
        local = db.search(Query().nome == l)[0]
        
        o = list[21].lower()
        origin = db.search(Query().nome == o)[0]    
    return jsonify(Personagem, 'O último local que este(a) personagem foi visto: ', local, 'a origem do(a) personagem é de:', origin)

@app.route('/local_atual/<int:id>', methods=['GET'])
def local_do_personagem(id):
    """Mostra todos os personagens que setão em um determinado local"""    
    try: 
        Local = db.search(Query().id == id)[0]
        p = str(Local)
        list = p.split("'")
        l = list[5].lower()
        pessoas = database.search(Query().location == l)
        print(l)
    except IndexError:
        return {'message': 'Não tem esse ID no nosso banco!'}, 404    
    return jsonify(Local, 'Personagens que foram vistos pela última vez neste local: ', pessoas)

#Abaixo um run para iniciar a api
app.run(port=5000, host='localhost',debug=True)