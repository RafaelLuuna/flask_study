from flask import Flask, url_for, request, render_template, make_response, redirect, abort
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return f'Hello... pessoa aleatória'


@app.route('/<name>')
def index_name(name):
    name = escape(name)
    return f'Hello {name}'


@app.route('/subpath/<path:path>')
def sub_path(path):
    path = escape(path)
    return path


@app.route('/uniquepage')
def unique_page():
    return 'this page is unique'

@app.route('/generalpage/')
def general_page():
    return 'this page in not unique'


@app.route('/get-post', methods=['GET','POST'])
def get_post():
    method = request.method
    if method == 'POST':
        val1 = 'default'
        try:
            val1 = request.form['val1']

        except KeyError as e:
            print(f'\n\nVariável não encontrada na requisição POST: {e}\n')
        except Exception as e:
            print(f'\n\nErro ao carregar requisição POST: {e}\n')
        
        return f'this is a POST method\n{val1}'
    

    if method == 'GET':
        try:
            val1 = request.args.get('val1', '')

        except Exception as e:
            print(f'\n\nErro ao carregar requisição GET: {e}\n')
        return f'this is a GET method\n{val1}'


@app.get('/get')
def get():
    return 'this is GET, and olny GET method'


@app.post('/post')
def post():
    return 'this is POST, and olny POST method'


@app.route('/static/<path:file_path>')
def custom_static(file_path):
    return url_for('static', filename=file_path)


@app.route('/runtemplate/<path:template_name>')
def run_template(template_name):
    return render_template(template_name)


@app.route('/upload_file', methods=['GET','POST'])
def upload_files():
    if request.method == 'POST':
        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            path = f'static/uploads/{filename}'
            file.save(path)
            return f'file saved in "{path}" with the name of: {filename}'
        
        except KeyError as e:
            print(f'\n\nVariável não encontrada na requisição POST: {e}\n')
        except Exception as e:
            print(f'\n\nErro ao carregar arquivo: {e}\n')


    if request.method == 'GET':
        try:
            return render_template('tests/upload.html')
        except Exception as e:
            print(f'\n\nErro ao carregar formulário: {e}\n')
    return 'Como você chegou aqui?'


@app.route('/cookie', methods=['GET','POST', 'DELETE'])
def cookie():
    METHOD = request.method
    try:
        if METHOD == 'POST':
            val = request.form['val']

            res = make_response('cookie atualizado')
            res.set_cookie('cookie',val)
        

        if METHOD == 'GET':
            cookie_val = request.cookies.get('cookie')

            res = make_response(cookie_val)

        if METHOD == 'DELETE':
            res = make_response('cookie deletado')
            res.delete_cookie('cookie')
        
    
    except KeyError as e:
        print(f'\n\nVariável não encontrada na requisição {METHOD}: {e}\n')
        res = make_response('cookie limpo')
        res.set_cookie('cookie','')
    
    except Exception as e:
        print(f'\n\nErro ao carregar requisição {METHOD}: {e}\n')
        res = make_response('erro ao carregar cookie')

    return res


@app.route('/redirect/<string:page>', methods=['GET','POST', 'DELETE'])
def redirect_page(page):
    METHOD = request.method
    try:
        # O redirect sempre redireciona usando o método GET, essa condição abaixo serve apenas para testar o abort()
        if METHOD != 'GET':
            abort(401)
        
        res = redirect(url_for(page))
    
    except Exception as e:
        print(f'\n\nErro ao carregar requisição {METHOD}: {e}\n')
    
    return res