import React, { useState } from 'react'
import {
  InputGroup,
  FormControl,
  Button,
  Form,
  Card
} from 'react-bootstrap'
import './RecoveryAI.css'
import 'react-confirm-alert/src/react-confirm-alert.css'

/**
 * Component representing /recovery-ai-page
 */
const RecoveryAI = () => {
  const [systemDescription, setSystemDescription] = useState('')
  const [networkLogs, setNetworkLogs] = useState('')
  const [reasoning, setReasoning] = useState('')
  const [recoveryPlan, setRecoveryPlan] = useState({
    incident: false,
    incidentDescription: '',
    mitreTactics: [],
    mitreTechniques: [],
    recoveryActions: [],
    actionExplanations: []
  })

  const handleSystemDescriptionChange = (e) => setSystemDescription(e.target.value)
  const handleNetworkLogsChange = (e) => setNetworkLogs(e.target.value)

  const handleGeneratePlan = () => {
    // Simulate reasoning and output — replace with actual LLM call
    setReasoning(
      'Analyzing network logs...\nDetecting patterns of compromise...\nMapping to MITRE ATT&CK...'
    )

    setRecoveryPlan({
      incident: true,
      incidentDescription:
        'Detected lateral movement via SMB and credential dumping behavior.',
      mitreTactics: ['Lateral Movement', 'Credential Access'],
      mitreTechniques: [
        'T1021.002 - SMB/Windows Admin Shares',
        'T1003 - OS Credential Dumping'
      ],
      recoveryActions: [
        'Isolate affected hosts (10.0.0.12, 10.0.0.15)',
        'Reset domain admin credentials',
        'Apply security patches to file servers',
        'Audit login activity across domain controllers'
      ],
      actionExplanations: [
        'Isolation prevents further propagation.',
        'Compromised credentials may have been reused.',
        'File server exploits likely contributed to lateral movement.',
        'Reviewing login history can reveal affected user accounts.'
      ]
    })
  }

  const BulletList = ({ items }) => (
    <ul
      className="mb-0 ps-3"
      style={{
        listStyleType: 'disc',
        listStylePosition: 'outside',
        paddingLeft: '1.25rem',
        margin: 0,
        textAlign: 'left',
      }}
    >
      {items.map((it) => (
        <li key={it} style={{ textAlign: 'left' }}>
          {it}
        </li>
      ))}
    </ul>
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
      </p>

      <InputGroup className="mb-3">
        <InputGroup.Text id="systemDescriptionLabel">
          <span className="d-flex align-items-center">
            <i className="fa fa-cogs faSymbolLabel" aria-hidden="true" />
            <span className="ms-2">System Description</span>
          </span>
        </InputGroup.Text>
        <FormControl
          placeholder="Enter system description"
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
        <Button variant="primary" size="md" onClick={handleGeneratePlan}>
          <i className="fa fa-magic me-2 faSymbolLabel" aria-hidden="true" />
          Generate Recovery Plan
        </Button>
      </div>

      {reasoning && (
        <div className="mb-5 reasoning">
          <h3 className="managementTitleNoUnderline mb-4 fw-bold">Model Reasoning</h3>
          <pre className="bg-light p-3 rounded border reasoningTitle">{reasoning}</pre>
        </div>
      )}

      {recoveryPlan.incidentDescription && (
        <Card className="shadow-lg border-0">
          <Card.Header className="bg-white text-center py-5 border-0">
            <div
              className="mx-auto mb-3 d-flex align-items-center justify-content-center rounded-circle bg-primary text-white shieldIcon"
              style={{ width: 72, height: 72 }}
            >
              <i className="fa fa-shield fa-2x" aria-hidden="true" />
            </div>
            <h3 className="managementTitleNoUnderline mb-4 fw-bold">Recovery Plan</h3>
          </Card.Header>

          <Card.Body className="p-4 planCard">
            <div className="border rounded mb-5 p-4 bg-light">
              <h3 className="text-uppercase fw-bold text-center fs-4 mb-4 border-bottom pb-3 incTitle">
                Incident Classification
              </h3>

              <div className="row align-items-center gx-2 gy-3 mb-4">
                <div className="col-auto fw-bold incDetected">Incident:</div>
                <div className="col-auto d-flex incidentCheckbox">
                  <Form.Check
                    type="checkbox"
                    checked={recoveryPlan.incident}
                    readOnly
                    disabled
                  />
                </div>
                <div className="col-auto text-muted incidentDescription">
                  {recoveryPlan.incidentDescription}
                </div>
              </div>

              <div className="row g-4">
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
              </div>
            </div>

            <div className="border rounded p-4 bg-light incResponse">
              <h3 className="text-uppercase fw-bold text-center fs-4 mb-4 border-bottom pb-3 incTitle">
                Incident response
              </h3>

              <div className="row g-4">
                <div className="col-md-6">
                  <Card className="h-100 shadow-sm">
                    <Card.Body className="p-3">
                      <h6 className="fw-bold text-center mb-3 incDetected">Recovery Actions</h6>
                      <BulletList items={recoveryPlan.recoveryActions} />
                    </Card.Body>
                  </Card>
                </div>

                <div className="col-md-6">
                  <Card className="h-100 shadow-sm">
                    <Card.Body className="p-3">
                      <h6 className="fw-bold text-center mb-3 incDetected">
                        Action Explanations
                      </h6>
                      <BulletList items={recoveryPlan.actionExplanations} />
                    </Card.Body>
                  </Card>
                </div>
              </div>
            </div>
          </Card.Body>
        </Card>
      )}
    </div>
  )
}

RecoveryAI.propTypes = {}
RecoveryAI.defaultProps = {}
export default RecoveryAI
