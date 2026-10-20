#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一实验报告各节的段前段后间距，让两份报告的行位置上下对齐。

用法：python align_spacing.py <输入.docx> <输出.docx>

规则（与实验1定稿一致）：
- 实验目的三条：段前段后各7.8磅
- 实验内容和要求一节：每组标题「1．实验内容」「2. 实验内容2」这类段前15.6磅、段后7.8磅；
  其余行段前段后各7.8磅
- 其余各节（实验原理、源程序、实验步骤与调试、实验结果与分析、主要仪器设备）：段前段后0
- 封面与一级标题不动
"""
import re
import sys

import docx
from docx.shared import Pt

HEADINGS = ('实验目的', '实验内容和要求', '主要仪器设备', '实验原理', '源程序',
            '实验步骤与调试', '实验结果与分析')


def set_space(para, before, after):
    para.paragraph_format.space_before = Pt(before)
    para.paragraph_format.space_after = Pt(after)


def main(src, dst):
    d = docx.Document(src)
    section = None
    for para in d.paragraphs:
        text = para.text.strip()
        if text in HEADINGS:
            section = text
            continue
        if section is None:
            continue
        if section == '实验目的':
            set_space(para, 7.8, 7.8)
        elif section == '实验内容和要求':
            is_heading = bool(re.match(r'^[0-9]+[．.]\s*实验内容', text.replace('\t', '')))
            if is_heading:
                set_space(para, 15.6, 7.8)
            else:
                set_space(para, 7.8, 7.8)
        else:
            set_space(para, 0, 0)
    d.save(dst)
    print('saved ' + dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
