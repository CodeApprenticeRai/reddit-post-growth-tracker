import React from 'react';
import SubscribeToSubredditForm from "../SubscribeToSubredditForm/SubscribeToSubredditForm";
import List from '../List/List';

import styles from "./SideBar.css"

class SideBar extends React.Component {
  constructor(props) {
   super(props);
  }

  render() {
    return (
      <div id="sidebar" className="row">
        <div className="no-padding col">
          <SubscribeToSubredditForm />
        </div>
        <div className="no-padding col">  
          <List subredditNames={this.props.subredditNames} />
        </div>
      </div>
    );
  }
}

export default SideBar;