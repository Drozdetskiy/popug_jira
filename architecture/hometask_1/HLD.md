# HLD
## Общая схема приложения
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/hometask_1/architecture/hometask_1/services_diagram.png)
В данной концепции сервис Auth отвечает за аутентификацию пользователей. А так же является мастером данных для модели юзера.
Сервис PopugGateway - Гейтвей для входа во внутренню сеть. Сервис выполняет роль фасада для веб-интерфейса приложения. Сервис так же выполняет проверку аутентификации и кеширование запросов.
Сервис TaskKeeper отвечает за создание и распространение информации о тасках. Процесс реассайна тасок происходит в отдельном воркере сервиса.
Сервис Accounting отвечает за ведение Transaction и за назначение таскам стоимости. Текущий баланс рассчитывается путем суммирования бизнес логов за определенный промежуток времени.
Сервис Analytics собирает всю информацию об использовании данных в приложении.
## Шины данных
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/hometask_1/architecture/hometask_1/events_diagram.png)
Auth - продьюсер ивентов о User
TaskKeeper - продьюсер ивентов о Task, потребитель ивентов о User
Accounting - продьюсер ивентов о Transaction, кроме того он продьюсер ивентов о TaskCost. Потребитель ивентов о User и Task
Analytics - потребитель всех ds и bc ивентов.
## EventStorming
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/hometask_1/architecture/hometask_1/eventstorming_diagram.png)
Описанные группы событий соответствуют указанным в задании бизнес требованиям
Отдельно хотелось бы отметить, что цепочка комманды add_task разбита на две части: create_task и assign_task. Это сделано для того, чтобы сохранить консистентность поведения системы при вызове shuffle и добавлении новой задачи.
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/hometask_1/architecture/hometask_1/data_diagram.png)
Диаграмма данных описывает принципы использования и хранения данных в приложении.
Сервис Accounting имеет вспомогательную таблицу AccrueBillRequests. Таблица необходима для асинхронной рассылки информации о зачислении на счет.

