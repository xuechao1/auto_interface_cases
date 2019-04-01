__author__ = 'Emerson'
import configparser
from conf import project_path

class ReadConfig:
    def read_config(self, file_path, section, option):
        cf = configparser.ConfigParser()
        cf.read(file_path, encoding='UTF-8')  #
        value = cf.get(section, option)
        return value


if __name__ == '__main__':
    # value=ReadConfig().read_config("../conf/http.conf",'HTTP','ip')
    # from conf import project_path
    value = ReadConfig().read_config(project_path.db_conf_path, 'DATABASE', 'config')
    print(value)
