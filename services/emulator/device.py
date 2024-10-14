# encoding:utf-8
import os
import random
import re
import time
# import phonenumbers
# from phonenumbers import carrier, geocoder
from subprocess import Popen, PIPE

# import mod.func as func, mod.api as api
from faker import Faker
from loguru import logger

from flaskServer.services.emulator import func


class Ldmnq(object):
    """雷电模拟器"""

    # https://www.ldmnq.com/forum/17995.html
    def __init__(self, emu_path, index=0, pc_share=None, android_share=None):
        super().__init__()
        self.emu = emu_path
        self.index = index
        self.pc_share = pc_share
        self.android_share = android_share
        self.ld_console_exe = os.path.join(self.emu, 'ldconsole.exe')
        self.ld_adb_exe = os.path.join(self.emu, 'adb.exe')
        self.ld_exe = os.path.join(self.emu, 'ld.exe')
        self.devices = {}
        self.device = self.adb_ip = self.local_ip = None
        self.init_device()
        if self.devices:
            self.device = self.devices[str(self.index)]
            if self.device:
                self.adb_ip = self.device['adb_ip']
                self.local_ip = self.device['local_ip']
            print(self.device, self.adb_ip, self.local_ip)
        self.faker = Faker(locale='en_US')

    def ldconsole(self, command):
        """NoxConsole执行命令"""
        try:
            shell = '"{}" {}'.format(self.ld_console_exe, command)
            # print(shell)
            pop = Popen(shell, stdout=PIPE, shell=True)
            resp_list = pop.stdout.readlines()
            pop.stdout.close()
            resp_list = [x.decode('gbk').strip('\r\n') for x in resp_list]
            resp_list = [x for x in resp_list if 'device not found' not in x]
            return resp_list
        except Exception as e:
            logger.error(e)

    def ldcmd(self, cmd):
        cmd_list = '"{}" -s {} "{}"'.format(self.ld_exe, self.index, cmd)
        pop = Popen(cmd_list, stdout=PIPE, shell=True)
        resp_list = pop.stdout.readlines()
        pop.stdout.close()
        resp_list = [x.decode('gbk').strip('\r\n') for x in resp_list]
        resp_list = [x for x in resp_list if 'device not found' not in x]
        return resp_list

    def adb_shell(self, command):
        """用ldconsole.exe执行adb shell命令. 注意: 不能执行adb外部命令, 如:push pull install等"""
        # command = 'adb --index {} --command "shell {}"'.format(
        #     self.index, command)
        # resp_list = self.ldconsole(command)
        # return resp_list
        return self.ldcmd(command)

    def get_devices(self):
        """获取模拟器列表, 返回: 索引, 标题, 顶层窗口句柄, 绑定窗口句柄, 是否进入android, 进程PID, VBOX进程PID"""
        resp = self.ldconsole('list2')
        return resp

    def init_device(self):
        """初始化模拟器信息, 获取模拟器index和adb_ip等信息"""
        device_list = self.get_devices()
        if device_list:
            for device in device_list:
                device_dict = {}
                spl_list = device.split(',')
                if spl_list:
                    device_dict['index'] = int(spl_list[0])  # 模拟器坐标
                    index = device_dict['index']
                    device_dict['title'] = spl_list[1]  # 虚拟机标题
                    device_dict['top_hwnd'] = spl_list[2]  # 顶层窗口句柄
                    device_dict['window_hwnd'] = spl_list[3]  # 工具栏窗口句柄
                    device_dict['isrunning'] = spl_list[4]  # 是否进入android
                    device_dict['pid'] = spl_list[5]  # 进程PID
                    device_dict['vbox_pid'] = spl_list[6]  # vbox进程id
                    port = 5555 + int(index) * 2
                    device_dict['adb_ip'] = '127.0.0.1:{}'.format(port)
                    # 获取局域网ip
                    local_ip = ''
                    resp = self.adb_shell('ifconfig')
                    if resp:
                        ip_str = ""
                        for i in range(len(resp)):
                            st = resp[i]
                            if 'eth0' in st:
                                ip_str = resp[i + 1]
                                break
                        if ip_str:
                            mc = re.search(r'inet addr:(.*?) ', ip_str)
                            if mc:
                                local_ip = mc.group(1)
                    device_dict['local_ip'] = local_ip
                    self.devices[str(index)] = device_dict

    def run_atx_agent(self):
        """运行atx-agent服务, 不存在则上传文件并启动"""
        # 安装uiautomator应用
        pkg = 'com.github.uiautomator'
        cmd = 'pm path {}'.format(pkg)
        resp = self.adb_shell(cmd)
        resp = [x for x in resp if x]  # 去除空值
        need_install = False
        if not resp:  # 未安装, 安装app
            need_install = True

        else:
            if func.str_in_list('java.lang.Exception:', resp):  # 报错, 不存在
                need_install = True
            pass
        if need_install:
            apk_path = 'app-uiautomator.apk'
            if os.path.exists(apk_path):
                # print('install uiautomator2 apk')
                self.install_app(apk_path)
            else:  # apk 不存在, 无法安装
                return
        # 启动/安装atx-agent服务
        atx_path = r'D:\python\github\atx-agent'
        for _ in range(2):
            # command = 'ls /data/local/tmp'
            # resp = self.adb_shell(command)
            # if 'atx-agent' in resp:  # 存在atx-agent, 直接启动
            if self.find_exist(atx_path, 'f'):
                cmd = '{} server -d'.format(atx_path)
                resp = self.adb_shell(cmd)
                if func.str_in_list('run atx-agent in background', resp):
                    # print('atx-agent is running')
                    return True
            else:
                if os.path.exists(
                        'atx-agent'):  # 本地存在atx-agent文件, 上传到目录, 修改权限, 并启动服务
                    # self.push('atx-agent', atx_path)
                    self.ldconsole(
                        'adb --index {} --command "push atx-agent {}"'.format(
                            self.index, atx_path))
                    cmd = 'chmod 777 /data/local/tmp/atx-agent'
                    self.adb_shell(cmd)
                else:  # 不存在atx-agent文件, 无法启动相关服务
                    return

    def set_proxy(self, proxy):
        """设置代理ip [注意:只支持http代理, 仅传入ip和port, 不需要带格式, 如: 127.0.0.1:10809]"""
        command = 'settings put global http_proxy {}'.format(proxy)
        self.adb_shell(command)

    def unset_proxy(self):
        """取消代理ip"""
        command = 'settings put global http_proxy :0'
        self.adb_shell(command)

    def run_app(self, pkg):
        """启动app"""
        cmd = 'runapp --index {} --packagename {}'.format(self.index, pkg)
        self.ldconsole(cmd)

    def kill_app(self, pkg):
        """强制退出app"""
        cmd = 'killapp  --index {} --packagename {}'.format(self.index, pkg)
        self.ldconsole(cmd)

    def install_app(self, apk_path):
        apk_path = func.path_win2linux(apk_path)
        cmd = 'installapp --index {} --filename {}'.format(
            self.index, apk_path)
        self.ldconsole(cmd)

    def clear_app(self, pkg):
        """清空app数据"""
        cmd = 'pm clear {}'.format(pkg)
        self.adb_shell(cmd)

    def mkdirs(self, dirname):
        cmd = 'mkdir -m 777 -p {}'.format(dirname)
        self.adb_shell(cmd)

    def find_exist(self, target, type='f'):
        """判断文件/目录是否存在 [target: 查找目标; type: f是文件, d是目录]"""
        cmd = '[ -{} {} ] && echo found'.format(type, target)
        resp = self.adb_shell(cmd)
        if resp and func.str_in_list('found', resp):
            return True

    def backup_data(self, package_name, backup_file, clear_data=True):
        """备份APP应用数据[backup_file: 备份路径, tar.gz格式. 如: /mnt/shared/App/com.whatsapp.tar.gz]"""
        try:
            if backup_file:
                dirname = os.path.dirname(backup_file)
                if not self.find_exist(dirname, type='d'):
                    self.mkdirs(dirname)
                self.kill_app(package_name)  # 先强制关闭应用
                # 打包命令, 忽略lib cache等系统链接和缓存目录
                command = 'tar -czvf {} /data/data/{}  --exclude data/data/{}/lib --exclude data/data/{}/cache'.format(
                    backup_file, package_name, package_name, package_name)
                self.adb_shell(command)  # 开始备份
                if self.find_exist(backup_file, type='f'):
                    if clear_data:
                        cmd = 'pm clear {}'.format(package_name)
                        self.adb_shell(cmd)
                    return True
        except Exception as e:
            print(str(e))
            return

    def restore_data(self, package_name, backup_file):
        """恢复APP应用数据.[备份路径, tar.gz格式. 如: /mnt/shared/App/com.whatsapp.tar.gz]. 注意: 默认恢复到/data/data/应用 路径下"""
        try:
            # 先获取权限, owner和group名称
            data_path = '/data/data/{}'.format(package_name)
            owner = group = None
            cmd = 'ls -l -d {}'.format(data_path)
            resp = self.adb_shell(cmd)
            if resp:
                st = None
                for res in resp:
                    if res and data_path in res:
                        st = res
                        break
                if st:
                    st_list = st.split(' ')
                    if st_list:
                        owner = st_list[2]
                        group = st_list[3]
            if backup_file:
                self.kill_app(package_name)  # 先强制关闭应用
                command = 'pm clear '.format(package_name)
                self.adb_shell(command)  # 清空应用数量
                command = 'tar -xzvf {} -C /'.format(backup_file)
                self.adb_shell(command)
                # print(owner, group)
                if owner and group:
                    cmd = 'chown -hR {}:{} {}'.format(owner, group, data_path)
                    self.adb_shell(cmd)
                    return True
        except Exception as e:
            print(str(e))
            return

    def set_locate(self, lng, lat):
        """修改定位[经度, 纬度]"""
        cmd = 'action --index {} --key call.locate --value {},{}'.format(
            self.index, lng, lat)
        self.ldconsole(cmd)

    def getRandomPhoneNumber(self):
        haoduan = ['130', '131', '132', '138', '137', '139']
        hao = random.randint(00000000, 99999999)
        number = "{}{}".format(random.choice(haoduan), hao)
        return number
    # 修改模拟器
    def modifyLd(self, modify_str):
        '''
        修改模拟器[modify_str: 修改的模拟器参数字符. 如: --resolution 600,360,160 --cpu 1 --memory 1024 --imei auto]
        注：调用modify需要在模拟器启动前，不然可能不生效
        '''
        try:
            '''
            modify <--name mnq_name | --index mnq_idx>
            [--resolution ] // 自定义分辨率
            [--cpu <1 | 2 | 3 | 4>] // cpu设置
            [--memory <512 | 1024 | 2048 | 4096 | 8192>] // 内存设置
            [--manufacturer asus] // 手机厂商
            [--model ASUS_Z00DUO] // 手机型号
            [--pnumber 13812345678] // 手机号码
            [--imei ] // imei设置，auto就自动随机生成
            [--imsi ]
            [--simserial ]
            [--androidid ]
            [--mac ] //12位m16进制mac地址
            [--autorotate <1 | 0>]
            [--lockwindow <1 | 0>]
            '''
            'modify --index 0 --resolution 600,360,160 --cpu 1 --memory 1024 --imei auto'
            resp = self.shell('modify  --index {} {}'.format(
                self.index, modify_str))
            return resp
        except:
            return
    # 随机修改模拟器信息
    def randomLdInfo(self,):
        brand, model = self.get_manufacturer_model()
        phone_number = self.getRandomPhoneNumber()
        st = "--manufacturer {} --model {} --pnumber {} --imei auto".format(
            brand, model, phone_number)
        self.modifyLd(st)
    # 运行模拟器
    def runLd(self):
        try:
            self.shell('launch --index {}'.format(self.index))
            return True
        except:
            return
    # 退出模拟器
    def quitLd(self):
        try:
            self.shell('quit --index {} '.format(self.index))
            return True
        except:
            return
    # 判断模拟器是否已经运行
    def isRunning(self):
        '''模拟器是否运行并已经进入安卓系统'''
        ld_list = self.getLdList()
        if ld_list:
            for dic in ld_list:
                index = dic['index']
                if index == self.index:
                    if dic['in_android'] == '1':
                        return True
        return
    # 获取模拟器列表. 返回模拟器列表.
    def getLdList(self):
        '''获取模拟器列表. 返回模拟器列表. '''
        resp = self.shell('list2')
        dlist = []
        if resp:
            for l in resp:
                st = str(l, encoding='gbk').strip()
                if st:
                    _li = func.Str2List(st, ',')
                    if _li:
                        _dic = {
                            'index': _li[0],
                            'title': _li[1],
                            'top_hwnd': _li[2],
                            'hwnd': _li[3],
                            'in_android': _li[4],
                            'pid': _li[5],
                            'vbox_pid': _li[6]
                        }
                        dlist.append(_dic)
        return dlist
    def shell(self, cmd):
        cmd_list = [self.ld_console_exe]
        if type(cmd) == list:
            cmd_list.extend(cmd)
        elif type(cmd) == str:
            cmd_list = "{} {}".format(self.ld_console_exe, cmd)
        # print(cmd_list)
        _p = Popen(cmd_list, stdout=PIPE, shell=True)
        _list = _p.stdout.readlines()
        return _list
    # 重置模拟器参数并启动
    def resetLd(self):
        self.quitLd()
        time.sleep(5)
        self.randomLdInfo()
        time.sleep(1)
        self.runLd()
        for _ in range(30):
            if self.isRunning():
                return True
            time.sleep(1)

    # 获取硬件信息
    def get_device_info(self):
        # https://www.ldmnq.com/forum/17485.html
        info = {}
        info['imei'] = self.ldconsole(
            'getprop --index {} --key phone.imei'.format(
                self.index))[0].strip()
        info['simserial'] = self.ldconsole(
            'getprop --index {} --key phone.simserial'.format(
                self.index))[0].strip()
        info['androidid'] = self.adb_shell(
            'getprop phone.androidid')[0].strip()
        info['manufacturer'] = self.ldconsole(
            'getprop --index {} --key phone.manufacturer'.format(
                self.index))[0].strip()
        info['model'] = self.adb_shell('getprop phone.model')[0].strip()
        info['pnumber'] = self.adb_shell(
            'getprop phone.number')[0].strip()  # 电话号码
        info['imsi'] = self.adb_shell('getprop phone.imsi')[0].strip()
        info['net_operatorname'] = self.adb_shell(
            'getprop phone.net_operatorname')[0].strip()  # 网络运营商
        info['sim_cid'] = self.adb_shell('getprop phone.sim_cid')[0].strip(
        )  # 客户地区, 基站坐标(可以随机), 也可以通过https://www.opencellid.org/等网站获取真实cellid
        info['sim_country'] = self.adb_shell(
            'getprop phone.sim_country')[0].strip()  # SIM区域
        info['sim_lac'] = self.adb_shell('getprop phone.sim_lac')[0].strip(
        )  # 地区  simcard, 基站区域坐标(可以随机, 也可以通过https://www.opencellid.org/获取真实lac数据)
        info['sim_operator'] = self.adb_shell(
            'getprop phone.sim_operator')[0].strip()  # 服务提供者
        info['sim_operatorname'] = self.adb_shell(
            'getprop phone.sim_operatorname')[0].strip()  # 电话运营商
        info['phone.simserial'] = self.adb_shell(
            'getprop phone.simserial')[0].strip()  # SIM序列
        # info['phone.turbo_mode'] = self.adb_shell('getprop phone.turbo_mode')[0].strip()  # 电话模式
        info['ro.product.board'] = self.adb_shell(
            'getprop ro.product.board')[0].strip()
        info['ro.product.brand'] = self.adb_shell(
            'getprop ro.product.brand')[0].strip()
        info['ro.serialno'] = self.adb_shell('getprop ro.serialno')[0].strip()
        info['ro.build.host'] = self.adb_shell(
            'getprop ro.build.host')[0].strip()
        info['ro.product.name'] = self.adb_shell(
            'getprop ro.product.name')[0].strip()
        info['ro.product.device'] = self.adb_shell(
            'getprop ro.product.device')[0].strip()
        info['ro.product.board'] = self.adb_shell(
            'getprop ro.product.board')[0].strip()
        info['dhcp.eth0.ipaddress'] = self.adb_shell(
            'getprop dhcp.eth0.ipaddress')[0].strip()
        info['ro.build.id'] = self.adb_shell('getprop ro.build.id')[0].strip()
        info['wifi.interface.mac'] = self.adb_shell(
            'getprop wifi.interface.mac')[0].strip()
        info['gsm.sim.operator.alpha'] = self.adb_shell(
            'getprop gsm.sim.operator.alpha')[0].strip()  # CMCCC'运营商名称1
        info['gsm.operator.numeric'] = self.adb_shell(
            'getprop gsm.operator.numeric')[0].strip()  # 46001'运营商代码1
        info['gsm.operator.alpha'] = self.adb_shell(
            'getprop gsm.operator.alpha')[0].strip()  # CMCCC'运营商名称2
        info['gsm.sim.operator.iso-country'] = self.adb_shell(
            'getprop gsm.sim.operator.iso-country')[0].strip()  # CN'国家码1
        info['gsm.operator.iso-country'] = self.adb_shell(
            'getprop gsm.operator.iso-country')[0].strip()  # CN'国家码2
        info['gsm.network.type'] = self.adb_shell(
            'getprop gsm.network.type')[0].strip()  # UMTS:4'网络类型
        info['gsm.operator.isroaming'] = self.adb_shell(
            'getprop gsm.operator.isroaming')[0].strip()  # false'漫游
        info['gsm.sim.state'] = self.adb_shell(
            'getprop gsm.sim.state')[0].strip()  # READY'SIM状态
        return info
        # 电话号码, androidid, imei和imsi, 品牌, model, gms和sim信息(运营商信息根据号码国家生成), 经纬度(根据代理ip获取坐标/根据国家随机)
    @staticmethod
    def get_manufacturer_model():
        '''品牌和模型'''
        dic = {}
        dic['HUAWEI'] = [
            'LIO-AN00', 'TAS-AN00', 'TAS-AL00', 'LYA-AL10', 'HMA-AL00',
            'VOG-AL00', 'ELE-AL00', 'OXF-AN10', 'OXF-AN00', 'PCT-AL10',
            'YAL-AL10', 'YAL-AL00', 'WLZ-AN00', 'SEA-AL10'
        ]
        dic['xiaomi'] = ['MI 9']
        dic['Meizu'] = ['M973Q']
        dic['smartisan'] = ['DT1901A']
        dic['OPPO'] = ['PCLM10', 'PCRT00']
        dic['vivo'] = [
            'V1916A', 'V1824A', 'V1936A', 'V1923A', 'V1938CT', 'V1938T'
        ]
        dic['samsung'] = ['SM-N9760', 'SM-N9700', 'SM-G9750', 'SM-G9730']
        dic['OnePlus'] = ['HD1910', 'HD1900', 'GM1910', 'GM1900']
        dic['blackshark'] = ['DLT-A0', 'SKW-A0']
        dic['realme'] = ['RMX1931']
        dic['nubia'] = ['NX629J', 'NX627J']
        key_list = []
        for key in dic.keys():
            key_list.append(key)
        manufacturer = random.choice(key_list)
        model = random.choice(dic[manufacturer])
        return manufacturer, model

    def set_device_info(self, phone_number):
        """设置设备硬件信息"""

        try:
            imei_list = ['phone.imei']
            imsi_list = ['phone.imsi']
            simserial_list = ['phone.simserial']
            manufacturer_list = ['ro.product.brand', 'ro.product.manufacturer']
            model_list = [
                'ro.product.board', 'ro.product.model', 'ro.product.name'
            ]
            androidid_list = [
                'phone.androidid', 'net.hostname'
            ]  # net.hostname = "android-{}".format(androidid)

            net_operatorname_list = [
                'phone.net_operatorname', 'phone.sim_operatorname',
                'gsm.sim.operator.alpha', 'gsm.operator.alpha'
            ]  # 运营商名称:CMCC/AT&T等
            sim_cid_list = [
                'phone.sim_cid'
            ]  # 基站坐标(可以随机), 也可以通过 www.opencellid.org 等网站获取真实cellid
            operator_list = ['gsm.operator.numeric',
                             'phone.sim_operator']  # mcc+mnc
            sim_country_list = [
                'phone.sim_country', 'ro.product.locale.region',
                'persist.sys.country', 'gsm.sim.operator.iso-country',
                'gsm.operator.iso-country'
            ]  # sim/网络国家代码, 如:us
            sim_lac_list = [
                'phone.sim_lac'
            ]  # sim card  基站区域坐标(可以随机, 也可以通过www.opencellid.org cellphonetrackers.org获取真实lac数据)
            serialno_list = ['ro.serialno', 'ro.boot.serialno']
            build_id_list = [
                'ro.build.id'
            ]  # ro.bootimage.build.fingerprint  ro.build.description  ro.build.fingerprint 需要替换
            wifi_mac_list = ['wifi.interface.mac']  # modify命令可以设置mac
            gsm_network_type_list = ['gsm.network.type']  # wifi/13(4g)
            gsm_status = ['gsm.sim.state']  # 固定值:READY

            # self.ldconsole('modify --index {} --imei auto --imsi auto --simserial auto --androidid auto'.format(self.index))
            self.ldconsole(
                'setprop --index {} --key "phone.imei" --value "auto"'.format(
                    self.index))  # 随机imei
            self.ldconsole(
                'setprop --index {} --key "phone.imsi" --value "auto"'.format(
                    self.index))  # 随机imsi
            self.ldconsole(
                'setprop --index {} --key "phone.simserial" --value "auto"'.
                format(self.index))  # 随机simserial
            manufacturer, model = Ldmnq.get_manufacturer_model()
            print(manufacturer, model)
            if manufacturer:
                self.ldconsole('modify --index {} --manufacturer {}'.format(
                    self.index, manufacturer))
                for m in manufacturer_list:
                    self.ldconsole(
                        'setprop --index {} --key "{}" --value "{}"'.format(
                            self.index, m, manufacturer))
            if model:
                self.ldconsole('modify --index {} --model {}'.format(
                    self.index, model))
                for m in model_list:
                    self.ldconsole(
                        'setprop --index {} --key "{}" --value "{}"'.format(
                            self.index, m, model))
            # androidid = ''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(16))
            # if androidid:
            #     self.ldconsole('setprop --index {} --key "{}" --value "{}"'.format(self.index, androidid_list[0], androidid))
            #     self.ldconsole('setprop --index {} --key "{}" --value "{}"'.format(self.index, androidid_list[1], "android-{}".format(androidid)))

            # 根据phonenumber, 获取国家简码; 根据国家信息获取运营商简码和id
            # if phone_number and '+' in phone_number:
            #     phone = phonenumbers.parse(phone_number, None)
            #     if phone:
            #         country_code = phone.country_code  # 电话国码
            #         national_number = phone.national_number  # 号码部分(无国码)
            #         if national_number:
            #             self.ldconsole(
            #                 'setprop --index {} --key "{}" --value "{}"'.
            #                 format(self.index, 'phone.number',
            #                        national_number))
            #         region_code = carrier.region_code_for_number(
            #             phone)  # 国家简码: us/cn
            #         carrier_name = carrier.name_for_number(
            #             phone, 'en')  # 运营上名称 如: vodafone/china unicom等
            #         # 获取mcc
            #         mcc_region_code = region_code
            #         # mcc_region_code = 'us'
            #         region_mcc_list = api.get_mcc_dict(mcc_region_code.lower())
            #         if region_mcc_list:
            #             mcc_dict = random.choice(region_mcc_list)
            #             mcc = '{}{}'.format(mcc_dict['mcc'], mcc_dict['mnc'])
            #             # 设置mcc
            #             if mcc:
            #                 for m in operator_list:
            #                     self.ldconsole(
            #                         'setprop --index {} --key "{}" --value "{}"'
            #                         .format(self.index, m, mcc))
            #             # 设置国家简码
            #             iso = mcc_dict[
            #                 'iso'] or mcc_region_code  # 运营商国家简码 us/vn/cn等
            #             if iso:
            #                 for m in sim_country_list:
            #                     self.ldconsole(
            #                         'setprop --index {} --key "{}" --value "{}"'
            #                         .format(self.index, m, iso.upper()))
            #             network = carrier_name or mcc_dict['network']
            #             if '/' in network:
            #                 network = network.split('/')[0]
            #             if ' ' in network:  # 处理名称带空格的问题
            #                 nlist = network.split(' ')
            #                 blist = [x for x in nlist if x]
            #                 if len(blist) >= 4:  # 长度大于等于4 , 取每一个首字母
            #                     bstr = ""
            #                     for bl in blist:
            #                         bstr += bl[0]
            #                     network = bstr
            #                 else:  # 小于4, 判断首字节长度, 如果大于等于3, 就取首节.
            #                     if len(nlist[0]) >= 3:
            #                         network = nlist[0]
            #                     else:
            #                         network = ''.join(nlist)[0:4]
            #             if network:  # 设置移动网络运营商
            #                 for m in net_operatorname_list:
            #                     self.ldconsole(
            #                         'setprop --index {} --key "{}" --value "{}"'
            #                         .format(self.index, m, network))
            #         # 设置cid (基站id: cellid)
            #         cid = random.randint(100, 9999999999)
            #         for m in sim_cid_list:
            #             self.ldconsole(
            #                 'setprop --index {} --key "{}" --value "{}"'.
            #                 format(self.index, m, cid))
            #         # 设置基站区域id lac: sim_lac_list
            #         lac = random.randint(100, 99999)
            #         for m in sim_lac_list:
            #             self.ldconsole(
            #                 'setprop --index {} --key "{}" --value "{}"'.
            #                 format(self.index, m, lac))
            #         # 设置 ro.sirialno
            #         serial = ''.join(
            #             random.choice(string.digits + string.ascii_lowercase)
            #             for _ in range(8))
            #         for m in serialno_list:
            #             self.ldconsole(
            #                 'setprop --index {} --key "{}" --value "{}"'.
            #                 format(self.index, m, serial))
            #         # 设置wifi mac
            #
            #         mac = self.faker.mac_address()
            #         if mac:
            #             for m in wifi_mac_list:
            #                 self.ldconsole(
            #                     'setprop --index {} --key "{}" --value "{}"'.
            #                     format(self.index, m, mac))
            #         # 设置gsm_network_type_list
            #         for m in gsm_network_type_list:
            #             self.ldconsole(
            #                 'setprop --index {} --key "{}" --value "{}"'.
            #                 format(self.index, m, 'wifi'))
            #         # 设置 gsm_status
            #         for m in gsm_status:
            #             self.ldconsole(
            #                 'setprop --index {} --key "{}" --value "{}"'.
            #                 format(self.index, m, 'READY'))
            #         # 设置经纬度
            #         resp = self.faker.local_latlng(country_code=iso.upper())
            #         if resp:
            #             # lat,lng = resp[0], resp[1]
            #             lat, lng = '34.0494', ' -118.2661'
            #             if lat and lng:
            #                 self.set_locate(lng, lat)
        except Exception as e:
            pass
            print(str(e))
