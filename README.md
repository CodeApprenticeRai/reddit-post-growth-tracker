# reddit-post-growth-tracker
Tracks which posts grow the fastest over time


#### Post-Objectives
* Modularize DB interactions. I.e, create a query executor,, have it handle errors.
* Add Date-Created to the subscribed_submissions table schema, fill value for each existing entry, update insertion logic to make sure that date-created is specified for each newly entered submission
* Add the functionality so that when making a GET /subreddits request, a start range can be specified. Memoize data on the front end. By asking only for the data we don't have, request fullfiment time is reduced significantly.


#### Quirks
* Node.js::Express is a better server choice than Python::Fla in my opinion, however, there was no JS reddit module I could find with the feature of being able to get the subreddit id simply, thus I just decided to use a Python Server.  
* subscribe is an ambiguous verb in the context of the because on reddit you 'subscribe' to subreddits.
In the case of this app, subscribe means to add that subreddit to the collection of subreddits whose posts we are tracking the growth of.
