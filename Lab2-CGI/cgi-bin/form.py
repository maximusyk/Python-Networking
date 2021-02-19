#! /usr/bin/env python3
import cgi
import html
import os
from http import cookies
import datetime


cook = cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
cookValue = cook.get('cookFormRequest')
expires = datetime.datetime.now() + datetime.timedelta(seconds=3)

if cookValue is None:
    countForm = 1
    print(
        f"Set-cookie: cookFormRequest={countForm}; max-age={str(60*10)}")
else:
    countForm = int(cookValue.value)+1
    print(
        f"Set-cookie: cookFormRequest={countForm}; max-age={str(60*10)}")

form = cgi.FieldStorage()
choice = html.escape(form["choice"].value)
name = html.escape(form["name"].value)
email = html.escape(form["email"].value)
branch = html.escape(form["branch"].value)
frameworks = form.getlist('framework')

print("Content-type: text/html\n")
print(f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" type="text/css" href="../css/util.css" />
    <link rel="stylesheet" type="text/css" href="../css/style.css" />
    <link rel="stylesheet" type="text/css" href="../css/helper.css" />
    <title>Form data handling</title>
</head>

<body>
    <div class="bg-cgi" style="background-image: url('../img/bg-01.jpg')">
    <div class="container-cgi">
        <div class="wrap-cgi">
            <h1 class="cgi-form-title">Form data have been successfully processed</h1>
            <p class="input">1-Choice -> <span class="cgi-res">'{choice}'</span></p>
            <p class="input">2-Name -> <span class="cgi-res">'{name}'</span></p>
            <p class="input">3-E-Mail -> <span class="cgi-res">'{email}'</span></p>
            <p class="input">4-Branch -> <span class="cgi-res">'{branch}'</span></p>
            <p class="input">
                5-Frameworks: """)
for framework in frameworks:
    print(f"\n<span class='cgi-res'> {framework} </span>")
print(
    f"<br><br><span class='cgi-cookie' style='font-size: 20px;'>Counter: <strong style='font-size: 20px;'>{cookValue.value}</strong></span>")
print(f"""
            </p>
        </div>
    </div>
    </div>

</body>

</html>
    """)
