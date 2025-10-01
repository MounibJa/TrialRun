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
    #now our bit counter should have a value of 0
    assert dut.uio_out.value == 0
    assert dut.uo_out.value == 0

    # enable outputs and count
    dut.ui_in.value = 1
    start_val = int(dut.uio_out.value)
    await ClockCycles(dut.clk, 5)
    expected = (start_val + 5) & 0xFF
    assert dut.uio_out.value == expected
    assert dut.uo_out.value == expected

    # disable outputs
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uio_oe.value == 0
    assert dut.uo_out.value == 0

    # re-enable outputs
    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uio_oe.value == 0xFF
    assert dut.uo_out.value == dut.uio_out.value

    # resetting again
    dut.rst_n.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uio_out.value == 0
    assert dut.uo_out.value == 0
    
    dut._log.info("all tests were passed")
