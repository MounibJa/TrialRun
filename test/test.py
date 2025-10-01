# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_tt_um_example(dut):

    dut._log.info("starting")

    # Setting clock value
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    # Setting counter to 0
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    # now our bit counter should have a value of 0
    assert dut.uio_out.value == 0
    assert dut.uo_out.value == 0

    # Loading a value (load=1, OE=0)
    dut.ui_in.value = 0b01
    dut.uio_in.value = 101
    await ClockCycles(dut.clk, 2)
    assert dut.uio_out.value == 101, f"value should 101, got {int(dut.uio_out.value)}"
    assert dut.uo_out.value == 0, f"OE=0 so output should be 0, got {int(dut.uo_out.value)}"
    assert dut.uio_oe.value == 0, f"OE pin should be 0, got {int(dut.uio_oe.value)}"

    # Increment 5 cycles with OE=0
    dut.ui_in.value = 0b00
    await ClockCycles(dut.clk, 5)
    expected = (101 + 5) & 0xFF
    assert dut.uio_out.value == expected
    assert dut.uo_out.value == 0
    assert dut.uio_oe.value == 0

    # Enable outputs, no load
    dut.ui_in.value = 0b10
    await ClockCycles(dut.clk, 1)
    assert dut.uio_oe.value == 0xFF
    assert dut.uo_out.value == dut.uio_out.value

    # Increment 3 cycles with OE=1
    await ClockCycles(dut.clk, 3)
    expected = (expected + 3) & 0xFF
    assert dut.uio_out.value == expected
    assert dut.uo_out.value == expected

    # Disable outputs
    dut.ui_in.value = 0b00
    await ClockCycles(dut.clk, 1)
    assert dut.uio_oe.value == 0
    assert dut.uo_out.value == 0

    # Reset counter again
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == 0
    assert dut.uo_out.value == 0

    dut._log.info("all tests were passed")
