// frontend\src\components\teoriaColas\ModeloCard.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

const ModeloCard = ({ icon, title, description, path }) => {
  const navigate = useNavigate();
  
  return (
    <div className="card shadow-sm h-100 hover-effect">
      <div className="card-body text-center">
        <i className={`${icon} fa-3x mb-3 text-primary`}></i>
        <h5 className="card-title">{title}</h5>
        <p className="card-text text-muted">{description}</p>
        <button 
          className="btn btn-primary"
          onClick={() => navigate(path)}
        >
          Seleccionar
        </button>
      </div>
    </div>
  );
};

export default ModeloCard;