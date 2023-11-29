from flask import Flask, render_template, redirect, request, flash
import json
import ast
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'VIOLETA'

logado = False

@app.route('/adm')
def adm():
    if logado == True:  
     with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        return render_template("administrador.html", usuarios=usuarios)
    if logado == False:
        
         return redirect('/')


@app.route('/')
def home():
    global logado
    logado =  False
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login():

    global logado

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('usuarios.json') as usuariosTemp:
       usuarios = json.load(usuariosTemp)
       cont = 0
       for usuario in usuarios:
          cont += 1

          if nome == 'adm' and senha == '000':
              logado = True
              
              return redirect('/adm')
          
          if usuario['nome'] == nome and usuario['senha'] == senha:
             return render_template("usuarios.html")
          
          if cont >= len(usuarios):
              flash('Usuário ou senha inválidos!')
              return redirect("/")
          
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
     global logado
     user = []
     nome = request.form.get('nome')
     senha = request.form.get('senha')
     user = [
         {
             "nome": nome,
             "senha": senha
         }
     ]
     with open('usuarios.json') as usuariosTemp:
         usuarios = json.load(usuariosTemp)
     usuarioNovo = usuarios + user

     with open('usuarios.json', 'w') as gravarTemp:
        json.dump(usuarioNovo, gravarTemp, indent=4 )
        logado = True
        flash(F'{nome} Cadastrado(a)!')

     return redirect('/adm')
    
          
@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('userExclusao')
    usuarioDic = ast.literal_eval(usuario)
    nome =  usuarioDic['nome']
    with open('usuarios.json') as usuariosTemp:
        usuariosJson = json.load(usuariosTemp)
        for c in usuariosJson:
            if c == usuarioDic:
                usuariosJson.remove(usuarioDic)
                with open('usuarios.json', 'w') as usuarioExclusao:
                    json.dump(usuariosJson, usuarioExclusao, indent=4)

    flash(F'{nome} EXCLUÍDO COM SUCESSO!')
    return redirect('/adm')


@app.route("/upload", methods=['POST'])
def upload():
    global logado
    logado = True

    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace("",".")
    arquivo.save(os.path.join('arquivos/', nome_arquivo))






    return redirect('/adm')




if __name__ in "__main__":
    app.run(debug=True)