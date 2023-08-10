# import requests, json


# url = "https://api.opensea.io/api/v1/collection/boredapeyachtclub"

# response = requests.request("GET", url)
# a = json.dumps(response.json(), indent=4)
# print(a)

# import requests

# url = "https://api.opensea.io/api/v1/asset/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/1/"

# response = requests.request("GET", url)

# print(response.text)

# url = "https://api.opensea.io/api/v1/collections?offset=0&limit=300"

# headers = {"Accept": "application/json"}

# response = requests.request("GET", url, headers=headers)

# print(response.text)
# 5AJqCETCc8HyMSaxWtSFmgqCKRNR5UrLPIKkB2bZ3I2jzGbEdInGKRnct7USAXQ3


trucks_raw = [1, 2, 3, 4, 5, 6, 7, 8, 9]

new_array = {9646': {
'truck_id': '9646', 
'lat': 50.711545, 
'lon': 9.164393, 
'NAME1': 'KN4903G - Mykhailo Smarovydlo (CH/IT)', 
'NAME2': 'Smarovydlo Mykhailo', 
'NAME3': '', 
'FIRMWARE': '0001'
}

for item_new in new_array:
    for item_old in trucks_raw:
        if item_new == item_old:
            print("DONE")



