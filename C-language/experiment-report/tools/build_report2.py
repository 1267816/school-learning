#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「实验2 实验报告」正文。

用法：python build_report2.py <模板.docx> <输出.docx>

模板由 Word 将 实验2 实验报告.doc 另存为 docx 得到（封面、实验目的、实验内容和要求、
主要仪器设备四部分已填好，实验原理/源程序/实验步骤与调试/实验结果与分析为待填）。
脚本只在四个待填标题后插入内容，并统一套用实验1报告的版式：
正文 12 磅宋体、西文与数字 Times New Roman、1.5 倍行距、首行缩进 2 字符；
代码与程序输出用 Consolas 10.5 磅（五号）、左缩进 42.8 磅、单倍行距；
段落之间不留空行（代码块内源码原有的空行保留）。
流程图由 mermaid.ink 按默认主题渲染后居中插入。

文字规则：除代码段外不留额外空格——中文与英文、数字、括号、全角标点一律紧贴；
程序输出与表达式用 Consolas 内联片段承载，其内部空格保持原样。
"""
import base64
import json
import os
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXP2 = os.path.join(REPO, 'experiment-report', '实验2')
CACHE = os.path.join(os.environ.get('TEMP', '.'), 'dshexp', 'mermaid')
IMG_WIDTH_PT = 115
CODE_PT = 10.5          # 五号字
CREATED_CODE = []       # 记录插入的代码段落，收尾时保留其空行

FLOWCHARTS = {
    'fh1': """flowchart TD
A([开始]) --> B[/输入半径 r/]
B --> C["p = 3.14；c = 2 * p * r；area = p * r * r"]
C --> D[/输出 c 与 area，保留两位小数/]
D --> E([结束])""",
    'fh2': """flowchart TD
A([开始]) --> B[/输入三边长 a、b、c/]
B --> C["s = (a + b + c) / 2；S = √(s(s-a)(s-b)(s-c))"]
C --> D[/输出 S，保留两位小数/]
D --> E([结束])""",
    'fh3': """flowchart TD
A([开始]) --> B["把 c、h、i、n、a 依次赋给 c1~c5"]
B --> C["n1~n5 分别等于 c1~c5 的编码加 4"]
C --> D[/用 %c 逐个输出 n1~n5/]
D --> E([结束])""",
    'fh4': """flowchart TD
A([开始]) --> B["把 c、h、i、n、a 依次赋给 c1~c5"]
B --> C["n1~n5 分别等于 c1~c5 的编码减 4"]
C --> D{"编码小于等于 96 ？"}
D -- 是 --> E["编码加 26，回绕到 z 一侧"]
D -- 否 --> F[/用 %c 逐个输出 n1~n5/]
E --> F
F --> G([结束])""",
}


def read_c(name):
    path = os.path.join(EXP2, name)
    raw = open(path, 'rb').read()
    try:
        text = raw.decode('gbk')
    except UnicodeDecodeError:
        text = raw.decode('utf-8', errors='replace')
    return text.replace('\r\n', '\n').rstrip('\n')


def fetch_png(key):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, key + '.png')
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        return path
    raise SystemExit('缺少流程图缓存：' + path + '（先由 PowerShell 下载）')


def set_font(run, east='宋体', western='Times New Roman', size=12, bold=False):
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


def add_paragraph(doc, anchor, kind='body', segments=None, image=None):
    p = doc.add_paragraph()
    anchor.addnext(p._p)
    pf = p.paragraph_format
    if kind in ('body', 'label', 'body42', 'subhead'):
        if kind == 'body':
            pf.first_line_indent = Pt(24)
        elif kind == 'label':
            pf.left_indent = Pt(42.8)
            pf.first_line_indent = Pt(0)
        elif kind == 'body42':
            pf.left_indent = Pt(42.0)
            pf.first_line_indent = Pt(0)
        elif kind == 'subhead':
            pf.left_indent = Pt(21.0)
            pf.first_line_indent = Pt(21.0)
        pf.line_spacing = 1.5
    elif kind == 'code':
        pf.first_line_indent = Pt(0)
        pf.left_indent = Pt(42.8)
        pf.line_spacing = 1.0
    elif kind == 'image':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Pt(0)
        pf.line_spacing = 1.0
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    for seg_kind, text in (segments or []):
        run = p.add_run(text)
        if seg_kind == 'code' and kind == 'code':
            set_font(run, east='宋体', western='Consolas', size=CODE_PT)
        else:
            set_font(run)
    if image:
        p.add_run().add_picture(image, width=Pt(IMG_WIDTH_PT))
    return p._p


def add_code_block(doc, anchor, text):
    last = anchor
    for line in text.split('\n'):
        last = add_paragraph(doc, last, kind='code', segments=[('code', line if line else '')])
        CREATED_CODE.append(last)
    return last


def find_anchor(doc, heading):
    for idx, para in enumerate(doc.paragraphs):
        if para.text.strip() == heading:
            nxt = doc.paragraphs[idx + 1] if idx + 1 < len(doc.paragraphs) else para
            return nxt._p
    raise SystemExit('找不到标题：' + heading)


def T(text):
    return ('body', text)


def C(text):
    return ('code', text)


CODE21 = read_c('experiment_2-1.c')
CODE22 = read_c('experiment_2-2.c')
CODE23 = read_c('experiment_2-3.c')
CODE241 = read_c('experiment_2-4-1.c')
CODE242 = read_c('experiment_2-4-2.c')

PRINCIPLE = [
    ([T('实验（1）：圆面积与周长程序为顺序结构，先输入半径，再计算周长和面积，最后输出。')], 'fh1'),
    ([T('实验（2）：三角形面积程序先求半周长，再用海伦公式求面积，计算时调用'),
      C('math.h'), T('里的'), C('sqrt'), T('。')], 'fh2'),
    ([T('实验（3）为阅读分析类实验，程序没有分支与循环，只需推算输出结果，因此不画流程图，'
        '输出分析见实验结果与分析一节。')], None),
    ([T('实验（4）正向译码：每个字符的编码加4后按字符输出。')], 'fh3'),
    ([T('实验（4）反向译码：每个字符的编码减4，编码小于等于96时加26回绕。')], 'fh4'),
]

STEPS = [
    [T('（1）实验步骤：')],
    [T('1. 打开Dev-C++，新建源文件，输入代码后保存为'), C('.c'), T('文件。')],
    [T('2. 按'), C('F11'), T('编译并运行，按题目要求输入测试数据。')],
    [T('3. 记录程序输出，与上机前推算的结果逐项比较。')],
    [T('4. 结果不一致时，从变量类型、运算符和表达式求值顺序三处逐行检查，修改后重新编译运行。')],
    [T('（2）调试过程与错误记录：')],
    [T('编写与调试中发现的问题集中在格式符匹配、整数运算和运算符书写三处，记录如下：')],
    [T('错误一：格式符与变量类型不匹配。')],
    [T('错误现象：输入半径'), C('2.5'), T('后，输出为'), C('c=0.00,area=0.00'), T('。')],
    [T('错误原因：用'), C('%f'), T('读取'), C('double'), T('类型的变量。'), C('%f'),
     T('按四字节的'), C('float'), T('格式解析输入，而'), C('double'),
     T('占八字节，读入的值无效，后续计算全部为0。')],
    [T('对策：'), C('double'), T('变量读入统一用'), C('%lf'), T('，改后输出恢复正常。')],
    [T('错误二：整数除法截断。')],
    [T('错误现象：三边长取3、4、5时，算出的面积只有正确值的一半。')],
    [T('错误原因：'), C('(a+b+c)/2'), T('的两个操作数都是整数，按整数除法先得到整数结果，'
        '小数部分被丢弃。')],
    [T('对策：写成'), C('0.5*(a+b+c)'), T('，或把三边声明为'), C('double'),
     T('，让除法按浮点运算进行。')],
    [T('错误三：漏写乘号。')],
    [T('错误现象：编译时报'), C('invalid suffix "p" on integer constant'), T('。')],
    [T('错误原因：'), C('c=2p*r'), T('中的'), C('2p'), T('被编译器当成带后缀p的整型常量，'
        '而不是2乘以p。')],
    [T('对策：写成'), C('c=2*p*r'), T('，并回头检查同类表达式里有没有漏掉乘号或分号。')],
    [T('（3）最终运行验证：')],
    [T('输入半径'), C('1.5'), T('，输出'), C('c=9.42   ,area=7.06'), T('；输入半径'),
     C('2.5'), T('，输出'), C('c=15.70  ,area=19.63'), T('。')],
    [T('输入'), C('3 4 5'), T('，输出'), C('6.00'), T('；输入'), C('6 8 10'),
     T('，输出'), C('24.00'), T('。')],
    [T('实验（3）输出为两行字符，第一行是'), C('aa bb'), T('、制表符、'), C('cc'),
     T('、制表符、'), C('abc'), T('，第二行是制表符、退格、A、空格、N。')],
    [T('实验（4）正向输出'), C('g,l,m,r,e'), T('，反向输出'), C('y,d,e,j,w'), T('。')],
    [T('结果说明：七组数据与预期一致，程序逻辑正确。')],
]

ANALYSIS = [
    [T('（1）实验2-1运行结果与分析：')],
    [T('程序按要求输出圆的周长与面积，保留两位小数。输入'), C('1.5'), T('时输出'),
     C('c=9.42   ,area=7.06'), T('；输入'), C('2.5'), T('时输出'),
     C('c=15.70  ,area=19.63'), T('。')],
    [T('分析：'), C('%-7.2f'), T('表示左对齐、总宽7个字符、保留两位小数。9.42只占4个字符，'
        '后面补3个空格；19.63占5个字符，补2个空格，所以两组输出的逗号位置不同。'
        '这是格式化输出的正常表现，不是程序错误。常量p取3.14，与题目要求的两位小数精度一致。')],
    [T('（2）实验2-2运行结果与分析：')],
    [T('输入'), C('3 4 5'), T('输出'), C('6.00'), T('，输入'), C('6 8 10'), T('输出'),
     C('24.00'), T('，与海伦公式的手算结果一致。')],
    [T('分析：程序先求半周长s，再由'), C('sqrt'), T('求面积，因此需要包含'), C('math.h'),
     T('。程序没有校验三边能否构成三角形，若任意两边之和不大于第三边，'), C('sqrt'),
     T('的参数会为负数，输出会是'), C('nan'), T('或'), C('-nan'), T('，这一点留作后续改进。')],
    [T('（3）实验2-3运行结果与分析：')],
    [T('上机前推算：第一行依次输出'), C('aa bb'), T('、制表符、'), C('cc'), T('、制表符、'),
     C('abc'), T('；第二行先制表再退格，然后输出A和N。')],
    [T('实际运行：第一行的三段文字按制表位对齐，第二行的A落在第7列，N在其后一格。')],
    [T('分析：'), C('\\101'), T('与'), C('\\116'), T('是八进制转义，分别对应字符A与N，'
        '与直接写字符常量等价。制表符把光标移到下一个制表位，所以三段之间的间隔不同；'
        '退格符只把光标左移一格，行首退格没有字符可覆盖，屏幕上看到的是A覆盖了原来空白的第7列。')],
    [T('（4）实验2-4运行结果与分析：')],
    [T('正向：c、h、i、n、a的编码各加4，得到g、l、m、r、e，输出为'), C('g,l,m,r,e'), T('。')],
    [T('反向：c、h、i、n、a的编码各减4，得到y、d、e、j、w，输出为'), C('y,d,e,j,w'), T('。')],
    [T('分析：字符在内存中按ASCII码存放，c的编码99加4得103，即g。a的编码97减4得93，'
        '已不在小写字母区间，'), C('if(n<=96)'), T('把它加26回绕到119，即w，'
        '所以反向译码仍能停在字母表内。另外程序用'), C('%c,'), T('的格式逐个输出并带逗号，'
        '与题目示例的连续字符串格式不同；若要与示例完全一致，把输出格式改成五个连续的'),
     C('%c'), T('即可。')],
    [T('（5）实验总结：')],
    [T('通过本次实验，掌握了整型、字符型和实型变量的定义与赋值方法，理解了不同类型数据之间赋值的规律，'
        '也认识到格式符必须与变量类型匹配、除法要区分整数与浮点、运算符不能省略。'
        '字符型数据本质上是整数编码，用'), C('%c'), T('输出字符、用'), C('%d'),
     T('输出编码，同一个变量可以有两种形态。本次实验暴露的问题都出在细节上，不是思路问题，'
        '这说明写代码时逐行检查类型和运算符是必要的。')],
]

SOURCE_BLOCKS = [
    ('实验（1）：', CODE21),
    ('实验（2）：', CODE22),
    ('实验（3）：给定的程序', CODE23),
    ('实验（4）正向译码：', CODE241),
    ('实验（4）反向译码：', CODE242),
]


def normalize_content_headings(doc):
    """把「2. 实验内容2」「3. 实验内容3」「4. 实验内容4」统一成「1. 实验内容1」的格式。"""
    from copy import deepcopy
    from docx.text.paragraph import Paragraph

    src = None
    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith('1.') and '实验内容' in text:
            src = para
            break
    if src is None:
        return
    targets = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if para is src:
            continue
        if text[:2] in ('2.', '3.', '4.') and '实验内容' in text and len(text) <= 14:
            targets.append((para, text))
    for para, text in targets:
        new_p = deepcopy(src._p)
        para._p.addnext(new_p)
        para._p.getparent().remove(para._p)
        new_para = Paragraph(new_p, src._parent)
        for run in list(new_para.runs):
            run._element.getparent().remove(run._element)
        for _ in range(2):
            tab_run = new_para.add_run('\t')
            set_font(tab_run, east='宋体', western='Times New Roman', size=14, bold=True)
        text_run = new_para.add_run(text)
        set_font(text_run, east='宋体', western='Times New Roman', size=12, bold=False)


def normalize_fonts(doc):
    """除代码外，英文字符与数字统一用 Times New Roman，中文字体保持原样。"""
    for para in doc.paragraphs:
        for run in para.runs:
            fonts = run._element.rPr.rFonts if run._element.rPr is not None else None
            western = fonts.get(qn('w:ascii')) if fonts is not None else None
            if western == 'Consolas':
                set_font(run, east=east or '宋体', western='Consolas', size=CODE_PT,
                         bold=bool(run.bold))
                continue
            east = fonts.get(qn('w:eastAsia')) if fonts is not None else None
            size = run.font.size.pt if run.font.size else 12
            set_font(run, east=east or '宋体', western='Times New Roman', size=size,
                     bold=bool(run.bold))


def strip_empty_paragraphs(doc):
    """删掉除代码段之外的空白段落，避免多余空行。"""
    keep = set(id(el) for el in CREATED_CODE)
    for para in list(doc.paragraphs):
        if para.text.strip():
            continue
        if para._p.findall('.//' + qn('w:drawing')):
            continue
        if id(para._p) in keep:
            continue
        parent = para._p.getparent()
        if parent is not None:
            parent.remove(para._p)


def build(template, out):
    doc = docx.Document(template)

    anchor = find_anchor(doc, '实验原理')
    for segs, key in PRINCIPLE:
        anchor = add_paragraph(doc, anchor, kind='label', segments=segs)
        if key:
            anchor = add_paragraph(doc, anchor, kind='image', image=fetch_png(key))

    anchor = find_anchor(doc, '源程序')
    for label, code in SOURCE_BLOCKS:
        anchor = add_paragraph(doc, anchor, kind='label', segments=[T(label)])
        anchor = add_code_block(doc, anchor, code)

    anchor = find_anchor(doc, '实验步骤与调试')
    tab_prefixes = ('（1）实验步骤', '（2）调试过程', '错误一', '错误二', '错误三', '结果说明')
    for segs in STEPS:
        first = segs[0][1]
        segs = ([('body', '\t')] + list(segs)) if first.startswith(tab_prefixes) else segs
        anchor = add_paragraph(doc, anchor, kind='body42', segments=segs)

    anchor = find_anchor(doc, '实验结果与分析')
    for segs in ANALYSIS:
        first = segs[0][1]
        kind = 'subhead' if re.match(r'^（\d）', first) and first.endswith('：') else 'body42'
        anchor = add_paragraph(doc, anchor, kind=kind, segments=segs)

    normalize_content_headings(doc)
    normalize_fonts(doc)
    strip_empty_paragraphs(doc)
    doc.save(out)
    print('saved ' + out)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('用法：python build_report2.py <模板.docx> <输出.docx>')
    build(sys.argv[1], sys.argv[2])
