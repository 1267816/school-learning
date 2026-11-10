#include <stdio.h>

int main() {
	long long product=1;
	long long sum=0;
	for (int i=1;i<=20;i++) {
		product*=i;
		sum+=product;
	}
	printf("%lld",sum);
	
	return 0;
}