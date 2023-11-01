import React from 'react';
import  "./SubscribeToSubredditForm.css"

class SubscribeToSubredditForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  async handleSubmit(event) {
    event.preventDefault();
    const response = await fetch(`http://localhost:5000/subscribe/${event.target.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
    });
    alert("Subscribed to " + this.state.value);
    this.setState({value: ''});
  }

  render() {
    return (
      <form className='row' onSubmit={this.handleSubmit}>
        <label className='col-8'>
          <input id="subreddit-input-box" type="text" value={this.state.value} onChange={this.handleChange} placeholder="Add Subreddit" />
        </label>
        <div className='col-4'>
          <input id="subreddit-submit-button" type="submit" value="Add" />
        </div>
      </form>
    );
  }
}

export default SubscribeToSubredditForm;