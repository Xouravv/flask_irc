from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'


@app.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html"),404

if __name__ == '__main__':
    app.run(debug=True,port=1234)