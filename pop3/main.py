from pop3 import POP3
from argparse import ArgumentParser
from getpass import getpass


comands = {'dele': 1,
           'list': 1,
           'noop': 0,
           'retr': 1,
           'rset': 0,
           'stat': 0,
           'top': 2,
           'quit': 0}


def get_help(cmd=None):
    hlp = {'dele': '(НОМЕР_СООБЩЕНИЯ) Сервер помечает '
                   'указанное сообщение для удаления.',
           'list': '(НОМЕР_СООБЩЕНИЯ) Если был передан аргумент, то сервер'
                   ' выдаёт информацию об указанном сообщении. Если аргумент не'
                   ' был передан, то сервер выдаёт информацию обо всех '
                   'сообщениях, находящихся в почтовом ящике. Сообщения,'
                   ' помеченные для удаления, не перечисляются.',
           'noop': '() Сервер ничего не делает, всегда отвечает положительно.',
           'retr': '(НОМЕР_СООБЩЕНИЯ) Сервер передаёт сообщение'
                   ' с указанным номером.',
           'rset': '() Этой командой производится откат'
                   ' транзакций внутри сессии',
           'stat': '() Сервер возвращает количество сообщений в почтовом ящике и'
                   ' размер почтового ящика в октетах.',
           'top': '(НОМЕР_СООБЩЕНИЯ КОЛИЧЕСТВО СТРОК) Сервер возвращает'
                  ' заголовки указанного сообщения, пустую строку и указанное'
                  ' количество первых строк тела сообщения.',
           'quit': '() Завершение сессии'}
    if cmd is not None:
        if cmd in hlp:
            return "{} - {}\n".format(cmd.upper(), hlp[cmd])
        else:
            return "Команда {} не найдена\r\n".format(cmd)
    else:
        res = ""
        for key in hlp:
            res += "{} - {}\n".format(key.upper(), hlp[key])
        return res


def parse_arg():
    parser = ArgumentParser(
        description='''POP3 клиент.
    Варианты соединения:with STL, without STL.
    Варианты авторизации:
    APOP - авторизация в одно сообщение с шифровкрой паролья по MD5.
    (Не все сервера распознают команду APOP)
    USER,PASS - стандартная авторизация за два сообщения, без шифрования.
    Список команд:\n''' + get_help(),
        epilog=''' Автор программы Новиков Андрей.
Автор программы не несет никакой ответсвенности ни за что.'''
    )
    parser.add_argument("-ho", "--host",
                        default=None,
                        help="Имя хоста")
    parser.add_argument("-po", "--port",
                        type=int,
                        default=None,
                        help="Логин пользователя")
    parser.add_argument("-u", "--user",
                        default=None,
                        help="Логин пользователя")
    parser.add_argument("-p", "--password",
                        default=None,
                        help="Пароль пользователя")
    parser.add_argument("-s", "--ssl",
                        type=bool, default=None,
                        help="Использовать ли SSL?")
    parser.add_argument("-a", "--apop",
                        type=bool, default=None,
                        help="Использовать ли авторизацию с шифрованием"
                             " пароля? Не все сервера распознают эту команду.")
    return parser


class WrongUserPass(Exception):
    pass


def main():
    prog_args = parse_arg().parse_args()
    while True:
        if prog_args.host is None:
            prog_args.host = input("Укажите имя хоста\n")
        if prog_args.port is None or not 0 < prog_args.port < 65536:
            msg = input("Вы хотите указать порт? "
                        "Варианты ответа: range(1,65535),-\n")\
                .replace(" ", "")
            while True:
                try:
                    msg = int(msg)
                    if 0 < msg < 65536:
                        prog_args.port = msg
                        break
                except Exception:
                    if msg == "-":
                        prog_args.port = None
                        break
                msg = input("Неверный ответ. Варианты ответа:"
                            " range(1,65535),-\n")\
                    .replace(" ", "")
        if prog_args.user is None:
            prog_args.user = input("Укажите логин пользователя\n")
        if prog_args.password is None:
            print("Введите пароль")
            prog_args.password = getpass()
        if prog_args.ssl is None:
            msg = input("Вы хотите использовать SSL? Варианты ответа: +,-\n")\
                .replace(" ", "")
            while msg not in ("+", "-"):
                msg = input("Неверный ответ. Варианты ответа: +,-\n")\
                    .replace(" ", "")
            prog_args.ssl = True if msg == "+" else False
        if prog_args.apop is None:
            msg = input("Вы хотите использовать шифровку пароля? Не все сервера "
                        "распознают эту команду. Варианты ответа: +,-\n")\
                .replace(" ", "")
            while msg not in ("+", "-"):
                msg = input("Неверный ответ. Варианты ответа: +,-\n")\
                    .replace(" ", "")
            prog_args.apop = True if msg == "+" else False

        pop = POP3(host=prog_args.host,
                   ssl=prog_args.ssl,
                   port=prog_args.port)
        cmd2fnc = {'dele': pop.cmd_dele,
                   'list': pop.cmd_list,
                   'noop': pop.cmd_noop,
                   'retr': pop.cmd_retr,
                   'rset': pop.cmd_rset,
                   'stat': pop.cmd_stat,
                   'top': pop.cmd_top,
                   'quit': pop.cmd_quit}

        try:
            if prog_args.apop:
                b, answer = pop.cmd_apop(prog_args.user, prog_args.password)
                if not b:
                    raise WrongUserPass()
            else:
                pop.cmd_user(prog_args.user)
                b, answer = pop.cmd_pass(prog_args.password)
                if not b:
                    raise WrongUserPass()
            print('Авторизация прошла успешно\n')
            while True:
                msg = input("- ").lower().split(" ")
                if msg[0] in comands:
                    answer = None
                    if msg[0] == "list":
                        answer = cmd2fnc[msg[0]](msg[1]
                                                 if len(msg) == 2 else None)
                    elif msg[0] == "quit":
                        answer = cmd2fnc[msg[0]]()
                        break
                    else:
                        args = comands[msg[0]]
                        if len(msg) == args+1:
                            if args == 0:
                                answer = cmd2fnc[msg[0]]()
                            elif args == 1:
                                answer = cmd2fnc[msg[0]](msg[1])
                            elif args == 2:
                                answer = cmd2fnc[msg[0]](msg[1], msg[2])
                        else:
                            print("Неверное число аргументов для команды {}\n"
                                  .format(msg[0]))
                    if answer[0]:
                        print(answer[1])
                    else:
                        print("Ошибка запроса\nОтвет сервера:{}"
                              .format(answer[1][4:]))
                elif msg[0] == "help":
                    if len(msg) < 3:
                        print(get_help(None if len(msg) == 1 else msg[1]))
                    else:
                        print("Неверное число аргументов для команды help\n")
                else:
                    print("Неизвестная команда {}".format(msg[0]))

        except WrongUserPass:
            print("Не правильный логин или пароль\n")
            prog_args.user = None
            prog_args.password = None
        except Exception:
            print("Что-то пошло не так! Ошибка соеденения.\n")
            input()
            break



if __name__ == "__main__":
    main()

