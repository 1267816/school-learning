#include <stdio.h>

void swap(int *pa,int *pb) {
	int t;
	t=*pa;
	*pa=*pb;
	*pb=t;
}

int main(void) {
	int a[3][4]={
		{5,2,8,9},
		{4,1,7,3},
		{6,0,2,1}
	};
	int i,j;
	printf("原矩阵：\n");
	for (i=0;i<3;i++) {
		for (j=0;j<4;j++) {
			printf("%-4d",a[i][j]);
		}
		printf("\n");
	}
	for (i=0;i<3;i++) {
		int k=0;
		for (j=0;j<4;j++) {
			if (a[i][j]<a[i][k]) {
				k=j;
			}
		}
		swap(&a[i][0],&a[i][k]);
	}
	printf("变换后矩阵：\n");
	for (i=0;i<3;i++) {
		for (j=0;j<4;j++) {
			printf("%-4d",a[i][j]);
		}
		printf("\n");
	}
	return 0;
}