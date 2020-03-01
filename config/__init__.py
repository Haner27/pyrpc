import os

import pyaml

CONFIG_DIR_NAME = 'config'
CONFIG_FILENAME = 'rpc.yaml'
THRIFTS_DIR_NAME = 'thrifts'


class Config:
    def __init__(self):
        # 自定义的配置
        self.listen_port = 9090
        self.path = self.PathConf()

        # 加载yaml里的配置
        self.yaml_obj = self.load_conf_from_yaml()
        self.stage = self.yaml_obj.get('stage')
        self.log = self.LogConf(self.yaml_obj.get('log'))
        self.zookeeper = self.ZookeeperConf(self.yaml_obj.get('zookeeper'))

    def load_conf_from_yaml(self):
        yaml_file = os.path.join(self.path.config_dir, CONFIG_FILENAME)  # 配置文件地址
        with open(yaml_file) as f:
            yaml = pyaml.yaml.safe_load(f)
        return yaml

    class LogConf:
        # 日志配置
        def __init__(self, log_conf):
            self.log_dir = log_conf['dir']
            self.common_log = os.path.join(self.log_dir, log_conf['common-log'])

    class ZookeeperConf:
        # zookeeper 配置
        def __init__(self, zookeeper_conf):
            self.url = zookeeper_conf['host']

    class PathConf:
        # 路径相关配置
        def __init__(self):
            self.work_dir = os.path.dirname(os.path.dirname(__file__))
            self.config_dir = os.path.join(self.work_dir, CONFIG_DIR_NAME)
            self.thrifts_dir =  os.path.join(self.work_dir, THRIFTS_DIR_NAME)


conf = Config()