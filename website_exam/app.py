from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# enumerate fonksiyonunu Jinja2'de kullanılabilir hale getirin
@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)


# Veritabanı bağlantısı
def connect_db():
    return sqlite3.connect('db/scores.db')

# Veritabanı tablo oluşturma
def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, score INTEGER)''')
    conn.commit()
    conn.close()

create_table()

# Ana Sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Sınav Sayfası
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = [
        {
            'question': 'Python’da veri tipi olarak hangisi kullanılmaz?',
            'options': ['List', 'Tuple', 'Dictionary', 'String', 'Tree'],
            'answer': 'Tree'
        },
        {
            'question': 'Python’da yapay zeka için hangi kütüphane kullanılır?',
            'options': ['numpy', 'pandas', 'scikit-learn', 'requests'],
            'answer': 'scikit-learn'
        },
        {
            'question': 'Flask nedir?',
            'options': ['Web framework', 'Veritabanı', 'Dosya sistemi', 'API'],
            'answer': 'Web framework'
        }
    ]

    if request.method == 'POST':
        score = 0
        for i, question in enumerate(questions):
            if request.form.get(f'question-{i}') == question['answer']:
                score += 1

        session['score'] = score

        conn = connect_db()
        c = conn.cursor()
        c.execute('INSERT INTO scores (score) VALUES (?)', (score,))
        conn.commit()
        conn.close()

        return redirect(url_for('result'))

    return render_template('quiz.html', questions=questions)

# Sonuç Sayfası
@app.route('/result')
def result():
    score = session.get('score', 0)

    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT MAX(score) FROM scores')
    max_score = c.fetchone()[0]
    conn.close()

    return render_template('result.html', score=score, max_score=max_score)

if __name__ == '__main__':
    app.run(debug=True)
