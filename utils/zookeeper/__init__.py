from random import randint

from kazoo.client import KazooClient


class ZkForServer:
    def __init__(self, app_name, hosts):
        self.__root_path = '/{}'.format(app_name)
        self.__hosts = hosts
        self.__zk = KazooClient(hosts=self.__hosts)
        self.__zk.start()
        self.services = {}

    def close(self):
        self.__zk.stop()
        self.__zk.close()

    def register_service(self, service_name, host, port):
        self.__zk.ensure_path('{}/{}'.format(self.__root_path, service_name))
        service_node = '{}/{}/{}:{}'.format(self.__root_path, service_name, host, port)
        if not self.__zk.exists(service_node):
            self.__zk.create(service_node, ephemeral=True)
        return service_node


class ZkForClient:
    def __init__(self, app_name, hosts):
        self.__root_path = '/{}'.format(app_name)
        self.__hosts = hosts
        self.__zk = KazooClient(hosts=self.__hosts)
        self.__zk.start()
        self.__services = {}
        self.load_services()

    def close(self):
        self.__zk.stop()
        self.__zk.close()

    @property
    def services(self):
        return self.__services

    def load_services(self, event=None):
        services = {}
        if self.__zk.exists(self.__root_path):
            for service_name in self.__zk.get_children(
                self.__root_path,
                watch=self.load_services
            ):
                if service_name not in services:
                    services[service_name] = []

                for host in self.__zk.get_children(
                    '{}/{}'.format(self.__root_path, service_name),
                    watch=self.load_services
                ):
                    services[service_name].append(host)
        self.__services = services

    def load_service_node(self, service_name):
        if service_name not in self.__services:
            raise Exception('service {} not found'.format(service_name))

        server_count = len(self.__services[service_name])
        if server_count <= 0:
            raise Exception('service {} have no available server'.format(service_name))

        node = self.__services[service_name][randint(0, server_count - 1)]
        return node

    def load_available_service(self, service_name):
        node = self.load_service_node(service_name)
        host, port = node.split(':')
        port = int(port)
        return host, port
