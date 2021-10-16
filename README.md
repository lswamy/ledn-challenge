# Ledn Token Interview Challenge
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
