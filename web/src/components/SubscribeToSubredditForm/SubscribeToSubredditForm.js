import React from 'react';
import ReactDOM from 'react-dom';

import styles from "./SubscribeToSubredditForm.css"

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
    // const response = await fetch("http://localhost:5000/subscribe", {
    //   method: 'GET',
    //   // mode: 'cors',
    //   cache: 'no-cache',
    //   // credentials: 'same-origin',
    //   headers: {
    //     'Content-Type': 'application/json'
    //   },
    //   redirect: 'follow',
    //   referrerPolicy: 'no-referrer',
    //   body: JSON.stringify({ "subreddits_name": this.state.value })
    // });
    alert("Fake Subscribed to " + this.state.value);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          <input id="subreddit-input-box" type="text" value={this.state.value} onChange={this.handleChange} placeholder="Add Subreddit" />
        </label>
        <input type="submit" value="Add" />
      </form>
    );
  }
}

export default SubscribeToSubredditForm;
