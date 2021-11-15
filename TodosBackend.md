[TOC]

# Todos Backend

## Models

### User Management

- [ ] Define user model schema

```
{
  id : uuid.str,
  created_at: timestamp,
  fullname: str, 
  email : str,
  username: str,
  birthday: str ,
  password: str
}
```



#### 1.  Registration | Signup Method

- [x] define uuid for '\_id'
- [x] encode password before persist on db
- [x] validate duplicity, check existing username and email 
- [ ] Generate token → Initiate session → Persist response

#### 2.  Login Method

- [x] Search matching username or email (identity)
- [x] Decode and validate password
- [x] Create auth token and define lifecycle (expiration)
- [x] Start session method (do we really need it? )
- [x] Return user details (wo password) and auth_oken

#### 3.  Logout method

- [ ] Kill token 
- [ ] clear session

#### 4. Check user status
#### 5. Edit | Delete user account

<!-- * Field Duplicity check api () -->



### Food Management

## Routes

```
'POST' /user/signup
'GET' /user/login
'GET' /user/logout
'POST' /user/track
'POST' /user/favorite
'GET' /user/favorite
'POST' /create/food
'POST' /create/recipe
'POST' /create/meal
'GET' /food
'GET'/product
```



## Data sources

- Python script to collect and parse multiple Datasources

  - Possible Data Sources:
  - https://github.com/openfoodfacts/openfoodfacts-python (API)
  - http://product-open-data.com/download (Direct download)
  - https://ibnreg.org/ (EUROPE)
  - https://fdc.nal.usda.gov/download-datasets.html (USDA Food and Brand Products db)


- Internal MongoDB collections setup

  - UsersDB
  - FoodDB

- Internal Search
- External Search: Redirect to other DBs when not found
- Save external search results when found
- Barcode search
- Define Data enrichment (Post user input)

  - - -

## Food data retrieval + Input pipelines

### 1. Barcode Scanner

- [ ] FtEnd decodes image into 13-char code -> GET request to BkEnd

- [ ] BkEnd search for code within local db -> return if found -> end

- [ ] If not found a db search hierarchy needs to be defined 

- [ ] Product is found -> Saves information on local db -> Send to FtEnd -> END

- [ ] Product not found -> User finishes -> END

- [ ] Product not found -> User opt for data input -> forward to user input process

### 2. Search Input

- [ ] FtEnd sends GET request based on user input ({type: "1", body: "banana"})
- [ ] As requests are processed based on every key stroke, API responds with top 10 results