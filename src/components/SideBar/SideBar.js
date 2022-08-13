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
      <div id="sidebar">
        <SubscribeToSubredditForm />
        <List subredditNames={this.props.subredditNames} />
      </div>
    );
  }
}

export default SideBar;