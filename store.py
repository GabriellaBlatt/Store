from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    passwd="root",
    db="store",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@post("/category")
def add_category():
    name = request.POST.get("name")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories WHERE category_name  = '{}'".format(name)
            cursor.execute(sql)
            info = cursor.fetchall()
            if name.isspace():
                result = {
                    "STATUS": "ERROR",
                    "MSG": "Name parameter is missing",
                    "CODE": "400"
                }
                return json.dumps(result)
            if info:
                result = {
                    "STATUS": "ERROR",
                    "MSG": "Category already exists",
                    "CODE": "200"
                }
                return json.dumps(result)
            sql = "INSERT INTO categories (category_name) values ('{}')".format(name)
            cursor.execute(sql)
            connection.commit()
            mys = "SELECT * FROM categories WHERE category_name = '{}'".format(name)
            cursor.execute(mys)
            catId = cursor.fetchall()
            result = {
                "STATUS": "SUCCESS",
                "MSG": "Category created successfully",
                "CAT_ID": catId[0]["CAT_ID"],
                "CODE": "201"
            }
            return json.dumps(result)
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "Internal Error",
            "CODE": "500"
        }
        return json.dumps(result)


@delete("/category/<id>")
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories WHERE CAT_ID = '{}'".format(id)
            cursor.execute(sql)
            info = cursor.fetchall()
            if info:
                sql = "DELETE * FROM categories WHERE CAT_ID = '{}'".format(id)
                cursor.execute(sql)
                connection.commit()
                result = {
                    "STATUS": "SUCCESS",
                    "MSG": "Category deleted successfully",
                    "CODE": "201"
                }
                return json.dumps(result)
            result = {
                "STATUS": "ERROR",
                "MSG": "Category not found",
                "CODE": "404"
            }
            return json.dumps(result)
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "Internal Error",
            "CODE": "500"
        }
        return json.dumps(result)


@get("/categories")
def fetch_category():
    try:
        print("im in get of cat")
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            info = cursor.fetchall()
            print("printing info from fetch")
            print(info)
            if info:
                result = {
                    "STATUS": "SUCCESS",
                    "CATEGORIES": info,
                    "CODE": "200"
                }
                return json.dumps(result)
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "Internal Error",
            "CODE": "500"
        }
        return json.dumps(result)


@post("/product")
def add_product():
    title = request.forms.get('title')
    desc = request.forms.get('desc')
    price = request.forms.get("price")
    img_url = request.forms.get("img_url")
    category = request.forms.get("category")
    favorite = request.forms.get("favorite")
    id = request.forms.get('id')
    if not favorite:
        fav = False
    else:
        fav = True
    mandatory = [title, desc, price, img_url, category]
    try:
        with connection.cursor() as cursor:
            for mand in mandatory:
                if not mand:
                    print("missing mandatory")
                    result = {
                        "STATUS": "ERROR",
                        "MSG": "Missing parameters",
                        "CODE": "400"
                    }
                    return json.dumps(result)
            sql = "SELECT * FROM categories WHERE CAT_ID = '{}'".format(category)
            cursor.execute(sql)
            catId = cursor.fetchall()
            if catId:
                print("valid Category")
                if id is None:
                    print("there is an id inserted")
                    sql = "UPDATE customers SET title={0}, prod_desc={1}, price={2}, img_url={3}," \
                          " CAT_ID={4}, favorite={5}" \
                          " WHERE PRODUCT_ID={6}".format(title, desc, str(price),
                                                         img_url, str(category), str(fav), str(id))
                    cursor.execute(sql)
                    connection.commit()
                    result = {
                        "STATUS": "SUCCESS",
                        "PRODUCT_ID": catId[0]["CAT_ID"],
                        "CODE": "201"
                    }
                    return json.dumps(result)
                else:
                    print("id is none here")
                    sql = "INSERT INTO products (title, prod_desc, price, img_url, CAT_ID, favorite) " \
                          "VALUES({0}, {1}, {2}, {3}, {4}, {5});".format(title, desc,
                                                                         str(price), img_url, str(category), str(fav))
                    cursor.execute(sql)
                    connection.commit()
                    result = {
                        "STATUS": "SUCCESS",
                        "CATEGORIES": cursor.lastrowid,
                        "CODE": "201"
                    }
                    return json.dumps(result)
            else:
                result = {
                    "STATUS": "ERROR",
                    "MSG": "Category not found",
                    "CODE": "404"
                }
                return json.dumps(result)
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "Internal Error",
            "CODE": "500"
        }
        return json.dumps(result)


@get("/product/<id>")
def fetch_product(id):
    try:
        print("im in get of product")
        with connection.cursor() as cursor:
            sql = "SELECT * FROM product WHERE PRODUCT_ID={}".format(id)
            cursor.execute(sql)
            info = cursor.fetchall()
            print("printing info from fetch of product id")
            print(info)
            if info:
                result = {
                    "STATUS": "SUCCESS",
                    "PRODUCT": info,
                    "CODE": "200"
                }
                return json.dumps(result)
            else:
                result = {
                    "STATUS": "ERROR",
                    "MSG": "Product not found",
                    "CODE": "404"
                }
                return json.dumps(result)
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "Internal Error",
            "CODE": "500"
        }
        return json.dumps(result)


@delete("/product/<id>")
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories WHERE PRODUCT_ID = '{}'".format(id)
            cursor.execute(sql)
            info = cursor.fetchall()
            if info:
                sql = "DELETE * FROM categories WHERE PRODUCT_ID = '{}'".format(id)
                cursor.execute(sql)
                connection.commit()
                result = {
                    "STATUS": "SUCCESS",
                    "MSG": "Product deleted successfully",
                    "CODE": "201"
                }
                return json.dumps(result)
            result = {
                "STATUS": "ERROR",
                "MSG": "Product not found",
                "CODE": "404"
            }
            return json.dumps(result)
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "Internal Error",
            "CODE": "500"
        }
        return json.dumps(result)


@get("/products")
def fetch_products():
    try:
        print("im in get of cat")
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            info = cursor.fetchall()
            print("printing info from products fetch")
            print(info)
            if info:
                result = {
                    "STATUS": "SUCCESS",
                    "PRODUCTS": info,
                    "CODE": "200"
                }
                return json.dumps(result)
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "Internal Error",
            "CODE": "500"
        }
        return json.dumps(result)


@get("/category/<id>/products")
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE CAT_ID = '{}'".format(id)
            cursor.execute(sql)
            info = cursor.fetchall()
            if info:
                result = {
                    "STATUS": "SUCCESS",
                    "PRODUCTS": info,
                    "CODE": "200"
                }
                return json.dumps(result)
            else:
                result = {
                    "STATUS": "ERROR",
                    "MSG": "Category not found",
                    "CODE": "404"
                }
                return json.dumps(result)
    except:
        result = {
            "STATUS": "ERROR",
            "MSG": "Internal Error",
            "CODE": "500"
        }
        return json.dumps(result)


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


# run(host='0.0.0.0', port=argv[1])
if __name__ == "__main__":
    run(host="localhost", port=7000, debug=True)
