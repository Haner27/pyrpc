# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket
from thrift.server import TServer

from handlers import multi_processor


def make_server(port=9000):
    # 指定端口启动transport
    transport = TSocket.TServerSocket(port=port)

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


if __name__ == '__main__':
    server = make_server()
    print('Starting the server...')
    server.serve()


