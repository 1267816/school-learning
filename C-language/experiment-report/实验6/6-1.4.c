#include <stdio.h>

int M(int x,int y,int z)
{
	int p;
	p=x*y+z;
	return (p);
}

int main() {
	int a=1,b=2,c=3;
	printf("%d\n",M(a+b,b+c,c+a));
	return 0;
}