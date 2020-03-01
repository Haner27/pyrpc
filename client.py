from contextlib import contextmanager

from thrift import Thrift
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

# 连接Socket
socket = TSocket.TSocket('localhost', 9000)


@contextmanager
def connect_rpc(socket, service_name, service_module):
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


if __name__ == '__main__':
    # 使用样例：
    # # 导入thrift生成对应语言的service以及数据对象结构
    from thrifts.user_service import UserService

    service_name = 'User'
    with connect_rpc(socket, service_name, UserService) as cli:
        # 调用某个没有返回值的函数

        hnf = cli.CreateUser(UserService.User(id=1, name='hnf', desc='i am hnf'))
        print(hnf.id, hnf.name, hnf.gender, hnf.desc)
        lx = cli.CreateUser(UserService.User(id=2, name='lx', gender='female', desc='i am lx'))
        print(hnf.id, hnf.name, hnf.gender, hnf.desc)
        fgy = cli.CreateUser(UserService.User(id=3, name='fgy'))
        print(hnf.id, hnf.name, hnf.gender, hnf.desc)
        print('\n')

        users = cli.GetUsers()
        for u in users:
            print(u.id, u.name, u.gender, u.desc)

        r = cli.Ping()
        print(r.code)

        print(cli.DeleteUserById(user_id=3))

        print('\n')
        users = cli.GetUsers()
        for u in users:
            print(u.id, u.name, u.gender, u.desc)

        lx = cli.GetUserById(user_id=2)
        print(lx.id, lx.name, lx.gender, lx.desc)
