import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;

  useEffect(() => {
    console.log('Leaderboard Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Leaderboard Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard Component - Processed leaderboard:', leaderboardData);
        setLeaderboard(leaderboardData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard Component - Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return (
    <div className="container mt-4">
      <div className="loading-spinner">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  );
  
  if (error) return (
    <div className="container mt-4">
      <div className="error-message">
        <h5>Error Loading Leaderboard</h5>
        <p>{error}</p>
      </div>
    </div>
  );

  const getMedal = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  const getTotalCalories = (entry) => {
    // Check various possible field names for total calories
    if (entry.total_calories !== undefined) return entry.total_calories;
    if (entry.totalCalories !== undefined) return entry.totalCalories;
    if (entry.calories !== undefined) return entry.calories;
    console.log('Leaderboard Component - Entry data structure:', entry);
    return 0;
  };

  const getActivityCount = (entry) => {
    // Check various possible field names for activity count
    if (entry.activity_count !== undefined) return entry.activity_count;
    if (entry.activityCount !== undefined) return entry.activityCount;
    if (entry.activities !== undefined) return entry.activities;
    return 0;
  };

  const getTeamName = (entry) => {
    // Check various possible field names for team
    if (entry.team_name) return entry.team_name;
    if (entry.teamName) return entry.teamName;
    if (entry.team && typeof entry.team === 'string') return entry.team;
    if (entry.team && entry.team.name) return entry.team.name;
    return 'No Team';
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">🏆 Leaderboard</h2>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th style={{width: '80px'}}>Rank</th>
              <th>User</th>
              <th>Team</th>
              <th>Total Calories</th>
              <th>Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center">No leaderboard data available.</td>
              </tr>
            ) : (
              leaderboard.map((entry, index) => {
                const totalCalories = getTotalCalories(entry);
                const activityCount = getActivityCount(entry);
                const teamName = getTeamName(entry);
                
                return (
                  <tr key={entry.user_id || entry.id || index} className={index < 3 ? 'table-warning' : ''}>
                    <td><h5>{getMedal(index + 1)}</h5></td>
                    <td><strong>{entry.user_username || entry.username || entry.user}</strong></td>
                    <td><span className="badge bg-primary">{teamName}</span></td>
                    <td><span className="badge bg-danger">{totalCalories} cal</span></td>
                    <td><span className="badge bg-info">{activityCount}</span></td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
