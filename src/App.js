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
  

  render(){
    return (
      <div className="App container">
        <div className='row'>
          <div className='pageTitle'>Reddit Post Growth Tracker</div>
        </div>
        <div className='mainContent'>  
          <SideBar subredditNames={this.state.subreddits} />
          <GraphWrapper selectedSubreddit={this.state.selectedSubreddit}  />
        </div>'
      </div>
    )
  }
}  


export default App;
