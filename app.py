from flask import Flask,render_template,request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Konfigurasi MongoDB
connect_string = 'mongodb+srv://fransiscafortuasimamora29:sparta@cluster0.4ftdsad.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connect_string)
db = client.dbsparta

app=Flask(__name__)

@app.route('/')
def home():
    # Handle POST Request here
    return render_template('index.html')

@app.route('/personaldiary', methods =['GET'])
def show_diary():
    # Mengambil data dari MongoDB
    articles = list(db.personaldiary.find({},{'_id' : False}))
    return jsonify({'articles' : articles})

@app.route('/personaldiary', methods =['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    # Untuk memberi waktu
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    # Untuk bagian save file yang akan diunggah
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    # Untuk bagian save profile yang akan diunggah
    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    time = today.strftime('%Y.%m.%d')

    doc = {
        'file': filename,
        'profile': profilename,
        'title' : title_receive,
        'content' : content_receive,
        'time': time,
    }
    db.personaldiary.insert_one(doc)
    return jsonify({'msg' : 'Data Tersimpan'})

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)