# -*- encoding=utf8 -*-
__author__ = "yaoliang.cui"
import os
import time
from airtest.core.api import *
from airtest.core.api import using
from airtest.core.android.android import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

using("solopi_FeedBrowse.air")
from solopi_FeedBrowse import feed_browse
using("solopi_FeedBrowse_PlayRecording.air")
from solopi_FeedBrowse_PlayRecording import feed_browse_playRecording
using("solopi_FeedBrowse_PlayVideo.air")
from solopi_FeedBrowse_PlayVideo import feed_browse_playVideo
using("solopi_RecordVideo.air")
from solopi_RecordVideo import record_video
dev = connect_device("android:///")
devs = device()
path = os.getcwd()
auto_setup(__file__)

version = "766"

# feed浏览
a = feed_browse(5, 600)
save_data("feed浏览", a)

# feed浏览recording
b = feed_browse_playRecording(5, 600)
save_data("feed浏览recording", b)

# feed浏览Video
c = feed_browse_playVideo(5, 600)
save_data("feed浏览video", c)

# 录制视频recording
d = record_video(5, 2)
save_data("录制视频recording", d)



def save_data(data_name, data, localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ):
    with open(path + '/' + version + '.txt', 'a') as f:
        f.write(data_name + "_数据列表(" + localtime + ")\n")
        f.write(str(data))
        f.write("\n\n")

