#include <stdio.h>
#include <string.h>

void f(char* a,int length,int *pletter,int *pnum,int *pspace,int *pother) {
	int i=0;
	for (i=0;i<length;i++) {
		int x=a[i];
		if ((x>='a'&&x<='z')||(x>='A'&&x<='Z')) {
			(*pletter)++;
		} else if (x>='0'&&x<='9') {
			(*pnum)++;
		} else if (x==' ') {
			(*pspace)++;
		} else {
			(*pother)++;
		}
	}
}

int main() {
	char a[101]={0};
	int i=0;
	char ch;
	while ((ch=getchar())!='\n'&&ch!=EOF) {
		a[i]=ch;
		i++;
	}
	
	int length=strlen(a);
	int letter=0,num=0,space=0,other=0;
	f(a,length,&letter,&num,&space,&other);
	printf("letter=%d\n",letter);
	printf("num=%d\n",num);
	printf("space=%d\n",space);
	printf("other=%d\n",other);
	
	return 0;
}