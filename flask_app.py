import re
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import db
from User import User
from Report import Report

ADMIN_LOGINS = ["Ivan_Trufanov", "admin"]

LOGIN_PAGE = "login.html"
EMPLOYEE_DASHBOARD_PAGE = "employee_dashboard.html"
ADMIN_PANEL_PAGE = "admin_panel.html"

app = Flask(__name__)
CORS(app)
db.Init()


# ! start

@app.route("/")
def start():
    return render_template(LOGIN_PAGE)

# ! templates

@app.route("/admin_panel")
def admin_panel():
    login = request.args.get("login")
    if login not in ADMIN_LOGINS:
        return redirect(url_for("employee_dashboard", login=login))
    return render_template(ADMIN_PANEL_PAGE, 
                            users=db.get_users(), reports=db.get_reports(),
                            user=db.get_user(login))

@app.route("/employees")
def employees():
    if request.args.get("login") not in ADMIN_LOGINS: 
        return redirect(url_for("employee_dashboard", login=request.args.get("login")))
    return render_template("employees.html", users=db.get_users(), 
                            user=db.get_user(request.args.get("login")))

@app.route("/routes")
def routes():
    return render_template("routes.html", user=db.get_user(request.args.get("login")))

@app.route("/vehicles")
def vehicles():
    return render_template("vehicles.html", user=db.get_user(request.args.get("login")))

@app.route("/submit_route")
def submit_route():
    return render_template("submit_route.html", user=db.get_user(request.args.get("login")))

@app.route("/charter")
def charter():
    return render_template("charter.html", user=db.get_user(request.args.get("login")))

@app.route("/employee_dashboard")
def employee_dashboard():
    login = request.args.get("login")
    user = db.get_user(login)
    if user is None:
        return jsonify({"status": "error", "message": "Пользователь не найден"}), 400
    return render_template("employee_dashboard.html", user=user)

@app.route("/login")
def login():
    if request.args.get("login") is not None: 
        return render_template("login.html", user=db.get_user(request.args.get("login")))
    return render_template("login.html")


# ! files

@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

# ! API 

# * login
@app.route("/login", methods=["POST"])
def api_login():
    user = db.get_user(request.form["login"])
    if user is None: 
        return jsonify({"status": "error", "message": "Пользователь не найден"}), 400
        # return redirect("/error?m=unknown")
    if user.login in ADMIN_LOGINS and request.form["password"] == user.password:
        return redirect(url_for("admin_panel", login=user.login))
    if user.password == request.form["password"]:
        # return jsonify({"status": "ok", "user": user.to_dict()}), 200
        return redirect(url_for("employee_dashboard", login=user.login))
    else:
        return jsonify({"status": "error", "message": "Неправильный пароль"}), 400
        # return redirect("/error?m=password")
    
# * errors 
@app.route("/error")
def error():
    m = request.args.get("m")
    if m == "unknown": 
        return render_template("error", message="Пользователь не найден")
    if m == "password": 
        return render_template("error", message="Неправильный пароль")

# * add user
@app.route("/add_user", methods=["POST"])
def add_user():
    # jsons = request.get_json()
    user = User(request.form["login"], request.form["password"], request.form["vk"], request.form["account"])
    if db.add_user(user)["status"] == "error": 
        return jsonify({"status": "error"}), 400
    return redirect(url_for("admin_panel", login=request.args.get("login")))

# * add route
@app.route("/add_route", methods=["POST"])
def api_submit_route():
    route = Report("ты сам не ввёл этого параметра", request.form["routes"], request.form["passengers"], request.form["fuel_bonus"])
    db_res = db.add_route(route)
    if db_res["status"] == "error": 
        return jsonify(db_res), 400
    return jsonify(db_res), 200


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
    # db.add_user(User("admin", "admin", "https://vk.com/sargsyan_albert", 777777))
