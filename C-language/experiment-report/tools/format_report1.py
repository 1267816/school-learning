#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把实验1报告改成实验2报告现在的版式。

用法：python format_report1.py <输入.docx> <输出.docx>

规则（对齐实验2报告）：
- 一级标题：左缩进42.8磅、悬挂42.8磅（首行回到页边距），1.5倍行距，14磅加粗不动
- 实验目的正文、实验原理标签、源程序标签：左缩进42.8磅，不设首行缩进，1.5倍行距
- 主要仪器设备两行：左缩进0、首行缩进21磅，1.5倍行距
- 实验步骤与调试正文：左缩进42磅，不设首行缩进，1.5倍行距，去掉段首制表符
- 实验结果与分析：编号小标题左缩进21磅＋首行缩进21磅，其余正文左缩进42磅
- 代码段：Consolas 10.5磅，左缩进42.8磅，单倍行距
- 插图段落：居中，左缩进0，单倍行距
- 末尾空段落删除
"""
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt

HEADINGS = ('实验目的', '实验内容和要求', '主要仪器设备', '实验原理', '源程序',
            '实验步骤与调试', '实验结果与分析')
CODE_PT = 10.5


def western(run):
    if run._element.rPr is not None and run._element.rPr.rFonts is not None:
        return run._element.rPr.rFonts.get(qn('w:ascii'))
    return None


def set_fmt(para, li, fli, ls, align=None):
    pf = para.paragraph_format
    pf.left_indent = Pt(li)
    pf.first_line_indent = Pt(fli)
    pf.line_spacing = ls
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    if align is not None:
        para.alignment = align


def has_image(para):
    for tag in ('w:drawing', 'w:pict'):
        if para._p.findall('.//' + qn(tag)):
            return True
    if para._p.findall('.//{urn:schemas-microsoft-com:vml}imagedata'):
        return True
    if para._p.findall('.//{urn:schemas-microsoft-com:vml}shape'):
        return True
    return False


def is_code(para):
    texts = [r for r in para.runs if r.text.strip()]
    return bool(texts) and all(western(r) == 'Consolas' for r in texts)


def strip_leading_tabs(para):
    for run in para.runs:
        if run.text.startswith('\t'):
            run.text = run.text.lstrip('\t')
        elif run.text.strip() == '':
            continue
        else:
            break


def main(src, dst):
    d = docx.Document(src)
    section = None
    for para in list(d.paragraphs):
        text = para.text.strip()
        if text in HEADINGS:
            set_fmt(para, 42.8, -42.8, 1.5)
            section = text
            continue
        if has_image(para):
            set_fmt(para, 0, 0, 1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
            continue
        if is_code(para) or (section == '源程序' and not text and not has_image(para)):
            for run in para.runs:
                if run.text.strip():
                    run.font.size = Pt(CODE_PT)
                    run.font.name = 'Consolas'
                    rpr = run._element.get_or_add_rPr()
                    fonts = rpr.find(qn('w:rFonts'))
                    if fonts is None:
                        fonts = docx.oxml.OxmlElement('w:rFonts')
                        rpr.insert(0, fonts)
                    fonts.set(qn('w:ascii'), 'Consolas')
                    fonts.set(qn('w:hAnsi'), 'Consolas')
                    fonts.set(qn('w:eastAsia'), '宋体')
            set_fmt(para, 42.8, 0, 1.0)
            continue
        if section == '实验目的':
            set_fmt(para, 42.8, 21, 1.5)
        elif section == '主要仪器设备':
            set_fmt(para, 0, 21, 1.5)
        elif section == '实验原理':
            set_fmt(para, 42.8, 21, 1.5)
        elif section == '源程序':
            set_fmt(para, 42.8, 21, 1.5)
        elif section == '实验步骤与调试':
            strip_leading_tabs(para)
            set_fmt(para, 42, 21, 1.5)
        elif section == '实验结果与分析':
            if text.startswith('（') and text.endswith('：'):
                set_fmt(para, 21, 21, 1.5)
            else:
                set_fmt(para, 42, 21, 1.5)

    # 非代码段落里的等宽字体归位成 Times New Roman 12磅
    for para in d.paragraphs:
        if is_code(para):
            continue
        for run in para.runs:
            if western(run) == 'Consolas':
                run.font.name = 'Times New Roman'
                run.font.size = Pt(12)
                rpr = run._element.get_or_add_rPr()
                fonts = rpr.find(qn('w:rFonts'))
                if fonts is None:
                    fonts = docx.oxml.OxmlElement('w:rFonts')
                    rpr.insert(0, fonts)
                fonts.set(qn('w:ascii'), 'Times New Roman')
                fonts.set(qn('w:hAnsi'), 'Times New Roman')
                fonts.set(qn('w:eastAsia'), '宋体')

    # 删掉末尾空段落
    body = d.element.body
    for para in reversed(d.paragraphs):
        if para.text.strip() or has_image(para):
            break
        body.remove(para._p)

    d.save(dst)
    print('saved ' + dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
