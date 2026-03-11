# PDF 离线解密/去加密工具（已知密码）& 字典尝试脚本（需授权）

本项目用于对 **你本人或已获明确授权** 的 PDF 进行离线处理：

- `decrypt_pdf.py`：**已知密码**情况下，将加密 PDF 另存为**不加密**的 PDF（支持单文件/批量）。
- `1.py`：基于**字典文件**对加密 PDF 进行**密码尝试**（仅供学习/授权场景；速度取决于字典大小与文件情况）。
- `filter_6digits.ps1`：从大字典（如 `rockyou.txt`）里筛出 **6 位纯数字**行，生成更小的 `rockyou_6digits.txt`（便于实验）。

> 重要提示：请遵守法律法规与目标系统/文件的使用条款。不要将包含隐私的 PDF 或大型字典文件推送到公开仓库（本仓库默认 `.gitignore` 已忽略 `*.pdf` 与 `rockyou*.txt`）。

## 环境要求

- Windows / macOS / Linux
- Python 3.9+

## 安装

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
```

## 1) 已知密码：解密/去加密（推荐用这个）

### 单个 PDF

```bash
python decrypt_pdf.py --in "C:\path\file.pdf" --out "C:\path\file.decrypted.pdf" --password "你的密码"
```

### 批量处理一个文件夹（匹配 `*.pdf`）

```bash
python decrypt_pdf.py --in-dir "C:\path\pdfs" --out-dir "C:\path\out" --password "你的密码" --recursive
```

### 批量模式：保持目录结构

如果你希望输出目录保留输入目录的相对路径结构：

```bash
python decrypt_pdf.py --in-dir "C:\path\pdfs" --out-dir "C:\path\out" --password "你的密码" --recursive --keep-structure
```

### 参数说明（`decrypt_pdf.py`）

- `--in`：输入 PDF 文件（与 `--in-dir` 二选一）
- `--in-dir`：输入目录（批量模式，扫描 `*.pdf`）
- `--out`：输出 PDF 文件路径（单文件模式必填）
- `--out-dir`：输出目录（批量模式必填）
- `--password`：PDF 密码（打开密码/权限密码）
- `--recursive`：批量模式递归扫描子目录
- `--keep-structure`：批量模式保持输入目录结构

## 2) 字典尝试密码（`1.py`，仅限授权/学习）

`1.py` 会读取字典文件逐行尝试打开 PDF，成功后打印密码并尝试写回 PDF（去除打开密码）。

注意事项：

- 字典文件通常非常大，运行会很久；请确保你有明确授权。
- `1.py` 里默认写死了本机路径，你需要改成自己的 `pdf` 路径和 `wordlist` 路径。
- 建议优先使用 `decrypt_pdf.py`（你已知密码时更安全、更直接）。

## 常见问题

- **密码错误/缺失**：`decrypt_pdf.py` 会提示“密码错误或缺失（无法打开该 PDF）”。请确认密码类型（打开密码 vs 权限密码）及输入是否正确。
- **权限限制 PDF**：有些 PDF 仅限制打印/复制；在提供正确权限密码（如有）时，另存为不加密 PDF 可能有效，但结果取决于 PDF 的具体实现。

