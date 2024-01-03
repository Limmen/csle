import React, {useState, useEffect, useCallback} from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import ProgressBar from 'react-bootstrap/ProgressBar';
import Select from 'react-select'
import ConditionalHistogramDistribution from "./ConditionalHistogramDistribution/ConditionalHistogramDistribution";
import './EmulationStatistics.css';
import DataCollection from './DataCollection.png'
import Collapse from 'react-bootstrap/Collapse'
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table'
import fileDownload from 'react-file-download'
import {useDebouncedCallback} from 'use-debounce';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import Form from 'react-bootstrap/Form';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import {useNavigate} from "react-router-dom";
import {useAlert} from "react-alert";
import fetchProgress from 'fetch-progress';
import serverIp from "../../Common/serverIp";
import serverPort from "../../Common/serverPort";
import {
    EMULATION_STATISTICS_RESOURCE,
    HTTP_PREFIX,
    HTTP_REST_DELETE,
    HTTP_REST_GET,
    LOGIN_PAGE_RESOURCE,
    TOKEN_QUERY_PARAM,
    IDS_QUERY_PARAM
} from "../../Common/constants";
import formatBytes from "../../Common/formatBytes";

/**
 * Component representing the /statistics-page
 */
const EmulationStatistics = (props) => {
    const [emulationStatisticIds, setEmulationStatisticIds] = useState([]);
    const [filteredEmulationStatisticIds, setFilteredEmulationStatisticIds] = useState([]);
    const [selectedEmulationStatistic, setSelectedEmulationStatistic] = useState(null);
    const [selectedEmulationStatisticId, setSelectedEmulationStatisticId] = useState(null);
    const [conditionals, setConditionals] = useState([]);
    const [selectedConditionals, setSelectedConditionals] = useState(null);
    const [metrics, setMetrics] = useState([]);
    const [selectedMetric, setSelectedMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingSelectedEmulationStatistic, setLoadingSelectedEmulationStatistic] = useState(true);
    const [progressStarted, setProgressStarted] = useState(true);
    const animationDurationFactor = 50000
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [deltaCountsOpen, setDeltaCountsOpen] = useState(false);
    const [initialCountsOpen, setInitialCountsOpen] = useState(false);
    const [deltaProbsOpen, setDeltaProbsOpen] = useState(false);
    const [initialProbsOpen, setInitialProbsOpen] = useState(false);
    const [descriptiveStatsOpen, setDescriptiveStatsOpen] = useState(false);
    const [fetchProgressState, setFetchProgressState] = useState({
        eta: "N/A",
        percentage: 0,
        remaining: "N/A",
        speed: "N/A",
        total: "N/A",
        transferred: "N/A"
    });
    const animationDuration = 5
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();
    const setSessionData = props.setSessionData

    const fetchEmulationStatistic = useCallback((statistic_id) => {
        fetch(
            (`${HTTP_PREFIX}${ip}:${port}/${EMULATION_STATISTICS_RESOURCE}/${statistic_id.value}` +
                `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`),
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(
                fetchProgress({
                    onProgress(progress) {
                        if (progress.percentage > 0) {
                            setProgressStarted(true)
                            if (progress.percentage < fetchProgressState.percentage) {
                                progress.percentage = fetchProgressState.percentage
                            }
                            setFetchProgressState(progress)
                        }
                    },
                }))
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                setSelectedEmulationStatistic(response)
                setLoadingSelectedEmulationStatistic(false)
                if (response !== null && response !== undefined && !(Object.keys(response).length === 0)) {
                    const conditionalOptions = Object.keys(response.conditionals_counts).map(
                        (conditionalName, index) => {
                            return {
                                value: conditionalName,
                                label: conditionalName
                            }
                        })
                    setConditionals(conditionalOptions)
                    setSelectedConditionals([conditionalOptions[0]])
                    const metricOptions = Object.keys(response.conditionals_counts[Object.keys(
                        response.conditionals_counts)[0]]).map((metricName, index) => {
                        return {
                            value: metricName,
                            label: metricName
                        }
                    })
                    setMetrics(metricOptions)
                    setSelectedMetric(metricOptions[0])
                    setProgressStarted(false)
                    setFetchProgressState({
                        eta: "N/A",
                        percentage: 0,
                        remaining: "N/A",
                        speed: "N/A",
                        total: "N/A",
                        transferred: "N/A"
                    })
                }
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, alert, props.sessionData.token, setSessionData]);

    const resetState = () => {
        setEmulationStatisticIds([])
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
        setProgressStarted(false)
        resetState()
        fetchEmulationStatisticsIds()
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
                    <Modal.Title id="contained-modal-title-vcenter" className="modalTitle">
                        Emulation statistics
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p className="modalText">
                        The emulation statistics are collected by measuring log files and other metrics from
                        the emulated infrastructure under different system conditions, e.g. intrusion and no intrsion,
                        high load and low load etc.
                    </p>
                    <div className="text-center">
                        <img src={DataCollection} alt="Data collection from the emulation" className="img-fluid"/>
                    </div>
                </Modal.Body>
                <Modal.Footer className="modalFooter">
                    <Button onClick={props.onHide} size="sm">Close</Button>
                </Modal.Footer>
            </Modal>
        );
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

    const updateEmulationStatisticId = (emulationStatisticId) => {
        setSelectedEmulationStatisticId(emulationStatisticId)
        setProgressStarted(false)
        setFetchProgressState({
            eta: "N/A",
            percentage: 0,
            remaining: "N/A",
            speed: "N/A",
            total: "N/A",
            transferred: "N/A"
        })
        fetchEmulationStatistic(emulationStatisticId)
        setSelectedConditionals(null)
        setSelectedMetric(null)
        setLoadingSelectedEmulationStatistic(true)
    }

    const fetchEmulationStatisticsIds = useCallback(() => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_STATISTICS_RESOURCE}?${IDS_QUERY_PARAM}=true`
            + `&${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_GET,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                const statisticsIds = response.map((id_obj, index) => {
                    return {
                        value: id_obj.id,
                        label: `ID:${id_obj.id}, emulation: ${id_obj.emulation}`
                    }
                })
                setEmulationStatisticIds(statisticsIds)
                setFilteredEmulationStatisticIds(statisticsIds)
                setLoading(false)
                if (statisticsIds.length > 0) {
                    var minIdx = 0
                    var minId = Number.MAX_VALUE
                    for (let i = 0; i < statisticsIds.length; i++) {
                        if (statisticsIds[i].value <= minId) {
                            minId = statisticsIds[i].value
                            minIdx = i
                        }
                    }
                    setSelectedEmulationStatisticId(statisticsIds[minIdx])
                    fetchEmulationStatistic(statisticsIds[minIdx])
                    setLoadingSelectedEmulationStatistic(true)
                } else {
                    setLoadingSelectedEmulationStatistic(false)
                    setSelectedEmulationStatistic(null)
                }
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, alert, props.sessionData.token, setSessionData, fetchEmulationStatistic]);

    useEffect(() => {
        setLoading(true)
        setProgressStarted(false)
        setFetchProgressState({
            eta: "N/A",
            percentage: 0,
            remaining: "N/A",
            speed: "N/A",
            total: "N/A",
            transferred: "N/A"
        })
        fetchEmulationStatisticsIds()
    }, [fetchEmulationStatisticsIds]);


    const removeEmulationStatisticRequest = useCallback((statistic_id) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/${EMULATION_STATISTICS_RESOURCE}/${statistic_id}` +
            `?${TOKEN_QUERY_PARAM}=${props.sessionData.token}`,
            {
                method: HTTP_REST_DELETE,
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                })
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    setSessionData(null)
                    navigate(`/${LOGIN_PAGE_RESOURCE}`);
                    return null
                }
                return res.json()
            })
            .then(response => {
                if (response === null) {
                    return
                }
                fetchEmulationStatisticsIds()
            })
            .catch(error => console.log("error:" + error))
    }, [ip, port, navigate, alert, props.sessionData.token, setSessionData, fetchEmulationStatisticsIds]);

    const removeStatistic = (stat) => {
        setLoading(true)
        resetState()
        removeEmulationStatisticRequest(stat.id)
        setSelectedEmulationStatistic(null)
    }

    const removeStatisticConfirm = (statistic) => {
        confirmAlert({
            title: 'Confirm deletion',
            message: 'Are you sure you want to delete the statistic with ID: ' + statistic.id +
                "? this action cannot be undone",
            buttons: [
                {
                    label: 'Yes',
                    onClick: () => removeStatistic(statistic)
                },
                {
                    label: 'No'
                }
            ],
            closeOnEscape: true,
            closeOnClickOutside: true,
            keyCodeForClose: [8, 32],
            overlayClassName: "remove-confirm",
            customUI: ({onClose}) => {
                return (
                    <div id="react-confirm-alert" onClick={onClose}>
                        <div className="react-confirm-alert-overlay">
                            <div className="react-confirm-alert" onClick={onClose}>
                                <div className="react-confirm-alert-body">
                                    <h1>Confirm deletion</h1>
                                    Are you sure you want to delete the statistic with ID {statistic.id}?
                                    this action cannot be undone
                                    <div className="react-confirm-alert-button-group">
                                        <Button className="remove-confirm-button"
                                                onClick={() => {
                                                    removeStatistic(statistic)
                                                    onClose()
                                                }}
                                        >
                                            <span className="remove-confirm-button-text">Yes, delete it.</span>
                                        </Button>
                                        <Button className="remove-confirm-button"
                                                onClick={onClose}>
                                            <span className="remove-confirm-button-text">No</span>
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        })
    }

    const searchFilter = (statIdObj, searchVal) => {
        return (searchVal === "" || statIdObj.label.toString().toLowerCase().indexOf(searchVal.toLowerCase()) !== -1)
    }

    const searchChange = (event) => {
        var searchVal = event.target.value
        const filteredEmStatsIds = emulationStatisticIds.filter(stat_id_obj => {
            return searchFilter(stat_id_obj, searchVal)
        });
        setFilteredEmulationStatisticIds(filteredEmStatsIds)

        var selectedStatRemoved = false
        if (!loadingSelectedEmulationStatistic && filteredEmStatsIds.length > 0) {
            for (let i = 0; i < filteredEmStatsIds.length; i++) {
                if (selectedEmulationStatistic !== null && selectedEmulationStatistic !== undefined &&
                    selectedEmulationStatistic.id === filteredEmStatsIds[i].value) {
                    selectedStatRemoved = true
                }
            }
            if (!selectedStatRemoved) {
                var minIdx = 0
                var minId = Number.MAX_VALUE
                for (let i = 0; i < filteredEmStatsIds.length; i++) {
                    if (filteredEmStatsIds[i].value <= minId) {
                        minId = filteredEmStatsIds[i].value
                        minIdx = i
                    }
                }
                setSelectedEmulationStatisticId(filteredEmStatsIds[minIdx])
                fetchEmulationStatistic(filteredEmStatsIds[minIdx])
                setLoadingSelectedEmulationStatistic(true)
            }
        } else {
            setSelectedEmulationStatistic(null)
        }
    }

    const searchHandler = useDebouncedCallback(
        (event) => {
            searchChange(event)
        },
        350
    );

    const DeleteSelectedStatisticOrEmpty = (props) => {
        if (props.sessionData !== null && props.sessionData !== undefined && props.sessionData.admin) {
            return (
                <OverlayTrigger
                    className="removeButton"
                    placement="top"
                    delay={{show: 100, hide: 400}}
                    overlay={renderRemoveStatisticTooltip}
                >
                    <Button variant="danger" className="removeButton" size="sm"
                            onClick={() => removeStatisticConfirm(selectedEmulationStatistic)}>
                        <i className="fa fa-trash startStopIcon" aria-hidden="true"/>
                    </Button>
                </OverlayTrigger>
            )
        } else {
            return (<></>)
        }
    }

    const SelectEmulationStatisticDropdownOrSpinner = (props) => {
        if (!props.loading && props.emulationStatisticsIds.length === 0) {
            return (
                <div>
                    <span className="emptyText">No statistics are available</span>
                    <OverlayTrigger
                        placement="right"
                        delay={{show: 0, hide: 0}}
                        overlay={renderRefreshTooltip}
                    >
                        <Button variant="button" onClick={refresh}>
                            <i className="fa fa-refresh refreshButton" aria-hidden="true"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            )
        }
        if (props.loading) {
            return (
                <div>
                    <span className="spinnerLabel"> Fetching statistics... </span>
                    <Spinner animation="border" role="status" className="dropdownSpinner">
                        <span className="visually-hidden"></span>
                    </Spinner>
                </div>)
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

                    <DeleteSelectedStatisticOrEmpty sessionData={props.sessionData}/>

                    <InfoModal show={showInfoModal} onHide={() => setShowInfoModal(false)}/>
                    <div className="conditionalDist inline-block">
                        <div className="conditionalDist inline-block conditionalLabel">
                            Statistic:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedEmulationStatisticId}
                                defaultValue={props.selectedEmulationStatisticId}
                                options={props.emulationStatisticsIds}
                                onChange={updateEmulationStatisticId}
                                placeholder="Select statistic"
                            />
                        </div>
                    </div>
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
                    <h4>
                        <div className="conditionalDist inline-block conditionalLabel">
                            Conditionals:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
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
                    </h4>
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
                    <h4>
                        <div className="conditionalDist inline-block conditionalLabel">
                            Metric:
                        </div>
                        <div className="conditionalDist inline-block" style={{width: "300px"}}>
                            <Select
                                style={{display: 'inline-block'}}
                                value={props.selectedMetric}
                                defaultValue={props.selectedMetric}
                                options={props.metrics}
                                onChange={updateMetric}
                                placeholder="Select metric"
                            />
                        </div>
                    </h4>
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

    const SelectedEmulationStatisticView = (props) => {
        if (props.loadingSelectedEmulationStatistic || props.selectedEmulationStatistic === null
            || props.selectedEmulationStatistic === undefined) {
            if (props.loadingSelectedEmulationStatistic) {
                if (!props.progressStarted) {
                    return (
                        <h3>
                            <span className="spinnerLabel"> Fetching emulation statistic... </span>
                            <Spinner animation="border" role="status">
                                <span className="visually-hidden"></span>
                            </Spinner>
                        </h3>
                    )
                } else {
                    return (
                        <div>
                            <h3>
                                <span className="spinnerLabel"> Fetching emulation statistic... </span>
                            </h3>
                            <p className="progressInfo">Speed: {formatBytes(fetchProgressState.speed)}/s,
                                transferred: {formatBytes(fetchProgressState.transferred)}/
                                {formatBytes(fetchProgressState.total)}</p>
                            <ProgressBar animated now={fetchProgressState.percentage}
                                         variant="info"
                                         label={
                                             <span className="progressLabel">{fetchProgressState.percentage}%</span>
                                         }
                                         className="text-center myProgress"/>
                        </div>
                    )
                }
            } else {
                return (
                    <p></p>
                )
            }
        } else {
            return (
                <div>
                    <SelectConditionalDistributionDropdownOrSpinner conditionals={props.conditionals}
                                                                    selectedConditionals={props.selectedConditionals}
                                                                    loading={props.loading}/>
                    <SelectMetricDistributionDropdownOrSpinner metrics={props.metrics}
                                                               selectedMetric={props.selectedMetric}
                                                               loading={props.loading}/>

                    <StatisticDescriptionOrSpinner selectedEmulationStatistic={props.selectedEmulationStatistic}
                                                   loading={props.loading}/>

                    <ConditionalChartsOrSpinner key={props.animationDuration}
                                                selectedEmulationStatistic={props.selectedEmulationStatistic}
                                                selectedConditionals={props.selectedConditionals}
                                                animationDurationFactor={props.animationDurationFactor}
                                                animationDuration={props.animationDuration}
                                                conditionals={props.conditionals}
                                                selectedMetric={props.selectedMetric}
                                                metrics={props.metrics}
                                                loading={props.loading}
                    />
                </div>
            )
        }
    }

    const StatisticDescriptionOrSpinner = (props) => {
        if (props.loading || props.selectedEmulationStatistic === null ||
            props.selectedEmulationStatistic === undefined) {
            return (
                <Spinner animation="border" role="status" className="dropdownSpinner">
                    <span className="visually-hidden"></span>
                </Spinner>)
        } else {
            return (
                <div>
                    <p className="statisticDescription">
                        Statistic description: {props.selectedEmulationStatistic.descr}
                        <span className="numSamples">
                        Number of samples: {getNumSamples(props.selectedEmulationStatistic)}
                    </span>
                    </p>
                </div>
            )
        }
    }

    const ConditionalChartsOrSpinner = (props) => {
        if (props.selectedEmulationStatistic === null || props.selectedEmulationStatistic === undefined) {
            return (
                <p className></p>
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
                        <Card className="col-sm-12 subCard">
                            <Card.Header>
                                <Button
                                    onClick={() => setDeltaCountsOpen(!deltaCountsOpen)}
                                    aria-controls="deltaCountsBody"
                                    aria-expanded={deltaCountsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Delta value count distributions
                                        <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaCountsOpen}>
                                <div id="deltaCountsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <h3 className="chartsTitle">
                                            {"Delta counts: " + props.selectedMetric.value} (downsampled to 100 samples)
                                        </h3>
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.conditionals_counts}
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

                        <Card className="col-sm-12 subCard">
                            <Card.Header>
                                <Button
                                    onClick={() => setInitialCountsOpen(!initialCountsOpen)}
                                    aria-controls="initialCountsBody"
                                    aria-expanded={initialCountsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Initial value count distributions
                                        <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={initialCountsOpen}>
                                <div id="initialCountsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <h3 className="chartsTitle">
                                            {"Initial counts of:" + props.selectedMetric.value} (downsampled to 100
                                            samples)
                                        </h3>
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.initial_distributions_counts}
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

                        <Card className="col-sm-12 subCard">
                            <Card.Header>
                                <Button
                                    onClick={() => setDeltaProbsOpen(!deltaProbsOpen)}
                                    aria-controls="deltaProbsBody"
                                    aria-expanded={deltaProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">Delta value probability distributions
                                        <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={deltaProbsOpen}>
                                <div id="deltaProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <h3 className="chartsTitle">
                                            {"Delta probabilities: " + props.selectedMetric.value} (downsampled to 100
                                            samples)
                                        </h3>
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.conditionals_probs}
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

                        <Card className="col-sm-12 subCard">
                            <Card.Header>
                                <Button
                                    onClick={() => setInitialProbsOpen(!initialProbsOpen)}
                                    aria-controls="initialProbsBody"
                                    aria-expanded={initialProbsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">
                                        Initial value probability distributions
                                        <i className="fa fa-bar-chart headerIcon" aria-hidden="true"></i>
                                    </h5>
                                </Button>
                            </Card.Header>
                            <Collapse in={initialProbsOpen}>
                                <div id="initialProbsBody" className="cardBodyHidden">
                                    <div className="col-sm-12 conditionalHisto">
                                        <h3 className="chartsTitle">
                                            {"Initial counts of::" + props.selectedMetric.value} (downsampled to 100
                                            samples)
                                        </h3>
                                        <ConditionalHistogramDistribution
                                            data={props.selectedEmulationStatistic.initial_distributions_probs}
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

                        <Card className="col-sm-12 subCard">
                            <Card.Header>
                                <Button
                                    onClick={() => setDescriptiveStatsOpen(!descriptiveStatsOpen)}
                                    aria-controls="descriptiveStatsBody"
                                    aria-expanded={descriptiveStatsOpen}
                                    variant="link"
                                >
                                    <h5 className="cardHeaderDists">
                                        Descriptive statistics
                                        <i className="fa fa-table headerIcon" aria-hidden="true"></i>
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
                                                        <td>{props.selectedEmulationStatistic.means[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} standard deviation</td>
                                                        <td>{props.selectedEmulationStatistic.stds[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} minimum value</td>
                                                        <td>{props.selectedEmulationStatistic.mins[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}

                                            {props.selectedConditionals.map((conditional, index) => {
                                                return (
                                                    <tr key={conditional.label + "-" + index}>
                                                        <td>{conditional.label} maximum value</td>
                                                        <td>{props.selectedEmulationStatistic.maxs[conditional.label][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            <tr>
                                                <td>Initial value mean</td>
                                                <td>{props.selectedEmulationStatistic.initial_means[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial value standard deviation</td>
                                                <td>{props.selectedEmulationStatistic.initial_stds[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial minimum value</td>
                                                <td>{props.selectedEmulationStatistic.initial_mins[props.selectedMetric.label]}</td>
                                            </tr>
                                            <tr>
                                                <td>Initial maximum value</td>
                                                <td>{props.selectedEmulationStatistic.initial_maxs[props.selectedMetric.label]}</td>
                                            </tr>
                                            {conditionalPairs().map((conditionalPair, index) => {
                                                return (
                                                    <tr key={conditionalPair.conditional_1 + "-" +
                                                        conditionalPair.conditional_2 + "-" + index}>
                                                        <td>Kullback-Leibler divergence between conditional
                                                            "{conditionalPair.conditional_1}" and
                                                            "{conditionalPair.conditional_2}"
                                                        </td>
                                                        <td>{props.selectedEmulationStatistic.conditionals_kl_divergences[conditionalPair.conditional_1][conditionalPair.conditional_2][props.selectedMetric.label]}</td>
                                                    </tr>
                                                )
                                            })}
                                            <tr>
                                                <td>Data</td>
                                                <td>
                                                    <Button variant="link" className="dataDownloadLink"
                                                            onClick={() => fileDownload(JSON.stringify(props.selectedEmulationStatistic), "config.json")}>
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
            <h3 className="managementTitle"> Statistics of Emulations </h3>
            <div className="row">
                <div className="col-sm-7">
                    <h4>
                        <SelectEmulationStatisticDropdownOrSpinner
                            emulationStatisticsIds={filteredEmulationStatisticIds}
                            selectedEmulationStatisticId={selectedEmulationStatisticId}
                            loading={loading}
                            sessionData={props.sessionData}
                        />
                    </h4>
                </div>
                <div className="col-sm-3">
                    <Form className="searchForm">
                        <InputGroup className="mb-3 searchGroup">
                            <InputGroup.Text id="basic-addon1" className="searchIcon">
                                <i className="fa fa-search" aria-hidden="true"/>
                            </InputGroup.Text>
                            <FormControl
                                size="lg"
                                className="searchBar"
                                placeholder="Search"
                                aria-label="Search"
                                aria-describedby="basic-addon1"
                                onChange={searchHandler}
                            />
                        </InputGroup>
                    </Form>
                </div>
                <div className="col-sm-2">
                </div>
            </div>
            <SelectedEmulationStatisticView conditionals={conditionals}
                                            selectedConditionals={selectedConditionals}
                                            loading={loadingSelectedEmulationStatistic}
                                            metrics={metrics}
                                            selectedMetric={selectedMetric}
                                            loadingSelectedEmulationStatistic={loadingSelectedEmulationStatistic}
                                            selectedEmulationStatistic={selectedEmulationStatistic}
                                            animationDuration={animationDuration}
                                            animationDurationFactor={animationDurationFactor}
                                            progressStarted={progressStarted}
            />
        </div>
    );
}

EmulationStatistics.propTypes = {};
EmulationStatistics.defaultProps = {};
export default EmulationStatistics;
