from audioop import cross
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
from rpgt import RPGT

_rpgt = RPGT()
api = Flask(__name__, static_url_path='/public', static_folder='build')

cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'


@api.route('/')
def index():
    return send_from_directory(api.static_folder, 'index.html')

@api.route('/subscribe/<subreddit>', methods=['POST'])
def subscribe(subreddit):
    if request.method == 'POST':
        subreddit_object = _rpgt.reddit_client.subreddit(display_name=subreddit)
        _rpgt.subscribe_to_subreddit(subreddit_object.id, subreddit_object.display_name) 
        return jsonify({"status": "success"})

@api.route('/subreddits/', methods=['GET'])
def get_subreddits():
    if request.method == 'GET':
        requested_data = _rpgt.get_subreddits_subscribed_to()
        formatted_data = [ {"id": subreddit[0], "display_name": subreddit[1]} for subreddit in requested_data ]
        print('requested_data: ', requested_data)
        return jsonify(formatted_data)

@api.route('/submissions/<subreddit_display_name>', methods=['GET', 'OPTIONS'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def submissions(subreddit_display_name):
    if request.method in ['GET', 'OPTIONS']:
        requested_data = _rpgt.get_submissions_subscribed_to_by_subreddit_display_name(subreddit_display_name)
        print('requested_data: ', requested_data) 
        
        response = jsonify(requested_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        # response.headers.add('Access-Control-Allow-Credentials', 'true')
        # response.headers.add('Access-Control-Allow-Methods', 'GET,HEAD,OPTIONS,POST,PUT')
        # response.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers')
        
        return response

@api.route('/records/<submission_id>', methods=['GET', 'OPTIONS'])
def records(submission_id):
    if request.method in ['GET', 'OPTIONS']:
        return jsonify(_rpgt.get_submission_records_by_submission_id(submission_id))