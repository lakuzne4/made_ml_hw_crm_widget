## Калькулятор откликов для маркетинговых кампаний с заданным таргетингом

Среди некоторых менеджеров целевых рекламных кампаний присутствует мнение, что весь эффект от ML-модели можно <br> 
повторить просто задав несколько параметров таргетинга клиентской аудитории. <br>

В данном прототипе можно интерактивно задать несколько параметров таргетинга рекламной кампании и сравнить <br>
эффект с эффектом, который был бы получен в результате коммуникаций с тем же количеством клиентов, отобранных<br>
по наибольшему скору модели.

Минимальная жизнеспособная чать программы состоит из трёх файлов: useful_tool.py и двух файлов данных ("scored_client_base_part1.zip" и "scored_client_base_part2.zip").<br>

Запуск происходит в Jupyter notebook таким кодом:
```python
from useful_tool import useful_tool
useful_tool()
```
Для запуска требуется иметь файлы "scored_client_base_part1.zip" и "scored_client_base_part2.zip" в той же дирректории, что и useful_tool.py

Вначале интерфейс выглядит так:

<img src="screenshots/Начальный_интерфейс.png" width=700>

Для каждого предлагаемого продукта и канала коммуникации с клиентом существует своя ML-модель. Продукт и канал возможной<br>
коммуникации выбирает пользователь:
<img src="screenshots/Выбор_модели.png" width=400 border="10">

В данном случае мы предлагаем нашим клиентам купить у нас плюшевых мишек, отправив им письмо через голубиную почту (ведь это оригинальнее, чем отправить Push-уведомления).

При этом на начальном интерфейсе отклик по модели и отклик по таргетингу равны т.к. начальный таргетинг = отсутствие таргетинга

Если задать таргетинг на людей (или хоббитов) проживающих в Шире и ставших клиентами через кампанию-партнёра и <br>
покупающих в среднем мало подгузников, то получим такие результаты:
<img src="screenshots/Таргетинг_на_хоббитов.png" width=700>
