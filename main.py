from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/insertion")
def insert():
    return render_template("insertion.html")

@app.route("/deletion")
def delete():
    return render_template("deletion.html")  
          
@app.route("/adt")
def adt():
    return render_template("adt.html")

@app.route("/visualization")
def visualization():
    return render_template("visualization.html") 

if __name__ == "__main__":
    app.run(debug=True)