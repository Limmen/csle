import React, { useState, useRef, useEffect } from 'react'
import {
  InputGroup,
  FormControl,
  Button,
  Card,
  Spinner,
  Tooltip,
  OverlayTrigger,
  Modal,
  ListGroup,
  ProgressBar,
  Form
} from 'react-bootstrap'
import './RecoveryAI.css'
import 'react-confirm-alert/src/react-confirm-alert.css'
import { useNavigate } from 'react-router-dom'
import { useAlert } from 'react-alert'
import RecoveryAIPic from './RecoveryAI.png'
import {
  LOGIN_PAGE_RESOURCE,
  TOKEN_QUERY_PARAM,
  HTTP_REST_POST,
  RECOVERY_AI_RESOURCE,
  RECOVERY_AI_EXAMPLE_RESOURCE,
  API_BASE_URL
} from '../../Common/constants'

const usePrevious = (value) => {
  const ref = useRef()
  useEffect(() => {
    ref.current = value
  }, [value])
  return ref.current
}

const downloadJson = (data, filename) => {
  const jsonString = `data:text/json;charset=utf-8,${encodeURIComponent(
    JSON.stringify(data, null, 2)
  )}`
  const link = document.createElement('a')
  link.href = jsonString
  link.download = filename
  link.click()
}

const RecoveryProgress = ({ systemState, recoveryActions }) => {
  const TOTAL_STAGES = 6

  const completedStages = systemState ? Object.values(systemState).filter(v => v === true).length : 0
  const progressPercentage = (completedStages / TOTAL_STAGES) * 100
  const progressLabel = `${completedStages} / ${TOTAL_STAGES} recovery stages complete (${recoveryActions.length} recovery actions taken)`

  return (
    <Card className="shadow-sm mb-4">
      <Card.Header as="h5" className="text-center fw-bold">
        <div className="d-flex justify-content-center align-items-center">
          <Spinner animation="border" size="sm" variant="secondary" className="me-2 spinnerMarginRight" />
          Generating recovery plan..
        </div>
      </Card.Header>
      <Card.Body>
        <ProgressBar
          className="black-progress-label"
          now={progressPercentage}
          label={progressLabel}
          animated
          variant="success"
          style={{ height: '25px', fontSize: '0.9rem' }}
        />
      </Card.Body>
    </Card>
  )
}

const initialSystemState = {
  is_attack_contained: false,
  is_knowledge_sufficient: false,
  are_forensics_preserved: false,
  is_eradicated: false,
  is_hardened: false,
  is_recovered: false
}

const RecoveryAI = (props) => {
  const [systemDescription, setSystemDescription] = useState('')
  const [networkLogs, setNetworkLogs] = useState('')
  const [currentReasoning, setCurrentReasoning] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [loadingExample, setLoadingExample] = useState(false)
  const [showInfoModal, setShowInfoModal] = useState(false)

  const [incidentClassification, setIncidentClassification] = useState(null)
  const [recoveryActions, setRecoveryActions] = useState([])
  const [systemState, setSystemState] = useState(null)
  const [historicalData, setHistoricalData] = useState([])
  const [noIncidentFound, setNoIncidentFound] = useState(false)

  const [partialJson, setPartialJson] = useState('')
  const [processingDescr, setProcessingDescr] = useState('')
  const [reasoningDescr, setReasoningDescr] = useState('')
  const parsingStateRef = useRef('REASONING')
  const jsonBuffer = useRef('')

  const [rag, setRag] = useState(true)
  const [optimizationSteps, setOptimizationSteps] = useState(1)
  const [lookaheadHorizon, setLookaheadHorizon] = useState(1)
  const [rolloutHorizon, setRolloutHorizon] = useState(0)
  const [temperature, setTemperature] = useState(1.0)

  const reasoningPreRef = useRef(null)
  const jsonPreRef = useRef(null)

  const setSessionData = props.setSessionData
  const alert = useAlert()
  const navigate = useNavigate()
  const abortRef = useRef(null)

  const abortCurrentStream = () => {
    if (abortRef.current) {
      abortRef.current.abort()
      abortRef.current = null
    }
    setIsProcessing(false)
    setProcessingDescr('')
    setCurrentReasoning('')
    setReasoningDescr('')
    jsonBuffer.current = ''
    setPartialJson('')
  }

  const resetAll = (keepLogs) => {
    abortCurrentStream()
    if (!keepLogs) {
      setSystemDescription('')
      setNetworkLogs('')
    }
    setCurrentReasoning('')
    setIncidentClassification(null)
    setRecoveryActions([])
    setSystemState(null)
    setPartialJson('')
    parsingStateRef.current = 'REASONING'
    setIsProcessing(false)
    setProcessingDescr('')
    setReasoningDescr('')
    setHistoricalData([])
    setNoIncidentFound(false)
  }

  const handleSystemDescriptionChange = (e) => setSystemDescription(e.target.value)
  const handleNetworkLogsChange = (e) => setNetworkLogs(e.target.value)

  const handleDownloadIncidentReport = () => {
    const incidentReportStep = historicalData.find(step => step.data && step.data.Entities)
    if (incidentReportStep) {
      const dataToDownload = {
        reasoning: incidentReportStep.reasoning,
        report: incidentReportStep.data
      }
      downloadJson(dataToDownload, 'incident_report.json')
    } else {
      alert.error('Could not find incident report data to download.')
    }
  }

  const handleDownloadRecoveryPlan = () => {
    if (historicalData.length > 0) {
      const allActions = historicalData.filter(step => step.data && step.data.Action).map(step => step.data)
      const allStates = historicalData.filter(step => step.data && Object.prototype.hasOwnProperty.call(step.data, 'is_recovered')).map(step => step.data)
      const allReasonings = historicalData.map(step => step.reasoning).filter(Boolean)

      const dataToDownload = {
        recovery_actions: allActions,
        system_states: allStates,
        reasonings: allReasonings,
        full_history: historicalData
      }
      downloadJson(dataToDownload, 'recovery_plan.json')
    } else {
      alert.error('No recovery plan data available to download.')
    }
  }

  const handleFetchExample = () => {
    const token = props.sessionData?.token || sessionStorage.getItem('token')
    if (!token) {
      alert.show('Session token expired. Please login again.')
      navigate(`/${LOGIN_PAGE_RESOURCE}`)
      return
    }
    const url = `${API_BASE_URL}/${RECOVERY_AI_RESOURCE}/${RECOVERY_AI_EXAMPLE_RESOURCE}?${TOKEN_QUERY_PARAM}=${token}`
    setLoadingExample(true)
    fetch(url)
      .then((res) => {
        if (res.status === 401) {
          alert.show('Session token expired. Please login again.')
          setSessionData(null)
          navigate(`/${LOGIN_PAGE_RESOURCE}`)
          return null
        }
        if (!res.ok) {
          alert.error(`Failed to fetch example (status ${res.status})`)
          return null
        }
        return res.json()
      })
      .then((data) => {
        if (!data) return
        setSystemDescription(data.systemDescription || '')
        setNetworkLogs(data.networkLogs || '')
      })
      .catch(() => {
        alert.error('Unable to connect to the Recovery AI service')
      })
      .finally(() => setLoadingExample(false))
  }

  const handleGeneratePlan = () => {
    resetAll(true)
    setIsProcessing(true)
    setProcessingDescr('Generating incident report..')
    setReasoningDescr('Analyzing the logs and the system description..')
    parsingStateRef.current = 'REASONING'

    const token = props.sessionData?.token || sessionStorage.getItem('token')
    if (!token) {
      alert.show('Session token expired. Please login again.')
      navigate(`/${LOGIN_PAGE_RESOURCE}`)
      return
    }

    const url = `${API_BASE_URL}/${RECOVERY_AI_RESOURCE}?${TOKEN_QUERY_PARAM}=${token}`
    const controller = new AbortController()
    abortRef.current = controller

    fetch(url, {
      method: HTTP_REST_POST,
      headers: {
        'Content-Type': 'application/json',
        Accept: 'text/event-stream'
      },
      body: JSON.stringify({
        systemDescription,
        networkLogs,
        rag,
        optimizationSteps: optimizationSteps,
        lookaheadHorizon: lookaheadHorizon,
        rolloutHorizon: rolloutHorizon,
        temperature
      }),
      signal: controller.signal
    })
      .then((res) => {
        if (res.status === 401) {
          alert.show('Session token expired. Please login again.')
          setSessionData(null)
          navigate(`/${LOGIN_PAGE_RESOURCE}`)
          return null
        }
        if (!res.ok) {
          alert.error(`Recovery AI returned status ${res.status}`)
          setIsProcessing(false)
          return null
        }
        return res.body
      })
      .then((body) => {
        if (body === null) return

        const reader = body.getReader()
        const decoder = new TextDecoder('utf-8')
        let buffer = ''
        let reasoningForCurrentStep = ''
        const processJson = (jsonString, reasoningText) => {
          try {
            const obj = JSON.parse(jsonString)
            setHistoricalData(prev => [...prev, { reasoning: reasoningText, data: obj }])
            if (obj.Entities) {
              if (Object.keys(obj.Entities).length === 0) {
                obj.Entities.Attacker = []
                obj.Entities.System = []
                obj.Entities.Targeted = []
              }
              setIncidentClassification(obj)

              if (obj.Incident === 'No') {
                setNoIncidentFound(true)
                abortCurrentStream()
                return
              }

              setSystemState(initialSystemState)
              setReasoningDescr('Selecting the next recovery action..')
              setProcessingDescr('Generating the recovery action..')
            } else if (obj.Action) {
              setRecoveryActions((prev) => [...prev, obj])
              setReasoningDescr(`Analyzing the effect of the action '${obj.Action}' and predicting the next state..`)
              setProcessingDescr(`Generating the next state after taking action '${obj.Action}'..`)
            } else if (Object.prototype.hasOwnProperty.call(obj, 'is_recovered')) {
              setSystemState(obj)
              setReasoningDescr('Selecting the next recovery action..')
              setProcessingDescr('Generating the recovery action..')
            }
            jsonBuffer.current = ''
            setCurrentReasoning('')
            setPartialJson('')
            parsingStateRef.current = 'REASONING'
          } catch (e) {
            console.error('Failed to parse JSON chunk:', jsonString, e)
          }
        }
        const pump = () =>
          reader.read().then(({ value, done }) => {
            if (done) {
              setIsProcessing(false)
              return
            }

            buffer += decoder.decode(value, { stream: true })
            let nl
            while ((nl = buffer.indexOf('\n')) >= 0) {
              let line = buffer.slice(0, nl)
              buffer = buffer.slice(nl + 1)
              if (line.endsWith('\r')) {
                line = line.slice(0, -1)
              }
              if (!line.startsWith('data: ')) continue
              const token = line.slice(6)

              if (token.trim() === '</think>') {
                if (parsingStateRef.current === 'REASONING') {
                  parsingStateRef.current = 'JSON'
                }
                continue
              }

              if (parsingStateRef.current === 'REASONING') {
                const cleanToken = token.replace(/\\n/g, '\n')
                setCurrentReasoning((prev) => (prev ? `${prev}${cleanToken}` : cleanToken))
                reasoningForCurrentStep += cleanToken
              } else if (parsingStateRef.current === 'JSON') {
                const token2 = token.replace(/\\n/g, '\n')
                const sanitizedToken = token2.replace(/\u00A0/g, ' ')
                setPartialJson(prev => prev + sanitizedToken)
                jsonBuffer.current += sanitizedToken.replace(/\r?\n|\r/g, ' ')
                try {
                  JSON.parse(jsonBuffer.current)
                  processJson(jsonBuffer.current, reasoningForCurrentStep)
                  reasoningForCurrentStep = ''
                } catch (e) {
                  // Not a complete JSON object yet, continue buffering
                }
              }
            }
            return pump()
          })

        pump().catch((err) => {
          if (err.name !== 'AbortError') {
            alert.error('Connection to Recovery AI lost')
            setIsProcessing(false)
          }
        })
      })
      .catch((error) => {
        if (error.name !== 'AbortError') {
          alert.error('Unable to connect to Recovery AI service')
          setIsProcessing(false)
        }
      })
  }

  const prevReasoning = usePrevious(currentReasoning)
  const prevPartialJson = usePrevious(partialJson)

  useEffect(() => {
    if (currentReasoning && !prevReasoning && reasoningPreRef.current) {
      reasoningPreRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
    if (partialJson && !prevPartialJson && jsonPreRef.current) {
      jsonPreRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }, [currentReasoning, partialJson, prevReasoning, prevPartialJson])

  const BulletList = ({ items }) => (
    <ul className="mb-0 ps-3" style={{
      listStyleType: 'disc',
      listStylePosition: 'outside',
      paddingLeft: '1.25rem',
      margin: 0,
      textAlign: 'left'
    }}>
      {items.map((it, idx) => (<li key={idx} style={{ textAlign: 'left' }}>{it}</li>))}
    </ul>
  )

  const InfoModal = (props) => (
    <Modal {...props} size="lg" aria-labelledby="contained-modal-title-vcenter" centered>
      <Modal.Header closeButton><Modal.Title id="contained-modal-title-vcenter" className="modalTitle">Recovery
        AI</Modal.Title></Modal.Header>
      <Modal.Body>
        <p className="modalText">
          RecoveryAI is a a decision-theoretic framework to enable effective use of LLMs for
          attack recovery. The key insight that underlies our framework is that the extensive knowledge about
          cyberattacks
          available in current LLMs can be used as a substitute for a system model. We exploit this insight to design
          a novel
          decision-theoretic framework for recovery planning, which does not require full knowledge of the system
          dynamics. As a
          consequence, we avoid the limitations of current recovery methods that rely on manually-designed models,
          which often
          are overly simplistic. Our framework includes three parts: (i) offline fine-tuning of the LLM to align it
          with the attack
          recovery objective; (ii) retrieval-augmented generation (RAG) to ground the LLM in current threat
          information and system
          knowledge; and (iii) in-context learning based on decision-theoretic planning to synthesize effective
          recovery strategies.
        </p>
        <div className="text-center"><img src={RecoveryAIPic} alt="Recovery AI" className="img-fluid" /></div>
      </Modal.Body>
      <Modal.Footer className="modalFooter"><Button onClick={props.onHide} size="sm">Close</Button></Modal.Footer>
    </Modal>
  )

  const StateVisualizer = ({ state }) => {
    if (!state) return null
    const stateEntries = [
      {
        key: 'is_attack_contained',
        label: 'Attack contained',
        tooltip: 'Has the immediate threat been stopped from spreading?'
      },
      {
        key: 'is_knowledge_sufficient',
        label: 'Information sufficient',
        tooltip: 'Have we gathered enough data to effectively contain and eradicate the attack?'
      },
      {
        key: 'are_forensics_preserved',
        label: 'Forensics preserved',
        tooltip: 'Has evidence been captured and stored in a forensically sound manner?'
      },
      {
        key: 'is_eradicated',
        label: 'Attack eradicated',
        tooltip: 'Is the attacker and any malware completely removed from the system?'
      },
      {
        key: 'is_hardened',
        label: 'System hardened',
        tooltip: 'Has the root cause of the attack been remediated? i.e., are future attacks of the same type prevented?'
      },
      { key: 'is_recovered', label: 'Services restored', tooltip: 'Are operational services restored for users?' }
    ]
    return (
      <Card>
        <Card.Header as="h6" className="text-center fw-bold">Recovery State</Card.Header>
        <Card.Body className="p-0">
          <ListGroup variant="flush">
            {stateEntries.map(entry => (
              <ListGroup.Item key={entry.key} className="d-flex justify-content-between align-items-center">
                <OverlayTrigger placement="top" overlay={renderTooltip(entry.tooltip)}>
                  <span><i className="fa fa-info-circle me-1 spinnerMarginRight"
                           aria-hidden="true" />{entry.label}:</span>
                </OverlayTrigger>
                {state[entry.key]
                  ? <i className="fa fa-check-circle text-success fa-lg" aria-hidden="true"></i>
                  : <i className="fa fa-times-circle text-danger fa-lg" aria-hidden="true"></i>}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Card.Body>
      </Card>
    )
  }

  const renderTooltip = (text) => (props) => <Tooltip {...props}>{text}</Tooltip>

  const StreamingUI = ({ reasoningRef, jsonRef }) => (
    <>
      {currentReasoning && (
        <div className="mb-4">
          <h4 className={`fw-bold ${currentReasoning && !partialJson ? 'reasoning-text-animated' : ''}`}>
            {reasoningDescr}
          </h4>
          <pre
            ref={reasoningRef}
            className="bg-light p-3 rounded border text-start"
            style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', textAlign: 'left' }}>
            {currentReasoning && !partialJson && <Spinner animation="grow" size="sm" className="me-2" />}
            {currentReasoning}
          </pre>
        </div>
      )}

      {isProcessing && partialJson && (
        <div className="mb-4">
          <h4 className={`fw-bold ${partialJson ? 'reasoning-text-animated' : ''}`}>
            {processingDescr}
          </h4>
          <pre
            ref={jsonRef}
            className="bg-dark text-white p-3 rounded text-start"
            style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', textAlign: 'left' }}>
            <Spinner animation="grow" variant="light" size="sm" className="me-2" />
            {partialJson}
          </pre>
        </div>
      )}
    </>
  )

  return (
    <div className="recoveryAI container py-5">
      <h3 className="managementTitle mb-4 fw-bold">Recovery AI</h3>

      <p className="text-muted mb-5 text-start">
        <strong>Recovery AI</strong> is a cybersecurity assistant powered by a
        fine-tuned large language model (LLM) with 14 billion parameters. It is
        designed to help analysts respond to cyber incidents by generating
        actionable recovery plans. To use the tool, provide a brief description
        of your system and paste in relevant network logs. Then click the
        <strong> "Generate Recovery Plan"</strong> button to receive a detailed
        recovery plan based on the provided data.
        <OverlayTrigger placement="top" delay={{ show: 0, hide: 0 }}
                        overlay={renderTooltip('More information about Recovery AI')}>
          <Button variant="button" onClick={() => setShowInfoModal(true)}>
            <i className="fa fa-info-circle infoButton" aria-hidden="true" />
          </Button>
        </OverlayTrigger>
        <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)} />
      </p>

      <InputGroup className="mb-3">
        <InputGroup.Text><i className="fa fa-cogs faSymbolLabel" aria-hidden="true" /><span className="ms-2">System Description</span></InputGroup.Text>
        <FormControl as="textarea" rows={10} placeholder="Enter system description here" value={systemDescription}
                     onChange={handleSystemDescriptionChange} readOnly={isProcessing} />
      </InputGroup>

      <InputGroup className="mb-4">
        <InputGroup.Text><i className="fa fa-file-text faSymbolLabel" aria-hidden="true" /><span className="ms-2">Network Logs</span></InputGroup.Text>
        <FormControl as="textarea" rows={10} placeholder="Paste network logs here" value={networkLogs}
                     onChange={handleNetworkLogsChange} readOnly={isProcessing} />
      </InputGroup>

      <InputGroup className="mb-4">
        <InputGroup.Text className="d-flex align-items-center">
          <label htmlFor="rag-checkbox" className="me-2 mb-0">RAG</label>
          <Form.Check
            type="checkbox"
            checked={rag}
            onChange={(e) => setRag(e.target.checked)}
            disabled={isProcessing}
            id="rag-checkbox"
          />
        </InputGroup.Text>
        <InputGroup.Text id="opt-steps-label">Optimization steps</InputGroup.Text>
        <FormControl
          type="number"
          aria-describedby="opt-steps-label"
          value={optimizationSteps}
          onChange={(e) => setOptimizationSteps(parseInt(e.target.value, 10) || 0)}
          disabled={isProcessing}
        />
        <InputGroup.Text id="lookahead-label">Lookahead horizon</InputGroup.Text>
        <FormControl
          type="number"
          aria-describedby="lookahead-label"
          value={lookaheadHorizon}
          onChange={(e) => setLookaheadHorizon(parseInt(e.target.value, 10) || 0)}
          disabled={isProcessing}
        />
        <InputGroup.Text id="rollout-label">Rollout horizon</InputGroup.Text>
        <FormControl
          type="number"
          aria-describedby="rollout-label"
          value={rolloutHorizon}
          onChange={(e) => setRolloutHorizon(parseInt(e.target.value, 10) || 0)}
          disabled={isProcessing}
        />
        <InputGroup.Text id="temp-label">Temperature</InputGroup.Text>
        <FormControl
          type="number"
          step="0.1"
          aria-describedby="temp-label"
          value={temperature}
          onChange={(e) => setTemperature(parseFloat(e.target.value) || 0)}
          disabled={isProcessing}
        />
      </InputGroup>

      <div className="d-flex justify-content-center mb-5">
        <OverlayTrigger placement="top" overlay={renderTooltip('Ask Recovery AI to generate a recovery plan.')}>
          <Button variant="primary" size="md" onClick={handleGeneratePlan}
                  disabled={isProcessing || !systemDescription || !networkLogs} className="buttonMarginRight">
            {isProcessing ? <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true"
                                     className="me-2 spinnerMarginRight" /> :
              <i className="fa fa-magic me-2 faSymbolLabel" />}
            {isProcessing ? 'Generating...' : 'Generate Recovery Plan'}
          </Button>
        </OverlayTrigger>
        <OverlayTrigger placement="top" overlay={renderTooltip('Load an example system description and logs.')}>
          <Button variant="outline-info" size="md" onClick={handleFetchExample}
                  disabled={loadingExample || isProcessing} className="ms-3 buttonMarginRight">
            {loadingExample ? <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true"
                                       className="me-2 spinnerMarginRight" /> :
              <i className="fa fa-lightbulb-o me-2 faSymbolLabel" />}
            Example
          </Button>
        </OverlayTrigger>
        <OverlayTrigger placement="top" overlay={renderTooltip('Reset all fields and the generated plan.')}>
          <Button variant="outline-secondary" size="md" className="ms-3" onClick={() => resetAll(false)}>Reset</Button>
        </OverlayTrigger>
      </div>

      {!incidentClassification && <StreamingUI reasoningRef={reasoningPreRef} jsonRef={jsonPreRef} />}

      {incidentClassification && (
        <Card className="shadow-lg border-0 mb-4">
          <Card.Header
            className="bg-primary text-white text-center py-3 d-flex justify-content-between align-items-center">
            <h3 className="mb-0 fw-bold">Incident Report</h3>
            {!isProcessing && (
              <Button variant="light" size="sm" onClick={handleDownloadIncidentReport}>
                <i className="fa fa-download me-2 spinnerMarginRight" />
                Download report (JSON)
              </Button>
            )}
          </Card.Header>
          <Card.Body className="p-4">
            <p><strong>Incident detected:</strong> {incidentClassification.Incident}</p>
            <p><strong>Description:</strong> {incidentClassification['Incident description']}</p>
            {incidentClassification.Entities && (
              <div className="row g-3 mb-3">
                {incidentClassification.Entities.Attacker && incidentClassification.Entities.Attacker.length > 0 && (
                  <div key="attacker" className="col-md-4">
                    <Card className="h-100">
                      <Card.Header className="fw-bold">IPs and hostnames of the attacker</Card.Header>
                      <Card.Body><BulletList items={incidentClassification.Entities.Attacker} /></Card.Body>
                    </Card>
                  </div>
                )}
                {incidentClassification.Entities.System && incidentClassification.Entities.System.length > 0 && (
                  <div key="system" className="col-md-4">
                    <Card className="h-100">
                      <Card.Header className="fw-bold">System components</Card.Header>
                      <Card.Body><BulletList items={incidentClassification.Entities.System} /></Card.Body>
                    </Card>
                  </div>
                )}
                {incidentClassification.Entities.Targeted && incidentClassification.Entities.Targeted.length > 0 && (
                  <div key="targeted" className="col-md-4">
                    <Card className="h-100">
                      <Card.Header className="fw-bold">Components targeted by the attack</Card.Header>
                      <Card.Body><BulletList items={incidentClassification.Entities.Targeted} /></Card.Body>
                    </Card>
                  </div>
                )}
              </div>
            )}
            <div className="row g-3">
              {incidentClassification['MITRE ATT&CK Tactics'] && incidentClassification['MITRE ATT&CK Tactics'].length > 0 && (
                <div className="col-md-6">
                  <Card>
                    <Card.Header className="fw-bold">MITRE ATT&CK Tactics</Card.Header>
                    <Card.Body><BulletList items={incidentClassification['MITRE ATT&CK Tactics']} /></Card.Body>
                  </Card>
                </div>
              )}
              {incidentClassification['MITRE ATT&CK Techniques'] && incidentClassification['MITRE ATT&CK Techniques'].length > 0 && (
                <div className="col-md-6">
                  <Card>
                    <Card.Header className="fw-bold">MITRE ATT&CK Techniques</Card.Header>
                    <Card.Body><BulletList items={incidentClassification['MITRE ATT&CK Techniques']} /></Card.Body>
                  </Card>
                </div>
              )}
            </div>
          </Card.Body>
        </Card>
      )}

      {noIncidentFound && (
        <Card border="danger" className="text-center shadow-sm mt-4">
          <Card.Header className="bg-danger text-white fw-bold">Recovery complete.</Card.Header>
          <Card.Body className="text-danger">
            <Card.Text>
              No recovery plan is needed since the logs do not indicate an incident.
            </Card.Text>
          </Card.Body>
        </Card>
      )}

      {incidentClassification && isProcessing && (
        <RecoveryProgress systemState={systemState} recoveryActions={recoveryActions} />
      )}

      <div>
        {incidentClassification && <StreamingUI reasoningRef={reasoningPreRef} jsonRef={jsonPreRef} />}
      </div>

      {(recoveryActions.length > 0 || systemState) && (
        <Card className="shadow-lg border-0 mb-4">
          <Card.Header
            className="bg-primary text-white text-center py-3 d-flex justify-content-between align-items-center">
            <h3 className="mb-0 fw-bold"><strong>Recovery Plan</strong></h3>
            {!isProcessing && (recoveryActions.length > 0 || systemState) && (
              <Button variant="light" size="sm" onClick={handleDownloadRecoveryPlan}>
                <i className="fa fa-download me-2 spinnerMarginRight" />
                Download plan (JSON)
              </Button>
            )}
          </Card.Header>
          <Card.Body className="p-4">
            <div className="row g-4">
              <div className="col-lg-8">
                {recoveryActions.length > 0 && (
                  <Card>
                    <Card.Header as="h6" className="text-center fw-bold">Recovery Actions</Card.Header>
                    <Card.Body>
                      {recoveryActions.map((action, index) => (
                        <div key={index} className="mb-3 p-3 border rounded bg-light">
                          <p><strong>Action {index + 1}</strong>: {action.Action}</p>
                          <p className="mb-0"><strong>Motivation: </strong>{action.Explanation}</p>
                        </div>
                      ))}
                    </Card.Body>
                  </Card>
                )}
              </div>
              <div className="col-lg-4">
                <StateVisualizer state={systemState} />
              </div>
            </div>
          </Card.Body>
        </Card>
      )}
    </div>
  )
}

export default RecoveryAI