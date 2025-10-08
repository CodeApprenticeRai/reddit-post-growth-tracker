import React from 'react';
import { createChart, LineSeries } from 'lightweight-charts';
import "./GraphWrapper.css"

class GraphWrapper extends React.Component {
  constructor(props) {
   super(props);

   this.state = {
      "submissions": this.props.selectedSubredditData,
      "selectedSubredditName": this.props.selectedSubredditName,
      "records": [],
     "chart": null
   };
   this.updateSubmissions =  this.updateSubmissions.bind(this);
   this.getRecords = this.getRecords.bind(this);
  //  this.graphData = this.graphData.bind(this);
  }

  async updateSubmissions(){
    // let url = buildApiUrl('ANALYTICS_SUBMISSIONS'); //, this.state.selectedSubreddit);

    // const response = await fetch(url, {
    //   method: 'GET',
    //   mode: 'cors',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'Access-Control-Allow-Origin': '*'
    //   }
    // });
    
    // const response_data = await response.json();
    
    // console.log(response_data);

    // this.setState({
    //   "submissions": response_data.slice(0, 50)
    // });
  }

  async getRecords(){
    console.log("processing records");
    console.log("selectedSubredditData:", this.props.selectedSubredditData);
    
    if (!this.props.selectedSubredditData) {
      console.log("No subreddit data available");
      this.setState({ records: [] });
      return;
    }
    
    let submissionIds = Object.keys(this.props.selectedSubredditData.submissions);
    var submissionRecords = submissionIds.map((submissionId) => {
      let submission = this.props.selectedSubredditData.submissions[submissionId];
      var series = submission.data.map(record => {
        let dateTime = record.time * 1000; //new Date(record.time * 1000);
        return {
          time: dateTime,
          value: record.score,
          title: submission.title
        };
      });
      // Sort by time to ensure proper chronological order
      series.sort((a, b) => new Date(a.time) - new Date(b.time));
      return series;
    });

    // Only include series with data
    submissionRecords = submissionRecords.filter(series => series.length > 0);
    
    console.log("Processed records:", submissionRecords);
    
    this.setState({ 
      "records" : submissionRecords,
    });
  }

  // async graphData(){
  //   this.state.records.forEach(record => { 
  //     const series = this.state.chart.addLineSeries();
  //     series.setData(record);
  //   });
  // }

  async componentDidMount(){
    await this.getRecords();
    // Small delay to ensure DOM is ready
    setTimeout(() => {
      this.renderChart();
    }, 100);
  }

  renderChart() {
    // Clear any existing chart
    const chartContainer = document.getElementById('graph');
    if (chartContainer) {
      chartContainer.innerHTML = '';
    } else {
      console.error("Chart container 'graph' not found!");
      return;
    }

    if (this.state.records.length === 0) {
      console.log("No records to display");
      return;
    }

    console.log("Creating chart with", this.state.records.length, "series");
    console.log("Chart container:", chartContainer);

    try {
      const chart =  createChart(chartContainer, {
        width: 800, 
        height: 300,
        layout: {
          background: { color: 'white' },
          textColor: 'black',
        },
        grid: {
          vertLines: { color: '#f0f0f0' },
          horzLines: { color: '#f0f0f0' },
        },
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
        },
      });

      console.log("Chart created successfully:", chart);

      // Add a line series for each submission, record is an array of objects with time, value, and title.
      this.state.records.forEach((record, index) => {
        if (record.length > 0) {
          try {
            console.log(`Adding series ${index + 1} with ${record.length} data points`);
            const lineSeries = chart.addSeries(LineSeries);
            
            // Configure the series
            lineSeries.applyOptions({
              color: this.getColorForIndex(index),
              lineWidth: 2,
              title: record[0]?.title || `Series ${index + 1}`
            });
            
            lineSeries.setData(record);
            console.log(`Successfully added series for ${record[0]?.title}`);
          } catch (error) {
            console.error(`Error adding series ${index + 1}:`, error);
          }
        }
      });

      // Fit the chart to show all data
      chart.timeScale().fitContent();

      this.setState({
        "chart": chart
      }, () => {
        console.log("Chart rendered with", this.state.records.length, "series");
      });

    } catch (error) {
      console.error("Error creating chart:", error);
    }
  }

  getColorForIndex(index) {
    const colors = [
      '#2196F3', // Blue
      '#4CAF50', // Green
      '#FF9800', // Orange
      '#F44336', // Red
      '#9C27B0', // Purple
      '#00BCD4', // Cyan
      '#FFEB3B', // Yellow
      '#795548', // Brown
    ];
    return colors[index % colors.length];
  }

  async componentDidUpdate(prevProps) {
    // Check if the selected subreddit has changed
    if (prevProps.selectedSubredditName !== this.props.selectedSubredditName || 
        prevProps.selectedSubredditData !== this.props.selectedSubredditData) {
      console.log("GraphWrapper.componentDidUpdate - subreddit data changed");
      await this.getRecords();
      // Small delay to ensure DOM is ready
      setTimeout(() => {
        this.renderChart();
      }, 100);
    }
  }
    
  render(){
    return (
      <div id="graph-wrapper">
        <div id="graph-subreddit-name-title">
          /r/{ this.props.selectedSubredditName ? this.props.selectedSubredditName : "" }
        </div>
        {this.state.records.length === 0 ? (
          <div id="graph" className="graph-no-data">
            {this.props.selectedSubredditName ? 
              "No data available for this subreddit" : 
              "Select a subreddit to view data"
            }
          </div>
        ) : (
          <div id="graph" />
        )}
      </div>
    );
  }
}

export default GraphWrapper;