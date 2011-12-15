#!/usr/bin/env pike
#!/usr/bin/env pike
import Stdio;

int main () {
    int a, b;
    sscanf(Stdio.read_file("adunare.in"), "%d%d", a, b);
    Stdio.write_file("adunare.out", (string)(a + b));
    return 0;
}
