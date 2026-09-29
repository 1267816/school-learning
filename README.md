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

- C 语言用 Dev-C++ 编写和编译（教室里是 Dev-C++ 5.11）
- `.gitignore` 已排除 `.exe`、`.o` 等编译产物，仓库里只保留源码

### 源码编码：保持 ANSI（GBK），不要另存为 UTF-8

`C-language/` 里的 `.c` 文件是在教室电脑上用 Dev-C++ 5.11 写的，它默认按系统的 ANSI 代码页
保存（简体中文 Windows 就是 GBK），所以中文注释在文件里是 GBK 字节。

- **在家用 VS Code 打开时显示乱码是正常的**：VS Code 默认按 UTF-8 解码。点右下角状态栏的
  编码（默认显示 `UTF-8`）→ 选 `Reopen with Encoding` → 选 **GBK**，中文注释就正常了。
  要保存回 GBK 就用同一菜单里的 `Save with Encoding` → GBK。
- **在教室电脑上不要改 Dev-C++ 的编码设置**，保持默认（ANSI）就行。
- **不要在 VS Code 里把文件另存为 UTF-8**：这样再拿到教室电脑上用 Dev-C++ 5.11 打开又会乱码。
  两边来回转就会出现"怎么又乱了"。如果以后确实想把整个仓库统一成 UTF-8，要两边一起改，
  并且编译时加 `-fexec-charset=GBK`，否则在 GBK 控制台里打印的中文也会乱码。
- 判断办法很简单：中文注释乱码，说明当前编辑器用的编码和文件本身不一致，换成另一个编码
  （GBK ↔ UTF-8）试一下就知道。
