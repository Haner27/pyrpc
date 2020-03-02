from contextlib import contextmanager
from functools import partial

from thrift import Thrift
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

from config import conf
from utils.zookeeper import ZkForClient


class RPCClient:
    def __init__(self, zookeeper_hosts):
        self.__zk_for_client = ZkForClient(conf.app_name, zookeeper_hosts)
        self.__service_bind_map = {}

    def bind(self, service_name, service_module):
        self.__service_bind_map[service_name] = service_module

    @contextmanager
    def load_service_client(self, service_name):
        if service_name not in self.__service_bind_map:
            raise Exception('service {} must bind service_module thrift generated.'.format(service_name))

        service_module = self.__service_bind_map[service_name]

        # 获取可用的服务
        host, port = self.__zk_for_client.load_available_service(service_name)
        print('we load service {} from {}:{}'.format(service_name, host, port))
        socket = TSocket.TSocket(host, port)

        transport = None
        try:
            # 获取Transport
            transport = TTransport.TBufferedTransport(socket)
            # 获取TBinaryProtocol
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            service_protocol = TMultiplexedProtocol(protocol, service_name)

            # 获取该service的客户端对象
            client = service_module.Client(service_protocol)

            # 连接通道transport
            transport.open()
            yield client

        except Thrift.TException as ex:
            print('%s' % (ex.message))

        finally:
            if transport:
                # 关闭通道transport
                transport.close()

    def close(self):
        self.__zk_for_client.close()

    def __getattr__(self, service_name):
        return self.load_service_client(service_name)


if __name__ == '__main__':
    # 使用样例：

    # # 导入thrift生成对应语言的service以及数据对象结构
    cli = RPCClient(conf.zookeeper.hosts)
    from thrifts.user_service import UserService
    cli.bind('User', UserService)

    with cli.User as user_service:
        hnf = user_service.CreateUser(UserService.User(id=1, name='hnf', desc='i am hnf'))
        print(hnf.id, hnf.name, hnf.gender, hnf.desc)
        lx = user_service.CreateUser(UserService.User(id=2, name='lx', gender='female', desc='i am lx'))
        print(hnf.id, hnf.name, hnf.gender, hnf.desc)
        fgy = user_service.CreateUser(UserService.User(id=3, name='fgy'))
        print(hnf.id, hnf.name, hnf.gender, hnf.desc)
        print('\n')

        users = user_service.GetUsers()
        for u in users:
            print(u.id, u.name, u.gender, u.desc)

        r = user_service.Ping()
        print(r.code)

        print(user_service.DeleteUserById(user_id=3))

        print('\n')
        users = user_service.GetUsers()
        for u in users:
            print(u.id, u.name, u.gender, u.desc)

        lx = user_service.GetUserById(user_id=9)
        if lx:
            print(lx.id, lx.name, lx.gender, lx.desc)

    cli.close()




