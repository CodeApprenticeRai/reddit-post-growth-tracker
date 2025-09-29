import React from 'react';
import './List.css';

class List extends React.Component {
  constructor(props) {
   super(props);
  }

  handleSubredditClick = (subredditName) => {
    if (this.props.onSubredditSelect) {
      this.props.onSubredditSelect(subredditName);
    }
  }

  render() {
    const { subredditNames, selectedSubreddit } = this.props;
    
    if (!subredditNames || subredditNames.length === 0) {
      return (
        <div className="no-subreddits">
          <p>No subreddits subscribed yet.</p>
          <p>Use the form above to subscribe to a subreddit.</p>
        </div>
      );
    }

    var subredditNamesList = subredditNames.map((subredditName, index) => {
      const isSelected = subredditName === selectedSubreddit;
      return (
        <li 
          key={subredditName} 
          className={isSelected ? 'selected' : ''}
          onClick={() => this.handleSubredditClick(subredditName)}
        >
          {subredditName}
        </li>
      );
    });
    
    return (
      <div className="subreddit-list-container">
        <h5>Subscribed Subreddits</h5>
        <ul id="subreddit-list">
          {subredditNamesList}
        </ul>
      </div>
    );
  }
}

export default List;