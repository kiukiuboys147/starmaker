# coding=utf-8
import re
import threading
import time

from PerformanceEvaluationTest import utils


class Info(object):
    def __init__(self):
        print("进入Info类")
        self.task = None

    def get_start_info(self):
        print("进入Info.get_start_info方法")
        pass

    def get_end_info(self):
        print("进入Info.get_end_info方法")
        pass

    def get_index(self):
        print("进入Info.get_index方法")
        if self.task.period == "" or self.task.period is None:
            return time.strftime("%H:%M:%S")
        else:
            return self.task.period


class CPUInfo(Info):
    TIME = "time"
    CPU_RATE = "进程CPU占比(%)"
    JIFFIES = "时间片"

    def __init__(self):
        print("进入CPUInfo类")
        super().__init__()
        self.count = 1
        self.is_running = True

    def get_cpu_usage(self):
        cpu_usage = 0.0
        result = self.get_cpu_action()
        for i in range(2, len(result)):
            cpu_usage += float(result[i])
        return cpu_usage

    def get_cpu_action(self):
        cpu_path = "/proc/stat"
        info = self.task.d.adb_shell("cat " + cpu_path)
        return re.split("\\s+", info.split("\n")[0])

    def get_process_cpu_usage(self):
        result = self.get_process_cpu_action()
        cpu_usage = float(result[1]) + float(result[2])
        return cpu_usage

    def get_process_cpu_action(self):
        cpu_path = "/proc/" + self.task.pid + "/stat"
        info = self.task.d.adb_shell("cat " + cpu_path)
        result = re.split("\\s+", info)
        return [result[1], result[13], result[14]]

    def get_start_info(self):
        t = threading.Thread(target=self.get_cpu_info)
        t.start()

    def get_end_info(self):
        print("结束")
        print(time.strftime('%H:%M:%S', time.localtime(time.time())))
        self.is_running = False

    def get_cpu_info(self):
        dirs = self.task.output + "/cpu_stats/"
        file_name = "cpu_" + self.task.device + "_" + self.task.applicationid + "_" + self.task.version_name + "_" + self.task.name
        field_names = [self.TIME, self.CPU_RATE, self.JIFFIES]
        writer = utils.get_csv_writer(dirs, file_name, field_names)
        while self.is_running:
            start_all_cpu = self.get_cpu_usage()
            start_p_cpu = self.get_process_cpu_usage()
            time.sleep(self.task.interval)
            end_all_cpu = self.get_cpu_usage()
            end_p_cpu = self.get_process_cpu_usage()
            cpu_rate = 0.0
            if (end_all_cpu - start_all_cpu) != 0:
                cpu_rate = (end_p_cpu - start_p_cpu) * 100.00 / (
                    end_all_cpu - start_all_cpu)
                if cpu_rate < 0:
                    cpu_rate = 0
                elif cpu_rate > 100:
                    cpu_rate = 100
            jiffies = start_p_cpu
            writer.writerow(
                {self.TIME: self.get_index(),
                 self.CPU_RATE: format(cpu_rate, ".2f"), self.JIFFIES: jiffies})
            self.count += 1


class MemInfo(Info):
    TIME = "time"
    NATIVE_HEAP = "Native Heap(MB)"
    DALVIK_HEAP = "Dalvik Heap(MB)"

    def __init__(self):
        print("进入MemInfo类")
        super().__init__()
        self.count = 1
        self.is_running = True

    def get_start_info(self):
        t = threading.Thread(target=self.get_mem_info)
        t.start()

    def get_end_info(self):
        self.is_running = False

    def get_mem_info(self):
        dirs = self.task.output + "/mem_stats/"
        file_name = "mem_" + self.task.device + "_" + self.task.applicationid + "_" + self.task.version_name + "_" + self.task.name
        field_names = [self.TIME, self.NATIVE_HEAP, self.DALVIK_HEAP]
        writer = utils.get_csv_writer(dirs, file_name, field_names)
        while self.is_running:
            native_info = self.task.d.adb_shell("dumpsys meminfo " + self.task.pid + " | grep 'Native Heap '")
            native_pss = format(int(re.findall(r"\d+", native_info)[0]) / 1000.0, ".2f")
            dalvik_info = self.task.d.adb_shell("dumpsys meminfo " + self.task.pid + " | grep 'Dalvik Heap '")
            dalvik_pss = format(int(re.findall(r"\d+", dalvik_info)[0]) / 1000.0, ".2f")
            writer.writerow(
                {self.TIME: self.get_index(),
                 self.NATIVE_HEAP: native_pss, self.DALVIK_HEAP: dalvik_pss})
            self.count += 1
            time.sleep(self.task.interval)


class FPSInfo(Info):
    TIME = "time"
    FPS = "FPS"

    def __init__(self):
        print("进入FPSInfo类")
        super().__init__()
        self.is_running = True
        self.is_first = True
        self.last_time = 0.0
        self.last_fps = 0
        self.count = 1

    def get_start_info(self):
        t = threading.Thread(target=self.get_fps_info)
        t.start()

    def get_end_info(self):
        self.is_running = False

    def get_fps_info(self):
        command = "dumpsys gfxinfo " + self.task.pid + " | grep 'Total frames'"
        dirs = self.task.output + "/fps_stats/"
        file_name = "fps_" + self.task.device + "_" + self.task.applicationid + "_" + self.task.version_name + "_" + self.task.name
        field_names = [self.TIME, self.FPS]
        writer = utils.get_csv_writer(dirs, file_name, field_names)
        try:
            while self.is_running:
                if self.is_first:
                    self.last_time = time.time_ns()
                    self.last_fps = int(re.findall("\\d+", self.task.d.adb_shell(command))[0])
                    self.is_first = False
                current_time = time.time_ns()
                current_fps = int(re.findall("\\d+", self.task.d.adb_shell(command))[0])
                time_delta = (current_time - self.last_time) / 1000000000.0
                fps_delta = current_fps - self.last_fps
                fps = fps_delta / time_delta
                self.last_time = current_time
                self.last_fps = current_fps
                writer.writerow({self.TIME: self.get_index(), self.FPS: "{:.2f}".format(fps)})
                self.count += 1
                time.sleep(self.task.interval)
        except IndexError:
            pass


class NetInfo(Info):
    TIME = "time"
    DOWN_SPEED = "下载速度(KB/s)"
    UP_SPEED = "上传速度(KB/s)"
    AVERAGE_DOWN_SPEED = "平均下载速度(KB/s)"
    AVERAGEUP_SPEED = "平均上传速度(KB/s)"
    TOTAL_DOWN_SPEED = "下载总流量(KB)"
    TOTAL_UP_SPEED = "上传总流量(KB)"

    def __init__(self):
        print("进入NetInfo类")
        super().__init__()
        self.count = 1
        self.is_running = True
        self.is_first = True
        self.last_time = 0
        self.last_net_up = 0
        self.last_net_down = 0
        self.start_time = 0
        self.start_net_up = 0
        self.start_net_down = 0

    def get_start_info(self):
        t = threading.Thread(target=self.get_net_info)
        t.start()

    def get_end_info(self):
        self.is_running = False

    def get_net_info(self):
        command = "cat /proc/" + self.task.pid + "/net/dev | grep wlan"
        dirs = self.task.output + "/net_stats/"
        file_name = "net_" + self.task.device + "_" + self.task.applicationid + "_" + self.task.version_name + "_" + self.task.name
        field_names = [self.TIME,
                       self.DOWN_SPEED,
                       self.UP_SPEED,
                       self.AVERAGE_DOWN_SPEED,
                       self.AVERAGEUP_SPEED,
                       self.TOTAL_DOWN_SPEED,
                       self.TOTAL_UP_SPEED]
        writer = utils.get_csv_writer(dirs, file_name, field_names)
        while self.is_running:
            if self.is_first:
                self.start_time = time.time_ns()
                self.last_time = self.start_time
                net_info = self.task.d.adb_shell(command)
                net_array = re.split("\\s+", net_info)
                self.start_net_down = int(net_array[2])
                self.last_net_down = self.start_net_down
                self.start_net_up = int(net_array[10])
                self.last_net_up = self.start_net_up
                self.is_first = False
            current_time = time.time_ns()
            current_info = self.task.d.adb_shell(command)
            current_array = re.split("\\s+", current_info)
            current_net_down = int(current_array[2])
            current_net_up = int(current_array[10])
            time_delta = (current_time - self.last_time) / 1000000000.0
            time_total = (current_time - self.start_time) / 1000000000.0
            net_delta_up = (current_net_up - self.last_net_up) / 1024.0
            net_delta_down = (current_net_down - self.last_net_down) / 1024.0
            net_total_up = (current_net_up - self.start_net_up) / 1024.0
            net_total_down = (current_net_down - self.start_net_down) / 1024.0
            net_speed_up = net_delta_up / time_delta
            net_speed_down = net_delta_down / time_delta
            net_average_speed_up = net_total_up / time_total
            net_average_speed_down = net_total_down / time_total

            writer.writerow({self.TIME: self.get_index(),
                             self.DOWN_SPEED: "{:.2f}".format(net_speed_down),
                             self.UP_SPEED: "{:.2f}".format(net_speed_up),
                             self.AVERAGE_DOWN_SPEED: "{:.2f}".format(net_average_speed_down),
                             self.AVERAGEUP_SPEED: "{:.2f}".format(net_average_speed_up),
                             self.TOTAL_DOWN_SPEED: "{:.2f}".format(net_total_down),
                             self.TOTAL_UP_SPEED: "{:.2f}".format(net_total_up)
                             })
            # print("下载速度：{:.2f} KB/s".format(net_speed_down))
            # print("上传速度：{:.2f} KB/s".format(net_speed_up))
            # print("平均下载速度：{:.2f} KB/s".format(net_average_speed_down))
            # print("平均上传速度：{:.2f} KB/s".format(net_average_speed_up))
            # print("下载总流量：{:.0f} KB/s".format(net_total_down))
            # print("上传总流量：{:.0f} KB/s".format(net_total_up))
            # print("\n")
            self.last_time = current_time
            self.last_net_up = current_net_up
            self.last_net_down = current_net_down
            self.count += 1
            time.sleep(self.task.interval)
