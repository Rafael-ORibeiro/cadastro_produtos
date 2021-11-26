from dns.rdatatype import NULL
from flask import Flask, Response, request
from flask.sessions import NullSession
from flask_pymongo import PyMongo
from bson import json_util
from bson.json_util import dumps
import os


    

app = Flask(__name__)

app.config['MONGO_URI'] = ""

#collection produtos
mongo = PyMongo(app)

def retornarDados(resp):
    jsonResposta = []
    for dados in resp.json:
        jsonResposta.append({"produto":dados["produto"],"quantidade":dados["quantidade"]})
    return {"result": jsonResposta}

@app.route('/',methods=['GET'])

def getStart():
    
    return {'message':'Api(CRUD) para matéria Projeto Front-end para Soluções Sociais. 5ºPeríodo UNIFAA - ADS - Dezembro -2021'}


@app.route('/produtos',methods=['GET'])

def getProdutos():
    
    query_ = mongo.db.produtos.find()
    
    response = Response(json_util.dumps(query_),mimetype='application/json')
    
    return retornarDados(response)


@app.route('/produtos',methods=['POST'])

def postProdutos():
       
    duplicidade = dumps(mongo.db.produtos.find({"produto":request.json[0]["produto"]}))
    
    if duplicidade == "[]":
        
        mongo.db.produtos.insert_one(request.json[0])
        
        return{"message":"SUCESS"}
    
    return{"message":"Produto já cadastrado"}
    
    
    
@app.route('/produtos/update',methods=['PUT'])

def updateProdutos():
    
    existeNovoNome = dumps(mongo.db.produtos.find({"produto":request.json[0]["novoNome"]}))
    
    existeAntigoNome = dumps(mongo.db.produtos.find({"produto":request.json[0]["antigoNome"]}))

    if existeNovoNome == "[]" and existeAntigoNome != "[]":
    
        novo = {"$set": {"produto":request.json[0]["novoNome"],"quantidade":request.json[0]["novaQuantidade"]}}
        
        filtro ={"produto":request.json[0]["antigoNome"]}
        try:
            mongo.db.produtos.update(filtro,novo)
            
            return{"message":"Produto atualizado","novo Produto":{"produto":request.json[0]["novoNome"],"quantidade":request.json[0]["novaQuantidade"]}}
        
        except:
            
            return{"message":"Erro ao tentar atualizar produto"}
        #response = Response(json_util.dumps(query_),mimetype='application/json')
        
    return {"message":"Esse produto não existe ou o nome que será atualizado já existe!"}



@app.route('/produtos/delete',methods=['DELETE'])

def deleteProdutos():
    
    produtoQueSeraDeletado = dumps(mongo.db.produtos.find({"produto":request.json[0]["produto"]}))
    
    if produtoQueSeraDeletado != "[]":
        try:
            filtro ={"produto":request.json[0]["produto"]}
            
            mongo.db.produtos.remove(filtro)
            
            return {"message":"Produto Deletado","produto":filtro}
        
        except:
            
            return {"message":"Erro na tentativa de deletar"}
        
        #response =  Response(json_util.dumps(query_),mimetype='application/json')
    
    return{"message":"Produto não encontrado"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
