#include <stdio.h>

#define SWAP(x,y) {int temp=x;x=y;y=temp;}

int main(void) {
	int a,b;
	scanf("%d %d",&a,&b);
	printf("a=%d b=%d\n",a,b);
	SWAP(a,b);
	printf("a=%d b=%d\n",a,b);
	return 0;
}