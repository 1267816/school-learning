#include <stdio.h>
int main() {
	int x=1;
	int sum=0;
	while (x<=100) {
		sum+=x;
		x++;
	}
	printf("%d",sum);
	
	return 0;
}