import React from 'react';
import SideBar from './components/SideBar/SideBar.jsx';
import GraphWrapper from './components/GraphWrapper/GraphWrapper.jsx';
import SubscribeToSubredditForm from './components/SubscribeToSubredditForm/SubscribeToSubredditForm.jsx';
import { buildApiUrl } from './config/api.js';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      "subreddits": {},
      "selectedSubredditName": "",
      "loading": true,
      "error": null
    }
    
    this.loadSubredditsData = this.loadSubredditsData.bind(this);
    this.handleSubredditSubscription = this.handleSubredditSubscription.bind(this);
  }
  
  async loadSubredditsData() {
    try {
      this.setState({ loading: true, error: null });
      
      const response = await fetch(buildApiUrl('ANALYTICS_SUBMISSIONS', '300'), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Loaded subreddits data:', data);

      const subredditNames = Object.keys(data);
      const selectedSubredditName = subredditNames.length > 0 ? subredditNames[0] : "";

      this.setState({
        "subreddits": data,
        "selectedSubredditName": selectedSubredditName,
        "loading": false
      });
    } catch (error) {
      console.error('Error loading subreddits data:', error);
      this.setState({
        "subreddits": {},
        "selectedSubredditName": "",
        "loading": false,
        "error": error.message
      });
    }
  }

  async handleSubredditSubscription(subredditName) {
    try {
      const response = await fetch(buildApiUrl('SUBREDDIT_SUBSCRIBE'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ subreddit_name: subredditName })
      });

      const result = await response.json();
      
      if (result.success) {
        // Reload data after successful subscription
        await this.loadSubredditsData();
        return { success: true, message: 'Successfully subscribed to subreddit!' };
      } else {
        return { success: false, message: result.message };
      }
    } catch (error) {
      console.error('Error subscribing to subreddit:', error);
      return { success: false, message: 'Failed to subscribe to subreddit' };
    }
  }
  
  async componentDidMount() {
    await this.loadSubredditsData();
    
    // Set up periodic data refresh
    this.refreshInterval = setInterval(this.loadSubredditsData, 60000); // Every minute
  }

  componentWillUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }

  render(){
    const { subreddits, selectedSubredditName, loading, error } = this.state;
    
    if (loading) {
      return (
        <div className="App container">
          <div className='row'>
            <div className='pageTitle'>Reddit Post Growth Tracker</div>
          </div>
          <div className='mainContent row'>
            <div className='col-12 text-center'>
              <div className="spinner-border" role="status">
                <span className="sr-only">Loading...</span>
              </div>
              <p>Loading subreddit data...</p>
            </div>
          </div>
        </div>
      );
    }

    if (error) {
      return (
        <div className="App container">
          <div className='row'>
            <div className='pageTitle'>Reddit Post Growth Tracker</div>
          </div>
          <div className='mainContent row'>
            <div className='col-12 text-center'>
              <div className="alert alert-danger" role="alert">
                <h4 className="alert-heading">Error Loading Data</h4>
                <p>{error}</p>
                <button className="btn btn-primary" onClick={this.loadSubredditsData}>
                  Retry
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    const subredditNames = Object.keys(subreddits);
    const selectedSubredditData = subredditNames.length > 0 ? subreddits[selectedSubredditName] : {};

    return (
      <div className="App container">
        <div className='row'>
          <div className='pageTitle'>Reddit Post Growth Tracker</div>
        </div>
        <div className='mainContent row'>  
          <div className='col-md-3'>
            <SubscribeToSubredditForm onSubscribe={this.handleSubredditSubscription} />
            <SideBar 
              subredditNames={subredditNames} 
              selectedSubredditName={selectedSubredditName}
              onSubredditSelect={(name) => this.setState({ selectedSubredditName: name })}
            />
          </div>
          <div className='col-md-9'>
            <GraphWrapper 
              selectedSubredditData={selectedSubredditData} 
              selectedSubredditName={selectedSubredditName}
            />
          </div>
        </div>
      </div>
    )
  }
}  


export default App;
