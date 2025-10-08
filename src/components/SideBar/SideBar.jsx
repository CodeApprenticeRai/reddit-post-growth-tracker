import React from 'react';
import List from '../List/List';
import "./SideBar.css"

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
            selectedSubredditName={this.props.selectedSubredditName}
            onSubredditSelect={this.props.onSubredditSelect}
          />
        </div>
      </div>
    );
  }
}

export default SideBar;