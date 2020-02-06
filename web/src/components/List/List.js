import React from 'react';
import ReactDOM from 'react-dom';

class List extends React.Component {
  constructor(props) {
   super(props);
  }

  render() {
    var subredditNamesList = this.props.subredditNames.map( (key, index) => {
      return( <li key={key}>{key}</li> );
    });

    // let test_subredditNamesList = [ "AskReddit", "unpopularopinions", "AmITheAsshole", "AskMen", "ShowerThoughts", "AskReddit", "unpopularopinions", "AmITheAsshole", "AskMen", "AskReddit", "unpopularopinions", "AmITheAsshole", "AskMen", "ShowerThoughts", "AskReddit", "unpopularopinions", "AmITheAsshole", "AskMen"].map( (key, index) => {
    //   return( <li key={key}>{key}</li> );
    // });

    return (
      <ul id="subreddit-list">
        { subredditNamesList }
      </ul>
    );
  }
}

export default List;
