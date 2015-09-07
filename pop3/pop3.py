__author__ = 'Андрей'
from socket import create_connection, _GLOBAL_DEFAULT_TIMEOUT
from ssl import _create_stdlib_context
from hashlib import md5
from re import compile


def isOk(answer):
    return answer.startswith("+")

POP3PORT = 110
POP3PORTSSL = 995


class POP3:
    def __init__(self, host,
                 ssl=True,
                 port=None,
                 timeout=_GLOBAL_DEFAULT_TIMEOUT):
        if port is None:
            port = POP3PORTSSL if ssl else POP3PORT
        self.sock = create_connection((host, port), timeout)
        if ssl:
            self.sock = _create_stdlib_context().wrap_socket(self.sock)
        self.read_sock = self.sock.makefile('rb')
        self.first_message = self.get_answer()

    def get_answer(self):
        line = self.read_sock.readline()
        if len(line) < 2:
            raise Exception()
        if line[-2:] == b"\r\n":
            return bytes.decode(line[:-2])
        if line[0] == b"\r":
            return bytes.decode(line[1:-1])
        return bytes.decode(line[:-1])

    def get_long_answer(self):
        answer = self.get_answer()
        array = ""
        line = self.get_answer()
        while line != '.':
            array += line + "\n"
            line = self.get_answer()
        return answer, array

    def send_msg(self, line):
        self.sock.sendall(str.encode(line) + b"\r\n")
        return self.get_answer()

    def send_long_msg(self, line):
        self.sock.sendall(str.encode(line) + b"\r\n")
        return self.get_long_answer()

    def cmd_apop(self, user, pswd):
        try:
            digest = compile(r'\+OK.*(<[^>]+>)')\
                .match(self.first_message).group(1)
        except Exception:
            return False, "Server does not support authentication" + \
                   " with encrypted password"
        digest += pswd.encode()
        digest = md5(digest).hexdigest()
        answer = self.send_msg("APOP {} {}".format(user, digest))
        return isOk(answer), answer

    def cmd_user(self, user):
        answer = self.send_msg('USER {}'.format(user))
        return isOk(answer), answer

    def cmd_pass(self, pswd):
        answer = self.send_msg('PASS {}'.format(pswd))
        return isOk(answer), answer

    def cmd_dele(self, number):
        answer = self.send_msg('DELE {}'.format(number))
        return isOk(answer), answer

    def cmd_list(self, number=None):
        msg = 'LIST'
        if number is not None:
            answer = self.send_msg("{0} {1}".format(msg, number))
        else:
            answer, array = self.send_long_msg(msg)
        isok = isOk(answer)
        if isok:
            if number is not None:
                return True, answer[4:]
            else:
                return True, array
        else:
            return False, answer

    def cmd_noop(self):
        answer = self.send_msg('NOOP')
        return isOk(answer), answer

    def cmd_retr(self, number):
        answer, array = self.send_long_msg('RETR {}'.format(number))
        #TODO parser
        isok = isOk(answer)
        if isok:
            return True, array
        else:
            return False, answer

    def cmd_stat(self):
        answer = self.send_msg('STAT')
        return isOk(answer), answer

    def cmd_rset(self):
        answer = self.send_msg('RSET')
        return isOk(answer), answer

    def cmd_top(self, number, size):
        answer, array = self.send_long_msg('TOP {} {}'.format(number, size))
        #TODO parser
        isok = isOk(answer)
        if isok:
            return True, array
        else:
            return False, answer

    def cmd_quit(self):
        answer = self.send_msg('QUIT')
        return isOk(answer), answer

    def close(self):
        self.read_sock.close()
        self.sock.close()


class POP3Pro(POP3):
    def parse_list(answer):
        dict = {}
        for part in bytes.decode(answer).split("\n"):
            splt = part.split(" ")
            if len(splt) == 2:
                dict[splt[0]] = splt[1]
        return dict
