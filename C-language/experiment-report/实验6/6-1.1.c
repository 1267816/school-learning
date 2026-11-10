#include <stdio.h>

double fun(int m) {
	double y=1.0;
	int i;
	for (i=2;i<=m;i++) {
		y-=1.0/(i*i);
	}
	return y;
}

int main() {
	int n=5;
	printf("\nThe result is %lf\n",fun(n));
	return 0;
}