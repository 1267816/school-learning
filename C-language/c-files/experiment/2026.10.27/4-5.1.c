#include <stdio.h>

int main() {
	int a=1;
	int b=0;
	int c=0;
	
	while (a<=9) {
		int a3=a;
		int b3=b;
		int c3=c;
		for (int i=0;i<2;i++) {
			a3*=a;
			b3*=b;
			c3*=c;
		}
		if ((a*100+b*10+c)==(a3+b3+c3)) {
			printf("%d%d%d\n",a,b,c);
		}
		c++;
		if (c==10) {
			c=0;
			b++;
		}
		if (b==10) {
			b=0;
			a++;
		}
	}
	
	return 0;
}