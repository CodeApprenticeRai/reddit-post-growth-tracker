import React from 'react';

// import Taucharts from 'taucharts';
// import 'taucharts/dist/plugins/tooltip';
import "./GraphWrapper.css"

// const tauCharts = require('taucharts');


class GraphWrapper extends React.Component {
  constructor(props) {
   super(props);

   this.state = {
     "chartData": {},
     "chart": null
   };
  }

  async componentDidUpdate(){}

  render(){
    return (

      <div id="graph-wrapper">
        <div id="graph-subreddit-name-title">/r/{ this.props.selectedSubredditName ? this.props.selectedSubredditName : "" }</div>
        <div id="graph" />
      </div>
    );
  }
}

export default GraphWrapper;