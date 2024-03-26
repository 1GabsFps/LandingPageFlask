from flask import Flask, render_template, request, redirect
import mysql.connector as sql
import csv
import os

connection = sql.connect(host="127.0.0.1", user="root", password="", database="logins")


app = Flask(__name__)

app.config["STATIC_FOLDER"] = "static"
if not os.path.exists("products.csv"):
    with open("products.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Produto", "Preco", "Estoque"])


@app.route("/")
def home():
    return redirect("/login")


@app.route("/list", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        product = request.form["product"]
        price = float(request.form["price"])
        stock = int(request.form["stock"])
        with open("products.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([product, price, stock])
        return redirect("/list")
    with open("products.csv", "r") as f:
        products = [row for row in csv.reader(f)]
    return render_template("index.html", products=products)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM usuarios WHERE nome = '{username}' AND senha = '{password}'"
        )
        user = cursor.fetchall()
        connection.commit()
        cursor.close()
        if user:
            return redirect("/list")
        else:
            return redirect("/login")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO usuarios (nome, senha) VALUES ('{username}', '{password}')"
        )
        connection.commit()
        cursor.close()
        return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
