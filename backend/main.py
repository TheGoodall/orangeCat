from flask import Flask
app = Flask(__name__,
        static_folder='../frontend/')

#@app.route('/')
#def send_statics(path):
#    return send_from_directory('../frontend', "index.html")


app.run()
