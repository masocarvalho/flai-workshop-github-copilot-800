import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  console.log('App Component - Initializing with CODESPACE_NAME:', process.env.REACT_APP_CODESPACE_NAME);
  
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img src="/octofitapp-small.png" alt="OctoFit Logo" />
              OctoFit Tracker
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">
                    Workouts
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">
                    Activities
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">
                    Users
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">
                    Teams
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">
                    Leaderboard
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={
            <div className="container mt-4">
              <div className="welcome-section">
                <h1>🏋️ Welcome to OctoFit Tracker</h1>
                <p className="lead">Track your fitness journey, compete with friends, and achieve your goals!</p>
                <div className="alert alert-info" role="alert">
                  <h5 className="alert-heading">Getting Started</h5>
                  <p>Use the navigation menu above to explore workouts, track activities, view teams, and check the leaderboard.</p>
                  <hr />
                  <p className="mb-0">Start your fitness journey today and see your progress in real-time!</p>
                </div>
                <div className="row mt-4">
                  <div className="col-md-4 mb-3">
                    <Link to="/activities" style={{ textDecoration: 'none' }}>
                      <div className="card text-center">
                        <div className="card-body">
                          <h5 className="card-title">📊 Track Activities</h5>
                          <p className="card-text">Log your workouts and monitor your progress over time.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-4 mb-3">
                    <Link to="/users" style={{ textDecoration: 'none' }}>
                      <div className="card text-center">
                        <div className="card-body">
                          <h5 className="card-title">👤 View Users</h5>
                          <p className="card-text">See all registered users and their profiles.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-4 mb-3">
                    <Link to="/leaderboard" style={{ textDecoration: 'none' }}>
                      <div className="card text-center">
                        <div className="card-body">
                          <h5 className="card-title">🏆 Leaderboard</h5>
                          <p className="card-text">Check the leaderboard and see how you rank!</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          } />
          <Route path="/workouts" element={<Workouts />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/users" element={<Users />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
