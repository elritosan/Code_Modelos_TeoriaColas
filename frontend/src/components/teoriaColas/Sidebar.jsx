// frontend\src\components\teoriaColas\Sidebar.jsx
import React from 'react';
import { Nav } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();

  return (
    <Nav className="flex-column sidebar bg-light p-3" style={{ width: '250px', minHeight: '100vh' }}>
      <div className="sidebar-header mb-4">
        <h4 className="text-center">Modelos de Colas</h4>
      </div>
      
      <Nav.Item>
        <Nav.Link 
          as={Link} 
          to="/teoria-colas" 
          active={location.pathname === '/teoria-colas'}
          className="mb-2"
        >
          <i className="fas fa-home me-2"></i>
          Dashboard
        </Nav.Link>
      </Nav.Item>
      
      <div className="sidebar-divider my-3 border-top"></div>
      
      <h6 className="sidebar-subtitle px-3 mb-2 text-muted">Modelos Básicos</h6>
      
      <Nav.Item>
        <Nav.Link 
          as={Link} 
          to="/teoria-colas/pics" 
          active={location.pathname.includes('/teoria-colas/pics')}
          className="mb-1"
        >
          <i className="fas fa-1 me-2"></i>
          Modelo PICS
        </Nav.Link>
      </Nav.Item>
      
      <Nav.Item>
        <Nav.Link 
          as={Link} 
          to="/teoria-colas/picm" 
          active={location.pathname.includes('/teoria-colas/picm')}
          className="mb-1"
        >
          <i className="fas fa-users me-2"></i>
          Modelo PICM
        </Nav.Link>
      </Nav.Item>
      
      <div className="sidebar-divider my-3 border-top"></div>
      
      <h6 className="sidebar-subtitle px-3 mb-2 text-muted">Modelos Población Finita</h6>
      
      <Nav.Item>
        <Nav.Link 
          as={Link} 
          to="/teoria-colas/pfcs" 
          active={location.pathname.includes('/teoria-colas/pfcs')}
          className="mb-1"
        >
          <i className="fas fa-user-friends me-2"></i>
          Modelo PFCS
        </Nav.Link>
      </Nav.Item>
      
      <Nav.Item>
        <Nav.Link 
          as={Link} 
          to="/teoria-colas/pfcm" 
          active={location.pathname.includes('/teoria-colas/pfcm')}
          className="mb-1"
        >
          <i className="fas fa-users-cog me-2"></i>
          Modelo PFCM
        </Nav.Link>
      </Nav.Item>
    </Nav>
  );
};

export default Sidebar;