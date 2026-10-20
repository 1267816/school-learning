#include <stdio.h>
int main(){
	char c1='c',c2='h',c3='i',c4='n',c5='a';
	int n1,n2,n3,n4,n5;
	n1=c1;
	n2=c2;
	n3=c3;
	n4=c4;
	n5=c5;
	n1-=4;
	n2-=4;
	n3-=4;
	n4-=4;
	n5-=4;
	if (n1<=96) {
		n1+=26;
	}
	if (n2<=96) {
		n2+=26;
	}
	if (n3<=96) {
		n3+=26;
	}
	if (n4<=96) {
		n4+=26;
	}
	if (n5<=96) {
		n5+=26;
	}
	printf("%c,%c,%c,%c,%c",n1,n2,n3,n4,n5);
	return 0;
}