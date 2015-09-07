from socket import socket, AF_INET, SOCK_STREAM
import pickle
import re
from queue import Queue
from threading import Thread
from header import MSG
from types import FunctionType


module_port = 14242


class Host:
    def __init__(self, port=module_port,
                 portionSize=1024,
                 maxContacts=5,
                 first_messages=[],
                 auto_message_get=True):
        self.amg = auto_message_get
        self.port = port
        self.maxContacts = maxContacts+1
        self.portionSize = portionSize
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.clients = {}
        self.messages = {}
        self.threads = {}
        self.thread = Thread(target=self.listen)
        self.ids = set()
        self.first_messages = first_messages
        self.is_work = False

    def start(self):
        self.listen()

    def listen(self):
        try:
            self.sock.bind(('', self.port))
            self.sock.listen(self.maxContacts)
            tmp = self.sock.accept()
            self.is_work = True
            id = self.get_free_id()
            self.clients[id] = tmp
            self.ids.add(id)
            if len(self.ids) != self.maxContacts:
                self.send_pickle(id, (MSG.id, id))
                for i in self.first_messages:
                    if isinstance(i[1], FunctionType):
                        self.send_pickle(id, (i[0], i[1]()))
                    else:
                        self.send_pickle(id, i)
                if self.amg:
                    self.threads[id] = Thread(target=self.auto_messages,
                                              args=(id,))
                    self.threads[id].start()
                print("Connect is ok({}:{})"
                      .format(self.clients[id][1][0], self.port))
            else:
                print("Cant connect to {}:{} because max contacts)"
                      .format(self.clients[id][1][0], self.port))
                self.send_pickle(id, (MSG.max_contacts, 0))
                self.close_client(id)
        except Exception:
            self.close()

    def get_free_id(self):
        id = len(self.ids)
        if id == 0:
            return 0
        for i in range(0, id):
            if i not in self.ids:
                id = i
                break
        return id

    def get_data(self, id):
        try:
            if self.clients[id] is not None:
                data = self.clients[id][0].recv(self.portionSize)
                return data
        except Exception:
            self.close_client(id)

    def get_pickle(self, id):
        try:
            return pickle.loads(self.get_data(id))
        except Exception:
            self.close_client(id)

    def send_data(self, id, data):
        try:
            self.clients[id][0].sendall(data)
            return data
        except Exception:
            self.close_client(id)

    def send_pickle(self, id, data):
        try:
            return self.send_data(id, pickle.dumps(data))
        except Exception:
            self.close_client(id)

    def auto_messages(self, id):
        self.messages[id] = Queue()
        while True:
            tmp = self.get_pickle(id)
            if tmp is not None:
                self.messages[id].put(tmp)
            else:
                self.close_client(id)
                break

    def get_message(self, id):
        try:
            if id < self.maxContacts \
                    and id in self.messages\
                    and not self.messages[id].empty():
                return self.messages[id].get()
        except AttributeError:
            pass

    def get_message_from_all(self):
        result = []
        for i in self.ids.copy():
            tmp = self.get_message(i)
            if tmp is not None:
                result.append(i, tmp)
        return result

    def send_all(self, data):
        for i in self.ids.copy():
            if i in self.ids:
                self.send_pickle(i, data)

    def close(self):
        self.sock.close()
        self.is_work = False
        tmp = self.ids.copy()
        for i in tmp:
            if i in self.ids:
                self.send_pickle(i, ("Exit",))
                self.close_client(i)

    def close_client(self, id):
        if id in self.ids:
            print("Connect is end({}:{})"
                  .format(self.clients[id][1][0], self.port))
            self.ids.remove(id)
            self.clients[id] = None
            if self.amg:
                self.messages[id] = None
                self.threads[id] = None



class Client:
    def __init__(self, port=module_port, portionSize=1024):
        self.port = port
        self.portionSize = portionSize
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.is_work = False

    def start(self, ip="localhost"):
        self.sock.connect((ip, self.port))
        self.is_work = True
        print("Connect is ok({}:{})".format(ip, self.port))

    def get_data(self):
        try:
            data = self.sock.recv(self.portionSize)
            return data
        except Exception:
            self.close()

    def send_data(self, data):
        try:
            self.sock.sendall(data)
            return data
        except Exception:
            self.close()

    def send_pickle(self, tmp, data):
        try:
            return self.send_data(pickle.dumps(data))
        except Exception:
            self.close()

    def get_pickle(self, tmp=None):
        try:
            return pickle.loads(self.get_data())
        except Exception:
            self.close()

    def close(self):
        self.sock.close()
        self.is_work = False


ipReg = \
    re.compile(r'^(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])'
               r'(\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[0-9])){2}'
               r'(\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[0-9]{2}|[1-9]))$')


def is_it_ip(ip):
    if ipReg.match(ip) is None:
        return False
    return True