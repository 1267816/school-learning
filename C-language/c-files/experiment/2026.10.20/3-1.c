#include <stdio.h>

int main(void) {
	char c1;
	char c2;
	c1=((char)getchar());
	getchar();
	c2=((char)getchar());
	printf("%c\n",c1);
	printf("%c\n",c2);
	printf("===\n");
	putchar((int)c1);
	putchar('\n');
	putchar((int)c2);
	putchar('\n');
	
	return 0;
}