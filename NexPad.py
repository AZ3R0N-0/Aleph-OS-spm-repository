import curses
import os


def main(stdscr):
  # Настройки терминала
  curses.curs_set(1)  # Включаем видимость курсора
  stdscr.keypad(True)  # Включаем чтение спец-клавиш (стрелочки и т.д.)
  curses.use_default_colors()

  # Инициализация цветов: зеленый текст на черном фоне (или стандартном)
  curses.init_pair(1, curses.COLOR_GREEN, -1)
  curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Для плашек

  filename = "untitled.txt"
  lines = [""]  # Хранилище строк текста
  cursor_y, cursor_x = 0, 0  # Позиция курсора в тексте
  scroll_y = 0  # Для прокрутки, если текст не влезает в экран

  while True:
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # 1. Верхний статус-бар (как в nano)
    stdscr.attron(curses.color_pair(2))
    status_top = f"  NexPad 1.0  |  Файл: {filename}".ljust(width - 1)
    stdscr.addstr(0, 0, status_top[: width - 1])
    stdscr.attroff(curses.color_pair(2))

    # 2. Отрисовка текста
    max_visible_lines = height - 3  # Минус верхняя и две нижние строки
    for i in range(max_visible_lines):
      line_idx = scroll_y + i
      if line_idx < len(lines):
        # Выводим строку зеленым цветом
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(1 + i, 0, lines[line_idx][: width - 1])
        stdscr.attroff(curses.color_pair(1))

    # 3. Нижний статус-бар и подсказки клавиш
    stdscr.attron(curses.color_pair(2))
    help_text = " ^O Сохранить    ^X Выход"
    stdscr.addstr(height - 2, 0, help_text.ljust(width - 1))
    stdscr.addstr(
        height - 1,
        0,
        f" Стр: {cursor_y + 1}, Кол: {cursor_x + 1}".ljust(width - 1),
    )
    stdscr.attroff(curses.color_pair(2))

    # Корректируем прокрутку экрана
    if cursor_y < scroll_y:
      scroll_y = cursor_y
    elif cursor_y >= scroll_y + max_visible_lines:
      scroll_y = cursor_y - max_visible_lines + 1

    # Устанавливаем курсор в правильную позицию на экране
    stdscr.move(1 + cursor_y - scroll_y, min(cursor_x, width - 1))
    stdscr.refresh()

    # Чтение нажатия клавиши
    try:
      key = stdscr.getch()
    except KeyboardInterrupt:
      key = 24  # Перехват Ctrl+C как Ctrl+X (Выход)

    # --- Обработка управления ---

    # Выход: Ctrl+X (код 24)
    if key == 24:
      break

    # Сохранение: Ctrl+O (код 15)
    elif key == 15:
      # Простейшая запись в файл
      with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
      # Быстрое уведомление на нижней строке
      stdscr.attron(curses.color_pair(2))
      stdscr.addstr(
          height - 1, 0, f" [ Записано {len(lines)} строк ] ".ljust(width - 1)
      )
      stdscr.attroff(curses.color_pair(2))
      stdscr.refresh()
      curses.napms(1000)  # Пауза 1 секунда, чтобы увидеть надпись

    # Движение курсора (Стрелочки)
    elif key == curses.KEY_UP:
      if cursor_y > 0:
        cursor_y -= 1
        cursor_x = min(cursor_x, len(lines[cursor_y]))
    elif key == curses.KEY_DOWN:
      if cursor_y < len(lines) - 1:
        cursor_y += 1
        cursor_x = min(cursor_x, len(lines[cursor_y]))
    elif key == curses.KEY_LEFT:
      if cursor_x > 0:
        cursor_x -= 1
      elif cursor_y > 0:
        cursor_y -= 1
        cursor_x = len(lines[cursor_y])
    elif key == curses.KEY_RIGHT:
      if cursor_x < len(lines[cursor_y]):
        cursor_x += 1
      elif cursor_y < len(lines) - 1:
        cursor_y += 1
        cursor_x = 0

    # Клавиша Enter
    elif key in (10, 13, curses.KEY_ENTER):
      left_part = lines[cursor_y][:cursor_x]
      right_part = lines[cursor_y][cursor_x:]
      lines[cursor_y] = left_part
      lines.insert(cursor_y + 1, right_part)
      cursor_y += 1
      cursor_x = 0

    # Клавиша Backspace (Удаление символа)
    elif key in (8, 127, curses.KEY_BACKSPACE):
      if cursor_x > 0:
        lines[cursor_y] = (
            lines[cursor_y][: cursor_x - 1] + lines[cursor_y][cursor_x:]
        )
        cursor_x -= 1
      elif cursor_y > 0:
        # Перенос текущей строки к предыдущей
        cursor_x = len(lines[cursor_y - 1])
        lines[cursor_y - 1] += lines[cursor_y]
        lines.pop(cursor_y)
        cursor_y -= 1

    # Ввод обычного текста
    elif 32 <= key <= 126 or (key >= 192):  # Поддержка ASCII и базового ввода
      try:
        char = chr(key)
        lines[cursor_y] = (
            lines[cursor_y][:cursor_x] + char + lines[cursor_y][cursor_x:]
        )
        cursor_x += 1
      except ValueError:
        pass


# Запуск консольного приложения с автоматическим восстановлением терминала при ошибках
if __name__ == "__main__":
  curses.wrapper(main)
