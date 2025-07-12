// frontend\src\views\teoriaColas\TeoriaColasDashboard.jsx
import React from 'react';
import ModeloCard from '../../components/teoriaColas/ModeloCard';
import { Container, Row, Col } from 'react-bootstrap';

const TeoriaColasDashboard = () => {
  const modelos = [
    {
      icon: 'fas fa-1',
      title: 'PICS (M/M/1)',
      description: 'Un servidor, población infinita',
      path: '/teoria-colas/pics',
      color: 'primary'
    },
    {
      icon: 'fas fa-users',
      title: 'PICM (M/M/k)',
      description: 'Múltiples servidores, población infinita',
      path: '/teoria-colas/picm',
      color: 'success'
    },
    {
      icon: 'fas fa-user-friends',
      title: 'PFCS (M/M/1/M)',
      description: 'Un servidor, población finita',
      path: '/teoria-colas/pfcs',
      color: 'warning'
    },
    {
      icon: 'fas fa-users-cog',
      title: 'PFCM (M/M/k/M)',
      description: 'Múltiples servidores, población finita',
      path: '/teoria-colas/pfcm',
      color: 'info'
    }
  ];

  return (
    <Container className="py-4">
      <div className="text-center mb-5">
        <h1 className="display-4 mb-3">Modelos de Teoría de Colas</h1>
        <p className="lead text-muted">
          Seleccione el modelo de cola que desea analizar
        </p>
      </div>

      <Row className="g-4 justify-content-center">
        {modelos.map((modelo, index) => (
          <Col key={index} xs={12} md={6} lg={4} xl={3}>
            <ModeloCard 
              icon={modelo.icon}
              title={modelo.title}
              description={modelo.description}
              path={modelo.path}
              color={modelo.color}
            />
          </Col>
        ))}
      </Row>

      <div className="mt-5 pt-4 border-top">
        <h3 className="h5 mb-3">Acerca de los modelos</h3>
        <div className="text-muted">
          <p>
            La teoría de colas estudia el comportamiento de líneas de espera en sistemas.
            Seleccione un modelo para calcular métricas como tiempos de espera, longitud de cola
            y probabilidades del sistema.
          </p>
        </div>
      </div>
    </Container>
  );
};

export default TeoriaColasDashboard;