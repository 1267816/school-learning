#include <stdio.h>

void swap(int *pa,int *pb) {
	int t;
	t=*pa;
	*pa=*pb;
	*pb=t;
}

int main(void) {
	int a[10];
	int i;
	for (i=0;i<10;i++) {
		scanf("%d",&a[i]);
	}
	
	for (i=0;i<10;i++) {
		int max=a[0];
		int k=0;
		for (int j=0;j<10-i;j++) {
			if (a[j]>max) {
				max=a[j];
				k=j;
			}
		}
		swap(&a[k],&a[9-i]);
	}
	
	for (i=0;i<10;i++) {
		printf("%-4d",a[i]);
	}
	
	return 0;
}