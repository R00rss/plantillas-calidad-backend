from base64 import decode
import json
import subprocess

from functions.format.format import formatDataUserDB2
from functions.DB.queries import generalQuery, updateQuery
from os import path

pathname = path.dirname(path.realpath(__file__))


def manageEncryp(data, option=1):  # option 1 = decrypt, option 2 = encrypt
    pathFile = path.join(pathname, "data.txt")
    pathPhp = path.join(pathname, "manageEncryp.php")
    currentData = "{" + '"data": "{}","option": "{}"'.format(data, option) + "}"

    with open(pathFile, "w") as txtFile:
        txtFile.write(currentData)
        txtFile.close()

    proc = subprocess.Popen(
        'php "{}"'.format(pathPhp), shell=True, stdout=subprocess.PIPE
    )
    result = json.loads(proc.stdout.read().decode("utf-8"))
    return result


def verifyUserPassword(username, password):
    # path del archivo json
    query = "SELECT * FROM user WHERE STATE = 1"
    result = generalQuery(query, 2)
    response = {
        "message": "usuario no autenticado",
        "success": True,
        "auth": False,
    }
    for row in result:
        usernameDB = manageEncryp(row[1], 1)["decrypted"]
        passwordDB = manageEncryp(row[12], 1)["decrypted"]
        # print(
        #     "usernameDB: {} - passwordDB: {} ".format(
        #         usernameDB,
        #         passwordDB,
        #     )
        # )
        if username == usernameDB and password == passwordDB:
            response["auth"] = True
            response["message"] = "usuario autenticado"
            response["user"] = formatDataUserDB2(row)
    return response
