import re
from flask import render_template, redirect, url_for, request, flash, abort
from comunidadeimpressionadora import application, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image



@application.route("/") #caminho da página
def home():
    lista_posts = Post.query.order_by(Post.id.desc())

    return render_template('home.html', lista_posts=lista_posts)


@application.route("/contato")
def contato():
    return render_template('contato.html')


@application.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios) #parametro lista_usuarios pode ser qualquer nome, porém após o '=' deve ser a variável da lista


@application.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    #Login
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # varifica se usuario existe e se a senha está correta
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # Exibir mensagem de sucesso
            flash(f'Login realizado com sucesso no e-mail: {form_login.email.data}', 'alert-success')

            #Redirecioanr para home
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login e-mail ou senha incorretos', 'alert-danger')
    # Cadastrar

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #criar o usaurio
        #criptografar senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)

        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)

        #adicionar sessão
        database.session.add(usuario)

        #commit na sessao
        database.session.commit()

        # Conta criada com sucesso
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        #Redirecionar para home
        return redirect(url_for('home'))

    return(render_template('login.html', form_login = form_login, form_criarconta = form_criarconta))

@application.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout realizado com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@application.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename= 'fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)



@application.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criarpost = FormCriarPost()

    if form_criarpost.validate_on_submit():
        post = Post(titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data, autor=current_user)

        # adicionar sessão
        database.session.add(post)

        # commit na sessao
        database.session.commit()

        # Conta criada com sucesso
        flash('Post criado com sucesso!', 'alert-success')

        # Redirecionar para home
        return redirect(url_for('home'))

    return render_template('criarpost.html', form_criarpost=form_criarpost)


def salvar_imagem(imagem):
    # Adicionar um código aleatorio ao nome da imagem 
    codigo = secrets.token_hex(8)            
    nome, extensao =  os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    
    #caminho para salvar a imagem
    caminho_completo = os.path.join(application.root_path, 'static/fotos_perfil', nome_arquivo)
    
    # Reduzir o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    
    # Salvar a foto na pasta fotos perfil
    imagem_reduzida.save(caminho_completo)

    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []

    for campo in form:
        if 'curso' in campo.name:
            if campo.data:
                # Adicionar o texto do campo.label na lista de cursos
                lista_cursos.applicationend(campo.label.text)
    
    # Adicioanar cursos a tabela
    return ';'.join(lista_cursos)



@application.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        
        # se o usuário carregou uma foto salva-la
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()

        flash('Perfil do usuário atualizado com sucesso.', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil = foto_perfil, form = form)


@application.route('/post/<post_id>', methods=['GET', 'POST']) # <post_id> faz referencia a uma variavel que vai se chamar assim
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect( url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)



@application.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)

    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()

        flash('Post excluído com sucesso.', 'alert-danger')
        return redirect( url_for('home') )

    else:
        abort(403) # Erro 403 é o link que o usuário tentou acessar um link que não tem autorização


