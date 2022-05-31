import React, {useState, useEffect, useCallback} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Select from 'react-select'
import ConditionalHistogramDistribution from "./ConditionalHistogramDistribution/ConditionalHistogramDistribution";
import './EmulationStatistics.css';
import DataCollection from './DataCollection.png'
import Collapse from 'react-bootstrap/Collapse'
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'

const EmulationStatistics = () => {
    const [emulationStatistics, setEmulationStatistics] = useState([]);
    const [selectedEmulationStatistic, setSelectedEmulationStatistic] = useState(null);
    const [conditionals, setConditionals] = useState([]);
    const [selectedConditionals, setSelectedConditionals] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [selectedMetric, setSelectedMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    const [animationDuration, setAnimationDuration] = useState(5);
    const animationDurationFactor = 50000
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [deltaCountsOpen, setDeltaCountsOpen] = useState(false);
    const [initialCountsOpen, setInitialCountsOpen] = useState(false);
    const [deltaProbsOpen, setDeltaProbsOpen] = useState(false);
    const [initialProbsOpen, setInitialProbsOpen] = useState(false);
    const [descriptiveStatsOpen, setDescriptiveStatsOpen] = useState(false);

    const ip = "localhost"
    // const ip = "172.31.212.92"

    const resetState = () => {
        setEmulationStatistics([])
        setSelectedEmulationStatistic(null)
        setConditionals([])
        setSelectedConditionals(null)
        setMetrics([])
        setSelectedMetric(null)
    }

    const renderRefreshTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Reload statistics from the backend
        </Tooltip>
    );

    const refresh = () => {
        setLoading(true)
        resetState()
        fetchEmulationStatistics()
    }

    const renderInfoTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            More information about the statistics
        </Tooltip>
    );

    const renderRemoveStatisticTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props} className="toolTipRefresh">
            Remove the selected statistics.
        </Tooltip>
    );

    const InfoModal = (props) => {
        return (
            <Modal
                {...props}
                size="xl"
                aria-labelledby="contained-modal-title-vcenter"
                centered
            >
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Emulation statistics
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h4>Emulation statistics</h4>
                    <p className="modalText">
                        The emulation statistics are collected by measuring log files and other metrics from
                        the emulated infrastructure under different system conditions, e.g. intrusion and no intrsion,
                        high load and low load etc.
                    </p>
                    <div className="text-center">
                        <img src={DataCollection} alt="Data collection from the emulation"/>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={props.onHide}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }

    const updateEmulationStatistic = (stat) => {
        setSelectedEmulationStatistic(stat)
        const conditionalOptions = Object.keys(stat.value.conditionals_counts).map((conditionalName, index) => {
            return {
                value: conditionalName,
                label: conditionalName
            }
        })
        setConditionals(conditionalOptions)
        setSelectedConditionals([conditionalOptions[0]])
        const metricOptions = Object.keys(stat.value.conditionals_counts[
            Object.keys(stat.value.conditionals_counts)[0]]).map((metricName, index) => {
            return {
                value: metricName,
                label: metricName
            }
        })
        setMetrics(metricOptions)
        setSelectedMetric(metricOptions[0])
    }
    const updateSelectedConditionals = (selected) => {
        setSelectedConditionals(selected)
    }

    const updateMetric = (metricName) => {
        setSelectedMetric(metricName)
    }

    const getFirstTwoConditionals = () => {
        if (selectedConditionals.length >= 2) {
            return [selectedConditionals[0], selectedConditionals[1]]
        } else {
            return selectedConditionals
        }
    }

    const getNumSamples = (statistic) => {
        var num_samples = 0
        for (let i = 0; i < Object.keys(statistic.conditionals_counts).length; i++) {
            var metric = Object.keys(statistic.conditionals_counts[Object.keys(statistic.conditionals_counts)[i]])[0]
            for (let j = 0; j < Object.keys(statistic.conditionals_counts[Object.keys(statistic.conditionals_counts)[i]][metric]).length; j++) {
                var value = Object.keys(statistic.conditionals_counts[Object.keys(statistic.conditionals_counts)[i]][metric])[j]
                num_samples = num_samples + statistic.conditionals_counts[Object.keys(statistic.conditionals_counts)[i]][metric][value]
            }
        }
        return num_samples
    }

    const fetchEmulationStatistics = useCallback(() => {
        fetch(
            `http://` + ip + ':7777/emulationstatisticsdata',
            {
                method: "GET",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                const statisticsOptions = response.map((stat, index) => {
                    return {
                        value: stat,
                        label: stat.id + "-" + stat.emulation_name
                    }
                })
                setEmulationStatistics(statisticsOptions)
                setLoading(false)
                if (response.length > 0) {
                    setSelectedEmulationStatistic(statisticsOptions[0])
                    const conditionalOptions = Object.keys(response[0].conditionals_counts).map((conditionalName, index) => {
                        return {
                            value: conditionalName,
                            label: conditionalName
                        }
                    })
                    setConditionals(conditionalOptions)
                    setSelectedConditionals([conditionalOptions[0]])
                    const metricOptions = Object.keys(response[0].conditionals_counts[Object.keys(
                        response[0].conditionals_counts)[0]]).map((metricName, index) => {
                        return {
                            value: metricName,
                            label: metricName
                        }
                    })
                    setMetrics(metricOptions)
                    setSelectedMetric(metricOptions[0])
                }
            })
            .catch(error => console.log("error:" + error))
    }, []);

    useEffect(() => {
        setLoading(true)
        fetchEmulationStatistics()
    }, [fetchEmulationStatistics]);


    const removeEmulationStatisticRequest = useCallback((statistic_id) => {
        fetch(
            `http://` + ip + ':7777/emulationstatisticsdata/remove/' + statistic_id,
            {
                method: "POST",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => res.json())
            .then(response => {
                fetchEmulationStatistics()
            })
            .catch(error => console.log("error:" + error))
    }, []);

    const removeStatistic = (stat) => {
        setLoading(true)
        resetState()
        removeEmulationStatisticRequest(stat.id)
    }

    const SelectEmulationStatisticDropdownOrSpinner = (props) => {
        if (!props.loading && props.emulationStatistics.length === 0) {
            return (
                <span className="emptyText">No statistics are available</span>
            )
        }
        if (props.loading) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="inline-block">
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderInfoTooltip}
                    >
                        <Button variant="button" onClick={() => setShowInfoModal(true)}>
                            <i className="fa fa-info-circle infoButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <OverlayTrigger
                        className="removeButton"
                        placement="top"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRemoveStatisticTooltip}
                    >
                        <Button variant="danger" className="removeButton"
                                onClick={() => removeStatistic(selectedEmulationStatistic.value)}>
                            <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>

                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Statistic:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "400px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationStatistic}
                                defaultValue={props.selectedEmulationStatistic}
                                options={props.emulationStatistics}
                                onChange={updateEmulationStatistic}
                                placeholder="Select statistic"
                            />
                        </div>
                    </div>

                    <SelectConditionalDistributionDropdownOrSpinner conditionals={conditionals}
                                                                    selectedConditionals={selectedConditionals}
                                                                    loading={loading}/>
                    <SelectMetricDistributionDropdownOrSpinner metrics={metrics}
                                                               selectedMetric={selectedMetric}
                                                               loading={loading}/>
                </div>
            )
        }
    }

    const SelectConditionalDistributionDropdownOrSpinner = (props) => {
        if (!props.loading && props.conditionals.length === 0) {
            return (
                <span>  </span>
            )
        }
        if (props.loading || props.selectedConditional === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block">
                    <div className="conditionalDist inline-block conditionalLabel">
                        Conditionals:
                    </div>
                    <div className="conditionalDist inline-block" style={{width: "400px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.selectedConditionals}
                            isMulti={true}
                            defaultValue={props.selectedConditionals}
                            options={props.conditionals}
                            onChange={updateSelectedConditionals}
                            placeholder="Select conditional distributions"
                        />
                    </div>
                </div>
            )
        }
    }

    const SelectMetricDistributionDropdownOrSpinner = (props) => {
        if (!props.loading && props.metrics.length === 0) {
            return (
                <span>  </span>
            )
        }
        if (props.loading || props.selectedMetric === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div className="conditionalDist inline-block metricLabel">
                    <div className="conditionalDist inline-block conditionalLabel">
                        Metric:
                    </div>
                    <div className="conditionalDist inline-block" style={{width: "400px"}}>
                        <Select
                            style={{display: 'inline-block'}}
                            value={props.selectedMetric}
                            defaultValue={props.selectedMetric}
                            options={props.metrics}
                            onChange={updateMetric}
                            placeholder="Select metric"
                        />
                    </div>
                </div>
            )
        }
    }

    const conditionalPairs = () => {
        if (selectedConditionals.length < 2) {
            return []
        } else {
            var conditionalPairs = []
            for (let i = 0; i < selectedConditionals.length; i++) {
                for (let j = 0; j < selectedConditionals.length; j++) {
                    if (selectedConditionals[i] !== selectedConditionals[j]) {
                        conditionalPairs.push({
                            "conditional_1": selectedConditionals[i].label,
                            "conditional_2": selectedConditionals[j].label
                        })
                    }
                }
            }
            return conditionalPairs
        }
    }

    const StatisticDescriptionOrSpinner = (props) => {
        if (!props.loading && props.emulationStatistics.length === 0) {
            return (<span> </span>)
        }
        if (props.loading || props.selectedEmulationStatistic === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <p className="statisticDescription">
                        Statistic description: {props.selectedEmulationStatistic.value.descr}
                        <span className="numSamples">
                        Number of samples: {getNumSamples(props.selectedEmulationStatistic.value)}
                    </span>
                    </p>
                </div>
            )
        }
    }

    const ConditionalChartsOrSpinner = (props) => {
        if (!props.loading && props.conditionals.length === 0) {
            return (
                <p className="statisticDescription"></p>
            )
        }
        if (!props.loading && props.selectedConditionals !== null && props.selectedConditionals !== undefined &&
            props.selectedConditionals.length === 0) {
            return (
                <p className="statisticDescription">Select a conditional distribution from the dropdown list.</p>
            )
        }
        if (props.loading || props.selectedConditionals === null || props.selectedConditionals.length === 0
            || props.selectedMetric === null) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <div className="row chartsRow">
                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDeltaCountsOpen(!deltaCountsOpen)}
                                    aria-controls="deltaCountsBody"
                                    aria-expanded={deltaCountsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Delta value count distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaCountsOpen}>
                                <div id="deltaCountsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.value.conditionals_counts}
                                            selectedConditionals={getFirstTwoConditionals()}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Delta counts: " + props.selectedMetric.value}
                                            title2={"Delta counts: " + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Count"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setInitialCountsOpen(!initialCountsOpen)}
                                    aria-controls="initialCountsBody"
                                    aria-expanded={initialCountsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Initial value count distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={initialCountsOpen}>
                                <div id="initialCountsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.value.initial_distributions_counts}
                                            selectedConditionals={[]}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Initial counts of::" + props.selectedMetric.value}
                                            title2={"Initial counts of:" + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Count"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDeltaProbsOpen(!deltaProbsOpen)}
                                    aria-controls="deltaProbsBody"
                                    aria-expanded={deltaProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Delta value probability distributions</h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaProbsOpen}>
                                <div id="deltaProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.value.conditionals_probs}
                                            selectedConditionals={getFirstTwoConditionals()}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Delta probabilities: " + props.selectedMetric.value}
                                            title2={"Delta probabilities: " + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Probability"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setInitialProbsOpen(!initialProbsOpen)}
                                    aria-controls="initialProbsBody"
                                    aria-expanded={initialProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">
                                        Initial value probability distributions
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={initialProbsOpen}>
                                <div id="initialProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.value.initial_distributions_probs}
                                            selectedConditionals={[]}
                                            selectedMetric={props.selectedMetric}
                                            title1={"Initial counts of::" + props.selectedMetric.value}
                                            title2={"Initial counts of:" + props.selectedMetric.value}
                                            animationDuration={props.animationDuration}
                                            animationDurationFactor={props.animationDurationFactor}
                                            yAxisLabel={"Probability"}
                                        />
                                    </div>
                                </div>
                            </Collapse>
                        </Card>

                        <Card className="col-sm-12">
                            <Card.Header>
                                <Button
                                    onClick={() => setDescriptiveStatsOpen(!descriptiveStatsOpen)}
                                    aria-controls="descriptiveStatsBody"
                                    aria-expanded={descriptiveStatsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">
                                        Descriptive statistics
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={descriptiveStatsOpen}>
                                <div id="descriptiveStatsBody" className="cardBodyHidden">
                                    <div className="table-responsive">
                                        <Table striped bordered hover>
                                            <thead>
                                            <tr>
                                                <th>Attribute</th>
                                                <th> Value</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} mean</td>
                                                        <td>{props.selectedEmulationStatistic.value.means[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} standard deviation</td>
                                                        <td>{props.selectedEmulationStatistic.value.stds[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} minimum value</td>
                                                        <td>{props.selectedEmulationStatistic.value.mins[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} maximum value</td>
                                                        <td>{props.selectedEmulationStatistic.value.maxs[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            <tr>
                                                <td>Initial value mean</td>
                                                <td>{props.selectedEmulationStatistic.value.initial_means[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial value standard deviation</td>
                                                <td>{props.selectedEmulationStatistic.value.initial_stds[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial minimum value</td>
                                                <td>{props.selectedEmulationStatistic.value.initial_mins[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial maximum value</td>
                                                <td>{props.selectedEmulationStatistic.value.initial_maxs[props.selectedMetric.label]}</td>
                                            </tr>
                                            {conditionalPairs().map((conditionalPair, index) => {
                                                return (
                                                    <tr key={conditionalPair.conditional_1 + "-" +
                                                        conditionalPair.conditional_2 + "-" + index}>
                                                        <td>Kullback-Leibler divergence between conditional
                                                            "{conditionalPair.conditional_1}" and
                                                            "{conditionalPair.conditional_2}"
                                                        </td>
                                                        <td>{props.selectedEmulationStatistic.value.conditionals_kl_divergences[conditionalPair.conditional_1][conditionalPair.conditional_2][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            <tr>
                                                <td>Data</td>
                                                <td>
                                                    <Button variant="link"
                                                            onClick={() => fileDownload(JSON.stringify(props.selectedEmulationStatistic.value), "config.json")}>
                                                        data.json
                                                    </Button>
                                                </td>
                                            </tr>
                                            </tbody>
                                        </Table>
                                    </div>
                                </div>
                            </Collapse>
                        </Card>
                    </div>
                </div>
            )
        }
    }


    return (
        <div className="emulationStatistics">

            <h5 className="text-center inline-block emulationsHeader">
                <SelectEmulationStatisticDropdownOrSpinner emulationStatistics={emulationStatistics}
                                                      selectedEmulationStatistic={selectedEmulationStatistic}
                                                      loading={loading}
                />
            </h5>
            <StatisticDescriptionOrSpinner emulationStatistics={emulationStatistics}
                                       selectedEmulationStatistic={selectedEmulationStatistic}
                                       loading={loading}/>

            <ConditionalChartsOrSpinner key={animationDuration}
                                        selectedEmulationStatistic={selectedEmulationStatistic}
                                        selectedConditionals={selectedConditionals}
                                        animationDurationFactor={animationDurationFactor}
                                        animationDuration={animationDuration}
                                        conditionals={conditionals} emulationStatistics={emulationStatistics}
                                        selectedMetric={selectedMetric}
                                        metrics={metrics}
                                        loading={loading}
            />

        </div>
    );
}
EmulationStatistics.propTypes = {};
EmulationStatistics.defaultProps = {};
export default EmulationStatistics;
