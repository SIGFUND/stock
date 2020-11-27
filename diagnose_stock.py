# -*-coding=utf-8-*-

__author__ = 'Rocky'
'''
http://30daydo.com
Email: weigesysu@qq.com
'''
from configure.settings import DBSelector
from common.BaseService import BaseService
from common.SecurityBase import StockBase

# 是否黑名单,东北股


class StockDoctor(BaseService,StockBase):

    def __init__(self):
        # super(StockDoctor, self).__init__(f'log/{self.__class__.__name__}.log')
        BaseService.__init__(self,f'log/{self.__class__.__name__}.log') # 新写法
        StockBase.__init__(self)
        self.logger.info('start')
        self.DB = DBSelector()


    def check_blacklist(self,code):
        conn = self.DB.get_mysql_conn('db_stock','qq')
        cur = conn.cursor()
        cmd = 'select * from tb_blacklist where code="{}"'.format(code)
        cur.execute(cmd)
        ret = cur.fetchone()
        if ret:
            return True
        else:
            return False

    # 是否是东北的
    def north_east(self,code):
        north_east_area = ['黑龙江','吉林','辽宁']
        conn = self.DB.get_mysql_conn('db_stock','qq')
        cur = conn.cursor()
        cmd = 'select area from tb_basic_info where code=\'{}\''.format(code)
        cur.execute(cmd)
        ret = cur.fetchone()
        if ret and ret in north_east_area:
            return True
        else:
            return False

    def get_code(self,name):
        conn = self.DB.get_mysql_conn('db_stock','qq')
        cur = conn.cursor()
        cmd = 'select code from tb_basic_info where name=\'{}\''.format(name)
        cur.execute(cmd)
        ret = cur.fetchone()
        return ret

    def diagnose(self,code):
        if not self.valid_code(code):
            raise ValueError('输入有误')

        issue = False
        if self.check_blacklist(code):
            self.logger.info('存在黑名单')
            issue = True

        if self.north_east(code):
            self.logger.info('是东北股')
            issue = True

        if issue:
            self.logger.info(f'{code} 问题股')

def main():
    code = input('输入诊断个股的代码或者名称: ')

    doctor = StockDoctor()
    doctor.diagnose(code)


if __name__ == '__main__':
    main()