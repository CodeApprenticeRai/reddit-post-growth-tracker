import React from 'react';
import SideBar from './components/SideBar/SideBar';
import GraphWrapper from './components/GraphWrapper/GraphWrapper';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      "subreddits": [],
      "selectedSubreddit": "",
    }
  }
  
  async componentDidMount() {
    let response = await fetch('http://localhost:5000/subreddits/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
    let response_data = await response.json();
    let selectedSubreddit = (response_data.length > 0) ? response_data[0]["display_name"] : "";
    let subreddits = response_data.map(subreddit => {
      return subreddit["display_name"];
    });

    this.setState({
      "subreddits": subreddits,
      "selectedSubreddit": selectedSubreddit
    }, () => {
      console.log(this.state);
    });
  }

  render(){
    return (
      <div className="App container">
        <div className='row'>
          <div className='pageTitle'>Reddit Post Growth Tracker</div>
        </div>
        <div className='mainContent row'>  
          <div className='col'>
            <SideBar subredditNames={this.state.subreddits} />
          </div>
            <div className='col'>
              <GraphWrapper selectedSubreddit={this.state.selectedSubreddit}  />
            </div>
        </div>
      </div>
    )
  }
}  


export default App;
