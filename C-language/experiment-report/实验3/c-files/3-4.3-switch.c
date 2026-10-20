#include <stdio.h>

int main() {
	int score;
	scanf("%d",&score);
	
	int tens=score/10;
	switch (tens) {
		case 10:
			switch (score==100) {
				case 1:
					printf("A");
					break;
				case 0:
					printf("输入数据错");
					break;
			}
			break;
		case 9:
			printf("A");
			break;
		case 8:
			printf("B");
			break;
		case 7:
			printf("C");
			break;
		case 6:
			printf("D");
			break;
		case 5:
		case 4:
		case 3:
		case 2:
		case 1:
		case 0:
			switch (score>=0) {
				case 1:
					printf("E");
					break;
				case 0:
					printf("输入数据错");
					break;
			}
			break;
		default:
			printf("输入数据错");
			break;
	}
	
	return 0;
}