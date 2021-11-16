## Flask-API

### Dedicated repository to Health buddy API

#### Installing Mongo Client

MacOS 

```
brew tap mongodb/brew
brew install mongodb-community@5.0

# run service 
brew services start mongodb-community@5.0

# stop service 
brew services stop mongodb-community@5.0

# run on background
mongod --config /usr/local/etc/mongod.conf --fork

```
---
Linux

Windows

#### Flask (Instalation and Setup)

#### Sending requests from Terminal (examples)

Routes

```
# /auth/login body = {"identity": "username/email", password = "********"}
curl localhost:5000/auth/login -d '{"identity": "rodtest", "password":"12345"}' -H 'Content-Type: application/json'
```


