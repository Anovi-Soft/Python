POP3 клиент. 
main.py - работа с пользователем
pop3.py - Работа с протоколом pop3
test_pop3 - тэсты для модуля pop3

Варианты соединения:
with STL, 
without STL.

Варианты авторизации:
APOP - авторизация в одно сообщение с шифровкрой паролья по MD5. (Не все сервера распознают команду APOP)
USER,PASS - стандартная авторизация за два сообщения, без шифрования.

Список команд:
LIST - (НОМЕР_СООБЩЕНИЯ) Если был передан аргумент, то сервер выдаёт информацию об указанном сообщении. Если аргумент не был передан, то сервер выдаёт информацию обо всех сообщениях, находящихся в почтовом ящике. Сообщения, помеченные для удаления, не перечисляются.
QUIT - () Завершение сессии 
STAT - () Сервер возвращает количество сообщений в почтовом ящике и размер почтового ящика в октетах. 
TOP - (НОМЕР_СООБЩЕНИЯ КОЛИЧЕСТВО СТРОК) Сервер возвращает заголовки указанного сообщения, пустую строку и указанное количество первых строк тела сообщения.
NOOP - () Сервер ничего не делает, всегда отвечает положительно. 
DELE - (НОМЕР_СООБЩЕНИЯ) Сервер помечает указанное сообщение для удаления. 
RETR - (НОМЕР_СООБЩЕНИЯ) Сервер передаёт сообщение с указанным номером. 
RSET - ()Этой командой производится откат транзакций внутри сессии