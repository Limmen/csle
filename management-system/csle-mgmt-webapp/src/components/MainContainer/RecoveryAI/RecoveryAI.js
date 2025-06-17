import React, { useState, useRef, useEffect } from 'react'
import {
  InputGroup,
  FormControl,
  Button,
  Form,
  Card,
  Spinner
} from 'react-bootstrap'
import './RecoveryAI.css'
import 'react-confirm-alert/src/react-confirm-alert.css'
import serverIp from '../../Common/serverIp'
import serverPort from '../../Common/serverPort'
import { useNavigate } from 'react-router-dom'
import { useAlert } from 'react-alert'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import Tooltip from 'react-bootstrap/Tooltip'
import Modal from 'react-bootstrap/Modal'
import RecoveryAIPic from './RecoveryAI.png'
import {
  HTTP_PREFIX,
  LOGIN_PAGE_RESOURCE,
  TOKEN_QUERY_PARAM,
  HTTP_REST_POST,
  RECOVERY_AI_RESOURCE,
  RECOVERY_AI_EXAMPLE_RESOURCE,
  RECOVERY_AI_INCIDENT_DESCRIPTION_FIELD,
  RECOVERY_AI_INCIDENT_FIELD,
  RECOVERY_AI_ACTION_EXPLANATIONS_FIELD,
  RECOVERY_AI_MITRE_ATTACK_TECHNIQUES_FIELD,
  RECOVERY_AI_MITRE_ATTACK_TACTICS_FIELD,
  RECOVERY_AI_RECOVERY_ACTIONS_FIELD
} from '../../Common/constants'

const FIELDS = [
  RECOVERY_AI_INCIDENT_FIELD,
  RECOVERY_AI_INCIDENT_DESCRIPTION_FIELD,
  RECOVERY_AI_MITRE_ATTACK_TACTICS_FIELD,
  RECOVERY_AI_MITRE_ATTACK_TECHNIQUES_FIELD,
  RECOVERY_AI_RECOVERY_ACTIONS_FIELD,
  RECOVERY_AI_ACTION_EXPLANATIONS_FIELD
]

const initialPlan = {
  incident: false,
  incidentDescription: '',
  mitreTactics: [],
  mitreTechniques: [],
  recoveryActions: [],
  actionExplanations: []
}

const RecoveryAI = (props) => {
  const [systemDescription, setSystemDescription] = useState('')
  const [networkLogs, setNetworkLogs] = useState('')
  const [reasoning, setReasoning] = useState('')
  const [waitingforUserInput, setWaitingForUserInput] = useState(true)
  const [generatingAnalysis, setGeneratingAnalysis] = useState(false)
  const [loadingAnalysis, setLoadingAnalysis] = useState(false)
  const [loadingPlan, setLoadingPlan] = useState(false)
  const [planProgress, setPlanProgress] = useState(0)
  const [recoveryPlan, setRecoveryPlan] = useState(initialPlan)
  const [showInfoModal, setShowInfoModal] = useState(false)
  const [loadingExample, setLoadingExample] = useState(false)
  const [partialJson, setPartialJson] = useState('')
  const ip = serverIp
  const port = serverPort
  const setSessionData = props.setSessionData
  const alert = useAlert()
  const navigate = useNavigate()
  const abortRef = useRef(null)
  const capturedRef = useRef(new Set())
  const stepBufferRef = useRef(null);

  const abortCurrentStream = () => {
    if (abortRef.current) {
      abortRef.current.abort()
      abortRef.current = null
    }
    setLoadingAnalysis(false)
    setLoadingPlan(false)
  }

  const resetAll = () => {
    abortCurrentStream()
    setSystemDescription('')
    setNetworkLogs('')
    setReasoning('')
    setWaitingForUserInput(true)
    setGeneratingAnalysis(false)
    setRecoveryPlan(initialPlan)
    setPlanProgress(0)
    setPartialJson('')
    capturedRef.current = new Set()
  }

  const handleDownloadPlan = () => {
    const dataStr =
      'data:text/json;charset=utf-8,' +
      encodeURIComponent(JSON.stringify(recoveryPlan, null, 2))
    const dl = document.createElement('a')
    dl.setAttribute('href', dataStr)
    dl.setAttribute('download', 'recovery_plan.json')
    document.body.appendChild(dl)
    dl.click()
    dl.remove()
  }

  const handleSystemDescriptionChange = (e) => setSystemDescription(e.target.value)
  const handleNetworkLogsChange = (e) => setNetworkLogs(e.target.value)

  const handleFetchExample = () => {
    const token = props.sessionData?.token || sessionStorage.getItem('token')
    if (!token) {
      alert.show('Session token expired. Please login again.')
      navigate(`/${LOGIN_PAGE_RESOURCE}`)
      return
    }
    const url = `/${RECOVERY_AI_RESOURCE}/${RECOVERY_AI_EXAMPLE_RESOURCE}?${TOKEN_QUERY_PARAM}=${token}`
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
        setWaitingForUserInput(true)
      })
      .catch(() => {
        alert.error('Unable to connect to the Recovery AI service')
      })
      .finally(() => setLoadingExample(false))
  }

  const handleGeneratePlan = () => {
    setWaitingForUserInput(false)
    setReasoning('')
    setRecoveryPlan(initialPlan)
    setLoadingPlan(false)
    setGeneratingAnalysis(false)
    setPlanProgress(0)
    setPartialJson('')
    capturedRef.current = new Set()
    abortCurrentStream()
    setLoadingAnalysis(true)

    const token = props.sessionData?.token || sessionStorage.getItem('token')
    if (!token) {
      alert.show('Session token expired. Please login again.')
      navigate(`/${LOGIN_PAGE_RESOURCE}`)
      return
    }

    const url = `/${RECOVERY_AI_RESOURCE}?${TOKEN_QUERY_PARAM}=${token}`
    const controller = new AbortController()
    abortRef.current = controller

    fetch(url, {
      method: HTTP_REST_POST,
      headers: {
        'Content-Type': 'application/json',
        Accept: 'text/event-stream'
      },
      body: JSON.stringify({ systemDescription, networkLogs }),
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
          return null
        }
        return res.body
      })
      .then((body) => {
        if (body === null) return

        const reader = body.getReader()
        const decoder = new TextDecoder('utf-8')
        let buffer = ''
        const lastTokens = []

        let capturingJson = false
        let jsonTokens = []

        const pump = () =>
          reader.read().then(({ value, done }) => {
            if (done) return

            buffer += decoder.decode(value, { stream: true })

            let nl
            while ((nl = buffer.indexOf('\n')) >= 0) {
              const rawLine = buffer.slice(0, nl).trim()
              buffer = buffer.slice(nl + 1)

              if (!rawLine.startsWith('data:')) continue
              const token = rawLine.slice(5).trim()

              if (!capturingJson) {
                setLoadingAnalysis(false)
                setGeneratingAnalysis(true)
                if (token === '</think>') {
                  capturingJson = true
                  setLoadingPlan(true)
                  lastTokens.length = 0
                  continue
                }
                setReasoning((prev) => {
                  const cleanToken = token.replace(/\\n/g, '\n');

                  if (stepBufferRef.current) {
                    if (/^\d+[:.]?$/.test(cleanToken)) {
                      const stepToken = `\n\n${stepBufferRef.current}`;
                      stepBufferRef.current = null;
                      return prev ? `${prev} ${stepToken} ${cleanToken}` : `${stepToken} ${cleanToken}`;
                    } else {
                      const stepToken = stepBufferRef.current;
                      stepBufferRef.current = null;
                      return prev ? `${prev} ${stepToken} ${cleanToken}` : `${stepToken} ${cleanToken}`;
                    }
                  }

                  if (cleanToken === 'Step') {
                    stepBufferRef.current = cleanToken;
                    return prev || '';
                  }

                  return prev ? `${prev} ${cleanToken}` : cleanToken;
                });

                continue
              }
              setGeneratingAnalysis(false)

              lastTokens.push(token)
              if (lastTokens.length > 3) lastTokens.shift()
              const merged = lastTokens.join(' ').trim()

              FIELDS.forEach((f) => {
                if (!capturedRef.current.has(f) && (token.includes(f) || merged.includes(f))) {
                  capturedRef.current.add(f)
                  setPlanProgress(capturedRef.current.size)
                }
              })

              jsonTokens.push(token)
              setPartialJson(jsonTokens.join(' '))
              if (!token.endsWith('}')) continue
              const jsonStr = jsonTokens.join(' ')
              try {
                const obj = JSON.parse(jsonStr)
                setRecoveryPlan({
                  incident: obj[RECOVERY_AI_INCIDENT_FIELD] || '',
                  incidentDescription: obj[RECOVERY_AI_INCIDENT_DESCRIPTION_FIELD] || '',
                  mitreTactics: obj[RECOVERY_AI_MITRE_ATTACK_TACTICS_FIELD] || [],
                  mitreTechniques: obj[RECOVERY_AI_MITRE_ATTACK_TECHNIQUES_FIELD] || [],
                  recoveryActions: obj[RECOVERY_AI_RECOVERY_ACTIONS_FIELD] || [],
                  actionExplanations: obj[RECOVERY_AI_ACTION_EXPLANATIONS_FIELD] || []
                })
              } catch (e) {
                console.log(jsonStr)
                alert.error('Failed to parse recovery plan')
              } finally {
                setLoadingPlan(false)
                abortCurrentStream()
              }
            }
            return pump()
          })

        pump().catch((err) => {
          if (err.name !== 'AbortError') {
            alert.error('Connection to Recovery AI lost')
          }
        })
      })
      .catch((error) => {
        if (error.name !== 'AbortError') {
          alert.error('Unable to connect to Recovery AI service')
        }
      })
  }

  useEffect(() => () => abortCurrentStream(), [])

  const BulletList = ({ items }) => (
    <ul
      className="mb-0 ps-3"
      style={{
        listStyleType: 'disc',
        listStylePosition: 'outside',
        paddingLeft: '1.25rem',
        margin: 0,
        textAlign: 'left'
      }}
    >
      {items.map((it, idx) => (
        <li key={idx} style={{ textAlign: 'left' }}>
          {it}
        </li>
      ))}
    </ul>
  )

  const NumberedList = ({ items }) => (
    <ol
      className="mb-0 ps-3"
      style={{
        listStyleType: 'decimal',
        listStylePosition: 'outside',
        paddingLeft: '1.25rem',
        margin: 0,
        textAlign: 'left'
      }}
    >
      {items.map((it, idx) => (
        <li key={idx} style={{ textAlign: 'left' }}>
          {it}
        </li>
      ))}
    </ol>
  )

  const info = () => {
    setShowInfoModal(true)
  }

  const renderInfoTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
      More information about Recovery AI
    </Tooltip>
  )

  const renderResetTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
      Remove the recovery plan and reset the system/log description.
    </Tooltip>
  )

  const renderGenerateTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
      Ask Recovery AI to generate a recovery plan based on the provided information.
    </Tooltip>
  )

  const renderDownloadTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
      Download the recovery plan in JSON format.
    </Tooltip>
  )

  const renderExampleTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
      Load an example system description and network logs.
    </Tooltip>
  )

  const InfoModal = (props) => {
    return (
      <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
            Recovery AI
          </Modal.Title>
        </Modal.Header>
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
          <div className="text-center">
            <img src={RecoveryAIPic} alt="Recovery AI" className="img-fluid" />
          </div>
        </Modal.Body>
        <Modal.Footer className="modalFooter">
          <Button onClick={props.onHide} size="sm">Close</Button>
        </Modal.Footer>
      </Modal>
    )
  }

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
        <OverlayTrigger
          placement="top"
          delay={{ show: 0, hide: 0 }}
          overlay={renderInfoTooltip}
        >
          <Button variant="button" onClick={info}>
            <i className="fa fa-info-circle infoButton" aria-hidden="true" />
          </Button>
        </OverlayTrigger>
        <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)} />
      </p>

      <InputGroup className="mb-3">
        <InputGroup.Text id="systemDescriptionLabel">
          <span className="d-flex align-items-center">
            <i className="fa fa-cogs faSymbolLabel" aria-hidden="true" />
            <span className="ms-2">System Description</span>
          </span>
        </InputGroup.Text>
        <FormControl
          as="textarea"
          rows={10}
          placeholder="Enter system description here"
          aria-label="System Description"
          aria-describedby="systemDescriptionLabel"
          value={systemDescription}
          onChange={handleSystemDescriptionChange}
        />
      </InputGroup>

      <InputGroup className="mb-4">
        <InputGroup.Text id="networkLogsLabel">
          <span className="d-flex align-items-center">
            <i className="fa fa-file-text faSymbolLabel" aria-hidden="true" />
            <span className="ms-2">Network Logs</span>
          </span>
        </InputGroup.Text>
        <FormControl
          as="textarea"
          rows={10}
          placeholder="Paste network logs here"
          aria-label="Network Logs"
          aria-describedby="networkLogsLabel"
          value={networkLogs}
          onChange={handleNetworkLogsChange}
        />
      </InputGroup>

      <div className="d-flex justify-content-center mb-5">
        <OverlayTrigger
          placement="top"
          delay={{ show: 0, hide: 0 }}
          overlay={renderGenerateTooltip}
        >
          <Button variant="primary" size="md" onClick={handleGeneratePlan}>
            {loadingAnalysis || generatingAnalysis || loadingPlan ? (
              <Spinner animation="border" size="sm" className="me-2 generateSpinner" />
            ) : (
              <i className="fa fa-magic me-2 faSymbolLabel" aria-hidden="true" />
            )}
            Generate Recovery Plan
          </Button>
        </OverlayTrigger>
        <OverlayTrigger
          placement="top"
          delay={{ show: 0, hide: 0 }}
          overlay={renderExampleTooltip}
        >
          <Button variant="outline-info" size="md" disabled={loadingExample} className="me-3 resetButton"
                  onClick={handleFetchExample}>
            {loadingExample ? (
              <Spinner animation="border" size="sm" className="me-2 exampleSpinner" />
            ) : (
              <i className="fa fa-lightbulb-o me-2 faSymbolLabel" aria-hidden="true" />
            )}
            Example
          </Button>
        </OverlayTrigger>
        <OverlayTrigger
          placement="top"
          delay={{ show: 0, hide: 0 }}
          overlay={renderResetTooltip}
        >
          <Button variant="outline-secondary" size="md" className="ms-3 resetButton" onClick={resetAll}>
            Reset
          </Button>
        </OverlayTrigger>
      </div>

      {!waitingforUserInput && loadingAnalysis && (
        <div className="d-flex justify-content-center align-items-center mb-5">
          <Spinner animation="border" role="status" className="me-3" />
          <span className="fs-5 analysisSpinner">Contacting the server...</span>
        </div>
      )}

      {!waitingforUserInput && !loadingAnalysis && (
        <div className="mb-4 reasoning">
          <h3 className="managementTitleNoUnderline mb-3 fw-bold">
            Analysis of the provided information
          </h3>
          <pre
            className="bg-light p-3 rounded border reasoningTitle"
            style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}
          >
            {reasoning}
          </pre>
        </div>
      )}

      {!waitingforUserInput && loadingPlan && (
        <div className="d-flex flex-column justify-content-center align-items-center mb-5">
          <div className="d-flex align-items-center mb-2">
            <Spinner animation="border" role="status" className="me-3" />
            <span className="fs-5 analysisSpinner">
              Analysis complete, generating recovery plan... (Progress: {planProgress}/6)
            </span>
          </div>
          <pre
            className="text-muted small mb-0"
            style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}
          >
            {partialJson}
          </pre>
        </div>
      )}

      {!waitingforUserInput && !loadingAnalysis && !generatingAnalysis && !loadingPlan && (
        <Card className="shadow-lg border-0">
          <Card.Header className="bg-white text-center py-5 border-0">
            <div
              className="mx-auto mb-3 d-flex align-items-center justify-content-center rounded-circle bg-primary text-white shieldIcon"
              style={{ width: 72, height: 72 }}>
              <i className="fa fa-shield fa-2x" aria-hidden="true" />
            </div>
            <div className="d-flex align-items-center justify-content-center">
              <h3 className="managementTitleNoUnderline mb-0 fw-bold">Recovery Plan</h3>
              <OverlayTrigger
                placement="top"
                delay={{ show: 0, hide: 0 }}
                overlay={renderDownloadTooltip}
              >
                <Button variant="outline-primary" size="sm" className="ms-3 border-0 shadow-none"
                        onClick={handleDownloadPlan}>
                  <i className="fa fa-download" aria-hidden="true" />
                </Button>
              </OverlayTrigger>
            </div>
          </Card.Header>

          <Card.Body className="p-4 planCard">
            <div className="border rounded mb-5 p-4 bg-light">
              <h3 className="text-uppercase fw-bold text-center fs-4 mb-4 border-bottom pb-3 incTitle">
                Incident Classification
              </h3>

              <div className="row align-items-center gx-2 gy-3 mb-4">
                <div className="col-auto text-muted incidentDescription">
                  Incident: {recoveryPlan.incident}. Description: {recoveryPlan.incidentDescription}
                </div>
              </div>

              {(recoveryPlan.mitreTactics.length > 0 || recoveryPlan.mitreTechniques.length > 0) && (
                <div className="row g-4">
                  {recoveryPlan.mitreTactics.length > 0 && (
                    <div className="col-md-6">
                      <Card className="h-100 shadow-sm">
                        <Card.Body className="p-3">
                          <h6 className="fw-bold text-center mb-3 incDetected">
                            MITRE ATT&CK Tactics
                          </h6>
                          <BulletList items={recoveryPlan.mitreTactics} />
                        </Card.Body>
                      </Card>
                    </div>
                  )}
                  {recoveryPlan.mitreTechniques.length > 0 && (
                    <div className="col-md-6">
                      <Card className="h-100 shadow-sm">
                        <Card.Body className="p-3">
                          <h6 className="fw-bold text-center mb-3 incDetected">
                            MITRE ATT&CK Techniques
                          </h6>
                          <BulletList items={recoveryPlan.mitreTechniques} />
                        </Card.Body>
                      </Card>
                    </div>
                  )}
                </div>
              )}
            </div>
            {(recoveryPlan.recoveryActions.length > 0 || recoveryPlan.actionExplanations.length > 0) && (
              <div className="border rounded p-4 bg-light incResponse">
                <h3 className="text-uppercase fw-bold text-center fs-4 mb-4 border-bottom pb-3 incTitle">
                  Incident Response
                </h3>

                <div className="row g-4">
                  {recoveryPlan.recoveryActions.length > 0 && (
                    <div className="col-md-6">
                      <Card className="h-100 shadow-sm">
                        <Card.Body className="p-3">
                          <h6 className="fw-bold text-center mb-3 incDetected">
                            Recovery Actions
                          </h6>
                          <NumberedList items={recoveryPlan.recoveryActions} />
                        </Card.Body>
                      </Card>
                    </div>
                  )}
                  {recoveryPlan.actionExplanations.length > 0 && (
                    <div className="col-md-6">
                      <Card className="h-100 shadow-sm">
                        <Card.Body className="p-3">
                          <h6 className="fw-bold text-center mb-3 incDetected">
                            Action Explanations
                          </h6>
                          <NumberedList items={recoveryPlan.actionExplanations} />
                        </Card.Body>
                      </Card>
                    </div>
                  )}
                </div>
              </div>
            )}
          </Card.Body>
        </Card>
      )}
    </div>
  )
}

RecoveryAI.propTypes = {}
RecoveryAI.defaultProps = {}
export default RecoveryAI
