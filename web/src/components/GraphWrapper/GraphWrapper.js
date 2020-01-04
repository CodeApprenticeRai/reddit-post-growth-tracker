import React from 'react';
import ReactDOM from 'react-dom';

import Taucharts from 'taucharts';
import 'taucharts/dist/plugins/tooltip';
// import styles from "./GraphWrapper.css"

const tauCharts = require('taucharts');


class GraphWrapper extends React.Component {
  constructor(props) {
   super(props);

   this.state = {
     "chartData": {},
   };


  }

  async componentDidUpdate(){

    if (
      (
        (this.props.selectedSubreddit != undefined ) &&
        (Object.entries(this.state.chartData).length == 0)
      )
    ){

    let data= [];

    await Object.keys(this.props.selectedSubreddit.submissions).map( (key) => {
      this.props.selectedSubreddit.submissions[key].data.map( (data_element) => {
        let _date = new Date(0);
        _date.setUTCSeconds(data_element.time);
        data_element.time = _date;
        data.push( Object.assign( data_element, { "title": this.props.selectedSubreddit.submissions[ key ].title }) );
      });
    });


    var chart = new Taucharts.Chart({
      data: data,
      type: 'line',
      x: 'time',
      y: 'upvotes',
      color: 'title', // there will be two lines with different colors on the chart
      plugins: [
        tauCharts.api.plugins.get('tooltip')({
          // will see only name and age on tooltip
          fields: ['title', "upvotes", "time"]
        }),
        tauCharts.api.plugins.get('legend')
      ]
    });

    chart.renderTo(document.getElementById('graph'));
    }


    //
  }

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
