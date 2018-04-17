import os
from flask import Flask, render_template, request, g, redirect, url_for,flash
from werkzeug import secure_filename
from pathlib import Path
import sqlite3
from pybtex.database import parse_file
import serial

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
db_path = os.path.join(app.root_path, 'uploads/biblio.db')
ALLOWED_EXTENSIONS = set(['bib'])

def get_db():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return connection, cursor  #connection and cursor pointing to the database

def create_db():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    #create the table
    cursor.execute('''CREATE TABLE bib
             (tag text, authors text, journal text, volume int, pages text, year int, title text, collection text)''')
    #and save it
    connection.commit()
    return connection, cursor


def query_db(query_string):
    connection, cursor = get_db()
    cursor.execute(f'SELECT * FROM bib WHERE '+ query_string)
    all_rows = cursor.fetchall()
    return all_rows #a list of database entries matching the query criterion
    
def fill(bib_data, collection):
    connection, cursor = get_db()
    for entry in bib_data.entries: 
        #get the authors
        authors = get_db_authors(bib_data, entry)
        #get everything else
        tag,journal,volume,pages,year,title= entry, get_db_string('journal', bib_data, entry),\
        get_db_int('volume', bib_data, entry), get_db_string('pages', bib_data, entry), \
        get_db_int('year', bib_data, entry), get_db_string('title', bib_data, entry)
        
        #we'll clean up the title/journal strings a bit
        title = title.replace('{', '')
        title = title.replace('}', '')
        journal = journal.replace("\\", '')
        
        #populate the database
        exe_string = f"INSERT INTO bib VALUES ('{tag}', '{authors}', '{journal}', '{volume}', '{pages}', '{year}', '{title}', '{collection}')"
        cursor.execute(exe_string)
    #and save the changes
    connection.commit()

def get_db_string(key, bib_data, entry):
    try:
        return bib_data.entries[entry].fields[key]
    except KeyError:
        return ''  #when there's no journal, title, etc. for this entry
    
def get_db_int(key, bib_data, entry):
    try:
        return int(bib_data.entries[entry].fields[key])
    except KeyError:
        return 0   #when there's no year or volume for this entry
    
def get_db_authors(bib_data, entry):
    authors = ''
    try: 
        for author in bib_data.entries[entry].persons['author']:
            new_author = str(author)
            
            #we'll clean up the author names a bit
            characters = ['{', '}', "'",'"', '\\', '//']
            for c in characters:
                new_author = new_author.replace(c, '')
            authors += new_author + ' and '
        authors = authors[:-5]  #remove final 'and'
        
    except KeyError:
        authors = 'no authors'   #when there's no author listed for this entry
        
    return authors  #a string with all of the authors listed
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    #truth value of appropriate file type
    
def get_collections(all_rows):
    output = []
    for row in all_rows:
        if row[7] not in output:
            output.append(row[7])
    return output  #a list of unique collection names
    
@app.route('/')
@app.route('/index')
def index():
    if Path(db_path).is_file():  #if there's a database,
        db = 1
        connection, cursor = get_db()
        cursor.execute(f'SELECT * FROM bib')  #look at all entries
        all_rows = cursor.fetchall()
        collections = get_collections(all_rows)  #and find unique collection names
        
    #if there's not a database
    else:
        db = 0
        connection, cursor = create_db()  #create one
        all_rows = cursor.fetchall()
        collections = get_collections(all_rows)  #and get an empty list of collections
    return render_template('index.html', db = db, collections = collections)
    
@app.route('/upload')
def upload():
    message = request.args.get('message')  #a message about recent upload attempts will be displayed to the user
    if message == None:
        message = ''
    return render_template('upload.html', message = message)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #Check for file selection and appropriate file type
        if 'file' not in request.files:
            return redirect(url_for('upload', message = 'Please select a file.'))
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('upload', message = 'Please select a file with a name.'))
        if not allowed_file(file.filename):
            return redirect(url_for('upload', message = 'Please select a .bib file.'))
        
        #if everything looks good, upload the selected file
        else:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            collection = request.form['collection']
            bib_data = parse_file(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))  #parse the .bib file
            fill(bib_data, collection)   #populate the database
            return redirect(url_for('upload', message = 'Upload successful!'))
            
@app.route('/query')
def query():
    query_string = request.args.get('query_string')
    if query_string == None:
        results = []
    else:
        try:
            results = query_db(query_string)   #a good query string will return a list of matching database entries
        except sqlite3.OperationalError:  #the user may enter a non-sensical query
            results = ['error']
    return render_template('query.html', results = results)

@app.route('/query-er', methods = ['GET', 'POST'])  #following the upload/uploader naming convention
def upload_query():
    if request.method == 'POST':
        query_string = request.form['query_string']
        return redirect(url_for('query', query_string = query_string))   
    
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
   
if __name__ == '__main__':
    pass
    #app.run()
    #shutdown()
