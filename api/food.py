import re 
from flask import Blueprint, request, jsonify,make_response, current_app as app
from api import mongo

bp = Blueprint("food", __name__, url_prefix="/food")


@bp.route('/food',methods= ['GET'])
def food():
  response = []
  search = request.args.get('search')
  if isinstance(search, str):
      query = '.+'.join(search.split())
      # for s in search.split():
      #   query =  f'(?=.*?\{s}\b)'
      print(query)
      cursor= list(mongo.food.find({'description':\
        {"$regex":re.compile(query, re.IGNORECASE)}},\
          {'_id':True, 'description':True }, max_time_ms=1000, limit=20))

      for item in cursor:
        item['_id'] = str(item['_id'])
        response.append(item)

      return make_response(
        jsonify({
          "ok" : 1, 
          "data": response})), 201   
  else:
    return None