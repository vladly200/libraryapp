from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('templates/index.html')
@app.route('/handle_click',methods = ['POST'])
def handle_click():
    print("Button was clicked!")
    return "Button was clicked!"

if __name__ == "__main__":
    app.run()