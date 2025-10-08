import React from 'react';
import "./SubscribeToSubredditForm.css"

class SubscribeToSubredditForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
      loading: false,
      message: null,
      messageType: null
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  async handleSubmit(event) {
    event.preventDefault();
    
    if (!this.state.value.trim()) {
      this.setState({
        message: 'Please enter a subreddit name',
        messageType: 'error'
      });
      return;
    }

    this.setState({ loading: true, message: null });

    try {
      const result = await this.props.onSubscribe(this.state.value.trim());
      
      this.setState({
        message: result.message,
        messageType: result.success ? 'success' : 'error',
        value: result.success ? '' : this.state.value
      });
    } catch (error) {
      this.setState({
        message: 'Failed to subscribe to subreddit',
        messageType: 'error'
      });
    } finally {
      this.setState({ loading: false });
    }
  }

  render() {
    const { value, loading, message, messageType } = this.state;

    return (
      <div className="subscribe-form-container">
        <h5>Subscribe to Subreddit</h5>
        <form className='row' onSubmit={this.handleSubmit}>
          <label className='col-8'>
            <input 
              id="subreddit-input-box" 
              type="text" 
              value={value} 
              onChange={this.handleChange} 
              placeholder="Enter subreddit name" 
              disabled={loading}
            />
          </label>
          <div className='col-4'>
            <input 
              id="subreddit-submit-button" 
              type="submit" 
              value={loading ? "Adding..." : "Add"} 
              disabled={loading}
            />
          </div>
        </form>
        
        {message && (
          <div className={`message ${messageType}`}>
            {message}
          </div>
        )}
      </div>
    );
  }
}

export default SubscribeToSubredditForm;