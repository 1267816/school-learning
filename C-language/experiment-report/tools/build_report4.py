#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「实验4 实验报告」。

用法：python build_report4.py <模板.docx> <输出.docx>
模板取实验3报告的封面（前七段），本脚本删去其正文后按实验4内容重排七节。
"""
import os
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXP4 = os.path.join(REPO, 'experiment-report', '实验4')
CODE_PT = 10.5

HEADINGS = ('实验目的', '实验内容和要求', '主要仪器设备', '实验原理', '源程序',
            '实验步骤与调试', '实验结果与分析')


def read_c(name):
    raw = open(os.path.join(EXP4, name), 'rb').read()
    try:
        text = raw.decode('gbk')
    except UnicodeDecodeError:
        text = raw.decode('utf-8', errors='replace')
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
    elif kind == 'image':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Pt(0)
        pf.left_indent = Pt(0)
        pf.line_spacing = 1.0
        path = os.path.join(EXP4, 'image', text)
        from PIL import Image as _Image
        w_px, h_px = _Image.open(path).size
        max_h, max_w = 480, 415
        if h_px / w_px > max_h / max_w:
            width_pt = max_h * w_px / h_px
        else:
            width_pt = max_w
        p.add_run().add_picture(path, width=Pt(width_pt))
    return p


def add_code_block(doc, name):
    for line in read_c(name).split('\n'):
        add_paragraph(doc, 'code', line)


PURPOSE = [
    '1. 熟悉掌握用while语句、do-while语句和for语句实现循环的方法。',
    '2. 掌握在程序设计中用循环的方法实现一些常用算法。',
    '3. 进一步学习调试程序。',
]

CONTENT = [
    ('sub', '1．实验内容1'),
    ('body', '分析下面两段程序，对比上机运行结果，理解循环语句的使用方法。记录结果，采用书写方式。'),
    ('body', '（1）用do-while语句实现循环，循环体中重复执行x=x*x，循环条件为!x。'),
    ('body', '（2）用for语句实现循环，循环体中用if语句判断b的值，分别执行break与continue。'),
    ('body', '实验要求：'),
    ('body', '（1）输入事先已编好的程序，并运行该程序，分析运行结果是否正确。'),
    ('body', '（2）解释循环执行次数的原因。'),
    ('sub', '2．实验内容2'),
    ('body', '程序填空：从键盘输入若干学生的成绩，统计并输出最高成绩和最低成绩，当输入负数时结束。'),
    ('body', '实验要求：'),
    ('body', '（1）填出程序中标号1、2处的代码。'),
    ('body', '（2）运行程序，输入若干成绩与一个负数，记录输出。'),
    ('sub', '3．实验内容3'),
    ('body', '分别用while、do-while、for三种循环语句编写程序，计算1+2+3+…+100。'),
    ('body', '实验要求：比较三种写法在循环条件与循环变量更新上的差别。'),
    ('sub', '4．实验内容4'),
    ('body', '编写程序，输入一行字符（以回车结束），统计其中字母m出现的个数，不区分大小写。'),
    ('body', '实验要求：输入含大小写m的字符串，记录统计结果。'),
    ('sub', '5．实验内容5'),
    ('body', '编写程序，求水仙花数。水仙花数满足abc=a3+b3+c3，例如153=13+53+33。'),
    ('body', '实验要求：先分析思路再编写程序，可以用不同的拆位方法各写一个版本。'),
    ('sub', '6．实验内容6'),
    ('body', '使用continue语句编写程序，输出100-200之间不能被3整除的数（教材例5.5）。'),
    ('body', '实验要求：观察continue与break在循环中的作用差别。'),
    ('sub', '7．实验内容7'),
    ('body', '使用break语句编写程序，输出100-200之间的全部素数（教材例5.10）。'),
    ('body', '实验要求：记录素数个数与数值，说明内层循环的结束条件。'),
    ('sub', '8．实验内容8'),
    ('body', '编写程序求1!+2!+3!+…+20!。'),
    ('body', '实验要求：比较int与long long两种类型下的输出，说明差别的原因。'),
    ('sub', '9．实验内容9'),
    ('body', '编写程序，输入一行字符，分别统计出其中英文字母、空格、数字和其他字符的个数。'),
    ('body', '实验要求：'),
    ('body', '（1）输入事先编好的程序，并运行该程序，分析运行结果是否正确。'),
    ('body', '（2）修改程序，使之能分别统计大写字母、小写字母、空格、数字和其他字符的个数。'),
]

PRINCIPLE = [
    ('label', '实验4-1.1：do-while先执行循环体再判断条件，x初值为-1，执行一次后变成1，条件为假，循环只做一次。'),
    ('label', '实验4-1.2：for循环中先判断b>=20是否成立，成立就用break跳出；b%3==1时先累加再continue跳过本轮剩余语句。'),
    ('label', '实验4-2：每读入一个成绩就与当前最大值、最小值比较并更新，读到负数时结束循环。'),
    ('label', '实验4-3：三种循环写法都把1到100逐个累加到sum，循环条件分别用while、do-while、for表达。'),
    ('label', '实验4-4：用getchar逐字符读入，遇到回车结束，判断是否为m或M并计数。'),
    ('label', '实验4-5.1：用三层进位的方式枚举100到999的三位数，再判断三个数字的立方和。'),
    ('label', '实验4-5.2：用取余与整除把三位数拆成个位、十位、百位，再判断立方和。'),
    ('label', '实验4-6：for枚举100到200，遇到能被3整除的数就用continue跳过输出。'),
    ('label', '实验4-7：外层枚举100到200，内层用2到根号i试除，发现因子就break并把标志位置0。'),
    ('label', '实验4-8：累乘得到i的阶乘，再累加进sum，用long long容纳结果。'),
    ('label', '实验4-9：用getchar逐字符读入，用if-else if链把字符分成字母、空格、数字和其他四类分别计数。'),
]

SOURCE = [
    ('实验4-1.1：', '4-1.1.c'),
    ('实验4-1.2：', '4-1.2.c'),
    ('实验4-2：', '4-2.c'),
    ('实验4-3.1（while版）：', '4-3.1.c'),
    ('实验4-3.2（do-while版）：', '4-3.2.c'),
    ('实验4-3.3（for版）：', '4-3.3.c'),
    ('实验4-4：', '4-4.c'),
    ('实验4-5.1（进位枚举法）：', '4-5.1.c'),
    ('实验4-5.2（取余拆位法）：', '4.5-2.c'),
    ('实验4-6：', '4.6.c'),
    ('实验4-7：', '4-7.c'),
    ('实验4-8：', '4-8.c'),
    ('实验4-9：', '4-9.c'),
]

STEPS = [
    ('body', '（1）实验步骤：'),
    ('body', '1. 打开Dev-C++，新建源文件，按题目要求输入代码。'),
    ('body', '2. 编译前先检查分号、括号与格式符，再按F11编译。'),
    ('body', '3. 编译通过后运行，按题目给定的数据测试，记录输出。'),
    ('body', '4. 出现报错时按提示行号定位并修改，重新编译运行。'),
    ('body', '（2）调试过程与错误记录：'),
    ('body', '编写与调试中一共遇到五处问题，分别记录如下。'),
    ('body', '错误一：用char类型接收getchar的返回值，文件结束判断失效。'),
    ('body', '错误现象：输入若干字符后按结束键，程序不退出，一直等待输入。'),
    ('body', '原因分析：getchar的返回值是int，文件结束标志EOF为-1；char在部分环境下是无符号类型，'
             '把-1截断成255，ch!=EOF恒成立，循环退不出去。'),
    ('body', '解决办法：把接收变量声明为int类型，写成int ch。'),
    ('body', '调试结果：输入结束后循环正常退出，统计结果正确。'),
    ('body', '错误二：素数程序中标志位变量声明在内层循环，编译报错。'),
    ('body', "错误现象：编译时提示[Error] 'isprime' undeclared (first use in this function)，指向判断素数的if语句。"),
    ('body', '原因分析：isprime声明在内层for语句的代码块里，出了这对花括号，变量的作用域就结束了，'
             '外层无法访问。'),
    ('body', '解决办法：把isprime的声明与初始化移到外层循环内部、内层循环之前。'),
    ('body', '调试结果：编译通过；若初始化仍留在内层，每换一个除数标志位就被重置，结果依旧错误。'),
    ('body', '错误三：素数程序内层除数从1开始，运行后没有任何输出。'),
    ('body', '错误现象：程序编译通过、能运行，但屏幕上没有输出任何素数。'),
    ('body', '原因分析：任何整数除以1的余数都是0，内层循环第一次判断就把isprime置0并break，'
             '于是100到200的数全被判成非素数。'),
    ('body', '解决办法：内层循环初值改为2，结束条件用j*j<=i。'),
    ('body', '调试结果：输出101到199之间的全部素数，共21个。'),
    ('body', '错误四：阶乘求和用int类型存储，结果溢出。'),
    ('body', '错误现象：编译无误，运行输出268040729，与期望值相差很大。'),
    ('body', '原因分析：int的上限是2147483647，13!达到6227020800已经超出，溢出后符号位与数值全部失真，'
             '其后的累加也失去意义。'),
    ('body', '解决办法：把product与sum改为long long类型，printf的格式符改成%lld。'),
    ('body', '调试结果：输出2561327494111820313，与数学值一致。'),
    ('body', '错误五：统计含中文的输入时其他字符计数成倍增加。'),
    ('body', '错误现象：输入含中文汉字或中文标点时，其他字符的计数明显偏大。'),
    ('body', '原因分析：getchar按字节读取，一个汉字在GBK编码下占两个字节，这两个字节都不属于字母、'
             '空格或数字，各自落入else分支被累加一次。'),
    ('body', '解决办法：测试时使用半角英文输入；确实要处理中文时改用宽字符函数或按编码逐字解码。'),
    ('body', '调试结果：纯英文输入Hello 123, world! 4 u，统计为english=11、space=4、number=4、other=2，'
             '与手数结果一致。'),
    ('body', '（3）最终运行验证：'),
    ('body', '实验4-1.1输出=1；实验4-1.2输出8。'),
    ('body', '实验4-2输入85、92、78、66、-1，输出amax=92.000000、amin=66.000000。'),
    ('body', '实验4-3的三种写法都输出5050。'),
    ('body', '实验4-4输入morning mellow M，输出3。'),
    ('body', '实验4-5的两种写法都输出153、370、371、407。'),
    ('body', '实验4-6输出100到200之间不能被3整除的68个数，前几个是100、101、103、104、106。'),
    ('body', '实验4-7输出21个素数，前几个是101、103、107、109、113、127。'),
    ('body', '实验4-8输出2561327494111820313。'),
    ('body', '实验4-9输入Hello 123, world! 4 u，输出english=11、space=4、number=4、other=2。'),
    ('body', '结果说明：十三段程序全部编译通过，运行结果与推算一致。'),
]

ANALYSIS = [
    ('body', '（1）实验4-1运行结果与分析：'),
    ('body', '第一段先执行一次x=x*x，x由-1变成1，条件!x为假，循环结束；printf里的"%="不是合法转换符，'
             '只有%d起作用，所以屏幕上输出=1。第二段在a为8时b达到20，break生效跳出循环，输出8。'),
    ('body', '分析：do-while至少执行一次循环体，while可能一次都不执行；break跳出整个循环，'
             'continue只跳过本轮剩下的语句，两者不能混用。'),
    ('body', '手写批注（原文转录）：while(!x) 后面标了两条分支，continue 与 break；x-- 旁边注 x!=0；'
             'printf 那一行被圈起来打了个问号；运行结果记为=1。'),
    ('body', '手写批注（原文转录）：逐轮写出 a、b 的变化直到 b 超过20，末行标注 break；右侧写「预期」与 a=8，'
             '下方写「输出」8。'),
    ('body', '（2）实验4-2运行结果与分析：'),
    ('body', '输入85、92、78、66、-1，程序逐个比较，负数作为结束标志不参与比较，得到最高92、最低66。'),
    ('body', '分析：最大值与最小值都用第一个成绩初始化，避免初值为0时把全部正数都判成最小值；'
             '结束条件写在while里，靠读入负数退出，比固定次数的循环更灵活。'),
    ('body', '手写批注（原文转录）：两个空分别填 x>=0 与 x<amin，旁边写「符合预期」。'),
    ('body', '（3）实验4-3运行结果与分析：'),
    ('body', 'while、do-while、for三种写法都输出5050。'),
    ('body', '分析：do-while先把判断放到后面，循环变量的更新必须写在条件表达式里，写成++x<=100，'
             '否则会多累加一次；for把初始化、条件与增量集中在一行，次数已知时最清楚。'),
    ('body', '（4）实验4-4运行结果与分析：'),
    ('body', '输入morning mellow M，程序统计到3个m或M。'),
    ('body', '分析：判断写成ch=="m"||ch=="M"，两个条件用||连接；循环条件里同时判断EOF与换行，'
             '遇到回车就结束，符合题目要求。'),
    ('body', '（5）实验4-5运行结果与分析：'),
    ('body', '两种写法都输出153、370、371、407，这四个就是全部的三位水仙花数。'),
    ('body', '分析：第一种写法用手工进位枚举三个数字，第二种用%10与/10拆位，后者更直接；'
             '两种都验证了三个数字的立方和等于原数。'),
    ('body', '（6）实验4-6运行结果与分析：'),
    ('body', '程序输出100到200之间不能被3整除的68个数。'),
    ('body', '分析：continue只跳过本次输出，循环继续；若写成break，遇到第一个3的倍数就会停止，'
             '这正说明两者的差别。'),
    ('body', '（7）实验4-7运行结果与分析：'),
    ('body', '输出101到199之间的21个素数。'),
    ('body', '分析：内层只需试除到根号i，既能保证正确又减少了循环次数；标志位必须在外层每轮重新置1，'
             'break只跳出内层，外层继续判断下一个数。'),
    ('body', '（8）实验4-8运行结果与分析：'),
    ('body', '用long long存储时输出2561327494111820313，与数学值一致。'),
    ('body', '分析：int只能正确算到12!，从13!起溢出；数据类型的容量必须按最大值预估，'
             'printf的格式符也要与类型对应，写成%lld。'),
    ('body', '（9）实验4-9运行结果与分析：'),
    ('body', '输入Hello 123, world! 4 u，输出english=11、space=4、number=4、other=2。'),
    ('body', '分析：if-else if链保证一个字符只被统计一次；程序只面向单字节的ASCII字符，'
             '中文会按字节拆开计入其他字符，这是getchar按字节读取的必然结果。'),
    ('body', '（10）实验总结：'),
    ('body', '通过本次实验，掌握了while、do-while、for三种循环语句的写法与适用场合，理解了break与'
             'continue的区别，并练习了累加、累乘、枚举、素数判定与字符统计几类常用算法。调试方面体会最深的是三点：'
             '一是变量的作用域要跟着循环层次走，标志位要放在外层循环里；二是要预估数据的取值范围，'
             '该用long long时不能省；三是输入函数按字节读取，类型与编码都会影响统计结果。'),
]


def cover(doc):
    """改封面：实验项目名称、编号、实验时间。"""
    p2 = doc.paragraphs[2]
    p2.runs[1].text = '实验4'
    for i in range(2, 8):
        p2.runs[i].text = ''
    p2.runs[2].text = ' 循环控制 '
    p3 = doc.paragraphs[3]
    for run in p3.runs:
        if run.text == '3':
            run.text = '4'
            break
    p6 = doc.paragraphs[6]
    for run in p6.runs:
        if run.text == '20':
            run.text = '27'


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    doc = docx.Document(src)
    # 只保留封面七段（含页首标题）
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
