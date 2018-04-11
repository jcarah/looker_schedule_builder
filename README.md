# Looker Schedule Builder

Use this repo to maintain and update a set of Looker schedules for every dashboard and user attribute value combination. This will enable you to re-run dashboard queries tied to a datagroup as soon as Looker's query cache is invalidated.

## Getting Started
- Change the config_sample.yml to config.yml and update with your credentials. You can get API 3 credentials by:
   1) Go to Admin > Users in your Looker instance.
   2) Either make a new user or click to an existing users page using the "Edit" button. Remember the API user will have the same credentials as the user so keep that security point in mind when choosing a user.
   3) Click the "New API 3 Key" button to make API 3 credentials for the user.
   4) In the config.yml file, the "Client Secret" on the user page should be copied into the `secret:` string and the Client ID should be copied into the `token:` string. For the `host:` string replace the word `localhost` with your Looker instance domain name (i.e. _companyname_.looker.com).
   5) Make sure your Looker instance is configured to a working API Host URL by going to Admin > API in your Looker instance and checking the API Host URL field. A blank field is the default for Looker to auto-detect the API Host URL.
- Configure the following parameters in `scheduler.py`:
 - host
 - space_id
 - datagroup
 - email
 - user_attribute_id
- Run `scheduler.py` in the shell with `python scheduler.py`

## Usage
Create a cron job to run `scheduler.py` on some recurring interval. This will ensure that your schedules are up to date each time a new dashboard or user_attribute value is created.

## Built With

- [Looker Python API Samples](https://github.com/llooker/python_api_samples/): A simple, unofficial Python SDK for Looker.
