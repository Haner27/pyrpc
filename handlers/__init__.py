from thrift.TMultiplexedProcessor import TMultiplexedProcessor

multi_processor = TMultiplexedProcessor()


class RegisterService(type):
    def __new__(cls, name, bases, attrs):
        if 'REGISTER_NAME' not in attrs or not attrs['REGISTER_NAME']:
            raise Exception('class {} need REGISTER_NAME.'.format(name))
        service_name = attrs['REGISTER_NAME']

        if 'SERVICE' not in attrs or not attrs['SERVICE']:
            raise Exception('class {} nedd SERVICE'.format(name))
        service = attrs['SERVICE']

        handler_cls = super().__new__(cls, name, bases, attrs)
        processor = service.Processor(
            handler_cls()
        )
        multi_processor.registerProcessor(
            serviceName=service_name,
            processor=processor
        )
        return handler_cls


from handlers import image
from handlers import user
