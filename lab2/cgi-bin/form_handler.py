import cgi
import html

form = cgi.FieldStorage()

try:
    username = form.getfirst("username", "admin")
    password = form.getfirst("password", "")
    username = html.escape(username)
    password = html.escape(password)
   
    region = form.getvalue("region", "не обрано мову")
    region_data = ""

    if (region == "lv"):
        region_data = "Львівська"
    elif (region == "if"):
        region_data = "Івано-Франківська"
    elif (region == "te"):
        region_data = "Тернопільська"
    elif (region == "uzh"):
        region_data = "Закарпатська"
    elif (region == "cv"):
        region_data = "Чернівецька"
    else:
        region_data = "Регіон не обрано"

    groups = ["ipz31", "ipz32", "ipz33"]
    groups_checkbox = {}
    for group in groups:
        value_choice = form.getvalue(group, "off")
        groups_checkbox[group] = value_choice
       
    if username == "admin" and password == "admin1234":
        message = "вхід виконано успішно"
    else:
        message = "вхід не успішний, перевірте дані входу"

except (NameError, KeyError) as e:
    message = "введіть дані для форми"
    lang = None
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
</body>
</html>
"""
print(template_html)