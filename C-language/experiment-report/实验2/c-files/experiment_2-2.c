#include <stdio.h>
#include <math.h>
int main(){
	double a,b,c;
	double s,S,t;
	
	scanf("%lf %lf %lf",&a,&b,&c);
	
	s=0.5*(a+b+c);
	S=sqrt(s*(s-a)*(s-b)*(s-c));
	
	printf("%.2f",S);
	
	return 0;
}
