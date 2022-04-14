<h1 align="center">
  <br>
  <a href="https://antizharko.herokuapp.com"><img src="static/android-chrome-512x512.png" alt="Jarkotik" width="200"></a>
  <br>
  <br>
  <a href="https://antizharko.herokuapp.com">AntiZharko</a>
  <br>
</h1>

<h4 align="center">Веб-интерфейс и конфиг для clang-format 14 для форматирования лабораторных работ Жарко в соответствии с Coding Guidelines</h4>

<p align="center">
  <a href="https://antizharko.herokuapp.com">Сайт</a> •
  <a href="#key-features">Фичи</a> •
  <a href="#download">.clang-format</a> •
  <a href="#license">Лицензия</a> •
  <a href="#credits">Стек</a> •
  <a href="#contact">Автор</a>
</p>

![screenshot](docs/demonstration.gif)

## Фичи

- Форматирование
  - Да, оно делает ту самую лесенку в списках инициализации из CG
  - Да, оно убирает trailing whitespaces
  - Да, оно добавляет пустую строку в конце вашего кода
  - Да, оно фиксит line endings (CRLF)
  - Если найдете проблемы в форматировании, сообщите [мне](https://vk.com/druzhelubnyy)
- [Веб-интерфейс](https://antizharko.herokuapp.com) с подсветкой синтаксиса с помощью [Codemirror](https://codemirror.net/)
- При желании, можно запустить свой сервер используя только Python3 - clang-format 14 доступен через pip!
- Если вам не нравится использовать веб-интерфейс, можете настроить форматтер внутри вашего редактора с помощью исходного конфига .clang-format (в том числе, и отредактировать его на свой лад!)

## Скачать

Скачать .clang-format можно прямо из репозитория, или по [ссылке](.clang-format).

## Стек

Этот проект написан с помощью:

- [clang-format](https://clang.llvm.org/docs/ClangFormat.html)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [CodeMirror](http://codemirror.net/)
- [Catppuccin](https://github.com/catppuccin/catppuccin)
- [gunicorn](https://gunicorn.org/)
- [Heroku](https://www.heroku.com)

## Лицензия

MIT

---

## Автор

> Автор &nbsp;&middot;&nbsp; [vk.com/druzhelubnyy](https://vk.com/id388032588) &nbsp;&middot;&nbsp;
> GitHub [@Quakumei](https://github.com/Quakumei) &nbsp;&middot;&nbsp;
> Telegram [@Quakumei](https://telegram.me/Quakumei)
