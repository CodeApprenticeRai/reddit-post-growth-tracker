import React from 'react';
import SideBar from './components/SideBar/SideBar';
import GraphWrapper from './components/GraphWrapper/GraphWrapper';
import SubscribeToSubredditForm from './components/SubscribeToSubredditForm/SubscribeToSubredditForm';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      "subreddits": {},
      "selectedSubreddit": "",
      "loading": true,
      "error": null
    }
    
    this.loadSubredditsData = this.loadSubredditsData.bind(this);
    this.handleSubredditSubscription = this.handleSubredditSubscription.bind(this);
  }
  
  async loadSubredditsData() {
    try {
      this.setState({ loading: true, error: null });
      
      const response = await fetch('http://localhost:5000/api/analytics/submissions/300', {
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
      const selectedSubreddit = subredditNames.length > 0 ? subredditNames[0] : "";

      this.setState({
        "subreddits": data,
        "selectedSubreddit": selectedSubreddit,
        "loading": false
      });
    } catch (error) {
      console.error('Error loading subreddits data:', error);
      this.setState({
        "subreddits": {},
        "selectedSubreddit": "",
        "loading": false,
        "error": error.message
      });
    }
  }

  async handleSubredditSubscription(subredditName) {
    try {
      const response = await fetch('http://localhost:5000/api/subreddits/subscribe', {
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
    const { subreddits, selectedSubreddit, loading, error } = this.state;
    
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
    const selectedSubredditData = subreddits[selectedSubreddit];

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
              selectedSubreddit={selectedSubreddit}
              onSubredditSelect={(name) => this.setState({ selectedSubreddit: name })}
            />
          </div>
          <div className='col-md-9'>
            <GraphWrapper 
              selectedSubreddit={selectedSubredditData} 
              selectedSubredditName={selectedSubreddit}
            />
          </div>
        </div>
      </div>
    )
  }
}  


export default App;
