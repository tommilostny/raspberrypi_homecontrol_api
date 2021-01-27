#### Hello world endpoint ####
from flask_restful import Resource

names = { "tom":{ "age":21, "gender":"male" }, "bill":{ "age":70, "gender":"male" } }

class HelloWorld(Resource):
    def get(self, name):
        return names[name]
#### End of Hello world endpoint ####