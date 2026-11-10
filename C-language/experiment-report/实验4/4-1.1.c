#include <stdio.h>
int main() {
	int x=-1;
	do
	{
		x=x*x;
	} while (!x);
	printf("%=%d\n",x);
	return 0;
}