import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { queueModelsService } from '../../services/Basicos/queueModelsService';
import { Container, Row, Col, Card, Form, Button, Tab, Nav, Alert, Spinner, ListGroup } from 'react-bootstrap';

const ModeloColas = () => {
  const { modelType: modelTypeParam } = useParams();
  const modelType = modelTypeParam.toUpperCase();
  const navigate = useNavigate();
  
  // Estados principales
  const [params, setParams] = useState({
      lam: '',
      mu: '',
      k: modelType === 'PICM' || modelType === 'PFCM' ? 2 : '',
      M: modelType === 'PFCS' || modelType === 'PFCM' ? 10 : ''
  });
  
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Estados para costos
  const [costParams, setCostParams] = useState({
      hrlab: 8,
      CTE: '',
      CTS: '',
      CTSE: '',
      CS: ''
  });
  
  // Estados para probabilidades
  const [probInputs, setProbInputs] = useState({
      system: { exact: '', max: '', min: '' },
      queue: { exact: '', max: '', min: '' }
  });
  
  const [probResults, setProbResults] = useState({
      system: { exact: null, max: null, min: null },
      queue: { exact: null, max: null, min: null }
  });
  
  const [activeTab, setActiveTab] = useState('metrics');
  const [activeProbSection, setActiveProbSection] = useState('basics');

  // Títulos de modelos
  const modelTitles = {
      'PICS': 'PICS (M/M/1) - Un servidor, población infinita',
      'PICM': 'PICM (M/M/k) - Múltiples servidores, población infinita',
      'PFCS': 'PFCS (M/M/1/M) - Un servidor, población finita',
      'PFCM': 'PFCM (M/M/k/M) - Múltiples servidores, población finita'
  };

  // Resetear al cambiar de modelo
  useEffect(() => {
      setParams({
          lam: '',
          mu: '',
          k: modelType === 'PICM' || modelType === 'PFCM' ? 2 : '',
          M: modelType === 'PFCS' || modelType === 'PFCM' ? 10 : ''
      });
      setCostParams({
          hrlab: 8,
          CTE: '',
          CTS: '',
          CTSE: '',
          CS: ''
      });
      setResults(null);
      setError(null);
  }, [modelType]);

  // Manejadores de cambios
  const handleParamChange = (e) => {
      const { name, value } = e.target;
      setParams(prev => ({ ...prev, [name]: value }));
  };

  const handleCostParamChange = (e) => {
      const { name, value } = e.target;
      setCostParams(prev => ({ ...prev, [name]: value }));
  };

  const handleProbInputChange = (type, field, value) => {
      setProbInputs(prev => ({
          ...prev,
          [type]: { ...prev[type], [field]: value }
      }));
  };

  // Cálculo principal del modelo
  const handleCalculate = async (e) => {
      e.preventDefault();
      setLoading(true);
      setError(null);

      try {
          const numericParams = {
              lam: parseFloat(params.lam),
              mu: parseFloat(params.mu),
              k: params.k ? parseInt(params.k) : undefined,
              M: params.M ? parseInt(params.M) : undefined
          };

          if (isNaN(numericParams.lam)) throw new Error("λ debe ser un número válido");
          if (isNaN(numericParams.mu)) throw new Error("μ debe ser un número válido");
          if (numericParams.k && isNaN(numericParams.k)) throw new Error("k debe ser un número válido");
          if (numericParams.M && isNaN(numericParams.M)) throw new Error("M debe ser un número válido");

          const response = await queueModelsService.calcularMetricas({
              modelType,
              params: numericParams
          });

          setResults(response);
      } catch (err) {
          setError(err.message || 'Error al calcular las métricas');
      } finally {
          setLoading(false);
      }
  };

  // Cálculo de costos
  const handleCalculateCosts = async () => {
      if (!results) return;
      setLoading(true);
      setError(null);

      try {
          const numericCostParams = {
              hrlab: parseFloat(costParams.hrlab) || 8,
              CTE: parseFloat(costParams.CTE) || 0,
              CTS: parseFloat(costParams.CTS) || 0,
              CTSE: parseFloat(costParams.CTSE) || 0,
              CS: parseFloat(costParams.CS) || 0
          };

          const response = await queueModelsService.calcularMetricas({
              modelType,
              params: {
                  ...params,
                  hrlab: numericCostParams.hrlab
              },
              operations: {
                  costs: {
                      CTE: numericCostParams.CTE,
                      CTS: numericCostParams.CTS,
                      CTSE: numericCostParams.CTSE,
                      CS: numericCostParams.CS
                  }
              }
          });

          setResults(response);
      } catch (err) {
          setError(err.message || 'Error al calcular los costos');
      } finally {
          setLoading(false);
      }
  };

  // Cálculos de probabilidad
  const calculateProbability = async (type, field) => {
      if (!results) return;
      setLoading(true);

      try {
          const inputValue = probInputs[type][field];
          let operations = {};

          if (field === 'exact') {
              const values = inputValue.split(',').map(v => parseInt(v.trim())).filter(v => !isNaN(v));
              if (values.length === 0) throw new Error("Ingrese valores válidos");
              operations = {
                  [`${type}Probabilities`]: { exact: values }
              };
          } else {
              const value = parseInt(inputValue);
              if (isNaN(value)) throw new Error("Ingrese un número válido");
              operations = {
                  [`${type}Probabilities`]: { [field]: value }
              };
          }

          const response = await queueModelsService.calcularMetricas({
              modelType,
              params: params,
              operations
          });

          setProbResults(prev => ({
              ...prev,
              [type]: {
                  ...prev[type],
                  [field]: response.metrics.probabilities[type][field]
              }
          }));
      } catch (err) {
          setError(err.message || `Error al calcular probabilidad ${field}`);
      } finally {
          setLoading(false);
      }
  };

  // Renderizado de campos de parámetros
  const renderParamFields = () => {
      const fields = [
          { id: 'lam', label: 'Tasa de llegada (λ)', required: true },
          { id: 'mu', label: 'Tasa de servicio (μ)', required: true }
      ];

      if (modelType === 'PICM' || modelType === 'PFCM') {
          fields.push({ id: 'k', label: 'Número de servidores (k)', required: true });
      }

      if (modelType === 'PFCS' || modelType === 'PFCM') {
          fields.push({ id: 'M', label: 'Tamaño población (M)', required: true });
      }

      return fields.map((field) => (
          <Form.Group key={field.id} className="mb-3">
              <Form.Label>{field.label}{field.required && '*'}</Form.Label>
              <Form.Control
                  type="number"
                  step="0.01"
                  min="0.01"
                  name={field.id}
                  value={params[field.id]}
                  onChange={handleParamChange}
                  required={field.required}
              />
          </Form.Group>
      ));
  };

  // Renderizado de métricas
  const renderMetrics = () => {
      if (!results?.metrics) return null;

      return (
          <Row>
              <Col md={6}>
                  <Card className="mb-4">
                      <Card.Header>Número Esperado de Clientes</Card.Header>
                      <Card.Body>
                          <div className="mb-2">
                              <strong>En el sistema (L):</strong> {results.metrics.numClientes.L.toFixed(4)}
                          </div>
                          <div className="mb-2">
                              <strong>En la cola (Lq):</strong> {results.metrics.numClientes.Lq.toFixed(4)}
                          </div>
                          {results.metrics.numClientes.Ln && (
                              <div>
                                  <strong>En cola no vacía (Ln):</strong> {results.metrics.numClientes.Ln.toFixed(4)}
                              </div>
                          )}
                      </Card.Body>
                  </Card>
              </Col>
              <Col md={6}>
                  <Card className="mb-4">
                      <Card.Header>Tiempos Esperados de Espera</Card.Header>
                      <Card.Body>
                          <div className="mb-2">
                              <strong>En el sistema (W):</strong> {results.metrics.waitingTime.W.toFixed(4)}
                          </div>
                          <div className="mb-2">
                              <strong>En la cola (Wq):</strong> {results.metrics.waitingTime.Wq.toFixed(4)}
                          </div>
                          {results.metrics.waitingTime.Wn && (
                              <div>
                                  <strong>En cola no vacía (Wn):</strong> {results.metrics.waitingTime.Wn.toFixed(4)}
                              </div>
                          )}
                      </Card.Body>
                  </Card>
              </Col>
          </Row>
      );
  };

  // Renderizado de probabilidades
  const renderProbabilities = () => {
      if (!results?.metrics?.probabilities?.system) return null;

      return (
          <Row>
              <Col md={4}>
                  <ListGroup>
                      <ListGroup.Item 
                          action 
                          active={activeProbSection === 'basics'}
                          onClick={() => setActiveProbSection('basics')}
                      >
                          Probabilidades Básicas
                      </ListGroup.Item>
                      <ListGroup.Item 
                          action 
                          active={activeProbSection === 'system-calc'}
                          onClick={() => setActiveProbSection('system-calc')}
                      >
                          Cálculos en el Sistema
                      </ListGroup.Item>
                      <ListGroup.Item 
                          action 
                          active={activeProbSection === 'queue-calc'}
                          onClick={() => setActiveProbSection('queue-calc')}
                      >
                          Cálculos en Cola
                      </ListGroup.Item>
                  </ListGroup>
              </Col>
              
              <Col md={8}>
                  {activeProbSection === 'basics' && renderBasicProbabilities()}
                  {activeProbSection === 'system-calc' && renderSystemCalculations()}
                  {activeProbSection === 'queue-calc' && renderQueueCalculations()}
              </Col>
          </Row>
      );
  };

  const renderBasicProbabilities = () => {
      const systemProbs = results.metrics.probabilities.system;
      const queueProbs = results.metrics.probabilities.queue || {};

      return (
          <Card>
              <Card.Header>Probabilidades Básicas</Card.Header>
              <Card.Body>
                  <h5 className="mb-3">Sistema</h5>
                  {Object.entries(systemProbs).map(([key, value]) => (
                      <div key={key} className="mb-2 row">
                          <div className="col-8"><strong>{key}:</strong></div>
                          <div className="col-4">{typeof value === 'number' ? value.toFixed(6) : JSON.stringify(value)}</div>
                      </div>
                  ))}
                  
                  {Object.keys(queueProbs).length > 0 && (
                      <>
                          <hr />
                          <h5 className="mb-3">Cola</h5>
                          {Object.entries(queueProbs).map(([key, value]) => (
                              <div key={key} className="mb-2 row">
                                  <div className="col-8"><strong>{key}:</strong></div>
                                  <div className="col-4">{typeof value === 'number' ? value.toFixed(6) : JSON.stringify(value)}</div>
                              </div>
                          ))}
                      </>
                  )}
              </Card.Body>
          </Card>
      );
  };

  const renderSystemCalculations = () => {
      return (
          <Card>
              <Card.Header>Cálculos de Probabilidad en el Sistema</Card.Header>
              <Card.Body>
                  <Form.Group className="mb-3">
                      <Form.Label>Probabilidad de exactamente estos usuarios (separados por comas):</Form.Label>
                      <div className="input-group">
                          <Form.Control
                              type="text"
                              value={probInputs.system.exact}
                              onChange={(e) => handleProbInputChange('system', 'exact', e.target.value)}
                              placeholder="Ej: 0, 1, 2"
                          />
                          <Button 
                              variant="outline-secondary" 
                              onClick={() => calculateProbability('system', 'exact')}
                              disabled={!probInputs.system.exact}
                          >
                              Calcular
                          </Button>
                      </div>
                      {probResults.system.exact && (
                          <div className="mt-2 alert alert-light">
                              <strong>Resultado:</strong> {probResults.system.exact.exactSum.toFixed(6)}
                              <pre className="mt-2">
                                  {Object.entries(probResults.system.exact.exact).map(([n, p]) => 
                                      `P(${n}) = ${p.toFixed(6)}\n`
                                  )}
                              </pre>
                          </div>
                      )}
                  </Form.Group>

                  <Form.Group className="mb-3">
                      <Form.Label>Probabilidad de máximo este número de usuarios:</Form.Label>
                      <div className="input-group">
                          <Form.Control
                              type="number"
                              min="0"
                              value={probInputs.system.max}
                              onChange={(e) => handleProbInputChange('system', 'max', e.target.value)}
                              placeholder="Ej: 5"
                          />
                          <Button 
                              variant="outline-secondary" 
                              onClick={() => calculateProbability('system', 'max')}
                              disabled={!probInputs.system.max}
                          >
                              Calcular
                          </Button>
                      </div>
                      {probResults.system.max && (
                          <div className="mt-2 alert alert-light">
                              <strong>Resultado:</strong> P(≤{probInputs.system.max}) = {probResults.system.max.probability.toFixed(6)}
                              <div className="mt-1">Límite: {probResults.system.max.upTo}</div>
                          </div>
                      )}
                  </Form.Group>

                  <Form.Group className="mb-3">
                      <Form.Label>Probabilidad de al menos este número de usuarios:</Form.Label>
                      <div className="input-group">
                          <Form.Control
                              type="number"
                              min="0"
                              value={probInputs.system.min}
                              onChange={(e) => handleProbInputChange('system', 'min', e.target.value)}
                              placeholder="Ej: 2"
                          />
                          <Button 
                              variant="outline-secondary" 
                              onClick={() => calculateProbability('system', 'min')}
                              disabled={!probInputs.system.min}
                          >
                              Calcular
                          </Button>
                      </div>
                      {probResults.system.min && (
                          <div className="mt-2 alert alert-light">
                              <strong>Resultado:</strong> P(≥{probInputs.system.min}) = {probResults.system.min.probability.toFixed(6)}
                              <div className="mt-1">Límite: {probResults.system.min.upTo}</div>
                          </div>
                      )}
                  </Form.Group>
              </Card.Body>
          </Card>
      );
  };

  const renderQueueCalculations = () => {
      return (
          <Card>
              <Card.Header>Cálculos de Probabilidad en Cola</Card.Header>
              <Card.Body>
                  <Form.Group className="mb-3">
                      <Form.Label>Probabilidad de exactamente estos usuarios en cola (separados por comas):</Form.Label>
                      <div className="input-group">
                          <Form.Control
                              type="text"
                              value={probInputs.queue.exact}
                              onChange={(e) => handleProbInputChange('queue', 'exact', e.target.value)}
                              placeholder="Ej: 0, 1, 2"
                          />
                          <Button 
                              variant="outline-secondary" 
                              onClick={() => calculateProbability('queue', 'exact')}
                              disabled={!probInputs.queue.exact}
                          >
                              Calcular
                          </Button>
                      </div>
                      {probResults.queue.exact && (
                          <div className="mt-2 alert alert-light">
                              <strong>Resultado:</strong> {probResults.queue.exact.exactSum.toFixed(6)}
                              <pre className="mt-2">
                                  {Object.entries(probResults.queue.exact.exact).map(([r, p]) => 
                                      `Q(${r}) = ${p.toFixed(6)}\n`
                                  )}
                              </pre>
                          </div>
                      )}
                  </Form.Group>

                  <Form.Group className="mb-3">
                      <Form.Label>Probabilidad de máximo este número de usuarios en cola:</Form.Label>
                      <div className="input-group">
                          <Form.Control
                              type="number"
                              min="0"
                              value={probInputs.queue.max}
                              onChange={(e) => handleProbInputChange('queue', 'max', e.target.value)}
                              placeholder="Ej: 3"
                          />
                          <Button 
                              variant="outline-secondary" 
                              onClick={() => calculateProbability('queue', 'max')}
                              disabled={!probInputs.queue.max}
                          >
                              Calcular
                          </Button>
                      </div>
                      {probResults.queue.max && (
                          <div className="mt-2 alert alert-light">
                              <strong>Resultado:</strong> P(≤{probInputs.queue.max}) = {probResults.queue.max.probability.toFixed(6)}
                              <div className="mt-1">Límite: {probResults.queue.max.upTo}</div>
                          </div>
                      )}
                  </Form.Group>

                  <Form.Group className="mb-3">
                      <Form.Label>Probabilidad de al menos este número de usuarios en cola:</Form.Label>
                      <div className="input-group">
                          <Form.Control
                              type="number"
                              min="0"
                              value={probInputs.queue.min}
                              onChange={(e) => handleProbInputChange('queue', 'min', e.target.value)}
                              placeholder="Ej: 1"
                          />
                          <Button 
                              variant="outline-secondary" 
                              onClick={() => calculateProbability('queue', 'min')}
                              disabled={!probInputs.queue.min}
                          >
                              Calcular
                          </Button>
                      </div>
                      {probResults.queue.min && (
                          <div className="mt-2 alert alert-light">
                              <strong>Resultado:</strong> P(≥{probInputs.queue.min}) = {probResults.queue.min.probability.toFixed(6)}
                              <div className="mt-1">Límite: {probResults.queue.min.upTo}</div>
                          </div>
                      )}
                  </Form.Group>
              </Card.Body>
          </Card>
      );
  };

  // Renderizado de costos
  const renderCosts = () => {
      if (!results) return null;

      return (
          <Row>
              <Col md={6}>
                  <Card className="mb-4">
                      <Card.Header>Parámetros de Costo</Card.Header>
                      <Card.Body>
                          <Form.Group className="mb-3">
                              <Form.Label>Horas laborables al día (hrlab)</Form.Label>
                              <Form.Control
                                  type="number"
                                  step="0.1"
                                  min="0.1"
                                  name="hrlab"
                                  value={costParams.hrlab}
                                  onChange={handleCostParamChange}
                              />
                          </Form.Group>
                          <Form.Group className="mb-3">
                              <Form.Label>Costo espera en cola (CTE)</Form.Label>
                              <Form.Control
                                  type="number"
                                  step="0.01"
                                  min="0"
                                  name="CTE"
                                  value={costParams.CTE}
                                  onChange={handleCostParamChange}
                              />
                          </Form.Group>
                          <Form.Group className="mb-3">
                              <Form.Label>Costo tiempo sistema (CTS)</Form.Label>
                              <Form.Control
                                  type="number"
                                  step="0.01"
                                  min="0"
                                  name="CTS"
                                  value={costParams.CTS}
                                  onChange={handleCostParamChange}
                              />
                          </Form.Group>
                          <Form.Group className="mb-3">
                              <Form.Label>Costo tiempo servicio (CTSE)</Form.Label>
                              <Form.Control
                                  type="number"
                                  step="0.01"
                                  min="0"
                                  name="CTSE"
                                  value={costParams.CTSE}
                                  onChange={handleCostParamChange}
                              />
                          </Form.Group>
                          <Form.Group className="mb-3">
                              <Form.Label>Costo servidor (CS)</Form.Label>
                              <Form.Control
                                  type="number"
                                  step="0.01"
                                  min="0"
                                  name="CS"
                                  value={costParams.CS}
                                  onChange={handleCostParamChange}
                              />
                          </Form.Group>
                          <Button 
                              variant="primary" 
                              onClick={handleCalculateCosts}
                              disabled={!costParams.CTE && !costParams.CTS && !costParams.CTSE && !costParams.CS}
                          >
                              Calcular Costos
                          </Button>
                      </Card.Body>
                  </Card>
              </Col>
              <Col md={6}>
                  <Card className="mb-4">
                      <Card.Header>Resultados de Costos</Card.Header>
                      <Card.Body>
                          {results.metrics.costs ? (
                              <>
                                  <div className="mb-2 row">
                                      <div className="col-8">Horas laborables al día:</div>
                                      <div className="col-4">{costParams.hrlab}</div>
                                  </div>
                                  <div className="mb-2 row">
                                      <div className="col-8">Costo diario espera en cola (CTE):</div>
                                      <div className="col-4">${results.metrics.costs.daily.CTE.toFixed(2)}</div>
                                  </div>
                                  <div className="mb-2 row">
                                      <div className="col-8">Costo diario tiempo en sistema (CTS):</div>
                                      <div className="col-4">${results.metrics.costs.daily.CTS.toFixed(2)}</div>
                                  </div>
                                  <div className="mb-2 row">
                                      <div className="col-8">Costo diario tiempo en servicio (CTSE):</div>
                                      <div className="col-4">${results.metrics.costs.daily.CTSE.toFixed(2)}</div>
                                  </div>
                                  <div className="mb-2 row">
                                      <div className="col-8">Costo diario servidor (CS):</div>
                                      <div className="col-4">${results.metrics.costs.daily.CS.toFixed(2)}</div>
                                  </div>
                                  <div className="mt-3 pt-2 border-top row">
                                      <div className="col-8"><h5>COSTO TOTAL DIARIO:</h5></div>
                                      <div className="col-4"><h4 className="text-success">${results.metrics.costs.daily.total.toFixed(2)}</h4></div>
                                  </div>
                              </>
                          ) : (
                              <div className="text-center text-muted">
                                  <p>Ingrese los parámetros de costo y haga clic en "Calcular Costos"</p>
                              </div>
                          )}
                      </Card.Body>
                  </Card>
              </Col>
          </Row>
      );
  };

  return (
      <Container className="py-4">
          <Button variant="outline-secondary" onClick={() => navigate('/teoria-colas')} className="mb-4">
              <i className="fas fa-arrow-left me-2"></i> Volver a Modelos
          </Button>

          <h1 className="mb-4">{modelTitles[modelType]}</h1>

          <Card className="mb-4">
              <Card.Header>Parámetros del Modelo</Card.Header>
              <Card.Body>
                  <Form onSubmit={handleCalculate}>
                      <Row>
                          <Col md={6}>
                              {renderParamFields()}
                          </Col>
                          <Col md={6}>
                              <div className="d-flex align-items-end h-100">
                                  <Button 
                                      variant="primary" 
                                      type="submit" 
                                      disabled={loading}
                                      className="w-100"
                                  >
                                      {loading ? (
                                          <>
                                              <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" className="me-2"/>
                                              Calculando...
                                          </>
                                      ) : 'Calcular Métricas'}
                                  </Button>
                              </div>
                          </Col>
                      </Row>
                  </Form>
              </Card.Body>
          </Card>

          {error && (
              <Alert variant="danger" className="mb-4">
                  {error}
              </Alert>
          )}

          {results && (
              <>
                  <Tab.Container activeKey={activeTab} onSelect={(k) => setActiveTab(k)}>
                      <Nav variant="tabs" className="mb-3">
                          <Nav.Item>
                              <Nav.Link eventKey="metrics">Métricas</Nav.Link>
                          </Nav.Item>
                          <Nav.Item>
                              <Nav.Link eventKey="probabilities">Probabilidades</Nav.Link>
                          </Nav.Item>
                          <Nav.Item>
                              <Nav.Link eventKey="costs">Costos</Nav.Link>
                          </Nav.Item>
                      </Nav>

                      <Tab.Content>
                          <Tab.Pane eventKey="metrics">
                              {renderMetrics()}
                          </Tab.Pane>
                          <Tab.Pane eventKey="probabilities">
                              {renderProbabilities()}
                          </Tab.Pane>
                          <Tab.Pane eventKey="costs">
                              {renderCosts()}
                          </Tab.Pane>
                      </Tab.Content>
                  </Tab.Container>
              </>
          )}
      </Container>
  );
};

export default ModeloColas;