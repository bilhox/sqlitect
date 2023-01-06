import database

# Create a database
db = database.Database("here.db")

# Create a table
db.createTable(
    "users",
    {"user_id":"INT UNSIGNED","username":"VARCHAR(255)" , "user_password":"VARCHAR(255)"},
    primary_keys=["user_id"]
)

# Add elements to the table users
db.insert(
    "users",
    {"user_id":100 , "username":"Lody" , "user_password":"sussyPassword"}
)

# You can also get table attributes
db.getTableAttributes("users")
"""
>> ["user_id" , "username" , "user_password"]
"""

# Let's add more elements
for i in range(1 , 11):
    db.insert(
    "users",
    {"user_id":100+i , "username":f"Lody{i}" , "user_password":f"sussyPassword{i}"}
    )

# We can now get all elements
for entry in db.fetch("users",[]):
    print(entry)

"""
>> (100, 'Lody', 'sussyPassword')
>> (101, 'Lody1', 'sussyPassword1')
>> (102, 'Lody2', 'sussyPassword2')
>> (103, 'Lody3', 'sussyPassword3')
>> (104, 'Lody4', 'sussyPassword4')
>> (105, 'Lody5', 'sussyPassword5')
>> (106, 'Lody6', 'sussyPassword6')
>> (107, 'Lody7', 'sussyPassword7')
>> (108, 'Lody8', 'sussyPassword8')
>> (109, 'Lody9', 'sussyPassword9')
>> (110, 'Lody10', 'sussyPassword10')
"""

# You can also select specific datas with a condition
print(db.fetch("users" , attributes=["user_id"] , condition="username='Lody6'"))

"""
>> [(106)]
"""

# Let's add a new attribute to our table , by default , all other elements will have the email attribute set to None
db.addAttribute("users" , "email" , "VARCHAR(255)")

# More elements , you're familiar with it now , no ? 
db.insert("users" , {"user_id":55 , "username":"hecker" , "user_password":"impostor" , "email":"hecker@heck.me"})

# Finally , let's set the user_password element with the user_id 106 to sussyBaka
db.updateFromTable("users" , ["user_password='sussyBaka'"] , "user_id=106")

# let's verify if it got updated , so we fetch this specific element
print(db.fetch("users" , condition="user_id=106"))

"""
Result:
>> [(106, 'Lody6', 'sussyBaka', None)]
"""

#It works !