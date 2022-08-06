# Copyright 2022 Jonas Claes
# SPDX-License-Identifier: Apache-2.0
# pylint: disable=R0904
"""Definition for the MX100TP PSU made by AIM/TTi"""
from instrumentpy.common.common_device_interface import CommonDeviceInterface


class MX100TP():
    """
    MX100TP PSU supports serial over USB, TCP/IP and VISA communications.

    At the moment, only serial communications are implemented.
    """
    _device: CommonDeviceInterface | None = None

    def __init__(self, device: CommonDeviceInterface) -> None:
        self._device = device

    # Instrument Function Commands

    # Common commands

    def get_instrument_identification(self) -> str:
        """
        Implemented command: *IDN?

        Returns the instrument identification.
        The response is in the form <NAME>, <model>, <serial>, <version><RMT>
        where <NAME> is the manufacturer's name, <model> is the instrument
        type, <serial> is the interface serial number and <version> is the revision
        level of the firmware installed.
        """
        self._device.send_command("*IDN?\n")
        return self._device.receive_output()

    def factory_reset(self) -> None:
        """
        Implemented command: *RST

        Resets the functional parameters of the instrument to the default settings as
        listed in the Factory Default Settings, see section 18.
        Does not affect the contents of the Save and Recall stores.
        Does not affect any remote interface settings.
        """
        self._device.send_command("*RST\n")

    def save_settings(self, memory_store: int = 0) -> None:
        """
        Implemented command: *SAV <NRF>

        Save the settings for all three outputs simultaneously to the store specified by
        <NRF> where <NRF> can be 0-49. This includes output On/Off state, current
        meter averaging state, and the Multi-On/Multi-Off settings.
        """
        if memory_store < 0 or memory_store > 49:
            raise ValueError(
                "Memory store out of range. 0-49 inclusive is allowed.")
        self._device.send_command(f"*SAV;{memory_store}\n")

    def recall_settings(self, memory_store: int = 0) -> None:
        """
        Implemented command: *RCL <NRF>

        Recall the settings for all three outputs simultaneously from the store specified
        by <NRF> where <NRF> can be 0-49.This includes output On/Off state, current
        meter averaging state, and the Multi-On/Multi-Off settings.
        """
        if memory_store < 0 or memory_store > 49:
            raise ValueError(
                "Memory store out of range. 0-49 inclusive is allowed.")
        self._device.send_command(f"*RCL;{memory_store}\n")

    def set_operation_complete_bit(self) -> None:
        """
        Implemented command: *OPC

        Sets the Operation Complete bit (bit 0) in the Standard Event Status
        Register. This will happen immediately the command is executed because
        of the sequential nature of all operations.
        """
        self._device.send_command("*OPC\n")

    def get_operation_complete_status(self) -> str:
        """
        Implemented command: *OPC?

        Query Operation Complete status.
        The response is always 1<RMT> and is available immediately the command
        is executed because all commands are sequential.
        """
        self._device.send_command("*OPC?\n")
        return self._device.receive_output()

    def wait_for_complete(self) -> None:
        """
        Implemented command: *WAI

        Wait for Operation Complete true.
        This command does nothing because all operations are sequential.
        """
        self._device.send_command("*WAI\n")

    def self_test(self) -> str:
        """
        Implemented command: *TST?

        The product has no self-test capability and the response is always 0<RMT>.
        """
        self._device.send_command("*TST?\n")
        return self._device.receive_output()

    def trigger(self) -> None:
        """
        Implemented command: *TRG

        The product has no trigger capability. The command is ignored in this
        instrument.
        """
        self._device.send_command("*TRG\n")

    # Status commands

    def clear_status(self) -> None:
        """
        Implemented command: *CLS

        Clear Status. Clears all status indications, including the Status Byte.
        Does not clear any Enable Registers.
        """
        self._device.send_command("*CLS\n")

    def query_and_clear_limit_status_register(self, register_number: int) -> str:
        """
        Implemented command: LSR<N>?

        Query and clear the Limit Status Register<N>. The response format is
        <NR1><RMT>. See Status Reporting section for details of the response.
        """
        self._device.send_command(f"LSR{register_number}?\n")
        return self._device.receive_output()

    def set_limit_status_enable_register(self, register_number: int, limit: int | float) -> None:
        """
        Implemented command: LSE<N> <NRF>

        Set the Limit Status Enable Register<N> to <NRF>.
        """
        self._device.send_command(f"LSE{register_number};{limit}\n")

    def get_limit_status_enable_register(self, register_number: int) -> str:
        """
        Implemented command: LSE<N>?

        Returns the value in the value in the Limit Status Enable Register<N>.
        The response format is<NR1><RMT>.
        """
        self._device.send_command(f"LSE{register_number}?\n")
        return self._device.receive_output()

    def query_and_clear_execution_error_register(self) -> str:
        """
        Implemented command: EER?

        Query and clear Execution Error Register. The response format is
        <NR1><RMT>.
        """
        self._device.send_command("EER?\n")
        return self._device.receive_output()

    def query_and_clear_query_error_register(self) -> str:
        """
        Implemented command: QER?

        Query and clear Query Error Register. The response format is
        <NR1><RMT>.
        """
        self._device.send_command("QER?\n")
        return self._device.receive_output()

    def get_status_byte(self) -> str:
        """
        Implemented command: *STB?

        Report the value of the Status Byte. The response is: <NR1><RMT>.
        Because there is no output queue, MAV can only be read by a GPIB serial
        poll, not by this query, as any previous message must have already been
        sent.
        """
        self._device.send_command("*STB?\n")
        return self._device.receive_output()

    def set_service_request_enable_register(self, value: int | float) -> None:
        """
        Implemented command: *SRE <NRF>

        Sets the Service Request Enable Register to <NRF>
        """
        self._device.send_command(f"*SRE;{value}\n")

    def get_service_request_enable_register(self) -> str:
        """
        Implemented command: *SRE?

        Report the value in the Service Request Enable Register.
        The response is <NR1><RMT>.
        """
        self._device.send_command("*SRE?\n")
        return self._device.receive_output()

    def set_parallel_poll_enable_register(self, value: int | float) -> None:
        """
        Implemented command: *PRE <NRF>

        Set the Parallel Poll Enable Register to the value <NRF>.
        """
        self._device.send_command(f"*PRE;{value}\n")

    def get_parallel_poll_enable_register(self) -> str:
        """
        Implemented command: *PRE?

        Report the value in the Parallel Poll Enable Register.
        The response is <NR1><RMT>.
        """
        self._device.send_command("*PRE?\n")
        return self._device.receive_output()

    def get_ist_state(self) -> str:
        """
        Implemented command: *IST?

        Returns the state of the ist local message as defined by IEEE Std. 488.2.
        The response is 0<RMT> if the local message is false, or 1<RMT> if true.
        """
        self._device.send_command("*IST?\n")
        return self._device.receive_output()

    # Interface Management Commands

    def go_to_local(self) -> None:
        """
        Implemented command: LOCAL

        Go to local. Any subsequent command will restore the remote state.
        """
        self._device.send_command("LOCAL\n")

    def set_interface_lock(self, state: int) -> None:
        """
        Implemented command: IFLOCK <NRF>

        Set or Clear the lock requiring the instrument to respond only to this
        interface, where <NRF> has the meaning: 0 = clear and 1 = set the lock.
        It is an Execution Error (number 200) if the request is denied either because
        of conflict with a lock on this or another interface, or the user has disabled
        this interface from taking control using the web interface.
        """
        self._device.send_command(f"IFLOCK;{state}\n")

    def get_interface_lock(self) -> str:
        """
        Implemented command: IFLOCK?

        Query the status of the interface lock.
        The response is: <NR1><RMT> where <NR1> is
        = 0 if there is no active lock,
        = 1 if this interface instance owns the lock or
        = -1 if the lock is unavailable either because it is in use by another interface
        or the user has disabled this interface from taking control (via the web
        interface).
        """
        self._device.send_command("IFLOCK?\n")
        return self._device.receive_output()

    def get_interface_address(self) -> str:
        """
        Implemented command: ADDRESS?

        Returns the GPIB bus Address. The response is <NR1><RMT>.
        """
        self._device.send_command("ADDRESS?\n")
        return self._device.receive_output()

    def get_ip_address(self) -> str:
        """
        Implemented command: IPADDR?

        Returns the present IP address of the LAN interface, provided it is
        connected.
        If it is not connected, the response will be the static IP if configured to
        always use that static IP, otherwise it will be 0.0.0.0 if waiting for DHCP or
        Auto-IP.
        The response is nnn.nnn.nnn.nnn<RMT>, where each nnn is 0 to 255.
        """
        self._device.send_command("IPADDR?\n")
        return self._device.receive_output()

    def get_netmask(self) -> str:
        """
        Implemented command: NETMASK?

        Returns the present netmask of the LAN interface, provided it is connected.
        The response is nnn.nnn.nnn.nnn<RMT>, where each nnn is 0 to 255.
        """
        self._device.send_command("NETMASK?\n")
        return self._device.receive_output()

    def get_netconfig(self) -> str:
        """
        Implemented command: NETCONFIG?

        Returns the first means by which an IP address will be sought.
        The response is <CRD><RMT > where <CRD> is DHCP, AUTO or STATIC.
        """
        self._device.send_command("NETCONFIG?\n")
        return self._device.receive_output()

    def set_netconfig(self, config_type: str) -> None:
        """
        Implemented command: NETCONFIG <CPD>

        Specifies the first means by which an IP address will be sought.
        <CPD> must be one of DHCP, AUTO or STATIC.
        """
        self._device.send_command(f"NETCONFIG;{config_type}\n")

    def set_ip_address(self, address: str) -> None:
        """
        Implemented command: IPADDR <QUAD>

        Sets the potential static IP address of the LAN interface (as on the
        webpage).
        The parameter must be strictly a dotted quad for the IP address, with each
        address part an <NR1> in the range 0 to 255, (e.g. 192.168.1.101).
        """
        self._device.send_command(f"IPADDR;{address}\n")

    def set_netmask(self, address: str) -> None:
        """
        Implemented command: NETMASK <QUAD>

        Sets the netmask to accompany the static IP address of the LAN interface.
        The parameter must be strictly a dotted quad for the netmask, with each
        part an <NR1> in the range 0 to 255, (e.g. 255.255.255.0).
        """
        self._device.send_command(f"NETMASK;{address}\n")
