program adun;

var a, b : longint;
    
begin

    assign(input, 'adunare.in'); reset(input);
    assign(output, 'adunare.out'); rewrite(output);

    read(a, b);
    writeln (a + b);

    close(input);
    close(output);
end.
