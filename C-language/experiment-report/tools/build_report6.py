#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「实验6 实验报告」。

用法：python build_report6.py <模板.docx> <输出.docx>
模板取上一份报告的封面（前七段），本脚本删去其正文后按实验6内容重排七节。
"""
import os
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXP6 = os.path.join(REPO, 'experiment-report', '实验6')
CODE_PT = 10.5

HEADINGS = ('实验目的', '实验内容和要求', '主要仪器设备', '实验原理', '源程序',
            '实验步骤与调试', '实验结果与分析')


def read_c(name):
    # 源码有 UTF-8 也有 GBK 的：先按 UTF-8 严格解，失败再退回 GBK。
    raw = open(os.path.join(EXP6, name), 'rb').read()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        text = raw.decode('gbk')
    return text.replace('\r\n', '\n').rstrip('\n')


def set_font(run, western='Times New Roman', east='宋体', size=12, bold=False):
    run.font.size = Pt(size)
    run.bold = bold
    run.font.name = western
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn('w:rFonts'))
    if fonts is None:
        fonts = OxmlElement('w:rFonts')
        rpr.insert(0, fonts)
    fonts.set(qn('w:ascii'), western)
    fonts.set(qn('w:hAnsi'), western)
    fonts.set(qn('w:eastAsia'), east)
    fonts.set(qn('w:cs'), western)


def add_paragraph(doc, kind, text=''):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    if kind == 'heading':
        pf.first_line_indent = Pt(0)
        pf.line_spacing = 1.5
        run = p.add_run(text)
        set_font(run, size=14, bold=True)
    elif kind in ('body', 'label', 'boldlabel'):
        pf.first_line_indent = Pt(21)
        pf.line_spacing = 1.5
        run = p.add_run(text)
        set_font(run, bold=(kind == 'boldlabel'))
    elif kind == 'sub':
        pf.first_line_indent = Pt(12.1)
        pf.line_spacing = 1.5
        run = p.add_run(text)
        set_font(run, bold=True)
    elif kind == 'code':
        pf.first_line_indent = Pt(0)
        pf.left_indent = Pt(42.8)
        pf.line_spacing = 1.0
        run = p.add_run(text)
        set_font(run, western='Consolas', size=CODE_PT)
    return p


def add_code_block(doc, name):
    for line in read_c(name).split('\n'):
        add_paragraph(doc, 'code', line)


PURPOSE = [
    '1. 掌握定义函数的方法。',
    '2. 掌握函数实参与形参的对应关系，以及值传递的方式。',
    '3. 掌握函数的嵌套调用和递归调用的方法。',
    '4. 掌握全局变量和局部变量、动态变量、静态变量的概念和使用方法。',
    '5. 掌握宏定义的方法，文件包含处理方法。',
]

CONTENT = [
    ('sub', '1．实验内容1'),
    ('body', '程序改错：fun函数的形参是整型m，功能是把1依次减去2的平方分之一、3的平方分之一，一直减到m的平方分之一；m为5时应输出0.536389，改正程序中的错误。'),
    ('body', '（1）形参m没有写类型，编译器按int处理。'),
    ('body', '（2）循环条件写成i<m，最后一项没减掉。'),
    ('body', '（3）1/(i*i)是整数除法，结果恒为0。'),
    ('body', '（4）函数返回的是m，应当返回y。'),
    ('body', '实验要求：改正上述错误，运行程序，使输出为0.536389。'),
    ('body', '另有三段程序要求写出运行结果，分析函数的调用过程。'),
    ('sub', '2．实验内容2'),
    ('body', '试编写一个判素数的程序。函数完成判素数的功能，主函数输入一个整数，输出是否素数的信息。'),
    ('body', '实验要求：输入事先已编好的程序，并运行该程序，分析运行结果是否正确。'),
    ('sub', '3．实验内容3'),
    ('body', '编写一函数，由实参传来一个字符串，统计此字符串中字母、数字、空格和其他字符的个数，在主函数中输入字符串以及输出上述的结果。'),
    ('body', '实验要求：输入事先已编好的程序，并运行该程序，分析运行结果是否正确。'),
    ('sub', '4．实验内容4'),
    ('body', '输入10个学生5门课的成绩，分别用函数求：①每个学生平均分；②每门课的平均分；③找出最高的分数所对应的学生和课程。'),
    ('body', '实验要求：输入事先已编好的程序，并运行该程序，分析运行结果是否正确。'),
    ('sub', '5．实验内容5'),
    ('body', '定义一个带参数的宏，使两个参数的值互换，并写出程序，输入两个数作为使用宏时的实参，输出交换后的两个值。'),
    ('body', '实验要求：输入事先已编好的程序，并运行该程序，分析运行结果是否正确。'),
]

PRINCIPLE = [
    ('label', '实验6-1.1：y先置为1.0，再从i=2到i=m逐项减去1.0/(i*i)，最后返回y；用1.0做被除数才能按浮点数相除，形参也必须声明为int。'),
    ('label', '实验6-1.2：f里k是普通局部变量，每次调用都从2开始加1，再把k与形参m相加后返回；s=f(2)得5，再调用f(s)得8。'),
    ('label', '实验6-1.3：b是自动局部变量，每次调用重新初始化为0；c用static修饰，只初始化一次，之后保留上一次的值；三次调用分别返回7、8、9。'),
    ('label', '实验6-1.4：M的三个实参是表达式a+b、b+c、c+a，先算出3、5、4再按值传给形参，函数里算3乘5加4得19。'),
    ('label', '实验6-2：从i=2试除到i*i<=x，能整除就置ret为0并跳出；x为1时循环一次都不执行，要单独置ret为0。'),
    ('label', '实验6-3：四个计数器在主函数里定义，把地址传给f，函数里用*p累加，函数返回后主函数里的计数已经改好。'),
    ('label', '实验6-4：avg把数组和元素个数一起传进去求平均；max用两个指针把最高分所在的行、列下标带回主函数；求每个平均分之前先用reset把数组清成-1。'),
    ('label', '实验6-5：#define SWAP(a,b)在预处理阶段直接替换成三条语句，用临时变量temp把两个实参的值交换过来。'),
]

SOURCE = [
    ('实验6-1.1：', '6-1.1.c'),
    ('实验6-1.2：', '6-1.2.c'),
    ('实验6-1.3：', '6-1.3.c'),
    ('实验6-1.4：', '6-1.4.c'),
    ('实验6-2：', '6-2.c'),
    ('实验6-3：', '6-3.c'),
    ('实验6-4：', '6-4.c'),
    ('实验6-5：', '6-5.c'),
]

STEPS = [
    ('body', '（1）实验步骤：'),
    ('body', '1. 打开Dev-C++，新建源文件，先按题目给出的框架把程序抄进去。'),
    ('body', '2. 编译前先看函数头：形参写了类型没有、返回类型对不对。'),
    ('body', '3. 编译通过后运行，按题目要求输入测试数据，记录输出。'),
    ('body', '4. 输出和手工推算的结果对一遍，对不上就回头查形参、返回值与循环的终值条件。'),
    ('body', '（2）调试过程与错误记录：'),
    ('body', '编写与调试中一共遇到十一处问题，分别记录如下。'),
    ('body', '错误一：fun的形参没有写类型。'),
    ('body', "错误现象：编译时出现警告[Warning] type of 'm' defaults to 'int' [-Wimplicit-int]，程序仍然生成了可执行文件。"),
    ('body', '原因分析：函数定义里只写了形参名，没写类型，编译器按int处理并给出警告。'),
    ('body', '解决办法：在形参前补上int，写成double fun(int m)。'),
    ('body', '调试结果：警告消失，m=5时输出0.536389。'),
    ('body', '错误二：判素数的函数把1当成了素数。'),
    ('body', '错误现象：输入1，程序输出yes，而1既不是素数也不是合数。'),
    ('body', '原因分析：x为1时循环条件i*i<=x不成立，循环体一次都不执行，ret保持初始值1，函数直接返回1。'),
    ('body', '解决办法：在返回ret之前加一句if(x==1){ret=0;}。'),
    ('body', '调试结果：输入1输出no，输入2、7输出yes，输入9输出no。'),
    ('body', '错误三：统计字符的函数里形参length没写类型。'),
    ('body', '错误现象：编译时报[Error] unknown type name \'length\'，后面还跟着expected declaration specifiers or \'...\' before \'*\' token。'),
    ('body', '原因分析：形参列表里length前面没有类型名，编译器把它当成一个类型名去解析，后面几个指针参数也跟着报错。'),
    ('body', '解决办法：形参写成int length。'),
    ('body', '调试结果：编译通过。'),
    ('body', '错误四：字符串定义成了指针数组，传参时又在数组名后面加了方括号。'),
    ('body', '错误现象：编译时报[Note] expected \'const char *\' but argument is of type \'char **\'与[Error] expected expression before \']\' token。'),
    ('body', '原因分析：char* a[101]是指针数组，传给strlen时退化成char **；调用f时写成f(a[],...)，数组名后面不能加方括号。'),
    ('body', '解决办法：改成char a[101]={0};，调用时直接传a。'),
    ('body', '调试结果：编译通过，strlen能算出读入的字符个数。'),
    ('body', '错误五：用了strlen却没有包含对应的头文件。'),
    ('body', '错误现象：编译时出现[Warning] implicit declaration of function \'strlen\'与[Warning] incompatible implicit declaration of built-in function \'strlen\'。'),
    ('body', '原因分析：文件开头只包含了<stdio.h>，编译器找不到strlen的声明，只能按隐式声明处理。'),
    ('body', '解决办法：在#include区域加上<string.h>。'),
    ('body', '调试结果：两条警告消失。'),
    ('body', '错误六：四个计数器写成了*pnum++这样的形式，运行后全为0。'),
    ('body', '错误现象：编译没有报错，运行后输入的字符串无论是什么，输出的letter、num、space、other都是0。'),
    ('body', '原因分析：后缀自增的优先级高于解引用，*pnum++等价于*(pnum++)，改的是指针自己，不是它指向的变量。'),
    ('body', '解决办法：给解引用加上括号，写成(*pnum)++，其余三个计数器同样处理。'),
    ('body', '调试结果：四类字符的计数正常。'),
    ('body', '错误七：找最高分的函数把形参写成一维数组，函数体里却用了二维下标。'),
    ('body', '错误现象：编译时报[Error] subscripted value is neither array nor pointer。'),
    ('body', '原因分析：形参写成int a[]，函数体里却写a[i][j]，一维数组不能做两次下标访问。'),
    ('body', '解决办法：形参改成二维数组int a[][5]，与主函数传进来的int a[10][5]匹配。'),
    ('body', '调试结果：编译通过。'),
    ('body', '错误八：调用reset与avg时把数组实参写成了b[10]。'),
    ('body', '错误现象：编译时报[Error] passing argument 1 of \'reset\' makes pointer from integer without a cast，avg那一行同样报错。'),
    ('body', '原因分析：b的下标只到9，b[10]既越界又只是一个int值，而函数要的是数组首地址。'),
    ('body', '解决办法：调用时直接写数组名b。'),
    ('body', '调试结果：编译通过，十行学生平均分与五行课程平均分都能算出来。'),
    ('body', '错误九：交换宏的替换体里用了没定义的x、y。'),
    ('body', '错误现象：编译时报[Error] \'x\' undeclared (first use in this function)。'),
    ('body', '原因分析：宏的形参叫a、b，替换体里却写了x、y，展开后主函数里找不到这两个变量。'),
    ('body', '解决办法：替换体改用宏的形参，写成{int temp=a;a=b;b=temp;}。'),
    ('body', '调试结果：编译通过。'),
    ('body', '错误十：交换宏的替换体末尾漏了分号。'),
    ('body', '错误现象：编译时报[Error] expected \';\' before \'}\' token。'),
    ('body', '原因分析：替换体里最后一条语句b=temp后面没有分号，展开成b=temp};时语法不完整。'),
    ('body', '解决办法：把分号写进替换体。'),
    ('body', '调试结果：编译通过，交换结果正确。'),
    ('body', '错误十一：数字与空格的判断用了||，条件恒成立。'),
    ('body', '错误现象：编译没有报错，输入Hello World 123!这种带空格和符号的字符串，输出num=6、space=0、other=0，与预期的num=3、space=2、other=1不符。'),
    ('body', "原因分析：判断写成了x>='0'||x<='9'，任何字符要么大于等于'0'、要么小于等于'9'，条件永远为真，非字母的字符全被算进了数字。"),
    ('body', "解决办法：把||改成&&，写成x>='0'&&x<='9'。"),
    ('body', '调试结果：同一输入输出letter=10、num=3、space=2、other=1，与手工数的一致。'),
    ('body', '（3）最终运行验证：'),
    ('body', '实验6-1.1输出The result is 0.536389。'),
    ('body', '实验6-1.2输出5 8。'),
    ('body', '实验6-1.3输出7  8  9。'),
    ('body', '实验6-1.4输出19。'),
    ('body', '实验6-2输入1输出no，输入2、7输出yes，输入9输出no。'),
    ('body', '实验6-3输入Hello World 123!，输出letter=10、num=3、space=2、other=1。'),
    ('body', '实验6-4输入十行五列的成绩后，输出十个学生平均分、五门课平均分与最高分所在的学生和课程。'),
    ('body', '实验6-5输入3 5，输出a=3 b=5与a=5 b=3。'),
    ('body', '结果说明：八段程序全部编译通过，运行结果与手工推算一致。'),
]

ANALYSIS = [
    ('body', '（1）实验6-1运行结果与分析：'),
    ('body', '改错后的fun在m=5时输出The result is 0.536389，与题目给的结果一致。'),
    ('body', '分析：改正的三处分别是形参类型、整数除法与返回值。写成1.0/(i*i)，除法才按浮点数算，否则1除以大于1的整数结果总是0；循环的终值条件要取到i=m，公式的最后一项是m的平方分之一；函数最后返回的是累减得到的y，不是形参m。'),
    ('body', '实验6-1.2输出5 8。分析：f(2)里k从2自加到3，返回3+2=5，s得5；第二次调用f(5)，k重新从2开始加1得3，返回3+5=8。形参和局部变量都是每次调用重新生成，函数里怎么改都不影响主函数里的s。'),
    ('body', '实验6-1.3输出7  8  9。分析：b是自动局部变量，每次调用都重新初始化为0；c用static修饰，初始化只执行一次，之后在4、5、6上逐次递增，所以三次调用分别返回7、8、9。想得到7 7 7，去掉c前面的static即可。'),
    ('body', '实验6-1.4输出19。分析：实参是三个表达式，先算出a+b=3、b+c=5、c+a=4，再按值传给形参，函数里算3乘5加4得19。这说明实参的求值和传值都在调用之前完成，函数拿到的是数值，不是变量本身。'),
    ('body', '（2）实验6-2运行结果与分析：'),
    ('body', '输入1与9输出no，输入2与7输出yes。'),
    ('body', '分析：9能被3整除，循环走到i=3时ret被置0；7只试除i=2，2的平方是4不超过7，3的平方是9已经超过7，试除一次不能整除，ret保持1；1是特例，循环一次都不执行，必须在函数里单独置0。'),
    ('body', '（3）实验6-3运行结果与分析：'),
    ('body', '输入Hello World 123!，输出letter=10、num=3、space=2、other=1。'),
    ('body', '分析：字母10个、数字3个、空格2个、感叹号1个，与手工数的结果一致。四个计数器在主函数里定义，函数通过指针改的就是这四个变量本身；字符按ASCII区间分类，判断数字要用&&把两个边界夹住，用||会恒成立。'),
    ('body', '（4）实验6-4运行结果与分析：'),
    ('body', '输入的成绩按学生顺序为：第一行78 85 92 66 74，第二行90 88 71 95 60，第三行55 62 83 70 77，第四行68 79 84 71 63，第五行91 87 76 82 69，第六行73 64 88 59 81，第七行86 92 65 74 78，第八行62 70 79 85 90，第九行80 66 73 91 75，第十行77 83 60 68 84。'),
    ('body', '输出十名学生的平均分为79.00、80.80、69.40、73.00、81.00、73.00、79.00、77.20、77.00、74.40。'),
    ('body', '输出五门课的平均分为76.00、77.60、77.10、76.10、75.10。'),
    ('body', '最高分95分出现在第2个学生的第4门课。'),
    ('body', '分析：学生平均分是按行取出一维副本再求平均，课程平均分是按列取出；avg把数组和个数一起传进去，循环里累加后除以个数；max用两个指针把分数最大的行、列下标带回主函数，最后加1才是人习惯的序号。'),
    ('body', '（5）实验6-5运行结果与分析：'),
    ('body', '输入3 5，先输出a=3 b=5，交换后输出a=5 b=3。'),
    ('body', '分析：宏只在预处理阶段做文本替换，展开后是在主函数里用临时变量交换两个实参的值；宏名不带分号，替换体里最后一条语句后面要写分号。'),
    ('body', '（6）实验总结：'),
    ('body', '通过本次实验，掌握了函数的定义、声明与调用，实参与形参的值传递，静态局部变量与自动局部变量的区别，用指针作参数把结果带回主函数，二维数组作参数的写法，以及带参数宏的定义与使用。调试方面体会最深的是三点：一是形参一定要写类型，只缺类型时编译器大多只给警告，程序照样能跑，问题会被带到运行结果里；二是自增与解引用的优先级，*p++改的是指针，(*p)++才是改指向的值；三是宏是文本替换，替换体里必须用宏的形参名，末尾的分号不能少。'),
]


def cover(doc):
    """改封面：实验项目名称、编号、实验时间。"""
    p2 = doc.paragraphs[2]
    for run in p2.runs:
        if run.text == '5':
            run.text = '6'
            break
    for run in p2.runs:
        if run.text == '数组':
            run.text = '函数'
            break
    p3 = doc.paragraphs[3]
    for run in p3.runs:
        if run.text == '5':
            run.text = '6'
            break
    p6 = doc.paragraphs[6]
    for run in p6.runs:
        if run.text == '3':
            run.text = '10'


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    doc = docx.Document(src)
    for p in list(doc.paragraphs)[7:]:
        p._element.getparent().remove(p._element)
    cover(doc)

    def section(title, items):
        add_paragraph(doc, 'heading', title)
        for kind, text in items:
            add_paragraph(doc, kind, text)

    section('实验目的', [('body', t) for t in PURPOSE])
    section('实验内容和要求', CONTENT)
    section('主要仪器设备', [('boldlabel', '仪器：计算机'), ('boldlabel', '实验环境：Windows  Dev C++')])
    section('实验原理', PRINCIPLE)
    add_paragraph(doc, 'heading', '源程序')
    for label, name in SOURCE:
        add_paragraph(doc, 'label', label)
        add_code_block(doc, name)
    section('实验步骤与调试', STEPS)
    section('实验结果与分析', ANALYSIS)

    doc.save(dst)
    print('已生成:', dst)


if __name__ == '__main__':
    main()
