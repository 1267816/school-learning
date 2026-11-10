#include <stdio.h>

int main(void) {
	int a[15]={1,3,5,7,9,10,12,14,16,18,21,23,25,27,29};
	int n;
	scanf("%d",&n);
	
	int left=0;
	int right=14;
	int isfound=0;
	int result;
	
	while (left<right+1) {
		int mid=(left+right)/2;
		if (n==a[mid]) {
			isfound=1;
			result=mid+1;
			break;
		} else if (n>a[mid]) {
			left=mid+1;
		} else {
			right=mid-1;
		}
	}
	
	if (isfound) {
		printf("%d",result);
	} else {
		printf("不在表中");
	}
	
	return 0;
}