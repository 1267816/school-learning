#include <stdio.h>
int main()
{
	int i;
	int fib[12] = {1, 1}; /* 数组初始化*/
	for ( i = 2; i < 12; i++ )
	{
		fib[i] = fib[i - 1] +fib[i-2];
	}
	for ( i = 0;i<12; i++ )
	{
		printf ( "%d\t", fib[i] );
		if ((i+1)%4 == 0 )       /* 4个数换行*/
		{
			printf("\n");
		}
	}
	return 0;
}
