![Build Status](https://github.com/EgorDikanskiy/Sparq/actions/workflows/python-package.yml/badge.svg)


Dependecies install
We use poetry as dependecies manager. First install poetry using
1. `pip install poetry`
Than acitvate venv:
2. `poetry shell`
Than install all dependecies:
3. `poetry instlal`
To add new dependecies use:
`poetry add <dep_name>`

---

Run dev serever:
Run in src/
`fastapi dev main.py`

---

Как это рабоатет?

Сейчас есть 3 важных компонента:
1. В main.py есть WebSocket хэндлер, он принимает сообщения и подключения
2. В модуле ws_handlers, есть обработчики пользовательских сообщений. ws_handler принимает json из webscoket сообщения, и в зависимости от содержания, использует обработчик из ws_handlers.handlers. Важно, что handler никак не взаимодействует с WebSocket соедением.
3. в events_queue - обрабатываеются события связанные с ws подключениями. Отправка сообщений должна происходить тут. 
 - **Зачем это?**
 Отправка сообщений без отдельной очереди будет работать, до тех пор пока не появляется второй сервер/воркер. Напрмер, нам может потребоваться отправить сообщение пользователю, который подключен на другом узле. Для этого в очередь ивентов можно будет отправлять ивент об потребности в отправке данных какому-то пользователю (например с помощью redis или rabbitmq). Например, храним в redis словарь (user_id -> ивент). В очереди оправшиваем redis о новых ивентах для пользователей подключенных на нашем узле, как только в redis появляются eventы, обрабатываем их на нужном узле. 

---

Подключил postgresql
Чтобы подключиться к бд нужно указать её данные в файлах `alembic.ini` и `database.py`
При переходе на add_date/ в бд добавляется текущее дата и время


