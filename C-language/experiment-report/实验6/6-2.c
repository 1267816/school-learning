#include <stdio.h>

int isPrime(int x) {
	int ret=1;
	for (int i=2;i*i<=x;i++) {
		if (x%i==0) {
			ret=0;
			break;
		}
	}
	if (x==1) {
		ret=0;
	}
	return ret;
}

int main(void) {
	int x;
	scanf("%d",&x);
	
	if (isPrime(x)==1) {
		printf("yes\n");
	} else {
		printf("no\n");
	}
	return 0;
}