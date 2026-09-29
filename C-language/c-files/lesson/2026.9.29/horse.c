#include <stdio.h>
int main(){
	int a,b,c,sum;
	for (a=0;a<=34;a++) {
		for (b=0;b<=50;b++) {
			sum=5*a+3*b;
			c=100-a-b;
			if (sum==100) {
				printf("%d,%d,%d\n",a,b,c);
			}
		}
		b=1;
	}
	return 0;
}