# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_tt_um_example(dut):

    dut._log.info( "Beginning")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
     # resetting and disabling inputs to ensure counter starts at 0
    dut.rst_n.value = 0
    dut.ui_in.value = 0    
    dut.uio_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    dut._log.info("Counter should now be 0")
    assert dut.uio_out.value == 0
    assert dut.uo_out.value == 0
    dut._log.info("checked if it became 0")
    dut._log.info("Setting OE to 1 to enable outputs")
    
    dut.ui_in.value = 0b1   
    start_val = int(dut.uio_out.value)
    await ClockCycles(dut.clk, 5) 
    expected_val = (start_val + 5) & 0xFF
    assert dut.uio_out.value == expected_val #checking if values match what w eexpect
    
    dut._log.info(f"value of the counter currently {int(dut.uio_out.value)}")

    dut.ui_in.value = 0b0   # setting OE to 0 load enabling to 0
    await ClockCycles(dut.clk, 1)
    assert dut.uio_oe.value == 0
    dut._log.info("Tri-state disable check passed (uio_oe=0).")
    dut.ui_in.value = 0b1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == dut.uio_out.value


    dut._log.info("Passed tests")
