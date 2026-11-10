#include <stdio.h>

int main() {
	int ch;
	int englishcnt=0;
	int spacecnt=0;
	int numbercnt=0;
	int othercnt=0;
	while ((ch=getchar())!=EOF&&ch!='\n') {
		if (('a'<=ch&&ch<='z')||('A'<=ch&&ch<='Z')) {
			englishcnt++;
		} else if (ch==' ') {
			spacecnt++;
		} else if ('0'<=ch&&ch<='9') {
			numbercnt++;
		} else {
			othercnt++;
		}
	}
	
	printf("english=%d\n",englishcnt);
	printf("space=%d\n",spacecnt);
	printf("number=%d\n",numbercnt);
	printf("other=%d\n",othercnt);
	
	return 0;
}