#include <stdio.h>

int f(int m) {
	int k=2;
	k++;
	return k+m;
}

int main() {
	int s;
	s=f(2);
	printf("%d %d\n",s,f(s));
	return 0;
}