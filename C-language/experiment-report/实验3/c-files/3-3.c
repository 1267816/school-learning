#include <stdio.h>
int main() {
	char x,y;
	printf("Please input a letter:\n");
	scanf("%c",&x);
	if('A'<=x&&x<='Z')  /*表达式功能：判断输入的数据是否是大写字母*/
    {    
		x=x-'A'+'a';
		y=x;   /*语句功能：将输入的大写字母转换成小写，赋值给y*/
    } else 
	{
		y=x;
	} 
	printf("The lower letter is:%c\n",y);
	return 0;
}
