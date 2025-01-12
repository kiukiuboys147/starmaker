# coding=utf-8
"""
调整测试数据
依次运行对应测试脚本
"""
import os
import time

from automation.report.test_data_extraction import get_data

# 当前脚本的父目录的绝对路径
current_script_parent_dir = os.path.realpath(os.path.abspath(__file__ + '/..'))

class testSuite:
    # 测试数据调整
    def __init__(self):
        try:
            with open(os.path.join(current_script_parent_dir, 'config.txt'), 'r', encoding='utf-8') as f:
            # with open('/Users/Shared/Jenkins/Home/jobs/Performance-Test/workspace/automation/main/config.txt',
            #           'r', encoding='utf-8') as f:
                config = eval(f.read())

            print(config)
            # 测试版本
            self.ver = config["version"]
            # 包信息
            self.package = config["package"]
            # 设备信息
            self.platformVersion = config["platformVersion"]
            self.device = config["device"]
            self.deviceName = config["deviceName"]
        except:
            # 测试版本
            self.ver = "9.9.9"
            # 包信息
            self.package = "Product"
            # 设备信息
            self.platformVersion = "7.1"
            self.device = "Redmi_5A"
            self.deviceName = "riva"

        exit()

        # 取数据次数（最低5，因为结算时会减去最高和最低）
        self.num = 5
        # 单次数据运行时间
        self.run_time = 10
        # 录制歌曲数量
        self.song_num = 1

    # 测试数据处理
    def log_result(self, modular):
        result = get_data(self.ver, modular)
        if result:
            print("%s模块数据已记录成功" % modular)
        time.sleep(10)

    def liveSuite(self):
        from automation.live.performance_broadcaster import PerformanceBroadcaster
        modular = "live"
        num = 0
        while num < self.num:
            num += 1
            print("\n\n当前运行 %s模块 第%s次" % (modular, num))
            try:
                PerformanceBroadcaster().suiteRunner(PerformanceBroadcaster)
            except ValueError:
                num -= 1
                continue
        self.log_result(modular)

    def momentSuite(self):
        from automation.moment.performance_popular import PerformanceMoment
        modular = "popular"
        num = 0
        while num < self.num:
            num += 1
            print("\n\n当前运行 %s模块 第%s次" % (modular, num))
            try:
                PerformanceMoment().suiteRunner(PerformanceMoment)
            except ValueError:
                num -= 1
                continue
        self.log_result(modular)

    def recordingSuite(self):
        from automation.recording.performance_recording import PerformanceRecording
        modular = "recording"
        num = 0
        while num < self.num:
            num += 1
            print("\n\n当前运行 %s模块 第%s次" % (modular, num))
            try:
                PerformanceRecording().suiteRunner(PerformanceRecording)
            except ValueError:
                num -= 1
                continue
        self.log_result(modular)


if __name__ == '__main__':
    testSuite().liveSuite()
    testSuite().momentSuite()
    testSuite().recordingSuite()
