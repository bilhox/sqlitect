import database
    
db = database.Database("./db/database.db" , overwrite=True)
db.createTable("users"  , {"user_id":"INT UNSIGNED" , "username":"CHAR(40)" , "password":"CHAR(40)"}, primary_keys=["user_id"])
for i in range(1 , 11):
    db.insert("users" , {"user_id":i , "username":f"lody{i}" , "password":f"admin{i}"})

db.addAttribute("users" , "email" , "VARCHAR(255)")
db.insert("users" , {"user_id":11 , "username":"sussy" , "password":"impostor" , "email":"hecker@heck.exe"})

db.deleteFromTable("users" , "user_id=9")
db.updateFromTable("users" , ["username='SFML dude'"] , "user_id=8")

db.executeSQLFile("test.sql")
db.loadTable("test.csv" , "pays")

for entry in db.fetch(
    "users",
    ["username" , "user_password" , "user_id"]
):
    print(entry)

for entry in db.fetch(
    "pays",
    []
):
    print(entry)
