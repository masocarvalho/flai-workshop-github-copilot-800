import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Workouts Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts Component - Processed workouts:', workoutsData);
        setWorkouts(workoutsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts Component - Error fetching workouts:', error);
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
        <h5>Error Loading Workouts</h5>
        <p>{error}</p>
      </div>
    </div>
  );

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      'Easy': 'success',
      'Medium': 'warning',
      'Hard': 'danger'
    };
    return badges[difficulty] || 'secondary';
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">💪 Workouts</h2>
      {workouts.length === 0 ? (
        <div className="alert alert-info">No workouts found.</div>
      ) : (
        <div className="row">
          {workouts.map((workout) => (
            <div key={workout.id} className="col-md-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{workout.title || workout.name || 'Untitled Workout'}</h5>
                  <p className="card-text">{workout.description || 'No description available'}</p>
                </div>
                <ul className="list-group list-group-flush">
                  {workout.category && (
                    <li className="list-group-item">
                      <strong>Category:</strong> <span className="badge bg-info">{workout.category}</span>
                    </li>
                  )}
                  {workout.difficulty && (
                    <li className="list-group-item">
                      <strong>Difficulty:</strong> <span className={`badge bg-${getDifficultyBadge(workout.difficulty)}`}>{workout.difficulty}</span>
                    </li>
                  )}
                  {workout.duration && (
                    <li className="list-group-item">
                      <strong>Duration:</strong> {workout.duration} minutes
                    </li>
                  )}
                  {workout.calories_estimate && (
                    <li className="list-group-item">
                      <strong>Calories:</strong> ~{workout.calories_estimate} cal
                    </li>
                  )}
                  {workout.equipment && (
                    <li className="list-group-item">
                      <strong>Equipment:</strong> {workout.equipment}
                    </li>
                  )}
                  {workout.muscle_groups && (
                    <li className="list-group-item">
                      <strong>Muscle Groups:</strong> {workout.muscle_groups}
                    </li>
                  )}
                  {workout.instructions && (
                    <li className="list-group-item">
                      <strong>Instructions:</strong> <small>{workout.instructions}</small>
                    </li>
                  )}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Workouts;
