#include <stdio.h>

int main() {
	int score;
	scanf("%d",&score);
	
	if (score<0||score>100) {
		printf("输入数据错");
	} else if (score>=90) {
		printf("A");
	} else if (score>=80) {
		printf("B");
	} else if (score>=70) {
		printf("C");
	} else if (score>=60) {
		printf("D");
	} else if (score>=0){
		printf("E");
	}
	
	return 0;
}