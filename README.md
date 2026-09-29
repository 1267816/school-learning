# school-learning

记录学校上课学习的相关内容。

## 目录

| 目录 | 内容 |
| --- | --- |
| `C-language/` | C 语言课的课件、实验指导与实验代码 |
| `advanced-mathematics/` | 高等数学的课件与笔记 |
| `linear-algebra/` | 线性代数的课件与笔记 |

## 目录约定

每门课一个文件夹，文件夹里再按用途分：

- `docs/`：课件、实验指导等课程资料
- `notes/`：笔记
- 有代码的课程另放代码目录，例如 `C-language/c-files/experiment/` 放实验代码

实验代码的文件名体现序号，例如 `experiment_1-1.c` 是第 1 次实验第 1 题。

空目录里的 `.gitkeep` 是占位文件，用来让 git 保留该目录（git 本身不跟踪空目录）。

## 环境与约定

- C 语言用 Dev-C++ 编写和编译；源码目前多为 ANSI（GBK）编码（Dev-C++ 的默认编码），
  用其他编辑器打开时注意选对编码，否则注释里的中文会乱码
- `.gitignore` 已排除 `.exe`、`.o` 等编译产物，仓库里只保留源码
