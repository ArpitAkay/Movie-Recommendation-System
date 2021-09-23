from flask import Flask, render_template, request
from movierecommendation import movieteller,popular_movies

app = Flask(__name__)

@app.route('/')
def show_index_html():
    a=popular_movies()
    return render_template('interface.html',a=a)
@app.route('/send')
def fuction1():
    return render_template('face.html',movies=[],des=[])
@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
    pay = request.form['pay']
    movies,des = movieteller(pay)
    return render_template('face.html',movies = movies,des=des)

if __name__ =='__main__':
    app.run(debug=True)
