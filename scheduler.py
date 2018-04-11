import yaml ### install the pyyaml package
import json
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint


### ------- HERE ARE PARAMETERS TO CONFIGURE -------

# host name in config.yml
host = ''

# The space in which your dashboards live
space_id =

# datagroup that you want to trigger off of. Make sure to use the format model_name::datagroup_name (e.g. datagroup = 'thelook::users_dg')
datagroup = ''

# the email address that recieves all these schedules
email = ''

# the user attribute id that you're filtering on.
# go to Admin > User Attributes. Click 'Edit' next to your selected user attribute, and you'll see the user_attribute_id at the end of the URL
user_attribute_id =

### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)

### ------- GET RELEVANT GROUP IDs -------
user_attributes_groups = looker.get_user_attribute_group_values(user_attribute_id)

group_ids = []
for i in user_attributes_groups:
    group_ids.append(i['group_id'])

### ------- get first user_id in that group -------
user_ids = []
for i in group_ids:
    user_ids.append(looker.get_group_users(i)[0]['id'])

### ------- GET A LIST OF DASHBOARD_IDs IN A SPECIFIED SPACE-------
dashboard_ids = []
dashboard_names = []
dashboards = looker.get_space_dashboards(space_id)
for i in range(len(dashboards)):
    dashboard_ids.append(dashboards[i]['id'])
    dashboard_names.append(dashboards[i]['title'])


## ------- GET ALL SCHEDULED PLANS THAT CURRENTLY EXIST ------
existing_scheduled_plans = []
for j in user_ids:
    # auth as each user to get their scheduled_plans
    looker.auth_user(j)
    for i in looker.get_scheduled_plans(space_id):
        if len(i) > 0:
            existing_scheduled_plans.append(i['title'])
        else:
            pass
looker.auth

### ------- EVALUATE WHICH PLANS NEED TO BE CREATED -------

# First create a list of every possible scheduled plan
meta_info_all = []
all_scheduled_plans_names = []
for i in range(len(dashboard_names)):
    for j in range(len(group_ids)):
        all_scheduled_plans = {
            'name': 'dashboard: '+ dashboard_names[i] + ', group_id: ' + str(group_ids[j]),
            'dashboard_id' : str(dashboard_ids[i]),
            'group_id' : str(group_ids[j]),
            'user_id' : str(user_ids[j])
        }
        meta_info_all.append(all_scheduled_plans)
        all_scheduled_plans_names.append(all_scheduled_plans['name'])

# Identify which plans need to be created
scheduled_plans_to_create = list(set(all_scheduled_plans_names) - set(existing_scheduled_plans))

# Assemble the necessary meta info for the new scheduled plans to be built
meta_info_build = []
for i in meta_info_all:
    # print i['name']
    print 'evaluating ' + i['name']
    if i['name'] in scheduled_plans_to_create:
        meta_info_build.append(i)
    else:
        pass
pprint(meta_info_build)

### ------- CREATE A PLAN FOR EACH GROUP/DASHBOARD COMBINATION THAT HAS NOT YET BEEN BUILT -------
def json_builder(dashboard_name, user_id ,dashboard_id, datagroup, email):
    return json.dumps({
                        "name": dashboard_name,
                        "user_id": user_id,
                        "dashboard_id": dashboard_id,
                        "datagroup": datagroup,
                        "run_as_recipient": False,
                        "scheduled_plan_destination":
                            [
                                {
                                "address": email,
                                "format": "csv_zip",
                                "type":"email"
                                }
                            ],
                        "run_once": True
                        })

### ------- BUILD THE PLANS -------
for i in meta_info_build:
    looker.create_scheduled_plan(json_builder(i['name'], i['user_id'], i['dashboard_id'], datagroup, email))
