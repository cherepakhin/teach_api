## REST сервис для программы обучения и тестирования

## Настройка окружения

Создание виртуального окружения для python3.6
```bash
python3 -m venv env
```
Переключиться в виртуальное окружение
```bash
source env/bin/activate
```
Загрузка необходимых пакетов
```bash
pip3 install -r requirements.txt
```

## Тесты
```bash
$ nosetests tutorial
$ py.test -q
```

## Запуск
```bash
$ pserve development.ini --reload
```

[Демо-версия](http://v.el59.ru/teach)
```
Имя: Черепахин
Пароль: 2222
```
