# product database was taken from here
# https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/methods-and-application-of-food-composition-laboratory/mafcl-site-pages/sr11-sr28/
#  background img was taken from https://unsplash.com/photos/lcZ9NxhOSlo

import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///nutritions.db")


@app.route("/")
def index():
        # route index() renders the page with the form that the search() is processing
        return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":

        # get the keyword from the user from the form
        product = request.form.get("query").upper()

        # if there is no keyword, redirect to the main
        if not product:
            return redirect("/")

        # select all products discriptions from the database
        food = db.execute(
                "SELECT Shrt_Desc FROM nutritions")

        food_arr = []

        # add all products that start with a keyword to an empty array
        for f in food:
            if f["Shrt_Desc"].startswith(product):
                food_arr.append(f["Shrt_Desc"])

        if not food_arr:
            return render_template("apology.html", apology =  "There is no such meal!")

        # render a page with a selection of all products that start with a keyword
        return render_template("search.html", product=product, food=food, food_arr=food_arr)

    else:

        return redirect("/")


@app.route("/nutritions", methods=["GET", "POST"])
def nutritions():

    if request.method == "POST":

        # product selected by the user from the form on the search page
        product_single = request.form.get("check")

        # selection of the main food components from the database
        food_plc = db.execute(
                "SELECT Water_g, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g FROM nutritions WHERE Shrt_Desc = :product_single", product_single=product_single)

        # selection food minerals from the database
        food_min = db.execute(
                "SELECT Ash_g, Calcium_mg, Iron_mg, Magnesium_mg, Phosphorus_mg, Potassium_mg, Sodium_mg, Zinc_mg, Copper_mg, Manganese_mg, Selenium_µg FROM nutritions WHERE Shrt_Desc = :product_single", product_single=product_single)

        # selection of food vitamins from the database (three tables for easy display)
        food_vit1 = db.execute(
                "SELECT Vit_C_mg, Thiamin_mg, Riboflavin_mg, Niacin_mg, Panto_Acid_mg, Vit_B6_mg, Folate_Tot_µg, Folic_Acid_µg, Food_Folate_µg, Folate_DFE_µg, Choline_Tot_mg FROM nutritions WHERE Shrt_Desc = :product_single", product_single=product_single)

        food_vit2 = db.execute(
                "SELECT Vit_B12_µg, Vit_A_IU, Vit_A_RAE, Retinol_µg, Alpha_Carot_µg, Beta_Carot_µg,	Beta_Crypt_µg, Lycopene_µg, Lut_Zea_µg, Vit_E_mg, Vit_D_µg FROM nutritions WHERE Shrt_Desc = :product_single", product_single=product_single)

        food_vit3 = db.execute(
                "SELECT Vit_D_IU, Vit_K_µg, FA_Sat_g, FA_Mono_g, FA_Poly_g, Cholestrl_mg FROM nutritions WHERE Shrt_Desc = :product_single", product_single=product_single)


        return render_template("nutritions.html", product_single=product_single, food_plc = food_plc, food_min=food_min,
                                food_vit1=food_vit1, food_vit2=food_vit2, food_vit3=food_vit3)

    else:

        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("register.html")

    else:
        # Forget any user_id
        session.clear()

        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return render_template("apology.html", apology =  "Missing username!")

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return render_template("apology.html", apology =  "Missing password!")

        # Ensure confirmation was submitted
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return render_template("apology.html", apology =  "Missing confirmation!")

        # Ensure password == confirmation was submitted
        if not password == confirmation:
            return render_template("apology.html", apology =  "Password is not confirmated!")

        hash = generate_password_hash(password)

        # Query database for username
        result = db.execute("SELECT * FROM users WHERE username=:username", username=username)
        if result:
            return render_template("apology.html", apology ="Such name already exist")

        # Save user in database
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)

        rows1 = db.execute("SELECT * FROM users WHERE username=:username", username=username)

        # Remember which user has regested
        session["user_id"] = rows1[0]["id"]

        flash("You are registed!")

        return redirect("/")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", apology = "must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", apology ="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html", apology = "invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/add", methods=["GET", "POST"])
# @login_required
def add():

    # adding food to the diary only for registered users
    if request.method == "GET":

        return render_template("add.html")

    else:

        return redirect("/")


@app.route("/search_diary", methods=["GET", "POST"])
def search_diary():

    if request.method == "POST":

        # get the keyword from the user from the form
        product = request.form.get("query").upper()

        #   if there is no keyword, redirect to the add page
        if not product:
            return render_template("add.html")

        # select all products discriptions from the database
        food = db.execute(
                "SELECT Shrt_Desc FROM nutritions")

        food_arr = []

         # add all products that start with a keyword to an empty array
        for f in food:

            if f["Shrt_Desc"].startswith(product):
                food_arr.append(f["Shrt_Desc"])

        # if there is no such product in the database, display an apology
        if not food_arr:
            return render_template("apology.html", apology =  "There is no such meal!")

        # if everything is ok, display a page with a proposal to choose a product from the list
        return render_template("search_diary.html", product=product, food=food, food_arr=food_arr)

    else:

        return redirect("/")


@app.route("/diary_nutritions", methods=["GET", "POST"])
def diary_nutritions():

    if request.method == "POST":

        # get the keyword from the user from the form
        product = request.form.get("check")

        #   if there is no keyword, redirect to the add page
        if not product:
            return render_template("add.html")

        # turn the name of the product into upper case since such is in the database
        product = request.form.get("check").upper()

        # get the quantity from the user from the form
        quantity = request.form.get("quantity")

        #   if there is no quatity, redirect to the add page
        if not quantity:
            return render_template("add.html")

        quantity = int(request.form.get("quantity"))

        # add the selected product and quantity to the table
        db.execute("INSERT INTO history (user_id, product, quantity) VALUES (?, ?, ?)", session["user_id"], product, quantity)

        flash("Added!")

        return render_template("add.html")

    else:

        return redirect("/")

@app.route("/food_diary", methods=["GET", "POST"])
def food_diary():

    if request.method == "GET":

        # select from the table all the products entered and group by name
        food = db.execute(
            "SELECT product, SUM(quantity) as totalFood FROM history WHERE user_id=:user_id GROUP BY product", user_id=session["user_id"])

        # new dictionaries for recording the summed values of trace elements
        newdb = {}
        newdb_min = {}
        newdb_vit1 = {}
        newdb_vit2 = {}
        newdb_vit3 = {}

         # for each product in food
        for prod in food:
            # the product's name
            single_prod_name = prod["product"]

            # total product quantity
            single_prod_quantity = float(prod["totalFood"])

            # select from the table all trace elements for this product
            single_prod_plc = db.execute(
                "SELECT Water_g, Energ_Kcal, Protein_g, Lipid_Tot_g, Carbohydrt_g, Fiber_TD_g, Sugar_Tot_g FROM nutritions WHERE Shrt_Desc = :single_prod_name", single_prod_name=single_prod_name)
            single_prod_min = db.execute(
                "SELECT Ash_g, Calcium_mg, Iron_mg, Magnesium_mg, Phosphorus_mg, Potassium_mg, Sodium_mg, Zinc_mg, Copper_mg, Manganese_mg, Selenium_µg FROM nutritions WHERE Shrt_Desc = :single_prod_name", single_prod_name=single_prod_name)
            single_prod_vit1 = db.execute(
                "SELECT Vit_C_mg, Thiamin_mg, Riboflavin_mg, Niacin_mg, Panto_Acid_mg, Vit_B6_mg, Folate_Tot_µg, Folic_Acid_µg, Food_Folate_µg, Folate_DFE_µg, Choline_Tot_mg FROM nutritions WHERE Shrt_Desc = :single_prod_name", single_prod_name=single_prod_name)
            single_prod_vit2 = db.execute(
                "SELECT Vit_B12_µg, Vit_A_IU, Vit_A_RAE, Retinol_µg, Alpha_Carot_µg, Beta_Carot_µg,	Beta_Crypt_µg, Lycopene_µg, Lut_Zea_µg, Vit_E_mg, Vit_D_µg FROM nutritions WHERE Shrt_Desc = :single_prod_name", single_prod_name=single_prod_name)
            single_prod_vit3 = db.execute(
                "SELECT Vit_D_IU, Vit_K_µg, FA_Sat_g, FA_Mono_g, FA_Poly_g, Cholestrl_mg FROM nutritions WHERE Shrt_Desc = :single_prod_name", single_prod_name=single_prod_name)

            #
            for key, value in single_prod_plc[0].items():
                # if there are empty cells in the Nutrition database, change to 0,0
                if not value:
                    value = "0,0"

                # turn a string into a number
                # f the amount of trace elements in single_prod_name
                f = float(value.replace(',','.'))*single_prod_quantity/100

                # summarize trace elements for all products
                if key in newdb:

                    newdb[key] += f

                else:

                    newdb.update({
                    key: f
                })

            # round off the values in the finished newdb
            newdb.update((key, round(val, 2)) for key, val in newdb.items())


            # do the same for minerals
            for key, value in single_prod_min[0].items():
                if not value:
                    value = "0,0"
                f = float(value.replace(',','.'))*single_prod_quantity/100

                if key in newdb_min:

                    newdb_min[key] += f

                else:

                    newdb_min.update({
                    key: f
                })

            newdb_min.update((key, round(val, 2)) for key, val in newdb_min.items())

            # do the same for vitamins1
            for key, value in single_prod_vit1[0].items():
                if not value:
                    value = "0,0"
                f = float(value.replace(',','.'))*single_prod_quantity/100

                if key in newdb_vit1:

                    newdb_vit1[key] += f

                else:

                    newdb_vit1.update({
                    key: f
                })

            newdb_vit1.update((key, round(val, 2)) for key, val in newdb_vit1.items())

            # do the same for vitamins2
            for key, value in single_prod_vit2[0].items():
                if not value:
                    value = "0,0"
                f = float(value.replace(',','.'))*single_prod_quantity/100

                if key in newdb_vit2:

                    newdb_vit2[key] += f

                else:

                    newdb_vit2.update({
                    key: f
                })

            newdb_vit2.update((key, round(val, 2)) for key, val in newdb_vit2.items())

            # do the same for vitamins3
            for key, value in single_prod_vit3[0].items():
                if not value:
                    value = "0,0"
                f = float(value.replace(',','.'))*single_prod_quantity/100

                if key in newdb_vit3:

                    newdb_vit3[key] += f

                else:

                    newdb_vit3.update({
                    key: f
                })

            newdb_vit3.update((key, round(val, 2)) for key, val in newdb_vit3.items())

        return render_template("food_diary.html",
            food=food, newdb=newdb, newdb_min=newdb_min,
            newdb_vit1=newdb_vit1, newdb_vit2=newdb_vit2, newdb_vit3=newdb_vit3)

    else:
        return redirect("/")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "GET":

        products = db.execute(
            "SELECT DISTINCT product, SUM(quantity) as totalFood FROM history WHERE user_id=:user_id GROUP BY product HAVING totalFood > 0", user_id=session["user_id"])
        return render_template("delete.html", products=products)

    if request.method == "POST":

        product = request.form.get("check")

        if not product:
            return render_template("apology.html", apology =  "Enter a product!")

        product = request.form.get("check").upper()

        quantity = (request.form.get("quantity"))

        if not quantity:
            return render_template("apology.html", apology =  "Enter a quantity!")
        quantity = int(request.form.get("quantity"))

        food_exist = db.execute(
            "SELECT DISTINCT product, SUM(quantity) as totalFood FROM history WHERE user_id=:user_id GROUP BY product HAVING totalFood > 0", user_id=session["user_id"])

        for food in food_exist:

            if food["product"] == product:
                if int(food["totalFood"]) < int(quantity):
                    return render_template("apology.html", apology =  "You didn't eat soo much!")

        db.execute("INSERT INTO history (user_id, product, quantity) VALUES (?, ?, ?)", session["user_id"], product, -int(quantity))

        flash("Delete!")

        products = db.execute(
            "SELECT DISTINCT product, SUM(quantity) as totalFood FROM history WHERE user_id=:user_id GROUP BY product HAVING totalFood > 0", user_id=session["user_id"])

        return render_template("delete.html", products=products)

