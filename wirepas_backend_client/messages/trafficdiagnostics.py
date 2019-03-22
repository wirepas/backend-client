"""
    TrafficDiagnostics
    ==================

    Contains helpers to translate network data into TrafficDiagnostics objects used
    within the library and test framework.

    .. Copyright:
        Copyright 2018 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.
"""
import datetime
import logging
import struct
import binascii
import json

from .types import ApplicationTypes
from .generic import GenericMessage

from .. import tools


class TrafficDiagnosticsMessage(GenericMessage):
    """
    TrafficDiagnosticsMessage

    Represents traffic diagnostics report message sent by nodes.

    Message content:
        3.x: access_cycles              uint16
          4.0: cluster_members          uint8
          4.0: cluster_headnode_members uint8
        cluster_channel                 uint8
        channel_reliability             uint8
        rx_amount                       uint16
        tx_amount                       uint16
        aloha_rx_ratio                  uint8
        reserved_rx_success_ratio       uint8
        data_rx_ratio                   uint8
        rx_duplicate_ratio              uint8
        cca_success_ratio               uint8
        broadcast_ratio                 uint8
        failed_unicast_ratio            uint8
        max_reserved_slot_usage         uint8
        average_reserved_slot_usage     uint8
        max_aloha_slot_usage            uint8
    """

    def __init__(self, *args, **kwargs)-> 'TrafficDiagnosticsMessage':

        super(TrafficDiagnosticsMessage, self).__init__(*args, **kwargs)
        self.type = ApplicationTypes.TrafficDiagnosticsMessage

        if isinstance(self.data_payload, str):
            self.data_payload = bytes(self.data_payload, "utf8")

        apdu_values = struct.unpack('<HBBHHBBBBBBBBBB', self.data_payload)
        apdu_names = ('access_cycles',
                      'cluster_channel',
                      'channel_reliability',
                      'rx_amount',
                      'tx_amount',
                      'aloha_rx_ratio',
                      'reserved_rx_success_ratio',
                      'data_rx_ratio',
                      'rx_duplicate_ratio',
                      'cca_success_ratio',
                      'broadcast_ratio',
                      'failed_unicast_ratio',
                      'max_reserved_slot_usage',
                      'average_reserved_slot_usage',
                      'max_aloha_slot_usage')
        self.apdu = self.map_list_to_dict(apdu_names, apdu_values)
        # 4.0 interpretation of message fields:
        self.apdu['cluster_members'] = self.apdu['access_cycles'] & 0xff
        self.apdu['cluster_headnode_members'] = self.apdu['access_cycles'] >> 8
