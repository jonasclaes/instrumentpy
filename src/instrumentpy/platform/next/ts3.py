# Copyright 2022 Jonas Claes
# SPDX-License-Identifier: Apache-2.0
# pylint: disable=R0904
# pylint: disable=R0913
"""Definition for the TS3 platform made by Neways / NEXT"""
import datetime
import time
from crc import Configuration, CrcCalculator
from instrumentpy.common.common_device_interface import CommonDeviceInterface


class TS3Error(Exception):
    """
    Generic TS3 exception to use for all error messages from the platform.
    """


class TS3():
    """
    TS3 supports serial over USB and TCP/IP communications.

    At the moment, only TCP/IP communications are implemented.
    """
    _device: CommonDeviceInterface = None

    # CRC configuration
    width = 16  # bits
    poly = 0x8005  # Polynomial
    init_value = 0xFFFF  # Init value
    final_xor_value = 0x0000  # Final XOR value
    reverse_input = True  # Input reflection
    reverse_output = True  # Output reflection

    crc_configuration = Configuration(
        width, poly, init_value, final_xor_value, reverse_input, reverse_output)
    crc_calculator = CrcCalculator(crc_configuration, False)

    def __init__(self, device: CommonDeviceInterface) -> None:
        self._device = device

    def _calc_crc(self, data):
        result = self.crc_calculator.calculate_checksum(data)
        result = f"{result:04X}"
        return result[2:] + result[:2]

    def _build_cmd(self, *args):
        command_format = "${:03d};{:s};{:s}"
        command = command_format.format(0, ";".join(args), "0000")
        checksum = self._calc_crc(command.encode())
        cmd = command_format.format(len(command), ";".join(args), checksum)
        return cmd.encode() + "\r".encode()

    def _send_command(self, *args):
        command = self._build_cmd(*args)
        self._device.send_command(command)

    def _get_command_response(self, expected_command):
        response = self._device.receive_output(512).decode()
        response_array = response.split(";")

        if response_array[1] == "2":
            self._handle_nack_response(response_array)

        if response_array[1] == expected_command:
            return response_array

        raise TS3Error(-1)

    def _handle_nack_response(self, response_array):
        if response_array[2] == "1":
            raise TS3Error("Unknown command")

        if response_array[2] == "2":
            raise TS3Error(
                "Parameter out of range. \
                        One or more of the parameters are outside the range.")

        if response_array[2] == "3":
            raise TS3Error(
                "Busy. The unit is busy and cannot handle communications.")

        if response_array[2] == "4":
            raise TS3Error(
                "Not logged in. \
                        The command that has been sent requires a correct login.")

        if response_array[2] == "5":
            raise TS3Error(
                "Command not yet implemented. \
                        The command is known, but the implementation is not yet done.")

        if response_array[2] == "6":
            raise TS3Error(
                "Message structure incorrect. \
                        One or more parts of the message are incorrect \
                            (BOR, EOR, CRC, Length etc).")

        if response_array[2] == "7":
            raise TS3Error(
                "Incorrect number of parameters for this command.")

        if response_array[2] == "8":
            raise TS3Error("ID not found.")

        if response_array[2] == "9":
            raise TS3Error(
                "Internal error. \
                        The command could not be executed due to internal problems.")

        if response_array[2] == "10":
            raise TS3Error(
                "Booting. \
                        The unit is still booting and cannot handle communications at this time.")

        if response_array[2] == "11":
            raise TS3Error("DUT not present.")

        raise TS3Error(response_array[2])

    def poll_device(self):
        """
        Check if the unit is alive and kicking. If it is, it will send an ACK.
        """
        self._send_command("10")
        self._get_command_response("1")

    def get_version(self):
        """
        Ask for the current software version. The software version can be used to check if new
        commands are implemented yet.
        """
        self._send_command("13")
        response = self._get_command_response("13")
        return (f"{response[2]}.{response[3]}", response[4])

    def reset_device(self):
        """
        Reset the processor.
        """
        self._send_command("14")
        self._get_command_response("1")

    def get_product_id(self):
        """
        Get the product ID (article number) and product name.
        """
        self._send_command("15")
        response = self._get_command_response("15")
        return (response[2], response[3])

    def get_svn(self):
        """
        Get the SVN repository information regarding the unit.
        """
        self._send_command("16")
        response = self._get_command_response("16")
        return (response[2], response[3])

    def set_supply(self, supply=False, on_off=False):
        """
        Switch a major supply on or off.
        """
        self._send_command("22", str(int(supply)), str(int(on_off)))
        self._get_command_response("1")

    def set_buzzer(self, on_off=False):
        """
        Beep the on board buzzer.
        """
        self._send_command("23", str(int(on_off)))
        self._get_command_response("1")

    def set_dut_power(self, dut_power=False, dut_enable=False, overrule=False):
        """
        Set the DUT power.
        """
        self._send_command("24", str(int(dut_power)), str(
            int(dut_enable)), str(int(overrule)))
        self._get_command_response("1")
        time.sleep(0.5)

    def get_dut_present(self):
        """
        Get DUT detection switch state.
        """
        self._send_command("25")
        response = self._get_command_response("25")
        return response[2] == "1"

    def get_power_supply(self, power_supply=0):
        """
        Get the current power supply voltages.
        """
        self._send_command("26", str(int(power_supply)))
        response = self._get_command_response("26")
        return response[2] == "1"

    def get_dut_power(self):
        """
        Get DUT power relay states.
        """
        self._send_command("27")
        response = self._get_command_response("1")
        return (response[2] == "1", response[3] == "1")

    def set_dig_output_pin(self, module=0, pin=1, value=False):
        """
        Switch a digital output pin (or relay) on or off.
        """
        self._send_command("40", str(int(module)),
                           str(int(pin)), str(int(value)))
        self._get_command_response("1")

    def get_dig_input_pin(self, module=0, pin=1):
        """
        Read the state of a digital input pin.
        """
        self._send_command("41", str(int(module)), str(int(pin)))
        response = self._get_command_response("41")
        return response[2] == "1"

    def set_ana_output_pin(self, module=0, pin=1, value=0.0):
        """
        Set an analog output pin.
        """
        self._send_command("42", str(int(module)),
                           str(int(pin)), str(float(value)))
        self._get_command_response("1")

    def get_ana_input_pin(self, module=0, pin=1, input_range=0):
        """
        Read the value of an analog input pin.
        """
        self._send_command("43", str(int(module)),
                           str(int(pin)), str(int(input_range)))
        response = self._get_command_response("43")
        return float(response[2])

    def set_pwm_pin(self, frequency=1, duty_cycle=100):
        """
        Set the PWM pin on the main board.
        """
        self._send_command("44", str(int(frequency)), str(int(duty_cycle)))
        self._get_command_response("1")

    def get_user_highlow_input_pin(self, module=0, pin=1, high_low=0, timeout=5):
        """
        Wait for a PIN to transition for high to low (or vice versa).
        """
        self._send_command("45", str(int(module)), str(
            int(pin)), str(int(high_low)), str(int(timeout)))
        response = self._get_command_response("45")
        return response[2] == "1"

    def get_diff_ana_input_pin(
        self,
        module_a=0,
        pin_a=1,
        range_a=0,
        delay=0,
        module_b=0,
        pin_b=1,
        range_b=0
    ):
        """
        Read the value of two analog input pins with a specified delay in between
        (can be 0) and subtract the result. This leads to a differential measurement.
        """
        self._send_command("46", str(int(module_a)), str(int(pin_a)), str(
            int(range_a)), str(int(delay)), str(int(module_b)), str(int(pin_b)), str(int(range_b)))
        response = self._get_command_response("46")
        return float(response[2])

    def uart_txd(self, module=0, port=0, message=""):
        """
        Transmit a message on an UART port.
        """
        self._send_command("100", str(int(module)),
                           str(int(port)), str(message))
        self._get_command_response("1")

    def uart_rxd(self, module=0, port=0):
        """
        Receive a message from an UART port.
        """
        self._send_command("101", str(int(module)), str(int(port)))
        response = self._get_command_response("101")
        return response[2]

    def uart_set(self, module=0, port=0, baudrate=9600, databits=8, stopbits=1, parity=5):
        """
        Configures an UART port.
        """
        self._send_command("102", str(int(module)), str(int(port)), str(
            int(baudrate)), str(int(databits)), str(int(stopbits)), str(int(parity)))
        self._get_command_response("1")

    def uart_flush(self, module=0, port=0):
        """
        Flush any received bytes of an UART port.
        """
        self._send_command("103", str(int(module)), str(int(port)))
        self._get_command_response("1")

    def i2c_txd(self, module=0, port=0, i2c_address=0, message=""):
        """
        Transmit a message on an I2C port.
        """
        self._send_command("140", str(int(module)), str(
            int(port)), str(int(i2c_address)), str(message))
        self._get_command_response("1")

    def i2c_rxd(self, module=0, port=0, i2c_address=0, rxd_number_of_bytes=1, message=""):
        """
        Receive a message from an I2C port.
        """
        self._send_command("141", str(int(module)), str(int(port)), str(
            int(i2c_address)), str(int(rxd_number_of_bytes)), str(message))
        response = self._get_command_response("141")
        return response[2]

    def get_date(self):
        """
        Get the configuration date.
        """
        self._send_command("80")
        response = self._get_command_response("80")
        return (response[2], response[3], response[4], response[5], response[6], response[7])

    def set_date(self, year=None, month=None, day=None, hour=None, minute=None, second=None):
        """
        Set the configuration date.
        """
        now = datetime.datetime.now()
        if year is None:
            year = now.year
        if month is None:
            month = now.month
        if day is None:
            day = now.day
        if hour is None:
            hour = now.hour
        if minute is None:
            minute = now.minute
        if second is None:
            second = now.second
        self._send_command("81", str(int(year)), str(int(month)), str(
            int(day)), str(int(hour)), str(int(minute)), str(int(second)))
        self._get_command_response("1")

    def get_user(self):
        """
        Get the name of the user that configured this fixture.
        """
        self._send_command("82")
        response = self._get_command_response("82")
        return response[2]

    def set_user(self, username=""):
        """
        Set the name of the user that configured this fixture.
        """
        self._send_command("83", str(username))
        self._get_command_response("1")

    def get_script_filename(self):
        """
        Get the name of the script that is to be used.
        """
        self._send_command("84")
        response = self._get_command_response("84")
        return response[2]

    def set_script_filename(self, script_file_name=""):
        """
        Set the name of the script that is to be used.
        """
        self._send_command("85", str(script_file_name))
        self._get_command_response("1")

    def get_id(self):
        """
        Get the project number and class of the base article that can be tested with this fixture.
        """
        self._send_command("86")
        response = self._get_command_response("86")
        return (response[2], response[3])

    def set_id(self, project_number=0, class_number=0):
        """
        Set the project number and class of the base article that can be tested with this fixture.
        """
        self._send_command("87", str(int(project_number)),
                           str(int(class_number)))
        self._get_command_response("1")

    def get_external_modules(self):
        """
        Get a list of the detected modules in the fixture.
        """
        self._send_command("88")
        response = self._get_command_response("88")
        return tuple(response[i] for i in range(2, 18))

    def get_external_module_details(self, module=0):
        """
        Get more information on the detected module.
        """
        self._send_command("89", str(int(module)))
        response = self._get_command_response("89")
        return (response[2], response[3])

    def firmware_line(self, mhx_file_line=""):
        """
        Receive a single line from the MHX file.
        The line is decoded and the data is stored in RAM.
        The line should be from a Motorola HEX file.
        """
        self._send_command("200", str(mhx_file_line))
        self._get_command_response("1")

    def perform_flash(self):
        """
        When all line have been transmitted, this command copy
        the contents in RAM to the flash and restart the firmware.
        During the copy, no communication with the TS3 firmware is possible.
        The ACK is transmitted before the communication is lost.
        """
        self._send_command("201")
        self._get_command_response("1")
