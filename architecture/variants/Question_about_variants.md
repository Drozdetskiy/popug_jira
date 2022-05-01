# Variants

## Суть проблемы
Пытаюсь понять, как мне выполнить требование: "У каждого из сотрудников должен быть свой счёт, который показывает, сколько за сегодня он получил денег. У счёта должен быть аудитлог того, за что были списаны или начислены деньги, с подробным описанием каждой из задач."
Какие варианты решения архитектуры, я вижу:
## Gateway 
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/variants/architecture/variants/gateway/services_gateway_diagram.png)
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/variants/architecture/variants/gateway/events_gateway_diagram.png)
В этом варианте у нас есть гейтвей. В сервисе Accounting хранится информация о билинге. В сервисе TaskKeeper хранится информация о тасках.
Когда к нам приходит запрос на то, чтобы забрать биллинг логи и добавить к ним полную информацию о таске, наш гейтвей ходит в оба сервиса и возвращает композитный ответ.

### Плюсы такого решения
- гейтвей забирает на себя все проблемы по авторизации пользователей
- предоставляет слой для создания композитных запросов.

### Минусы такого решения
- гейтвей - бутылочное горлышко. На него приходится вся нагрузка. Проблема с отказоустойчивостью и плавной деградацией.
- плюс одно лишнее взаимодействие по http

## Объединение на клиенте
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/variants/architecture/variants/without_gateway/services_without_gateway_diagram.png)
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/variants/architecture/variants/without_gateway/events_without_gateway_diagram.png)

В этом варианте логика маппинга тасок по pid отдается на сторону клиента. То есть фронт делает у нас запрос сначала в accounting. А потом обогощает запрос данными из task_keeper.

### Плюсы такого решения
- нет лишнего слоя в виде гейтвея
- меньше http запросов

### Минусы
- больше логики на фронтенде. не получится сделать тонкий клиент
- вообще говоря, скорее всего, под фронтом все равно будет какой-то be for frontend, который будет проксировать запросы и теперь он станет узким местом.

## Хранить данные о таске в Accounting
Для того, чтобы отдавать billing log с полной информацией о таске, хранить в сервисе Accounting полную информацию о тасках. (Получая ее из CUD ивентов)
(схема такая же как в "Объединение на клиенте")

### Плюсы такого решения
- Простота
- Нет лишних запросов и слоев

### Минусы
- много дублирования данных
- по сути, можно было бы объединить тогда Accounting и TaskKeeper, так как Billing будет иметь всю ту же информацию, что и TaskKeeper
- при расширении схемы данных Task, придется менять ее и в Accounting

## Связать сервисы TaskKeeper и Accounting синхронным запросом
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/variants/architecture/variants/sync_link/services_sync_link_diagram.png)
![Service Diagram](https://github.com/Drozdetskiy/popug_jira/blob/variants/architecture/variants/sync_link/events_sync_link_diagram.png)

Сервис Accounting при запросе на получения дашборда ходит по http в TaskKeeper и обогащает данные.
### Плюсы такого решения
- Простота

### Минусы
- Повышает связанность сервисов.
- Страдает отказоустойчивость (хотя тут можно отдавать необогащенный ответ в случае ошибки taskkeeper)


## Резюме
Лично мне очень нравится вариант с гейтвеем. Он делает систему более логичной, более простой в эксплуатации и развитии.