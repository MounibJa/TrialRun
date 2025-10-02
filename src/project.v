`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // [0]=load, [1]=OE
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,

    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    reg [7:0] counts;

    wire load     = ui_in[0]; // load enable
    
    wire oecrtl = ui_in[1]; // crtl if oe is being toggled or not
    
    always @(negedge rst_n or posedge clk) begin
        if(!rst_n) begin
            counts <= 8'd0;
        end else if(load & !oecrtl) begin
            counts <= uio_in;       // load the value
        end else begin
            counts <= counts + 1;   // increment if no load
        end
    end

    assign uio_out = counts;
    assign uio_oe  = {8{oecrtl}};    // drive UIO only when OE=1
    assign uo_out = oecrtl ? 8'bz : counts;


    wire _unused = &{ena, ui_in[7:2], 1'b0};

endmodule
