// สตั้1-2 

#include <stdio.h>
int main(){
	int max(int x,int y);
	int a=0;
	int b=0;
	int c=0;
	int m=0;
	scanf("%d %d %d",&a,&b,&c);
	m=max(a,max(b,c));
	printf("%d",m);
	return 0;
}

int max(int x,int y){
	int z;
	if (x>=y) {
		z=x;
	} else {
		z=y;
	}
	return(z);
}
