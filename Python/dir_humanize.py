import argparse
import os
import sys
from datetime import datetime, timezone

import humanize


def get_mtime_display(mtime_float: float, now: datetime) -> str:
    """Возвращает человекочитаемое отображение времени изменения."""
    try:
        mtime = datetime.fromtimestamp(mtime_float, tz=timezone.utc)
    except (OSError, ValueError):
        return "?"
    delta = now - mtime.replace(tzinfo=now.tzinfo) if now.tzinfo else mtime
    # Для недавних (до ~недели) — относительное время, иначе день/дата
    if abs(delta.total_seconds()) < 7 * 24 * 3600:
        return humanize.naturaltime(delta)
    return humanize.naturalday(mtime)


def scan_directory(path: str, now: datetime):
    """Сканирует директорию и возвращает списки записей и сводку."""
    files = []
    dirs = []
    total_size = 0
    errors = []

    try:
        entries = os.listdir(path)
    except OSError as e:
        print(f"Ошибка доступа к директории: {e}", file=sys.stderr)
        return None

    for name in sorted(entries):
        full = os.path.join(path, name)
        try:
            stat = os.stat(full)
        except OSError as e:
            errors.append((name, str(e)))
            continue
        if os.path.isdir(full):
            dirs.append((name, stat.st_mtime))
        else:
            size = stat.st_size
            files.append((name, size, stat.st_mtime))
            total_size += size

    return {
        "files": files,
        "dirs": dirs,
        "total_size": total_size,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Вывод информации о файлах в директории в человекочитаемом виде."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Путь к директории (по умолчанию — текущая)",
    )
    parser.add_argument(
        "--locale",
        default=None,
        help="Локаль для вывода (например, ru_RU)",
    )
    parser.add_argument(
        "--binary",
        action="store_true",
        help="Размеры в бинарных единицах (KiB, MiB)",
    )
    args = parser.parse_args()

    if args.locale:
        try:
            humanize.i18n.activate(args.locale)
        except FileNotFoundError as e:
            print(f"Локаль {args.locale} не найдена, используется по умолчанию: {e}", file=sys.stderr)

    path = os.path.abspath(args.directory)
    if not os.path.isdir(path):
        print(f"Не является директорией: {path}", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc)
    data = scan_directory(path, now)
    if data is None:
        return 1

    print(f"Директория: {path}\n")

    for name, mtime in data["dirs"]:
        mtime_str = get_mtime_display(mtime, now)
        print(f"  [DIR]  {name:<40}  {mtime_str}")

    for name, size, mtime in data["files"]:
        size_str = humanize.naturalsize(size, binary=args.binary)
        mtime_str = get_mtime_display(mtime, now)
        print(f"  {size_str:>12}  {name:<40}  {mtime_str}")

    for name, err in data["errors"]:
        print(f"  (ошибка: {name}) — {err}", file=sys.stderr)

    # Сводка
    n_dirs = len(data["dirs"])
    n_files = len(data["files"])
    print()
    print(f"Папок: {humanize.intcomma(n_dirs)}, файлов: {humanize.intcomma(n_files)}.")
    if n_files > 0:
        total_str = humanize.naturalsize(data["total_size"], binary=args.binary)
        print(f"Суммарный размер файлов: {total_str}.")

    if args.locale:
        humanize.i18n.deactivate()

    return 0


if __name__ == "__main__":
    sys.exit(main())
