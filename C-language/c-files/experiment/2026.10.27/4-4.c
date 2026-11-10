#include <stdio.h>
int main() {
	char ch;
	int cnt=0;
	while ((ch=getchar())!=EOF&&ch!='\n') {
		if (ch=='m'||ch=='M') {
			cnt++;
		}
	}
	printf("%d",cnt);
	
	return 0;
}