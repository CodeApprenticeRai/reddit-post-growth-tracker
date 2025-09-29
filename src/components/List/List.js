import React from 'react';
import './List.css';

class List extends React.Component {
  constructor(props) {
   super(props);
  }

  render() {
    var subredditNamesList = this.props.subredditNames.map( (key, index) => {
      return( <li key={key}>{key}</li> );
    });
    return (
      <ul id="subreddit-list">
        { subredditNamesList }
      </ul>
    );
  }
}

export default List;