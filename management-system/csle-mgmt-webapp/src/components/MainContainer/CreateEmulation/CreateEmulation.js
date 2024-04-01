import React, {useState} from 'react';
import './CreateEmulation.css';
import Card from 'react-bootstrap/Card';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import Spinner from 'react-bootstrap/Spinner'
import Accordion from 'react-bootstrap/Accordion';
import Collapse from 'react-bootstrap/Collapse'

/**
 * Component representing the /create-emulation-page
 */
const CreateEmulation = (props) => {

  const [generalInfoOpen, setGeneralInfoOpen] = useState(false);
  const [description, setDescription] = useState({
    description: ''
  });

  const handleDescriptionChange = (event) => {
    setDescription({
      description: event.target.value
    });
    // console.log(description.description)
  };


  return (
        <div className="CreateEmulation">
          <h3 className="managementTitle"> Create Emulation </h3>
          <Accordion defaultActiveKey="0">
            <Card className="subCard">
              <Card.Header>
                <Button
                  onClick={() => setGeneralInfoOpen(!generalInfoOpen)}
                  aria-controls="generalInfoBody"
                  aria-expanded={generalInfoOpen}
                  variant="link"
                >
                  <h5 className="semiTitle">
                    General information about the emulation
                    <i className="fa fa-file-text headerIcon" aria-hidden="true"></i>
                  </h5>
                </Button>
              </Card.Header>
              <Collapse in={generalInfoOpen}>
                <div id="generalInfoBody" className="cardBodyHidden">
                  <div className="table-responsive">
                    <Table striped bordered hover>
                      <thead>
                      <tr>
                        <th>Attribute</th>
                        <th> Value</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr>
                        <td>Description</td>
                        <td>
                          <textarea
                            id="description"
                            value={description.textareaValue}
                            onChange={handleDescriptionChange}
                            rows="4"
                            style={{ width: '100%', boxSizing: 'border-box' }}
                          />
                        </td>
                      </tr>
                      {/*<tr>*/}
                      {/*  <td>Status</td>*/}
                      {/*  <td>{getStatus(emulation)} <SpinnerOrStatus emulation={emulation}/></td>*/}
                      {/*</tr>*/}
                      {/*<tr>*/}
                      {/*  <td>Emulation name</td>*/}
                      {/*  <td>{emulation.name}</td>*/}
                      {/*</tr>*/}
                      {/*<tr>*/}
                      {/*  <td>Subnets</td>*/}
                      {/*  <td>{getSubnetMasks(emulation)}</td>*/}
                      {/*</tr>*/}
                      {/*<tr>*/}
                      {/*  <td>Network names</td>*/}
                      {/*  <td>{getNetworkNames(emulation)}</td>*/}
                      {/*</tr>*/}
                      {/*<tr>*/}
                      {/*  <td># Containers</td>*/}
                      {/*  <td>{emulation.containers_config.containers.length}</td>*/}
                      {/*</tr>*/}
                      {/*<tr>*/}
                      {/*  <td>csle-collector version</td>*/}
                      {/*  <td>{emulation.csle_collector_version}</td>*/}
                      {/*</tr>*/}
                      {/*<tr>*/}
                      {/*  <td>csle-ryu*/}
                      {/*    version*/}
                      {/*  </td>*/}
                      {/*  <td>{emulation.csle_ryu_version}</td>*/}
                      {/*</tr>*/}
                      {/*<tr>*/}
                      {/*  <td>Configuration</td>*/}
                      {/*  <td>*/}
                      {/*    <Button variant="link" className="dataDownloadLink"*/}
                      {/*            onClick={() => fileDownload(JSON.stringify(emulation), "config.json")}>*/}
                      {/*      config.json*/}
                      {/*    </Button>*/}
                      {/*  </td>*/}
                      {/*</tr>*/}
                      </tbody>
                    </Table>
                  </div>
                </div>
              </Collapse>
            </Card>
          </Accordion>

        </div>
    );
}

CreateEmulation.propTypes = {};
CreateEmulation.defaultProps = {};
export default CreateEmulation;
