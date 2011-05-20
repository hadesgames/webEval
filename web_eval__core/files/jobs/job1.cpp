#include <stdio.h>
#include <math.h>
#include <string.h>

long i, v1[128], v2[128], vr[128], len;
char n1[128], n2[128];

void adun(long *v1, long *v2) {
	long ipr = 0, t = 0;
	for (ipr = 1; ipr <= v1[0] || ipr <= v2[0]; ++ipr) {
		t = t + v1[ipr] + v2[ipr];
		v1[ipr] = t % 10;
		t /= 10;
	}
	v1[0] = ipr - 1;
}

void show(long *v1) {
	for (long ipr = v1[0]; ipr >= 1; --ipr) {
		printf("%ld", v1[ipr]);
	}
}

int main() {
	freopen("adunare.in", "r", stdin);
	freopen("adunare.out", "w", stdout);
	gets(n1);
	len = strlen(n1);
	for (i = 0; i < len; ++i) {
		v1[len - i] = (long)(n1[i] - '0');
	}	
	v1[0] = len;
	gets(n2);
	len = strlen(n2);
	for (i = 0; i < len; ++i) {
		v2[len - i] = (long)(n2[i] - '0');
	}
	v2[0] = len;
	adun(vr, v1);
	adun(vr, v2);
	show(vr);
	return 0;
}
