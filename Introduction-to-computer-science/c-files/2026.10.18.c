#include <stdio.h>

int main(void) {
	int n;
	scanf("%d",&n);
	
	int a[32]={0};
	int i;
	
	i=0;
	if (n==0) {
		printf("0\n");
	} else {
		while (n>0) {
			a[i]=n%2;
			n/=2;
			i++;
		}
	
		i=31;
		while (a[i]==0) {
			i--;
		}
	
		for (;i>=0;i--) {
			printf("%d",a[i]);
		}
		printf("\n");
	}
	
	
	return 0;
}