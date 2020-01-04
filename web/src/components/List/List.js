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

    return (
      <ul>
        { subredditNamesList }
      </ul>
    );
  }
}

export default List;
