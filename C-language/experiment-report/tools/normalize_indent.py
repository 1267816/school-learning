#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一实验报告的缩进：正文左缩进0磅、首行缩进2字符（21磅）。

用法：python normalize_indent.py <输入.docx> <输出.docx>

规则：
- 一级标题（实验目的、实验内容和要求、主要仪器设备、实验原理、源程序、实验步骤与调试、
  实验结果与分析）：左缩进0、首行缩进0、1.5倍行距，字体字号不动
- 正文、二级标签、编号小标题：左缩进0、首行缩进21磅（2字符）、1.5倍行距，去掉段首制表符
- 代码段：保持左缩进42.8磅、首行缩进0、单倍行距，字号不动
- 插图段落：居中、左缩进0、首行缩进0、单倍行距
- 非代码段落里的 Consolas 字符改成 Times New Roman 12磅
- 末尾空段落删除
"""
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt

HEADINGS = ('实验目的', '实验内容和要求', '主要仪器设备', '实验原理', '源程序',
            '实验步骤与调试', '实验结果与分析')
CODE_INDENT = 42.8
FIRST_LINE = 21.0


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


def force_tnr(run):
    run.font.name = 'Times New Roman'
    if not run.font.size:
        run.font.size = Pt(12)
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn('w:rFonts'))
    if fonts is None:
        fonts = docx.oxml.OxmlElement('w:rFonts')
        rpr.insert(0, fonts)
    fonts.set(qn('w:ascii'), 'Times New Roman')
    fonts.set(qn('w:hAnsi'), 'Times New Roman')
    fonts.set(qn('w:eastAsia'), '宋体')


def split_linebreak_paragraphs(doc, sections):
    """把段内用换行分成多行的正文拆成独立段落，让每行都能吃到首行缩进。"""
    current = None
    for para in list(doc.paragraphs):
        text = para.text.strip()
        if text in HEADINGS:
            current = text
            continue
        if current not in sections:
            continue
        if is_code(para) or has_image(para):
            continue
        if '\n' not in para.text:
            continue
        lines = [line.strip() for line in para.text.split('\n') if line.strip()]
        if len(lines) < 2:
            continue
        anchor = para._p
        for line in lines:
            new_p = doc.add_paragraph()
            anchor.addnext(new_p._p)
            anchor = new_p._p
            new_p.style = para.style
            run = new_p.add_run(line)
            run.font.size = Pt(12)
            run.font.name = 'Times New Roman'
            rpr = run._element.get_or_add_rPr()
            fonts = rpr.find(qn('w:rFonts'))
            if fonts is None:
                fonts = docx.oxml.OxmlElement('w:rFonts')
                rpr.insert(0, fonts)
            fonts.set(qn('w:ascii'), 'Times New Roman')
            fonts.set(qn('w:hAnsi'), 'Times New Roman')
            fonts.set(qn('w:eastAsia'), '宋体')
            set_fmt(new_p, 0, FIRST_LINE, 1.5)
        para._p.getparent().remove(para._p)


def main(src, dst):
    d = docx.Document(src)
    split_linebreak_paragraphs(d, ('实验目的', '主要仪器设备', '实验原理', '源程序', '实验步骤与调试', '实验结果与分析'))
    section = None
    for para in list(d.paragraphs):
        text = para.text.strip()
        if text in HEADINGS:
            set_fmt(para, 0, 0, 1.5)
            section = text
            continue
        if section == '实验内容和要求':
            continue
        if has_image(para):
            set_fmt(para, 0, 0, 1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
            continue
        if is_code(para):
            set_fmt(para, CODE_INDENT, 0, 1.0)
            continue
        if section == '源程序' and not text:
            set_fmt(para, CODE_INDENT, 0, 1.0)
            continue
        if section in ('实验目的', '主要仪器设备', '实验原理', '源程序',
                       '实验步骤与调试', '实验结果与分析'):
            strip_leading_tabs(para)
            set_fmt(para, 0, FIRST_LINE, 1.5)
            for run in para.runs:
                if run.text.strip() and western(run) == 'Consolas':
                    force_tnr(run)

    for para in reversed(d.paragraphs):
        if para.text.strip() or has_image(para):
            break
        d.element.body.remove(para._p)

    d.save(dst)
    print('saved ' + dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
