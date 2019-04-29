## REST сервис для программы обучения и тестирования

## Настройка окружения

Должны быть установлены Python3, mod_wsgi_py3
```bash
sudo apt-get install libapache2-mod-wsgi-py3
```

Создание виртуального окружения для python3
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
Для настройки apache см. файл 000-default.conf

[Демо-версия](http://v.perm.ru/teach)
```
Имя: Черепахин
Пароль: 2222
```
