#include <stdio.h>
int main() {
	int x=1;
	int sum=0;
	do
	{
		sum+=x;
	} while (++x<=100);
	printf("%d",sum);
	
	return 0;
}