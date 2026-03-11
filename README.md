# PDF 解密（已知密码）离线工具

本项目**仅用于你本人或已获授权**的 PDF 文件：在你**提供正确密码**的前提下，将加密 PDF 另存为不加密的 PDF，便于后续打印/合并/检索等。

> 注意：本工具**不包含**密码破解、字典攻击、暴力尝试等功能。

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

## 用法

### 解密单个 PDF（必须提供正确密码）

```bash
python decrypt_pdf.py --in "C:\path\file.pdf" --out "C:\path\file.decrypted.pdf" --password "你的密码"
```

### 批量解密一个文件夹里的 PDF

```bash
python decrypt_pdf.py --in-dir "C:\path\pdfs" --out-dir "C:\path\out" --password "你的密码" --recursive
```

## 常见说明

- 如果 PDF 有“打开密码”，你必须提供正确密码才能读取并解密。
- 如果 PDF 只有“权限限制”（可打开但限制打印/复制），本工具在你提供权限密码（如果有）时可将其另存为无加密版本；不同 PDF 的限制/实现方式可能不同，结果以实际文件为准。

