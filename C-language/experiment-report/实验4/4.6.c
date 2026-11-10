#include <stdio.h>

int main() {
	for (int i=100;i<201;i++) {
		if (i%3==0) {
			continue;
		}
		printf("%d\n",i);
	}
	
	return 0;
}