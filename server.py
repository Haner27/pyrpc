import sys
import signal
from functools import partial

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket
from thrift.server import TServer

from config import conf
from handlers import multi_processor
from utils.zookeeper import ZkForServer


class RPCServer:
    def __init__(self, host, port, zookeeper_hosts):
        self.__host = host
        self.__port = port
        self.__zk_for_server = ZkForServer(conf.app_name, zookeeper_hosts)
        self.__server = self.make_server()

    def register_to_zookeeper(self, multi_processor, host, port):
        for service_name in multi_processor.services.keys():
            service_node = self.__zk_for_server.register_service(service_name, host, port)
            print('add service {}({}:{}) to zookeeper: {}'.format(service_name, host, port, service_node))

    def make_server(self):
        # 指定端口启动transport
        transport = TSocket.TServerSocket(host=self.__host, port=self.__port)

        '''
        TTransport（传输层），定义数据传输方式，可以为TCP/IP传输，内存共享或者文件共享等）被用作运行时库。
            TSocket：阻塞式socker；
            TFramedTransport：以frame为单位进行传输，非阻塞式服务中使用；
            TFileTransport：以文件形式进行传输；
            TMemoryTransport：将内存用于I/O，java实现时内部实际使用了简单的ByteArrayOutputStream；
            TZlibTransport：使用zlib进行压缩， 与其他传输方式联合使用，当前无java实现；
        '''
        tfactory = TTransport.TBufferedTransportFactory()

        '''
        TProtocol（协议层），定义数据传输格式:
            TBinaryProtocol：二进制格式；
            TCompactProtocol：压缩格式；
            TJSONProtocol：JSON格式；
            TSimpleJSONProtocol：提供JSON只写协议, 生成的文件很容易通过脚本语言解析；
            TDebugProtocol：使用易懂的可读的文本格式，以便于debug
        '''
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        '''
        Thrift支持的服务模型:
            TSimpleServer：简单的单线程服务模型，常用于测试；
            TThreadPoolServer：多线程服务模型，使用标准的阻塞式IO；
            TNonblockingServer：多线程服务模型，使用非阻塞式IO（需使用TFramedTransport数据传输方式）；
        '''
        server = TServer.TThreadPoolServer(multi_processor, transport, tfactory, pfactory)
        return server

    def run(self):
        try:
            # 服务注册
            self.register_to_zookeeper(multi_processor, host, port)
            print('Starting the server...')

            # 服务启动
            self.__server.serve()
        except Exception as ex:
            print(ex)
        finally:
            self.__zk_for_server.close()
            print('Stopping the server...')


if __name__ == '__main__':
    host, port = '127.0.0.1', int(sys.argv[1])
    server = RPCServer(host, port, conf.zookeeper.hosts)
    server.run()

