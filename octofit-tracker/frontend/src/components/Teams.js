import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Teams Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Teams Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams Component - Processed teams:', teamsData);
        setTeams(teamsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams Component - Error fetching teams:', error);
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
        <h5>Error Loading Teams</h5>
        <p>{error}</p>
      </div>
    </div>
  );

  const getMemberCount = (team) => {
    // Check various possible field names for member count
    if (team.member_count !== undefined) return team.member_count;
    if (team.members_count !== undefined) return team.members_count;
    if (team.memberCount !== undefined) return team.memberCount;
    if (team.members && Array.isArray(team.members)) return team.members.length;
    console.log('Teams Component - Team data structure:', team);
    return 0;
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">👥 Teams</h2>
      {teams.length === 0 ? (
        <div className="alert alert-info">No teams found.</div>
      ) : (
        <div className="row">
          {teams.map((team) => {
            const memberCount = getMemberCount(team);
            return (
              <div key={team.id} className="col-md-4 mb-4">
                <div className="card h-100">
                  <div className="card-header bg-primary text-white">
                    <h5 className="card-title mb-0">{team.name}</h5>
                  </div>
                  <div className="card-body">
                    <p className="card-text">{team.description || 'No description available'}</p>
                  </div>
                  <div className="card-footer">
                    <small className="text-muted">
                      <strong>Created:</strong> {new Date(team.created_at).toLocaleDateString()}
                    </small>
                    <div className="mt-2">
                      <span className="badge bg-secondary">{memberCount} {memberCount === 1 ? 'Member' : 'Members'}</span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Teams;
