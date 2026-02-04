import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

  useEffect(() => {
    console.log('Activities Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Activities Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Activities Component - Processed activities:', activitiesData);
        setActivities(activitiesData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Activities Component - Error fetching activities:', error);
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
        <h5>Error Loading Activities</h5>
        <p>{error}</p>
      </div>
    </div>
  );

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Invalid Date';
      return date.toLocaleDateString();
    } catch (e) {
      return 'Invalid Date';
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">📋 Activities</h2>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>Workout</th>
              <th>User</th>
              <th>Duration</th>
              <th>Calories</th>
              <th>Date</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {activities.length === 0 ? (
              <tr>
                <td colSpan="6" className="text-center">No activities found.</td>
              </tr>
            ) : (
              activities.map((activity) => (
                <tr key={activity.id}>
                  <td><strong>{activity.workout_title || activity.workout}</strong></td>
                  <td>{activity.user_username || activity.user}</td>
                  <td>{activity.duration} min</td>
                  <td><span className="badge bg-success">{activity.calories_burned} cal</span></td>
                  <td>{formatDate(activity.date)}</td>
                  <td>{activity.notes || '-'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Activities;
