# 📁 dir_humanize: Консольная утилита для анализа файловой системы

**dir_humanize** — это удобная консольная утилита, которая показывает содержимое директории в "человекочитаемом" формате. Вместо скучных байтов и временных меток вы получаете понятные размеры (12.5 KB), относительное время ("2 часа назад") и аккуратно отформатированные итоги.

Проект создан для наглядной демонстрации возможностей библиотеки [`humanize`](https://github.com/jazzband/humanize), которая превращает "машинные" данные в красивый и понятный текст.

💡 **Моё мнение о библиотеке humanize**
`humanize` — это та незаметная, но невероятно полезная библиотека, которая делает любое CLI-приложение более дружелюбным к пользователю. Вместо того чтобы вручную писать кучу функций для форматирования чисел, дат и размеров, вы просто вызываете `humanize.naturalsize(1024)` и получаете `"1.0 KB"`. 

Работа с библиотекой интуитивно понятна, а поддержка локализации (`ru_RU`, `en_US`) позволяет создавать приложения, которые "говорят" на языке пользователя. Это идеальный инструмент для быстрого улучшения пользовательского опыта в скриптах и утилитах.

---

## 🚀 Быстрый старт

### Требования
- Python 3.8+
- pip

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone <your-repo-url>
   cd dir_humanize
2. Создайте виртуальное окружение (рекомендуется):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows

3.Установите единственную зависимость:
   ```bash
   pip install humanize
   ```
## 📋 Справка по командам
```bash
usage: dir_humanize.py [-h] [--locale LOCALE] [--binary] [directory]

📁 Консольная утилита для анализа содержимого директории с humanize

positional arguments:
  directory             Путь к директории (по умолчанию: текущая)

options:
  -h, --help            Показать справку
  --locale LOCALE, -l LOCALE
                        Выбрать локаль (например, en_US, ru_RU)
  --binary              Использовать бинарные единицы (KiB, MiB) вместо десятичных (KB, MB)
```
### 🎨 Примеры вывода

## Английская локаль (en_US), десятичные единицы (KB, MB)
```
python dir_humanize.py ~/Documents

Директория: /home/user/Documents

  [DIR]  projects                                    today at 10:30
  [DIR]  archive                                     3 days ago
    2.4 MB  report.pdf                               2 hours ago
   145.2 KB  profile.png                             yesterday
    1.1 KB  notes.txt                                5 minutes ago

Папок: 2, файлов: 3.
Суммарный размер файлов: 2.5 MB.
```
## Русская локаль (ru_RU), бинарные единицы (KiB, MiB)
```
python dir_humanize.py C:\Users\user\Downloads --locale ru_RU --binary

Директория: C:\Users\user\Downloads

  [DIR]  установщики                                  2 дня назад
    2.3 MiB  driver_installer.exe                     3 дня назад
  512.0 KiB  image.jpg                                 1 час назад
    2.0 MiB  report.pdf                                сейчас

Папок: 1, файлов: 3.
Суммарный размер файлов: 4.8 MiB.
```

### 🔧 Детали реализации

## 📂 Структура проекта
```
dir_humanize/
├── dir_humanize.py   # Основной файл с реализацией утилиты
└── README.md         # Документация проекта
```

## 📦 Модуль dir_humanize.py

| Функция | Назначение | Использование humanize |
|---------|------------|------------------------|
| `get_mtime_display(mtime, now)` | Преобразует timestamp в относительное время | `humanize.naturaltime()` для свежих файлов (< 7 дней)<br>`humanize.naturalday()` для старых |
| `scan_directory(path, now)` | Сканирует директорию, собирает данные о файлах/папках | — |
| `main()` | Парсит аргументы, координирует работу, выводит результат | `humanize.i18n.activate()` для локализации<br>`humanize.naturalsize()` для размеров<br>`humanize.intcomma()` для чисел в сводке |

## 🧠 Ключевые концепции
1. Преобразование размеров (naturalsize)
```
size_str = humanize.naturalsize(size, binary=args.binary)
```
- binary=True → KiB, MiB, GiB
- binary=False (по умолчанию) → KB, MB, GB

2. Естественное время (naturaltime, naturalday)
```
if abs(delta.total_seconds()) < 7 * 24 * 3600:
    return humanize.naturaltime(delta)  # "3 minutes ago", "2 часа назад"
return humanize.naturalday(mtime)        # "yesterday", "вчера"
```

3. Локализация (i18n.activate)
```
if args.locale:
    humanize.i18n.activate(args.locale)
    # Все дальнейшие вызовы humanize будут на выбранном языке
```


4. Разделители разрядов (intcomma)
```
print(f"Папок: {humanize.intcomma(n_dirs)}")
# 1000 -> "1,000" (en) или "1 000" (ru)
```

### 🐛 Обработка ошибок

Утилита корректно обрабатывает различные проблемные ситуации, выводя понятные сообщения без технического traceback:

| Ситуация | Сообщение |
|----------|----------|
| Директория не существует | ❌ Ошибка: Директория не найдена: `/wrong/path` |
| Нет прав на чтение | ❌ Ошибка доступа: `[Errno 13] Permission denied: /root` |
| Недоступная локаль | ⚠️ Локаль `xx_XX` не найдена, используется локаль по умолчанию |
| Ошибка при чтении файла | `(ошибка: bad_file.txt) — [Errno 2] No such file or directory` |

