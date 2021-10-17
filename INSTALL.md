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
`
    curl -X POST http://localhost:5000/authorize -H 'Content-Type: application/json' -d '{"username":"ledn","password":"letmein"}'
`
This will return a json with a token
`{"auth_token":"a jwt token"}

`
    curl http://localhost:5000/accounts?country=CA&sort=amt -H 'Authorization: Bearer auth_token'
`



At Ledn, we are eager to find talented, resourceful, and passionate engineers to help us build the future of digital asset financial services. In light of this, we created a series of steps for us to know each other. One of these is a take home challenge, which will take a few hours to complete.

### Why a take-home challenge?
In-person coding interviews can be stressful and may hide your full potential. A take-home gives you a chance to work in a less stressful environment and showcase your talent.

### Our tech stack
As outlined in our job description, you will come across technologies which include a backend web framework (Typescript with NodeJS runtime) and a frontend library (React).

### Challenge Background
Ledn token is born! .. (fictional). Against our better judgement, we have rushed out our own token. We are now left with a slew of customer data and no way of capturing insights and managing accounts! Help us create a dashboard to better visualize our token holders' accounts. You are given a data set in the following format:
* `firstName` (Account Holder First Name)
* `lastName` (Account Holder Last Name)
* `country` (Country code)
* `email` (email)
* `dob` (Date of Birth)
* `mfa` (multi factor authentication type)
* `amt` (Number of ledn tokens held)
* `createdDate` (Account creation date)
* `referredBy` (email of referral account)

In this repo is a sample data file [`accounts.json`](/accounts.json).

### Requirements
1. You need to create an application which is either one of the following:
    * A web application displaying a table from the data provided. (Frontend leaning applicants)
    * An API which can request the data provided; (Backend leaning applicants)
  
2. Try to use fewer libraries and implement your own utilities and functionality.

3. For each case, your data needs to be displayed or requested as follows:
    * The user should be able to sort accounts on number of Ledn tokens held or creation date;
    * The user should be able to filter on account country, on mfa type, and by name;
    * The user should be able to download the data displayed as a CSV (Frontend only).
    
4. The system should be able to support larger sets of data on the order of 100k records.
   
5. Feel free to choose any tech stack that can accomplish the requirements. Although a similar stack to ours would be better.
   
### Time Estimate
Estimated effort to complete this challenge is up to 6 hours.

### Submission
You may choose to submit your solution however you'd like. Feel free to send us a link to a hosted git repo, or send us your solution directly. Whichever method you choose, please include instructions on running your solution locally.

### Following Steps
Upon submission of the challenge, we will review your code and reach out to you with comments. If your submission passes our criteria, a following interview will be scheduled to discuss your implementation in further detail. We feel this is another great way to assess your understanding rather than on the spot coding exercises!

We want you to succeed as much as you do, so we wish you the best of luck! Looking forward to your submission!
