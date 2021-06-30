import requests
from mysql import connector

import configparser


config = configparser.ConfigParser()
config.read('sf.ini')


mydb = connector.connect(
  host = config["sfDatabase"]['Host'],
  user = config["sfDatabase"]['User'],
  password = config["sfDatabase"]['Password'],
  database  = config["sfDatabase"]['Database']
)




client_id = config["sf"]['client_id']

client_secret = config["sf"]['client_secret']

sfdc_user = config["sf"]['sfusername']

sfdc_pass = config["sf"]['sfpassword']

auth_url = 'https://login.salesforce.com/services/oauth2/token'



response = requests.post(auth_url, data = {
                    'client_id':client_id,
                    'client_secret':client_secret,
                    'grant_type':'password',
                    'username':sfdc_user,
                    'password':sfdc_pass
                    })


json_res = response.json()
access_token = json_res['access_token']
auth = {'Authorization':'Bearer ' + access_token}


instance_url = json_res['instance_url']


url = instance_url + '/services/data/v45.0/query/?q=SELECT+name+,+id+,+AccountNumber+,+site+from+account'

res = requests.get(url, headers=auth)
r = res.json()

data = r['records']
for d in data:

    
    name = d["Name"]
    ID = d["Id"]
    num = d["AccountNumber"]
    site = d["Site"]
    try:
        mycursor = mydb.cursor()
            
        sql = 'INSERT INTO sfdata (Name,Id,Number,Site) VALUES ("{}","{}","{}","{}")'.format(name,ID,num,site)
            
            #print(sql)
        mycursor.execute(sql)
        mydb.commit()
    except connector.errors.IntegrityError as e:
        print(e)
    
