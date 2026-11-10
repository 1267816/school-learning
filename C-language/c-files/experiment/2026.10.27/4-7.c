#include <stdio.h>

int main() {
	for (int i=100;i<=200;i++) {
		int isprime=1;
		for (int j=2;j*j<=i;j++) {
			if (i%j==0) {
				isprime=0;
				break;
			}
		}
		if (isprime==1) {
			printf("%d\n",i);
		}
	}
	return 0;
}