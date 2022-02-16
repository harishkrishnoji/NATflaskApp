# https://pythonise.com/series/learning-flask/building-a-flask-app-with-docker-compose
# https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-18-04
# https://gabimelo.medium.com/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e

"""
# RUN below commands from app folder where docker-compose file
docker-compose images
docker-compose ps
docker-compose stop
docker-compose up --build

To run container from docker image and get into interactive mode
docker run -it natdata_nginx /bin/bash

To get into interactive mode for existing running container
$docker exec -it nginx /bin/bash

sudo iptables -nvL
"""

from crypt import methods
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from mongonator import MongoClientWithPagination, ASCENDING

# app = Flask(__name__)

# This is to get total count of document
app.config["MONGO_URI"] = "mongodb://mkwdmongo:Mkwdmong0_Cat@l1cvdb1018.1dc.com/fdc_inventory?authSource=admin"
app.config["MONGO_DBNAME"] = "fdc_inventory"
mongo = PyMongo(app)
# # print ("MongoDB Database:", mongo.db)
db = mongo.db["sane_fw_nat"]
# print(dir(db))
total_nat = db.count_documents({})

# db.init_app(app)

# Pagination 
MONGO_URI = "mongodb://mkwdmongo:Mkwdmong0_Cat@l1cvdb1018.1dc.com/fdc_inventory?authSource=admin"
DATABASE = 'fdc_inventory'
COLLECTION = 'sane_fw_nat'

# Instantiate mongo client with pagination
mongo_client = MongoClientWithPagination(MONGO_URI)
pdb = mongo_client[DATABASE]
pcol = pdb[COLLECTION]


@app.route("/")
def home():
    return render_template('home.html', total_nat=total_nat)

@app.route("/nat", methods=['POST'])
def nat_records():
    addr = request.form.get("addr")
    rule = query_mongo(addr)
    return render_template('nat.html', nat=rule)

# @app.route("/natapi/", methods=['GET'])
# def nat_api_records():
#     # data = request.get_json()
#     # addr = request.args.get("address")
#     if request.args.get("address"):
#         # addr = request.form.get("addr")
#         rules = query_mongo(request.args.get("address"))
#         for rule in rules:
#             rule.pop("_id", None)
#         return jsonify(rules)
#     else:
#         return jsonify({"error":"Invalid input, missing address key"})

@app.route("/natapi1/<num>", methods=['GET'])
def nat_api_records1(num):
    # addr = request.form.get("addr")
    rules = query_mongo(num)
    for rule in rules:
        rule.pop("_id", None)
    return jsonify(rules)

def query_mongo(addr):
    rule = []
    fields = ["OriginalSource", "TranslatedSourcequery", "OriginalDestination", "TranslatedDestination"]
    addr1 = "{addr}*".format(addr=addr)
    # search_string = {"$regex": f'{addr}*', "$options" :'i'}
    search_string = {"$regex": addr1, "$options" :'i'}
    for field in fields:
        fi = "{field}".format(field=field)
        # filter = {f"{field}": search_string}
        filter = {fi: search_string}
        query_resp = _query_mongo(filter)
        if query_resp.response:
            rule.extend(query_resp.response)
    return rule

def _query_mongo(filter):
    return pcol.paginate(query=filter, limit=100, ordering_field='name', ordering=ASCENDING, automatic_pagination=False)

# if __name__ == "__main__":
    # app.run(debug=True)
