import requests

BASE="http://127.0.0.1:5000/"

#response = requests.get(BASE + "helloworld/bill")
#print(response.json())

#response = requests.get(BASE + "helloworld/tom")
#print(response.json())


#input()

data = [
    {"likes":10, "name":"My video", "views":314},
    {"likes":0, "name":"I hate you", "views":98000},
    {"likes":1918, "name":"I love you", "views":30124}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + "video/1")
print(response.json())
input()
response = requests.delete(BASE + "video/1")
print(response)
input()
response = requests.get(BASE + "video/1")
print(response.json())

#https://youtu.be/GMppyAPbLYk (watched until databases at cca 48 mins)