#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「实验3 实验报告」正文。

用法：python build_report3.py <模板.docx> <输出.docx>

模板由 Word 把 实验3 实验报告.doc 另存为 docx 得到（封面六行已填好）。
脚本在六个一级标题后插入正文，版式由 normalize_indent.py 与 align_spacing.py 统一：
正文左缩进0、首行缩进2字符、1.5倍行距；代码 Consolas 10.5磅、左缩进42.8磅、单倍行距；
流程图由 mermaid.ink 渲染后居中插入。
"""
import os
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXP3 = os.path.join(REPO, 'experiment-report', '实验3')
CFILES = os.path.join(EXP3, 'c-files')
CACHE = os.path.join(os.environ.get('TEMP', '.'), 'dshexp', 'mermaid3')
CODE_PT = 10.5
IMG_MAX_HEIGHT_PT = 190
IMG_MAX_WIDTH_PT = 330

HEADINGS = ('实验目的', '实验内容和要求', '主要仪器设备', '实验原理', '源程序',
            '实验步骤与调试', '实验结果与分析')


def read_c(name):
    raw = open(os.path.join(CFILES, name), 'rb').read()
    try:
        text = raw.decode('gbk')
    except UnicodeDecodeError:
        text = raw.decode('utf-8', errors='replace')
    return text.replace('\r\n', '\n').rstrip('\n')


def png(key):
    path = os.path.join(CACHE, key + '.png')
    if not os.path.exists(path) or os.path.getsize(path) < 1024:
        raise SystemExit('缺少流程图缓存：' + path)
    return path


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


def add_paragraph(doc, anchor, kind='body', text='', image=None):
    p = doc.add_paragraph()
    anchor.addnext(p._p)
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    if kind in ('body', 'label'):
        pf.first_line_indent = Pt(21)
        pf.left_indent = Pt(0)
        pf.line_spacing = 1.5
        run = p.add_run(text)
        set_font(run)
    elif kind == 'sub':
        pf.first_line_indent = Pt(12.1)
        pf.left_indent = Pt(0)
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
        path = png(image)
        from PIL import Image as _Image
        w_px, h_px = _Image.open(path).size
        if h_px >= w_px:
            width_pt = min(IMG_MAX_HEIGHT_PT * w_px / h_px, IMG_MAX_WIDTH_PT)
        else:
            width_pt = IMG_MAX_WIDTH_PT
        p.add_run().add_picture(path, width=Pt(width_pt))
    return p._p


def add_code_block(doc, anchor, path):
    code = read_c(path)
    last = anchor
    for line in code.split('\n'):
        last = add_paragraph(doc, last, kind='code', text=line if line else '')
    return last


def find_anchor(doc, heading):
    for idx, para in enumerate(doc.paragraphs):
        if para.text.strip() == heading:
            nxt = doc.paragraphs[idx + 1] if idx + 1 < len(doc.paragraphs) else para
            return nxt._p
    raise SystemExit('找不到标题：' + heading)


PURPOSE = [
    '1. 掌握各种类型数据输入输出的方法，能正确使用各种格式转换符。',
    '2. 学会正确使用逻辑运算符和逻辑表达式，熟练掌握if语句和switch语句。',
    '3. 结合程序掌握一些简单的算法。',
]

CONTENT = [
    ('sub', '1．实验内容1'),
    ('body', '用getchar函数读入两个字符给c1、c2，再分别用putchar函数和printf函数输出这两个字符。'),
    ('body', '实验要求：'),
    ('body', '（1）输入事先已编好的程序，并运行该程序，分析运行结果是否正确。'),
    ('body', '（2）比较printf函数与putchar函数输出字符的特点。'),
    ('sub', '2．实验内容2'),
    ('body', '阅读下面两段程序，上机调试并记录程序结果。'),
    ('body', '（1）程序先令x等于3，判断x是否等于0，再按结果输出x或x+1。'),
    ('body', '（2）程序读入一个整数，若为奇数则输出它的平方。'),
    ('body', '实验要求：逐段运行，把实际输出与推算结果对照。'),
    ('sub', '3．实验内容3'),
    ('body', '程序填空：由键盘输入任意一个英文字母，以该字母的小写形式输出。'),
    ('body', '实验要求：'),
    ('body', '（1）填出程序中标号1、2处的代码。'),
    ('body', '（2）运行程序，输入大写字母与小写字母各一次，记录输出。'),
    ('sub', '4．实验内容4'),
    ('body', '给出一百分制成绩，要求输出成绩等级A、B、C、D、E。90分以上为A，80到89分为B，'
             '70到79分为C，60到69分为D，60分以下为E。'),
    ('body', '实验要求：'),
    ('body', '（1）分别用if语句和switch语句编写程序。'),
    ('body', '（2）输入程序并运行，分析运行结果是否正确。'),
    ('body', '（3）再运行一次，输入负值（如-70）和大于100的分数，修改程序，'
             '使非法输入时输出“输入数据错”。'),
]

PRINCIPLE = [
    ('label', '实验3-1：先读一个字符，再读一次并吃掉中间的回车，最后用两种函数输出。'),
    ('image', 'f1'),
    ('label', '实验3-2.1：判断x是否等于0，两条分支各输出一个结果。'),
    ('image', 'f2'),
    ('label', '实验3-2.2：读入整数后判奇偶，是奇数才输出平方。'),
    ('image', 'f3'),
    ('label', '实验3-3：读入字符，判断是否为大写字母后再转换输出。'),
    ('image', 'f4'),
    ('label', '实验3-4的if版本：先拦截非法分数，再按90、80、70、60依次分级。'),
    ('image', 'f5'),
    ('label', '实验3-4的switch版本：按十位数分组，case 10与0到9两组再嵌套判断，末尾用default兜底。'),
    ('image', 'f6'),
]

SOURCE = [
    ('实验3-1：', '3-1.c'),
    ('实验3-2.1：', '3-2.1.c'),
    ('实验3-2.2：', '3-2.2.c'),
    ('实验3-3：', '3-3.c'),
    ('实验3-4.1（if版）：', '3-4.1-if.c'),
    ('实验3-4.1（switch版）：', '3-4.1-switch.c'),
    ('实验3-4.3（if版）：', '3-4.3-if.c'),
    ('实验3-4.3（switch版）：', '3-4.3-switch.c'),
]

STEPS = [
    ('body', '（1）实验步骤：'),
    ('body', '1. 打开Dev-C++，新建源文件，按题目要求输入代码。'),
    ('body', '2. 编译前先检查引号、分号与格式符，再按F11编译。'),
    ('body', '3. 编译通过后运行，按题目给定的数据测试，记录输出。'),
    ('body', '4. 出现报错时按提示行号定位并修改，重新编译运行。'),
    ('body', '（2）调试过程与错误记录：'),
    ('body', '编写与调试中一共遇到五处问题，分别记录如下。'),
    ('body', '错误一：putchar的参数传成了字符串。'),
    ('body', '错误现象：编译通过，但控制台提示[Warning] passing argument 1 of ‘putchar’ '
             'makes integer from pointer without a cast [-Wint-conversion]，指向putchar("\\n")那一行。'),
    ('body', '原因分析：双引号括起来的是字符串常量，传进putchar时退化成指针，'
             '而putchar要的是字符对应的编码。'),
    ('body', "解决办法：把双引号改成单引号，写成putchar('\\n')。"),
    ('body', '调试结果：警告消失，换行正常输出。'),
    ('body', '错误二：输入缓冲区里残留的回车被第二次读走。'),
    ('body', '错误现象：输入一个字符并回车后，程序没有等待第二次输入就结束，'
             '第二个字符打印出来是空行。'),
    ('body', '原因分析：getchar按字节顺序从缓冲区取数据，回车产生的换行符留在缓冲区里，'
             '被下一次getchar读走。'),
    ('body', '解决办法：在两次读取之间加一句getchar()，把回车符吃掉。'),
    ('body', '调试结果：输入A回车B，输出A、B两行，两种输出方式结果一致。'),
    ('body', '错误三：中文输入法下输入的字母是全角字符。'),
    ('body', '错误现象：输入大写F，实验3-3输出一个问号。'),
    ('body', '原因分析：全角字符占两个字节，scanf("%c")只取其中一个字节，取到的值不在A到Z的区间内，'
             '程序走else分支原样输出。'),
    ('body', '解决办法：输入前按Shift切换到英文半角；排查时可以在scanf后加一句按%d打印编码的调试输出。'),
    ('body', '调试结果：半角输入F后正确输出The lower letter is:f。'),
    ('body', '错误四：if链只写了下限，越界分数被前面的分支接住。'),
    ('body', '错误现象：实验3-4.1的if版本输入105输出A，输入-70输出E。'),
    ('body', '原因分析：第一个分支只判断score>=90，没有上限，105满足条件直接输出A；'
             '负数一路不满足，最后落到else输出E。'),
    ('body', '解决办法：在分级之前先判断score<0||score>100，成立就输出“输入数据错”并跳过后续分级。'),
    ('body', '调试结果：实验3-4.3的if版本输入105与-70都输出“输入数据错”。'),
    ('body', '错误五：switch依赖整数除法截断，外层又缺少default。'),
    ('body', '错误现象：实验3-4.1的switch版本输入105输出A、输入-5输出E，输入-70时程序没有任何输出就结束。'),
    ('body', '原因分析：score/=10把105截成10，命中case 10；-5截成0，落进0那一组输出E；'
             '-70截成-7，没有任何case与之匹配，外层又没有default，整个switch被跳过。'),
    ('body', '解决办法：外层switch末尾补default输出“输入数据错”；case 10里再判断score==100，'
             '0到9那一组里再判断score>=0，把100与0附近的边界单独处理。'),
    ('body', '调试结果：实验3-4.3的switch版本输入100输出A，输入105、-5、-70都输出“输入数据错”。'),
    ('body', '（3）最终运行验证：'),
    ('body', '实验3-1输入A回车B，输出A、B、===、A、B；两个字符连写成AB时，中间的getchar会把B吃掉，'
             '第二个字符变成空行。'),
    ('body', '实验3-2.1输出x=4；实验3-2.2输入5输出b=25，输入4没有任何输出。'),
    ('body', '实验3-3输入F与f，都输出The lower letter is:f。'),
    ('body', '实验3-4.1的if版与switch版：95输出A，105输出A，-70时if版输出E、switch版也输出E。'),
    ('body', '实验3-4.3的if版与switch版：95与100输出A，105、-5、-70都输出“输入数据错”。'),
    ('body', '结果说明：八段程序编译运行都没有报错，输出与推算结果一致。'),
]

ANALYSIS = [
    ('body', '（1）实验3-1运行结果与分析：'),
    ('body', '输入A回车B，c1读到A，中间那句getchar读到回车，c2读到B，printf把两个字符各输出一行；'
             "putchar按编码输出同一个字符，但它不会自动换行，所以每输出一个字符都要再补一个putchar('\\n')。"),
    ('body', '分析：getchar按字节顺序读取，回车不会被跳过，这就是必须手动吃回车的原因。'
             '把两个字符连写成AB时，中间那句getchar会把B读走，c2变成换行符，输出里只剩一个A和一行空白，'
             '说明输入函数完全按缓冲区顺序工作。printf用%s、%c等格式符一次可以输出多个字符，'
             'putchar一次只能输出一个字符，两者都需要自己控制换行。'),
    ('body', '（2）实验3-2运行结果与分析：'),
    ('body', '第一段程序里x=3，x==0不成立，走else分支，输出x+1，结果是x=4。'
             '第二段程序输入5，5%2!=0成立，算出b=25并输出；输入4时条件不成立，if体不执行，程序直接结束。'),
    ('body', '分析：if-else只看条件真假，两条分支必走其一，所以第一段程序一定有输出；'
             '第二段只有一个if，条件不成立时什么也不做，这与“只处理奇数”的要求相符。'),
    ('body', '（3）实验3-3运行结果与分析：'),
    ('body', '输入半角F时，条件判断成立，x=x-‘A’+‘a’把70换算成102，赋给y后输出f；'
             '输入小写f时条件不成立，走else把x原样赋给y，输出仍是f。'),
    ('body', '分析：表达式x-‘A’+‘a’利用的是ASCII码中大写字母与小写字母相差32的规律，'
             '也可以直接写成x+32。判断条件必须写成‘A’<=x&&x<=‘Z’，缺了任意一边都会把别的字符放进来。'
             '输入全角字母时读到的是多字节字符的一半，条件不成立，所以输出问号。'),
    ('body', '（4）实验3-4运行结果与分析：'),
    ('body', 'if版按90、80、70、60从高到低依次判断，命中一个分支就输出并跳出；'
             'switch版先把分数除以10，用十位数分组，靠的是整数除法截断。'
             '两个实验3-4.1的版本都没有做非法值处理，105照样输出A，-70照样输出E。'),
    ('body', '分析：实验3-4.3的if版在最前面加了score<0||score>100的拦截，越界就直接输出“输入数据错”；'
             'switch版则在外层补default，并在case 10与0到9里再嵌套判断score==100与score>=0，'
             '把100、0这两个边界和负数都覆盖住。switch只能按离散值分支，用它做区间判断时必须借助除法，'
             '而除法会截断，边界就得自己补，这是这次实验最主要的教训。'),
    ('body', '（5）实验总结：'),
    ('body', '通过本次实验，掌握了getchar与putchar的用法、printf的格式转换符、逻辑运算符与逻辑表达式，'
             '以及if与switch两种分支结构的写法。体会最深的有三点：输入函数按字节顺序读取，'
             '回车也会被读走，必要时要用getchar把多余的字符吃掉；switch只能依据整数或字符的离散值分支，'
             '用除法分组时必须自己补边界，default不能省；非法数据要在程序开头先拦截，'
             '否则会被后面的条件意外接住。另外输入时要注意输入法的半角与全角状态，'
             '否则%c读到的可能只是一个多字节字符的一半。'),
]


def build(template, out):
    doc = docx.Document(template)

    anchor = find_anchor(doc, '实验目的')
    for line in PURPOSE:
        anchor = add_paragraph(doc, anchor, kind='body', text=line)

    anchor = find_anchor(doc, '实验内容和要求')
    for kind, text in CONTENT:
        anchor = add_paragraph(doc, anchor, kind=kind, text=text)

    anchor = find_anchor(doc, '实验原理')
    for kind, value in PRINCIPLE:
        if kind == 'image':
            anchor = add_paragraph(doc, anchor, kind='image', image=value)
        else:
            anchor = add_paragraph(doc, anchor, kind='label', text=value)

    anchor = find_anchor(doc, '源程序')
    for label, name in SOURCE:
        anchor = add_paragraph(doc, anchor, kind='label', text=label)
        anchor = add_code_block(doc, anchor, name)

    anchor = find_anchor(doc, '实验步骤与调试')
    for kind, text in STEPS:
        anchor = add_paragraph(doc, anchor, kind=kind, text=text)

    anchor = find_anchor(doc, '实验结果与分析')
    for kind, text in ANALYSIS:
        anchor = add_paragraph(doc, anchor, kind=kind, text=text)

    # 删掉骨架留下的空段落（只含制表符或空），代码块里的空行与插图段落保留
    for para in list(doc.paragraphs):
        if para.text.strip():
            continue
        if any(para._p.findall('.//' + qn(x)) for x in ('w:drawing', 'w:pict')):
            continue
        if (para.paragraph_format.line_spacing or 1.5) < 1.2:
            continue
        parent = para._p.getparent()
        if parent is not None:
            parent.remove(para._p)

    doc.save(out)
    print('saved ' + out)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('用法：python build_report3.py <模板.docx> <输出.docx>')
    build(sys.argv[1], sys.argv[2])
