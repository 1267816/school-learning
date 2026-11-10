#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「实验5 实验报告」。

用法：python build_report5.py <模板.docx> <输出.docx>
模板取上一份报告的封面（前七段），本脚本删去其正文后按实验5内容重排七节。
"""
import os
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXP5 = os.path.join(REPO, 'experiment-report', '实验5')
CODE_PT = 10.5

HEADINGS = ('实验目的', '实验内容和要求', '主要仪器设备', '实验原理', '源程序',
            '实验步骤与调试', '实验结果与分析')


def read_c(name):
    # 源码有 UTF-8 也有 GBK 的：先按 UTF-8 严格解，失败再退回 GBK。
    # 反过来先试 GBK 会「成功」解出乱码，因为 GBK 几乎接受任意双字节。
    raw = open(os.path.join(EXP5, name), 'rb').read()
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
    '1. 掌握一维数组和二维数组的定义、赋值和输入输出的方法。',
    '2. 掌握字符数组和字符串函数的使用。',
    '3. 掌握与数组有关的算法。',
]

CONTENT = [
    ('sub', '1．实验内容1'),
    ('body', '程序填空：求一个3乘3矩阵主对角线元素之和，按题目给的格式输出矩阵。'),
    ('body', '（1）用两重循环输出3乘3矩阵，再把主对角线上的a[i][i]累加进sum。'),
    ('body', '（2）用数组计算Fibonacci数列的前12个数，并按每行4个数的格式输出。'),
    ('body', '实验要求：填出标号1、2、3处的代码，运行程序并记录输出。'),
    ('sub', '2．实验内容2'),
    ('body', '编写代码，一个3乘4矩阵，找出每行中最小元素并与第一列元素交换。'),
    ('body', '实验要求：'),
    ('body', '（1）使用二维数组存放该3乘4矩阵。'),
    ('body', '（2）定义并初始化该二维数组。'),
    ('body', '（3）输出原矩阵和变换后的矩阵进行比较。'),
    ('body', '（4）有必要的提示信息。'),
    ('sub', '3．实验内容3'),
    ('body', '用选择法对10个整数排序。'),
    ('body', '实验要求：输入事先已编好的程序，并运行该程序，分析运行结果是否正确。'),
    ('sub', '4．实验内容4'),
    ('body', '有15个数按从小到大的顺序存放在一个数组中，输入一个数，用折半查找法找出该数是数组中第几个元素；如果该数不在数组中，输出“不在表中”。'),
    ('body', '实验要求：输入事先已编好的程序，并运行该程序，分析运行结果是否正确。'),
    ('sub', '5．实验内容5'),
    ('body', '一维数组长度为10，用排序算法排成由小到大的顺序并输出；再从键盘输入一个整数插入已排好的数组中，要求仍然有序，输出新生成的有序数组。'),
    ('body', '实验要求：编程并上机运行。'),
]

PRINCIPLE = [
    ('label', '实验5-1.1：用两重循环按行输出3乘3矩阵，再在第二个循环里把下标相同的a[i][i]累加，主对角线元素之和为27。'),
    ('label', '实验5-1.2：fib数组前两项固定为1，从第3项起fib[i]=fib[i-1]+fib[i-2]；输出时用(i+1)%4==0判断是否该换行。'),
    ('label', '实验5-2：逐行扫描，用变量k记录本行最小元素的下标，扫描完把a[i][0]与a[i][k]交换。'),
    ('label', '实验5-3：选择法每一轮在未排序区间里找最大元素，与区间末尾交换，10轮后数组由小到大。'),
    ('label', '实验5-4：折半查找用left与right夹住区间，每次取mid比较；目标大于a[mid]就把left移到mid+1，小于就把right移到mid-1，找到立即break。'),
    ('label', '实验5-5：先用冒泡排序把10个数排好并输出，再把新数放到第11个位置，对11个数重新冒泡排序后输出。'),
]

SOURCE = [
    ('实验5-1.1：', '5-1.1.c'),
    ('实验5-1.2：', '5-1.2.c'),
    ('实验5-2：', '5-2.c'),
    ('实验5-3：', '5-3.c'),
    ('实验5-4：', '5-4.c'),
    ('实验5-5：', '5-5.c'),
]

STEPS = [
    ('body', '（1）实验步骤：'),
    ('body', '1. 打开Dev-C++，新建源文件，按题目要求输入或补全代码。'),
    ('body', '2. 编译前先检查分号、括号与数组下标，再按F11编译。'),
    ('body', '3. 编译通过后运行，按题目给定的数据测试，记录输出。'),
    ('body', '4. 出现报错时按提示行号定位并修改，重新编译运行。'),
    ('body', '（2）调试过程与错误记录：'),
    ('body', '编写与调试中一共遇到三处问题，分别记录如下。'),
    ('body', '错误一：Fibonacci程序的换行条件写错。'),
    ('body', '错误现象：程序编译通过且能运行，但12个数全部输出在同一行。'),
    ('body', '原因分析：条件写成i%4+1==0，%的优先级高于+，等价于(i%4)+1==0；i%4只能是0到3，加1后最小是1，条件永远不成立，printf里的换行一次都没执行。'),
    ('body', '解决办法：把条件改成(i+1)%4==0，i为3、7、11时换行。'),
    ('body', '调试结果：输出分成3行，每行4个数。'),
    ('body', '错误二：找每行最小元素时变量作用域越界，比较方向也写反。'),
    ('body', "错误现象：编译时报[Error] 'k' undeclared (first use in this function)，指向swap那一行；把变量挪出来以后程序能跑，但换到第一列的是每行的最大值。"),
    ('body', '原因分析：int k=0声明在内层for的循环体里，内层循环结束变量就失效，外层访问不到；而且k每次从头初始化，也记不住最小值的下标。比较条件写成a[i][j]>a[i][k]是在找最大值，与题目要求的“最小”相反。'),
    ('body', '解决办法：把int k=0移到外层for内部、内层for之前；比较条件改成a[i][j]<a[i][k]。'),
    ('body', '调试结果：三行分别把2、1、0换到第一列，原矩阵与变换后的矩阵都输出正确。'),
    ('body', '错误三：折半查找的边界写成left=mid、right=mid，运行后死循环。'),
    ('body', '错误现象：编译没有报错，运行输入数字后程序不结束，窗口一直没有反应。'),
    ('body', '原因分析：目标大于中间值时把left赋成mid，下一次算出的mid不变，区间没有缩小；目标小于中间值时同理。另外找到目标后只记了结果，没有break，循环也不会立刻结束。'),
    ('body', '解决办法：把left=mid改成left=mid+1，right=mid改成right=mid-1；在n==a[mid]的分支里记录位置后加break。'),
    ('body', '调试结果：输入7输出4，输入8输出“不在表中”，输入29输出15，都能正常结束。'),
    ('body', '（3）最终运行验证：'),
    ('body', '实验5-1.1输出3乘3矩阵，主对角线元素之和为27。'),
    ('body', '实验5-1.2输出Fibonacci数列前12项：1、1、2、3、5、8、13、21、34、55、89、144，每行4个。'),
    ('body', '实验5-2原矩阵为5 2 8 9、4 1 7 3、6 0 2 1，变换后为2 5 8 9、1 4 7 3、0 6 2 1。'),
    ('body', '实验5-3输入5、3、8、1、9、2、7、4、6、10，输出1到10的升序排列。'),
    ('body', '实验5-4输入7输出4，输入8输出不在表中，输入29输出15。'),
    ('body', '实验5-5排序后输出5、8、12、21、33、45、60、77、89、99，插入35后输出5、8、12、21、33、35、45、60、77、89、99。'),
    ('body', '结果说明：六段程序全部编译通过，运行结果与推算一致。'),
]

ANALYSIS = [
    ('body', '（1）实验5-1运行结果与分析：'),
    ('body', '主对角线元素之和输出27，与1+9+17一致；Fibonacci前12项为1、1、2、3、5、8、13、21、34、55、89、144。'),
    ('body', '分析：二维数组用两重循环遍历，行下标与列下标相同的元素正好落在主对角线上；Fibonacci从第3项起由前两项相加得到，初始化时只给前两项赋值，其余元素自动为0。'),
    ('body', '（2）实验5-2运行结果与分析：'),
    ('body', '变换后每行第一个元素分别是本行的最小值2、1、0，其余元素顺序不变。'),
    ('body', '分析：找最小值只需记录下标，最后交换一次，比边找边换省事；交换函数用指针传参，函数里改的就是数组里的元素。'),
    ('body', '（3）实验5-3运行结果与分析：'),
    ('body', '输入10个无序整数，输出按由小到大的顺序排列。'),
    ('body', '分析：每轮把未排序部分的最大值换到末尾，已经排好的部分不再参与，内层循环的次数逐轮减少。'),
    ('body', '（4）实验5-4运行结果与分析：'),
    ('body', '7在表中排第4位，输出4；8不在表中，输出不在表中；29是最后一个元素，输出15。'),
    ('body', '分析：折半查找每次把区间缩小一半，15个元素最多比较4次；边界必须用mid+1与mid-1收缩，否则区间不缩小会死循环。'),
    ('body', '（5）实验5-5运行结果与分析：'),
    ('body', '排序后数组为5、8、12、21、33、45、60、77、89、99，插入35后为5、8、12、21、33、35、45、60、77、89、99。'),
    ('body', '分析：插入后重新排序写法简单，但效率不如从后往前找位置再移动元素；题目只要求结果有序，这种写法能满足要求。'),
    ('body', '（6）实验总结：'),
    ('body', '通过本次实验，掌握了一维数组与二维数组的定义、初始化、输入输出和遍历，练习了矩阵对角线求和、Fibonacci、按行求最小值、选择法排序、折半查找和有序插入几类与数组有关的算法。调试方面体会最深的是三点：一是变量的作用域要跟着循环层次走，循环里用到的下标变量要声明在正确的层；二是比较方向要和题目要求对齐，找最小值就不能写>；三是折半查找的边界收缩必须让区间真正变小，否则程序能编译却会死循环。'),
]


def cover(doc):
    """改封面：实验项目名称、编号、实验时间。"""
    p2 = doc.paragraphs[2]
    for run in p2.runs:
        if run.text == '4':
            run.text = '5'
            break
    for run in p2.runs:
        if run.text == '循环控制':
            run.text = '数组'
            break
    p3 = doc.paragraphs[3]
    for run in p3.runs:
        if run.text == '4':
            run.text = '5'
            break
    p6 = doc.paragraphs[6]
    fixed = {'10': '11', '27': '3'}
    for run in p6.runs:
        if run.text in fixed:
            run.text = fixed[run.text]


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
