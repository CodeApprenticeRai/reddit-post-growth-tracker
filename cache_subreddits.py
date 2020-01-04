import json, time
import controls

while True:
    print("fetching subreddits")
    execution_time = time.time()

    subscribed_subreddits = controls.get_subreddit_submission_time_series()

    execution_time = time.time() - execution_time
    print("subreddits fetched: {} s".format( execution_time ))

    with open('subreddits_cache.json', 'w') as subreddits_cache:
        json.dump( subscribed_subreddits, subreddits_cache)


    time.sleep( max(0, 60 - execution_time) )
