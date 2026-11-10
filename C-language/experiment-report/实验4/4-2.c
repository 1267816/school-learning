#include <stdio.h>
int main()
{
	double x,amax,amin;
	scanf("%lf",&x);
	amax=x;
	amin=x;
	while (x>=0) {
		if (x>amax) {
			amax=x;
		}
		if (x<amin) {
			amin=x;
		}
		scanf("%lf",&x);
	}
	printf("amax=%f\namin=%f\n",amax,amin);
	return 0;
}