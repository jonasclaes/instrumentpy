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

    def set_channel_voltage(self, channel: int, value: int | float) -> None:
        """
        Implemented command: V<N> <NRF>

        Set output <N> to <NRF> Volts.
        """
        self._device.send_command(f"V{channel} {value}\n")

    def set_channel_voltage_with_verify(self, channel: int, value: int | float) -> None:
        """
        Implemented command: V<N>V <NRF>

        Set output <N> to <NRF> Volts with verify.
        """
        self._device.send_command(f"V{channel}V {value}\n")

    def set_channel_over_voltage_protection(self, channel: int, value: int | float) -> None:
        """
        Implemented command: OVP<N> <NRF>

        Set output <N> over voltage protection trip point to <NRF> Volts.
        """
        self._device.send_command(f"OVP{channel} {value}\n")

    def toggle_channel_over_voltage_protection(self, channel: int, state: str) -> None:
        """
        Implemented command: OVP<N> <CPD>

        Enables or disables the over voltage protection trip point where <CPD>
        can be ON or OFF.
        """
        self._device.send_command(f"OVP{channel} {state}\n")

    def set_channel_current_limit(self, channel: int, value: int | float) -> None:
        """
        Implemented command: I<N> <NRF>

        Set output <N> current limit to <NRF> Amps.
        """
        self._device.send_command(f"I{channel} {value}\n")

    def set_channel_over_current_protection(self, channel: int, value: int | float) -> None:
        """
        Implemented command: OCP<N> <NRF>

        Set output <N> over current protection trip point to <NRF> Amps.
        """
        self._device.send_command(f"OCP{channel} {value}\n")

    def toggle_channel_over_current_protection(self, channel: int, value: str) -> None:
        """
        Implemented command: OCP<N> <CPD>

        Enables or disables the over current protection trip point where <CPD>
        can be ON or OFF.
        """
        self._device.send_command(f"OCP{channel} {value}\n")

    def set_channel_current_measurement_averaging(self, channel: int, value: str) -> None:
        """
        Implemented command: DAMPING<N> <CPD>

        Set the current meter measurement averaging of output <N> to <CPD >,
        where <CPD> can be ON, OFF, LOW, MED or HIGH.
        """
        self._device.send_command(f"DAMPING{channel} {value}\n")

    def get_channel_voltage_setpoint(self, channel: int) -> str:
        """
        Implemented command: V<N>?

        Return the set voltage of output < N>.
        Response is V< N > <NR2><RMT> where <NR2> is in Volts.
        """
        self._device.send_command(f"V{channel}?\n")
        return self._device.receive_output()

    def get_channel_current_limit_setpoint(self, channel: int) -> str:
        """
        Implemented command: I<N>?

        Return the set current limit of output <N>.
        Response is I< N> <NR2><RMT> where <NR2> is in Amps.
        """
        self._device.send_command(f"I{channel}?\n")
        return self._device.receive_output()

    def get_channel_over_voltage_setpoint(self, channel: int) -> str:
        """
        Implemented command: OVP<N>?

        Return the voltage trip setting of output <N>.
        Response is VP<N> <NR2><RMT> where <NR 2> is in Volts.
        Note: If over voltage protection has been disabled the response is
        VP<N> <CRD><RMT> where <CRD> is OFF.
        """
        self._device.send_command(f"OVP{channel}?\n")
        return self._device.receive_output()

    def get_channel_over_current_setpoint(self, channel: int) -> str:
        """
        Implemented command: OCP<N>?

        Return the current trip setting of output<N>.
        Response is CP<N> <NR2>< RMT> where <NR2> is in Amps.
        Note: If over current protection has been disabled the response is
        CP<N> <CRD><RMT> where <CRD> is OFF.
        """
        self._device.send_command(f"OCP{channel}?\n")
        return self._device.receive_output()

    def get_channel_voltage(self, channel: int) -> str:
        """
        Implemented command: V<N>O?

        Return the output readback voltage of output <N>
        Response is <NR2>V<RMT> where <NR2> is in Volts.
        """
        self._device.send_command(f"V{channel}O?\n")
        return self._device.receive_output()

    def get_channel_current(self, channel: int) -> str:
        """
        Implemented command: I<N>O?

        Return the output readback current of output <N>
        Response is <NR2>A<RMT> where <NR2> is in Amps.
        """
        self._device.send_command(f"I{channel}O?\n")
        return self._device.receive_output()

    def set_channel_voltage_stepsize(self, channel: int, value: int | float) -> None:
        """
        Implemented command: DELTAV<N> <NRF>

        Set the output voltage step size of output <N> to <NRF> Volts.
        """
        self._device.send_command(f"DELTAV{channel} {value}\n")

    def set_channel_current_stepsize(self, channel: int, value: int | float) -> None:
        """
        Implemented command: DELTAI<N> <NRF>

        Set the output current step size of output <N> to <NRF> Amps.
        """
        self._device.send_command(f"DELTAI{channel} {value}\n")

    def get_channel_voltage_stepsize(self, channel: int) -> str:
        """
        Implemented command: DELTAV<N>?

        Return the output voltage step size of output < N>
        Response is DELTAV<N> <NR2><RMT>, where <NR2> is in Volts.
        """
        self._device.send_command(f"DELTAV{channel}?\n")
        return self._device.receive_output()

    def get_channel_current_stepsize(self, channel: int) -> str:
        """
        Implemented command: DELTAI<N>?

        Return the output current step size of output <N>
        Response is DELTAI<N> <NR2><RMT >, where <NR2> is in Amps.
        """
        self._device.send_command(f"DELTAI{channel}?\n")
        return self._device.receive_output()

    def increase_channel_voltage(self, channel: int) -> None:
        """
        Implemented command: INCV<N>

        Increment the output<N> voltage by step size.
        """
        self._device.send_command(f"INCV{channel}\n")

    def increase_channel_voltage_with_verify(self, channel: int) -> str:
        """
        Implemented command: INCV<N>V

        Increment the output<N> voltage by step size, with verify.
        """
        self._device.send_command(f"INCV{channel}V\n")
        return self._device.receive_output()

    def decrease_channel_voltage(self, channel: int) -> None:
        """
        Implemented command: DECV<N>

        Decrement the output<N> voltage by step size.
        """
        self._device.send_command(f"DECV{channel}\n")

    def decrease_channel_voltage_with_verify(self, channel: int) -> str:
        """
        Implemented command: DECV<N>V

        Decrement output<N> voltage by step size, with verify.
        """
        self._device.send_command(f"DECV{channel}V\n")
        return self._device.receive_output()

    def increase_channel_current(self, channel: int) -> None:
        """
        Implemented command: INCI<N>

        Increment the output<N> current limit by step size.
        """
        self._device.send_command(f"INCI{channel}\n")

    def decrease_channel_current(self, channel: int) -> None:
        """
        Implemented command: DECI<N>

        Decrement the output<N> current limit by step size.
        """
        self._device.send_command(f"DECI{channel}\n")

    def set_channel(self, channel: int, value: int) -> None:
        """
        Implemented command: OP<N> <NRF>

        Set output<N> on/off where <NRF> has the following meaning:
        0=OFF, 1=ON.
        """
        self._device.send_command(f"OP{channel} {value}\n")

    def enable_channel(self, channel: int) -> None:
        """
        Enable an output channel.
        """
        self.set_channel(channel, 1)

    def disable_channel(self, channel: int) -> None:
        """
        Disable an output channel.
        """
        self.set_channel(channel, 0)

    def get_channel_status(self, channel: int) -> str:
        """
        Implemented command: OP<N>?

        Returns output<N> on/off status.
        The response is <NR1><RMT> where 1 = ON, 0 = OFF.
        """
        self._device.send_command(f"OP{channel}?\n")
        return self._device.receive_output()

    def set_all(self, value: int) -> None:
        """
        Implemented command: OPALL <NRF>

        By default simultaneously sets all outputs on/off where <NRF> has
        the following meaning: 0=ALL OFF, 1=ALL ON. However this
        behaviour can be changed to turn the outputs on or off in a timed
        sequence or to omit an output entirely. See section 9.4 for an
        explanation.
        """
        self._device.send_command(f"OPALL {value}\n")

    def enable_all(self) -> None:
        """
        Enable all output channels.
        """
        self.set_all(1)

    def disable_all(self) -> None:
        """
        Disable all output channels.
        """
        self.set_all(0)

    def reset_trip(self) -> None:
        """
        Implemented command: TRIPRST

        Attempt to clear all trip conditions.
        """
        self._device.send_command("TRIPRST\n")

    def set_channel_voltage_range(self, channel: int, value: int) -> None:
        """
        Implemented command: VRANGE<N><NRF>

        Set output<N> voltage range to <NRF> where <NRF> has the
        following meaning:
        Output1: 1= 16V/6A, 2 = 35V/3A.
        Output2: 1= 35V/3A, 2 = 16V/6A, 3 = 35V/6A.
        Output3: 1= 35V/3A, 2 = 70V/1.5A, 3 = 70V/3A.
        """
        self._device.send_command(f"VRANGE{channel} {value}\n")

    def get_channel_voltage_range(self, channel: int) -> str:
        """
        Implemented command: VRANGE<N>?

        Returns the voltage range for output<N>. The response is
        <NR1><RMT> where <NR1> has the following meaning:
        Output1: 1= 16V/6A, 2 = 35V/3A.
        Output2: 1= 35V/3A, 2 = 16V/6A, 3 = 35V/6A.
        Output3: 1= 35V/3A, 2 = 70V/1.5A, 3 = 70V/3A.
        """
        self._device.send_command(f"VRANGE{channel}?\n")
        return self._device.receive_output()

    def set_voltage_tracking_mode(self, value: int) -> None:
        """
        Implemented command: CONFIG <NRF>

        Sets the voltage tracking mode of the unit to <NRF> where <NRF>
        has the following meaning:
        0 = None.
        1 = Mode1.
        2 = Mode2.
        3 = Mode3.
        These modes are as defined within the Setting Voltage Tracking
        section of this manual see section 9.1.
        """
        self._device.send_command(f"CONFIG {value}\n")

    def get_voltage_tracking_mode(self) -> str:
        """
        Implemented command: CONFIG?

        Returns the voltage tracking mode of the unit. The response is
        <NR1><RMT>, where <NR1> has the following meaning:
        0 = None.
        1 = Mode1.
        2 = Mode2.
        3 = Mode3.
        These modes are as defined within the Setting Voltage Tracking
        section of this manual see section 9.1.
        """
        self._device.send_command("CONFIG?\n")
        return self._device.receive_output()

    def set_channel_on_delay(self, channel: int, value: int) -> None:
        """
        Implemented command: ONDELAY<N> <NRF>

        Set output<N> Multi-On delay where <NRF> is in milliseconds
        """
        self._device.send_command(f"ONDELAY{channel} {value}\n")

    def set_channel_off_delay(self, channel: int, value: int) -> None:
        """
        Implemented command: OFFDELAY<N> <NRF>

        Set output<N> Multi-Off delay where <NRF> is in milliseconds
        """
        self._device.send_command(f"OFFDELAY{channel} {value}\n")

    def set_channel_on_action(self, channel: int, value: str) -> str:
        """
        Implemented command: ONACTION<N> <CPD>

        Set output<N> Multi-On action where <CPD> can be QUICK, NEVER
        or DELAY.
        """
        self._device.send_command(f"ONACTION{channel} {value}\n")
        return self._device.receive_output()

    def set_channel_off_action(self, channel: int, value: str) -> str:
        """
        Implemented command: OFFACTION<N> <CPD>

        Set output<N> Multi-Off action where <CPD> can be QUICK, NEVER
        or DELAY.
        """
        self._device.send_command(f"OFFACTION{channel} {value}\n")
        return self._device.receive_output()

    def save_channel_settings(self, channel: int, value: int) -> str:
        """
        Implemented command: SAV<N> <NRF>

        Save the current settings of output<N> to the store specified by
        <NRF> where <NRF> can be 0-49.
        """
        self._device.send_command(f"SAV{channel} {value}\n")
        return self._device.receive_output()

    def recall_channel_settings(self, channel: int, value: int) -> str:
        """
        Implemented command: RCL<N> <NRF>

        Recall the settings for output<N> from the store specified by <NRF>
        where <NRF> can be 0-49.
        """
        self._device.send_command(f"RCL{channel} {value}\n")
        return self._device.receive_output()

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
        self._device.send_command(f"*SAV {memory_store}\n")

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
        self._device.send_command(f"*RCL {memory_store}\n")

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
        self._device.send_command(f"LSE{register_number} {limit}\n")

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
        self._device.send_command(f"*SRE {value}\n")

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
        self._device.send_command(f"*PRE {value}\n")

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
        self._device.send_command(f"IFLOCK {state}\n")

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
        self._device.send_command(f"NETCONFIG {config_type}\n")

    def set_ip_address(self, address: str) -> None:
        """
        Implemented command: IPADDR <QUAD>

        Sets the potential static IP address of the LAN interface (as on the
        webpage).
        The parameter must be strictly a dotted quad for the IP address, with each
        address part an <NR1> in the range 0 to 255, (e.g. 192.168.1.101).
        """
        self._device.send_command(f"IPADDR {address}\n")

    def set_netmask(self, address: str) -> None:
        """
        Implemented command: NETMASK <QUAD>

        Sets the netmask to accompany the static IP address of the LAN interface.
        The parameter must be strictly a dotted quad for the netmask, with each
        part an <NR1> in the range 0 to 255, (e.g. 255.255.255.0).
        """
        self._device.send_command(f"NETMASK {address}\n")
