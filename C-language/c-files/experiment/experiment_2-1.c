//สตั้2.1 
#include <stdio.h>
int main()
{	
	double r,c,area; 
	double p=3.14;
	printf("input r: ");
	scanf("%lf",&r);
	c=2*p*r;
	area=p*r*r;
	printf("c=%-7.2f,area=%-7.2f",c,area); 
	return 0;
}

