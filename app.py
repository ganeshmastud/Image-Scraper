from flask import Flask, render_template, request

from flask_bootstrap import Bootstrap
from scrapper.scrap import *
app = Flask(__name__)

Bootstrap(app)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/showimg', methods=["POST","GET"])
def showiamge():
    drive_path = './chromedriver'
    if request.method == "POST":
        search_term=request.form['keyword']
        srch_img=search_and_download_image(search_term,drive_path)
        print(srch_img)
        try:
            if len(srch_img)>0:

                return render_template('showimg.html', srch_img=srch_img,keyword=search_term,srch_img_len=len(srch_img))
            else:
                return "Please try with a different string"
        except Exception as e:
            print('no Images found ', e)
            return "Please try with a different string"


if __name__ == '__main__':
    app.run()
