import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple, List

import pikepdf


def _iter_pdfs(in_dir: Path, recursive: bool):
    if recursive:
        yield from in_dir.rglob("*.pdf")
    else:
        yield from in_dir.glob("*.pdf")


def decrypt_one(input_path: Path, output_path: Path, password: Optional[str]) -> Tuple[bool, str]:
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with pikepdf.open(input_path, password=password) as pdf:
            pdf.save(output_path)
        return True, "ok"
    except pikepdf._qpdf.PasswordError:
        return False, "密码错误或缺失（无法打开该 PDF）"
    except FileNotFoundError:
        return False, "输入文件不存在"
    except Exception as e:  # noqa: BLE001
        return False, f"解密失败：{type(e).__name__}: {e}"


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="PDF 解密/去加密（必须提供正确密码；不包含破解功能）"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--in", dest="in_file", help="输入 PDF 文件路径")
    group.add_argument("--in-dir", dest="in_dir", help="输入目录（批量处理 *.pdf）")

    parser.add_argument("--out", dest="out_file", help="输出 PDF 文件路径（单文件模式）")
    parser.add_argument("--out-dir", dest="out_dir", help="输出目录（批量模式）")
    parser.add_argument("--password", default=None, help="PDF 密码（打开密码/权限密码）")
    parser.add_argument(
        "--recursive", action="store_true", help="批量模式下递归扫描子目录"
    )
    parser.add_argument(
        "--keep-structure",
        action="store_true",
        help="批量模式下保持输入目录的相对目录结构",
    )

    args = parser.parse_args(argv)

    if args.in_file:
        in_path = Path(args.in_file).expanduser()
        if not args.out_file:
            parser.error("单文件模式必须指定 --out")
        out_path = Path(args.out_file).expanduser()
        ok, msg = decrypt_one(in_path, out_path, args.password)
        print(f"{'SUCCESS' if ok else 'FAIL'}: {in_path} -> {out_path} ({msg})")
        return 0 if ok else 2

    in_dir = Path(args.in_dir).expanduser()
    if not args.out_dir:
        parser.error("批量模式必须指定 --out-dir")
    out_dir = Path(args.out_dir).expanduser()

    if not in_dir.exists() or not in_dir.is_dir():
        print(f"FAIL: 输入目录不存在或不是目录：{in_dir}")
        return 2

    pdfs = list(_iter_pdfs(in_dir, args.recursive))
    if not pdfs:
        print(f"没有找到 PDF：{in_dir}")
        return 0

    total = 0
    success = 0
    for pdf_path in pdfs:
        total += 1
        if args.keep_structure:
            rel = pdf_path.relative_to(in_dir)
            out_path = out_dir / rel
        else:
            out_path = out_dir / pdf_path.name

        # 避免覆盖源文件
        if out_path.resolve() == pdf_path.resolve():
            out_path = out_path.with_name(out_path.stem + ".decrypted.pdf")

        ok, msg = decrypt_one(pdf_path, out_path, args.password)
        if ok:
            success += 1
        print(f"{'SUCCESS' if ok else 'FAIL'}: {pdf_path} -> {out_path} ({msg})")

    print(f"完成：{success}/{total} 成功")
    return 0 if success == total else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

