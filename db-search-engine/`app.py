from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, MetaData, Table

app = Flask(__name__)

# Database connection parameters
db_config = {
    'host': '',
    'user': '',
    'password': '',
    'dbname': ''
}

# Initialize the database engine and metadata
engine = None
metadata = None

@app.route('/')
def index():
    if not db_config['host']:
        return redirect(url_for('connect_wizard'))
    
    # List tables in the database
    tables = []
    with engine.connect() as connection:
        for table_name in metadata.tables.keys():
            tables.append(table_name)
    
    return render_template('index.html', tables=tables)

@app.route('/connect_wizard', methods=['GET', 'POST'])
def connect_wizard():
    global db_config, engine, metadata
    
    if request.method == 'POST':
        db_config['host'] = request.form['host']
        db_config['user'] = request.form['user']
        db_config['password'] = request.form['password']
        db_config['dbname'] = request.form['dbname']
        
        # Create database engine and metadata
        engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['dbname']}")
        metadata = MetaData(bind=engine)
        
        return redirect(url_for('index'))
    
    return render_template('connect_wizard.html')

if __name__ == '__main__':
    app.run(debug=True)
