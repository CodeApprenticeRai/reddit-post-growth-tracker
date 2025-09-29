import React from 'react';
import { createChart } from 'lightweight-charts';
import "./GraphWrapper.css"


class GraphWrapper extends React.Component {
  constructor(props) {
   super(props);

   this.state = {
      "submissions": [],
      "records": [],
     "chart": null
   };
   this.updateSubmissions =  this.updateSubmissions.bind(this);
   this.getRecords = this.getRecords.bind(this);
   this.graphData = this.graphData.bind(this);
  }

  async updateSubmissions(){
    let url = 'http://localhost:5000/submissions/' + this.props.selectedSubreddit;

    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
    
    const response_data = await response.json();
    
    console.log(response_data);

    this.setState({
      "submissions": response_data.slice(0, 50)
    });
  }

  async getRecords(){
    console.log("processing records");
    let submission_records = await Promise.all( this.state.submissions.map( async (submission) => {
      console.log("fetching records");
      let response = await fetch('http://localhost:5000/records/' + submission[0], {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
      
      let response_data = await response.json();
      
      console.log("submission_records for id: " + submission[0], response_data);

      const record = [submission[0], response_data]

      return record;
    }));

    console.log("submission_records:", submission_records);

    this.setState({ 
      "records" : submission_records,
    }, this.graphData);
  }

  async graphData(){
    console.log("graphData: ", this.state.records);
    this.state.records.forEach(record => {
      const data = record[1].map( (row) => {
        return {"time": row[0], "count": row[2]};
      });
      console.log("data: ", data); 
      const series = this.state.chart.addLineSeries();
      series.setData(data);
    });
  }

  componentDidMount(){
    const chart = createChart(document.getElementById('graph'), {width: 800, height: 300});
    this.setState({
      "chart": chart
    }, () => {console.log("chart bound to state: ", chart)} );
  }

  async componentDidUpdate() {
    if ( (this.props.selectedSubreddit !== "") && (this.state.submissions.length === 0) ) {
      console.log("GraphWrapper.componentDidUpdate did trigger");
      await this.updateSubmissions();
      await this.getRecords();
    }
  }
    
  render(){
    return (

      <div id="graph-wrapper">
        <div id="graph-subreddit-name-title">/r/{ this.props.selectedSubreddit ? this.props.selectedSubreddit : "" }</div>
        <div id="graph" />
      </div>
    );
  }
}

export default GraphWrapper;