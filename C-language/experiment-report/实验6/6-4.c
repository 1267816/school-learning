#include <stdio.h>

double avg(int b[],int length) {
	double ret=0;
	for (int i=0;i<length;i++) {
		if (b[i]!=-1) {
			ret+=b[i];
		} else {
			break;
		}
	}
	ret/=length;
	return ret;
}

void reset(int b[],int length) {
	for (int i=0;i<length;i++) {
		b[i]=-1;
	}
}

void max(int a[10][5],int *pmaxstudent,int *pmaxclass) {
	*pmaxstudent=0;
	*pmaxclass=0;
	for (int i=0;i<10;i++) {
		for (int j=0;j<5;j++) {
			if (a[i][j]>a[*pmaxstudent][*pmaxclass]) {
				*pmaxstudent=i;
				*pmaxclass=j;
			}
		}
	}
}

int main(void) {
	int a[10][5];
	int i,j;
	for (i=0;i<10;i++) {
		for (j=0;j<5;j++) {
			scanf("%d",&a[i][j]);
		}
	}
	int b[10];
	int length=5;
	for (i=0;i<10;i++) {
		reset(b,length);
		for (j=0;j<5;j++) {
			b[j]=a[i][j];
		}
		printf("第%d个学生的平均分为%.2f\n",i+1,avg(b,length));
	}
	
	length=10;
	for (i=0;i<5;i++) {
		reset(b,length);
		for (j=0;j<10;j++) {
			b[j]=a[j][i];
		}
		printf("第%d门课的平均分为%.2f\n",i+1,avg(b,length));
	}
	
	int maxstudent,maxclass;
	max(a,&maxstudent,&maxclass);
	printf("最高分数对应学生和课程分别为%d %d",maxstudent+1,maxclass+1);
	
	return 0;
}