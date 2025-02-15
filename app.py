from flask import Flask, request
from flask import render_template
 
app = Flask(__name__, template_folder="templates")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        return render_template("greet.html", latitude=request.form.get("latitude"), longitude=request.form .get("longitude"), households=request.form.get("households"), age=request.form.get("age"), population=request.form.get("population"), proximity=request.form.get("proximity"), income=request.form.get("income"))
        # return render_template("index.html")



if __name__ == "__main__":
    app.run()
