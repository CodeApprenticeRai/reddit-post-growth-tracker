import React from 'react';
import ReactDOM from 'react-dom';
import SideBar from '../SideBar/SideBar';
import GraphWrapper from "../GraphWrapper/GraphWrapper"

import styles from "./App.css";

class App extends React.Component {
  constructor(props) {
   super(props);

   this.state = {
     "subreddits" : {},
     "selectedSubreddit": ""
   }

   this.loadSubredditsData = this.loadSubredditsData.bind(this);
  }

  async loadSubredditsData(){
      const response = await fetch("http://localhost:5000/developmental/get_subreddit_submissions/300", {
      method: 'GET',
      // mode: 'cors',
      cache: 'no-cache',
      // credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json'
      },
      redirect: 'follow',
      referrerPolicy: 'no-referrer',
    });

    var data = await response.json();

    console.log( data );

    let newState = { "subreddits": data };
    let subredditNames = Object.keys(data);

    if ( subredditNames.length > 0 ){
      newState.selectedSubreddit = subredditNames[0];
    }

    this.setState( newState );

  };

  componentDidMount(){
    this.loadSubredditsData();
    setInterval( this.loadSubredditsData, 1000*60 );
  }


  render(){
    return(
      <div id="app-wrapper">
        <div id={styles.pageTitle}>Reddit Post Growth Tracker</div>
        <div className={styles.mainContent}>
          <SideBar subredditNames={Object.keys(this.state.subreddits)} />
          <GraphWrapper selectedSubreddit={this.state.subreddits[ this.state.selectedSubreddit ] } selectedSubredditName={this.state.selectedSubreddit} />
        </div>
      </div>
    );
  }
};

export default App;

// <div>Div 2</div>
