"""Собирает автономную HTML-страницу из исходников.

На выходе один файл, который работает по двойному клику,
без сервера и без интернета: шрифты, логотипы и весь код внутри.
"""
import re, io, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
def rd(name): return io.open(os.path.join(BASE, name), encoding='utf-8').read()

# Стартовый экран уже отрисован пререндером — страница видна без JS.
# Если пререндера нет, берём пустой каркас (тогда нужен JS).
try:
    html = rd('.prerendered.html')
except FileNotFoundError:
    html = rd('index.html')
sources = [rd(n) for n in ('logos.js', 'data.js', 'engine.js', 'app.js')]

def strip_modules(src):
    """Убирает import/export — в одном файле модули не нужны."""
    src = re.sub(r'^\s*import\s+\{[^}]*\}\s+from\s+[\'"][^\'"]+[\'"];?\s*$', '', src, flags=re.M)
    src = re.sub(r'^\s*export\s+(const|function)\s', r'\1 ', src, flags=re.M)
    return src

bundle = "\n".join(strip_modules(s) for s in sources)

# Шрифты: встроенные, если сгенерированы; иначе ссылка на Google Fonts
inline_path = os.path.join(BASE, 'fonts', 'inline-fonts.css')
offline = os.path.exists(inline_path) and '--online' not in sys.argv
if offline:
    fonts = io.open(inline_path, encoding='utf-8').read()
    html = re.sub(
        r'<link rel="preconnect"[^>]*>\s*<link rel="preconnect"[^>]*>\s*'
        r'<link rel="stylesheet" href="https://fonts\.googleapis[^>]*>',
        '<style>\n' + fonts + '\n</style>', html, flags=re.S)

# Обычный <script>, а не type="module": в собранном файле импортов уже нет,
# а модули блокируются при открытии через file:// в песочнице (Быстрый просмотр,
# предпросмотр вложений) — страница молча остаётся пустой.
# Скин по умолчанию (Пятёрочка): без JS переменные --sk-* иначе не заданы
out = html.replace('<div class="screen" id="screen">',
  '<div class="screen" id="screen" style="'
  '--sk-primary:#00923A;--sk-primary-ink:#00923A;--sk-on:#FFFFFF;'
  '--sk-surface:#F2FBF4;--sk-card:#FFFFFF;--sk-ink:#0E2A18;'
  '--sk-muted:#6B7A73;--sk-line:#E3EBE5;--sk-soft:#F2FBF4;">')

out = out.replace('<script type="module" src="./app.js"></script>',
                   '<script>\n' + bundle + '\n</script>')

# Artifact подставляет каркас документа сам; автономному файлу он нужен свой.
# Без charset браузер читает UTF-8 как latin-1 — вместо кириллицы кракозябры.
# Без viewport телефон рисует страницу шириной 980px и ужимает её.
out = ('<!doctype html>\n<html lang="ru">\n<head>\n'
       '<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
       + out.replace('<title>', '<title>', 1) +
       '\n</body>\n</html>\n')
out = out.replace('</style>\n\n<div class="top">', '</style>\n</head>\n<body>\n<div class="top">', 1)

dest = os.path.join(BASE, 'x5-game-layer.html')
io.open(dest, 'w', encoding='utf-8').write(out)
# Копия для деплоя: Vercel и GitHub Pages раздают public/
pub = os.path.join(BASE, '..', 'public')
os.makedirs(pub, exist_ok=True)
io.open(os.path.join(pub, 'index.html'), 'w', encoding='utf-8').write(out)

print(f"{os.path.relpath(dest)}: {round(len(out.encode())/1024)} KB, "
      f"шрифты {'встроены' if offline else 'по ссылке'}")
