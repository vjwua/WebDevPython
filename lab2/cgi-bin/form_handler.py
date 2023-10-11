import cgi
import html
import http.cookies
import os

form = cgi.FieldStorage()

cookie = http.cookies.SimpleCookie()

if "HTTP_COOKIE" in os.environ:
    cookie.load(os.environ["HTTP_COOKIE"])

counter = int(cookie.get("counter", 0))

try:
    username = form.getfirst("username", "admin")
    password = form.getfirst("password", "")
    username = html.escape(username)
    password = html.escape(password)
   
    region = form.getvalue("region", "не обрано мову")
    region_data = ""

    if (region == "lv"):
        region_data = "Львівська"
        counter += 1
    elif (region == "if"):
        region_data = "Івано-Франківська"
        counter += 1
    elif (region == "te"):
        region_data = "Тернопільська"
        counter += 1
    elif (region == "uzh"):
        region_data = "Закарпатська"
        counter += 1
    elif (region == "cv"):
        region_data = "Чернівецька"
        counter += 1
    else:
        region_data = "Регіон не обрано"

    groups = ["ipz31", "ipz32", "ipz33"]
    groups_checkbox = {}
    for group in groups:
        value_choice = form.getvalue(group, "off")
        groups_checkbox[group] = value_choice
        if value_choice == "on":
            counter += 1 
       
    if username == "admin" and password == "admin1234":
        message = "Вхід виконано успішно"
    else:
        message = "Вхід не успішний, перевірте дані входу"

    cookie["username"] = username
    cookie["password"] = password
    cookie["counter"] = str(counter)

    print(f"Set-cookie: {cookie['username']};")
    print(f"Set-cookie: {cookie['password']};")
    print(f"Set-cookie: {cookie['counter']};")

    if "delete_cookies" in form:
        cookie["username"] = ""
        cookie["password"] = ""
        cookie["counter"] = ""

except (NameError, KeyError) as e:
    message = "введіть дані для форми"
    region = None
    print(message)

print("Content-type:text/html\r\n\r\n")

template_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="UTF-8">
    <title>Обробка форми</title>
</head>
<body>
    <h1> Hi, {username} </h1>
    <h2> {message} </h1>
    <h3> Регіон: {region_data} </h2>
    <h3> Група: {groups_checkbox=} </h2>
    <h3> Кількість заповнених форм: {counter} </h3>
    <h3> {os.environ["HTTP_COOKIE"]=} </h3>
    <form method="POST">
        <input type="submit" name="delete_cookies" value="Видалити cookies">
    </form>
</body>
</html>
"""
print(template_html)