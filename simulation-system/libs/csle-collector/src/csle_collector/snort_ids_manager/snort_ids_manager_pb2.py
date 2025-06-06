# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: snort_ids_manager.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17snort_ids_manager.proto\"@\n\x14GetSnortIdsAlertsMsg\x12\x11\n\ttimestamp\x18\x01 \x01(\x02\x12\x15\n\rlog_file_path\x18\x02 \x01(\t\"\x18\n\x16StopSnortIdsMonitorMsg\"u\n\x17StartSnortIdsMonitorMsg\x12\x10\n\x08kafka_ip\x18\x01 \x01(\t\x12\x12\n\nkafka_port\x18\x02 \x01(\x05\x12\x15\n\rlog_file_path\x18\x03 \x01(\t\x12\x1d\n\x15time_step_len_seconds\x18\x04 \x01(\x05\"\x11\n\x0fStopSnortIdsMsg\"[\n\x10StartSnortIdsMsg\x12\x19\n\x11ingress_interface\x18\x01 \x01(\t\x12\x18\n\x10\x65gress_interface\x18\x02 \x01(\t\x12\x12\n\nsubnetmask\x18\x03 \x01(\t\"\x1d\n\x1bGetSnortIdsMonitorStatusMsg\"H\n\x12SnortIdsMonitorDTO\x12\x17\n\x0fmonitor_running\x18\x01 \x01(\x08\x12\x19\n\x11snort_ids_running\x18\x02 \x01(\x08\"\x8a\x0b\n\x0eSnortIdsLogDTO\x12\x11\n\ttimestamp\x18\x01 \x01(\x02\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x1e\n\x16\x61ttempted_admin_alerts\x18\x03 \x01(\x05\x12\x1d\n\x15\x61ttempted_user_alerts\x18\x04 \x01(\x05\x12$\n\x1cinappropriate_content_alerts\x18\x05 \x01(\x05\x12\x1f\n\x17policy_violation_alerts\x18\x06 \x01(\x05\x12\x1f\n\x17shellcode_detect_alerts\x18\x07 \x01(\x05\x12\x1f\n\x17successful_admin_alerts\x18\x08 \x01(\x05\x12\x1e\n\x16successful_user_alerts\x18\t \x01(\x05\x12\x1e\n\x16trojan_activity_alerts\x18\n \x01(\x05\x12 \n\x18unsuccessful_user_alerts\x18\x0b \x01(\x05\x12%\n\x1dweb_application_attack_alerts\x18\x0c \x01(\x05\x12\x1c\n\x14\x61ttempted_dos_alerts\x18\r \x01(\x05\x12\x1e\n\x16\x61ttempted_recon_alerts\x18\x0e \x01(\x05\x12\x1a\n\x12\x62\x61\x64_unknown_alerts\x18\x0f \x01(\x05\x12$\n\x1c\x64\x65\x66\x61ult_login_attempt_alerts\x18\x10 \x01(\x05\x12 \n\x18\x64\x65nial_of_service_alerts\x18\x11 \x01(\x05\x12\x1a\n\x12misc_attack_alerts\x18\x12 \x01(\x05\x12$\n\x1cnon_standard_protocol_alerts\x18\x13 \x01(\x05\x12!\n\x19rpc_portman_decode_alerts\x18\x14 \x01(\x05\x12\x1d\n\x15successful_dos_alerts\x18\x15 \x01(\x05\x12*\n\"successful_recon_largescale_alerts\x18\x16 \x01(\x05\x12\'\n\x1fsuccessful_recon_limited_alerts\x18\x17 \x01(\x05\x12)\n!suspicious_filename_detect_alerts\x18\x18 \x01(\x05\x12\x1f\n\x17suspicious_login_alerts\x18\x19 \x01(\x05\x12!\n\x19system_call_detect_alerts\x18\x1a \x01(\x05\x12-\n%unusual_client_port_connection_alerts\x18\x1b \x01(\x05\x12\'\n\x1fweb_application_activity_alerts\x18\x1c \x01(\x05\x12\x19\n\x11icmp_event_alerts\x18\x1d \x01(\x05\x12\x1c\n\x14misc_activity_alerts\x18\x1e \x01(\x05\x12\x1b\n\x13network_scan_alerts\x18\x1f \x01(\x05\x12\x1d\n\x15not_suspicious_alerts\x18  \x01(\x05\x12&\n\x1eprotocol_command_decode_alerts\x18! \x01(\x05\x12\x1c\n\x14string_detect_alerts\x18\" \x01(\x05\x12\x16\n\x0eunknown_alerts\x18# \x01(\x05\x12\x1d\n\x15tcp_connection_alerts\x18$ \x01(\x05\x12\x19\n\x11priority_1_alerts\x18% \x01(\x05\x12\x19\n\x11priority_2_alerts\x18& \x01(\x05\x12\x19\n\x11priority_3_alerts\x18\' \x01(\x05\x12\x19\n\x11priority_4_alerts\x18( \x01(\x05\x12\x14\n\x0ctotal_alerts\x18) \x01(\x05\x12\x16\n\x0ewarning_alerts\x18* \x01(\x05\x12\x15\n\rsevere_alerts\x18+ \x01(\x05\x12#\n\x1b\x61lerts_weighted_by_priority\x18, \x01(\x05\x32\xa5\x03\n\x0fSnortIdsManager\x12=\n\x11getSnortIdsAlerts\x12\x15.GetSnortIdsAlertsMsg\x1a\x0f.SnortIdsLogDTO\"\x00\x12\x45\n\x13stopSnortIdsMonitor\x12\x17.StopSnortIdsMonitorMsg\x1a\x13.SnortIdsMonitorDTO\"\x00\x12G\n\x14startSnortIdsMonitor\x12\x18.StartSnortIdsMonitorMsg\x1a\x13.SnortIdsMonitorDTO\"\x00\x12O\n\x18getSnortIdsMonitorStatus\x12\x1c.GetSnortIdsMonitorStatusMsg\x1a\x13.SnortIdsMonitorDTO\"\x00\x12\x37\n\x0cstopSnortIds\x12\x10.StopSnortIdsMsg\x1a\x13.SnortIdsMonitorDTO\"\x00\x12\x39\n\rstartSnortIds\x12\x11.StartSnortIdsMsg\x1a\x13.SnortIdsMonitorDTO\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'snort_ids_manager_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETSNORTIDSALERTSMSG._serialized_start=27
  _GETSNORTIDSALERTSMSG._serialized_end=91
  _STOPSNORTIDSMONITORMSG._serialized_start=93
  _STOPSNORTIDSMONITORMSG._serialized_end=117
  _STARTSNORTIDSMONITORMSG._serialized_start=119
  _STARTSNORTIDSMONITORMSG._serialized_end=236
  _STOPSNORTIDSMSG._serialized_start=238
  _STOPSNORTIDSMSG._serialized_end=255
  _STARTSNORTIDSMSG._serialized_start=257
  _STARTSNORTIDSMSG._serialized_end=348
  _GETSNORTIDSMONITORSTATUSMSG._serialized_start=350
  _GETSNORTIDSMONITORSTATUSMSG._serialized_end=379
  _SNORTIDSMONITORDTO._serialized_start=381
  _SNORTIDSMONITORDTO._serialized_end=453
  _SNORTIDSLOGDTO._serialized_start=456
  _SNORTIDSLOGDTO._serialized_end=1874
  _SNORTIDSMANAGER._serialized_start=1877
  _SNORTIDSMANAGER._serialized_end=2298
# @@protoc_insertion_point(module_scope)
