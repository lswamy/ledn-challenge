# Overview
I have chosen to focus on the backend api and build the app using Python/Flask and MongoDB. To keep it lightweight, minimal libraries were used.

There are two endpoints:
* `/authorize` is used first to fetch and authorization token to access the /accounts endpoint
* `/accounts` is used to retrieve account entries from the database

Since accounts contain personal information it is best practice to secure endpoints accessing this data. I have implemented a simple JWT flow to demonstrate this.
The /authorize endpoint will accept login credentials and provide a short lived access token.

The /accounts endpoint will accept the following parameters:
* `country` filter on country code
* `mfa` filter on mfa type
* `name` filter on first name or last name
* `sort` field to sort on, accepts "createdDate" or "amt"
* `sort_dir` sorting direction, accepts 1 (ascending) or -1 (descending)
* `limit` number of results to return
* `next_cursor` a token used for pagination, next set of results will start at this value

The authentication token retrieved from the /authorize endpoint must be included in the header of the /accounts request:
    * `Authorization: Bearer <auth_token>`

The response will be a json object with the following properties:
* `results` a list of accounts, number of results is limited to the requested amount
* `total_results` total number of accounts that meet the requested criteria
* `next_cursor` the value of createdDate or amt (depending of sort param) to fetch the next set of results


# Install Instructions
This app is can be run in a local python virtual environment or using docker.

### Docker
1. edit .env if necessary, the defaults are should work for the docker build
2. `docker-compose build`
3. `docker-compose up`
4. app is accessible at http://localhost:5000
    * authorize endpoint is http://localhost:5000/authorize
    * accounts endpoint is https://localhost:5000/accounts

### Local
1. edit .env MONGODB_URL to point to your local database
2. create a virtual environment and install requirements
    * `python3 -m venv .venv`
    * `source .venv/bin/activate`
    * `pip install -r requirements.txt`
3. run flask
    * `flask run`
4. app is accessible at http://localhost:5000
    * authorize endpoint is http://localhost:5000/authorize
    * accounts endpoint is https://localhost:5000/accounts

On first execution, if accounts collection in database is empty, the accounts.json file will be imported. Note that if you choose to use your own database,
the date fields in the json were converted to ISODate objects and indexes created for sorting and performance.

To use first call the /authorize endpoint, username and password are defined in `.env` file.

`curl -X POST http://localhost:5000/authorize -H 'Content-Type: application/json' -d '{"username":"ledn","password":"letmein"}'`

This will return a json with a token
`{"auth_token":"a jwt token"}`

`curl http://localhost:5000/accounts?country=CA&sort=amt -H 'Authorization: Bearer auth_token'`
