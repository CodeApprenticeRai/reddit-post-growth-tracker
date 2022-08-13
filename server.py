from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from rpgt import RPGT

_rpgt = RPGT()
api = Flask(__name__, static_url_path='/public', static_folder='build')

CORS(api)



@api.route('/')
def index():
    return send_from_directory(api.static_folder, 'index.html')

@api.route('/subscribe/<subreddit>', methods=['POST'])
def subscribe(subreddit):
    if request.method == 'POST':
        subreddit_object = _rpgt.reddit_client.subreddit(display_name=subreddit)
        _rpgt.subscribe_to_subreddit(subreddit_object.id, subreddit_object.display_name) 
        return jsonify({"status": "success"})

@api.route('/submissions/<subreddit_display_name>', methods=['GET'])
def submissions(subreddit_display_name):
    if request.method == 'GET':
        return jsonify(_rpgt.get_submissions_subscribed_to_by_subreddit_display_name(subreddit_display_name))

@api.route('/records/<submission_id>', methods=['GET'])
def records(submission_id):
    if request.method == 'GET':
        return jsonify(_rpgt.get_submission_records_by_submission_id(submission_id))