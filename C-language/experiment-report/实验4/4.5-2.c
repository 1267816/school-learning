#include <stdio.h>
int main() {
	for (int i=100;i<1000;i++) {
		int a;
		int b;
		int c;
		int temp=i;
		c=temp%10;
		temp/=10;
		b=temp%10;
		temp/=10;
		a=temp;
		int a3=a*a*a;
		int b3=b*b*b;
		int c3=c*c*c;
		if (i==a3+b3+c3) {
			printf("%d\n",i);
		}
	}
	
	return 0;
}