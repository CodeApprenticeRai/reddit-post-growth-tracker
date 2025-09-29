import React from 'react';
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
          <List 
            subredditNames={this.props.subredditNames}
            selectedSubreddit={this.props.selectedSubreddit}
            onSubredditSelect={this.props.onSubredditSelect}
          />
        </div>
      </div>
    );
  }
}

export default SideBar;