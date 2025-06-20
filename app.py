from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change this to your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Add your MySQL password
app.config['MYSQL_DB'] = 'student_management_system'

mysql = MySQL(app)

# Homepage Route (Login Page)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
        
        cursor.close()

    return render_template('index.html')

# Registration Page Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO students (name, age, course, username, password) 
                        VALUES (%s, %s, %s, %s, %s)''', (name, age, course, username, password))
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('index'))
    
    return render_template('index.html', registration=True)

# Dashboard Page Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
