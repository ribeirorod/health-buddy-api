# Todos Backend


## Models

* User Management
    + <s> Define model schema
    + Registration / Signup Method
        - <s> define uuid for '_id' 
        - encode password before persist on db
        - validate duplicity, check existing username / email </s>

    + Login Method
        - find matching username or email
        - decode validate password

    + Create auth token and define lifecycle
    + Start session method
        - return user details (wo password) and auth_oken
    + Logout method
        - clear session
    + Delete user/account method

<!-- * Field Duplicity check api () -->

* Food

## Routes

'POST' /user/signup \ 
'GET'  /user/login \ 
'GET'  /user/logout\ 
'POST' /user/track \ 
'POST' /user/favorite \ 
'GET'  /user/favorite \ 
'POST' /create/food \ 
'POST' /create/recipe \ 
'POST' /create/meal \ 
'GET'  /food \ 

## Database

* Python script to collect and parse multiple Datasources
    - list Data Sources

* Internal collections setup
    + UsersDB
    + FoodDB

* Internal Search
* External Search: Redirect to other DBs when not found
* Save external search results when found
* Barcode search

## How to implement a Barcode Reader ? Front or Backend ? 