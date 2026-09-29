# 2026.9.29

**P73**：printf函数中用到的格式字符
**P74**：scanf函数中用到的格式字符
**P357**：常用字符与ASCII代码对照表

P8笔记：
函数调用时，动态变量开辟空间；
函数调用结束后，动态变量释放空间。

```c
#include <stdio.h>
int main(){
    int max(int x,int y);
    int a,b,c;
    scanf...
    c=max(a,b);
    printf...
    return 0;
}
int max(int x,int y){
    ...
    return(z);
}
```
第一个`int max(int x,int y)`是对被调用函数max的声明，第二个是对max函数的定义。
