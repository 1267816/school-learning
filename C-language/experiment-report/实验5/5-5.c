#include <stdio.h>

int main(void) {
	int a[10]={45,12,89,5,33,77,21,60,8,99};
	int b[11];
	int i,j;
	
	for (i=0;i<10;i++) {
		for (j=0;j<9-i;j++) {
			if (a[j]>a[j+1]) {
				int t=a[j];
				a[j]=a[j+1];
				a[j+1]=t;
			}
		}
	}
	
	for (i=0;i<10;i++) {
		printf("%d",a[i]);
		if (i==9) {
			printf("\n");
		} else {
			printf(" ");
		}
	}
	
	int n;
	scanf("%d",&n);
	for (i=0;i<10;i++) {
		b[i]=a[i];
	}
	b[10]=n;
	
	for (i=0;i<11;i++) {
		for (j=0;j<10-i;j++) {
			if (b[j]>b[j+1]) {
				int t=b[j];
				b[j]=b[j+1];
				b[j+1]=t;
			}
		}
	}
	
	for (i=0;i<11;i++) {
		printf("%d",b[i]);
		if (i==10) {
			printf("\n");
		} else {
			printf(" ");
		}
	}
	
	return 0;
}