#include <stdio.h>

int main () {
	int bottlesCount;

	freopen("99bottles.in", "r", stdin);
	freopen("99bottles.out", "w", stdout);

	scanf("%d", &bottlesCount);

	for (; bottlesCount; -- bottlesCount) {
		printf("%d bottles of vodka on the wall\n", bottlesCount);
		printf("%d bottles of russian vodka\n", bottlesCount);
		printf("Take on down, pass it around\n");
		printf("%d bottles of vodka on the wall\n\n", bottlesCount - 1);
	}

	return 0;
}
