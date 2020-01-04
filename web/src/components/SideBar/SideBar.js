import React from 'react';
import ReactDOM from 'react-dom';
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
        <div className={styles.subredditSelectorGroup}>
        <SubscribeToSubredditForm />
        <List subredditNames={this.props.subredditNames} />
        </div>
      </div>
    );
  }
}

export default SideBar;
