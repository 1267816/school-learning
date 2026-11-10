#include <stdio.h>
int main()
{
	int a[3][3]={{1,3,6},{7,9,11},{14,15,17}},i,j,sum=0;
	for(i=0;i<3;i++) {
		for(j=0;j<3;j++) {
			printf("%5d",a[i][j]);
			}
		printf("\n");
	}
	for(i=0;i<3;i++) {
		sum=sum+a[i][i];
	}
	printf("主对角线元素之和为%d\n",sum);//结果是27
	return 0;
}
