#first flask restful app
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
#using Flask-JWT for authentification

from security import authenticate, identity


#create app
app=Flask(__name__)
api=Api(app)
app.secret_key='mwhahahaha'

items=[]

jwt=JWT(app, authenticate, identity) # /auth
#student class inherits resource class
class Item(Resource):
    @jwt_required()
    def get(self,name):
    #old way
        #for item in items:
            #if item['name']==name:
                #return item

                #returns filter object- can use next or list
                item=next((filter(lambda x: x['name']== name, items)),None)
                #only haveto use one next because we do not have duplicates
                return {'item': item}, 200 if item else 404
        #return {'item':None}, 404

    def post(self,name):
        #make sure only one of each item
        if next((filter(lambda x: x['name']== name, items)),None) is not None:
            return {'message',"An item with name ' {}'already exists.".format(name)},400

        data=request.get_json()
        item={'name':name, 'price':data['price']}
        items.append(item)
        return item, 201

def delete(self, name):
    global items#makes sure it is the items from above not in scope of method
    #replace list will list with all but the one we want removed
    items=list(filter(lambda x: x['name'] !=name, items))
    return {'message': 'Item deleted'}

def put(self,name):
    #run request through and see what matches
    parser=reqparse.RequestParser()
    #define arguement
    #makes sure price is put into api post or put would need to add to post for it to work like put
    #could make it's own function as a way to
    #could also just add to the item class
    parser.add_argument('price', type=float, required=True, help="This cannot be left blank")

    data=parser.parse_args()

    item=next(filter(lambda x: x[name]==name, items),None)
    if item is None:
        item={'name':name,'price':data['price']}
        items.append(item)
    else:
        #update
        item.update(data)
        return item
class ItemList(Resource):
    def get(self):
        return {'item':items}
#don't have to do route we do second parameter below
api.add_resource(Item, '/item/<string:name>')#will look like http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList,'/items')
app.run(port=5000, debug=True)
