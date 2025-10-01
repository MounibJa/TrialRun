/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)

    
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
    reg [7:0] counts;

    wire out_ena = ui_in[0];
    
    always @(negedge rst_n or posedge clk) begin
        if(!rst_n) begin
            counts<= 8'd0;
        end  else if( out_ena & !) begin
            counts <= counts+ 1'd1;
            
        end
    end
    
  // All output pins must be assigned. If not used, assign to 0.

    
  assign uio_out = counts;
  assign uio_oe  = {8{out_ena}};
  assign uo_out = out_ena ? counts : 8'b0;

  // List all unused inputs to prevent warnings
    wire _unused = &{ena, uio_in, ui_in[7:1], 1'b0};

endmodule
