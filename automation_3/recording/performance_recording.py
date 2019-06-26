# encoding=utf-8
import sys
import unittest

from automation_3.base.base import BaseTestCase
from automation_3.common.activity import Activity
from automation_3.home.launch import LaunchAction
from automation_3.recording.edit_info import RecordingEditInfoAction
from automation_3.recording.preview import RecordingPreviewAction
from automation_3.recording.recording import RecordingAction
from automation_3.recording.share import RecordingShareAction

sys.path.append('..')


class PerformanceRecording(BaseTestCase):

    def test_case001_performance(self):
        launch = LaunchAction(self)

        # 启动
        launch.launch()

        # 切换到sing tab
        launch.toTab(LaunchAction.Sing)

        # 开始统计内存占用
        self.startMemoryProfile()

        el = None
        index = 0
        while el is None:
            # sing按钮
            el = self.findElementById('btn_sing')
            if el:
                # 统计开始前的内存使用
                self.profile()
                el[0].click()
                break

            index += 1
            if index > 5:
                break

        if index > 5:
            self.log('error: can not find sing button...')
            return

        # 找到弹窗按钮，选择第一个
        el = self.findElementsById('item_play_detail_dialog_text')
        el[0].click()

        recordingAction = RecordingAction(self)
        recordingAction.checkPermission()

        # 等待录制页面出现
        self.waitActivity(Activity.Recording)

        # 清理各种引导
        recordingAction.clearGuide()

        # 切换摄像头
        recordingAction.switchCamera()

        # 开始录制
        recordingAction.startRecording()

        # 录制时间
        recordingDuration = 70

        # 不能睡眠太长时间，否则session会断掉
        cd = 0
        while cd < recordingDuration:
            self.actionSleep(5)
            self.profile()
            cd += 5

        # 停止录制
        recordingAction.stopRecording()

        # 小于60秒，确认退出
        recordingAction.dialogBtnClick(confirm=True)

        # 进入到预览页面
        self.waitActivity(Activity.RecordingPreview)

        previewAction = RecordingPreviewAction(self)

        # 发布作品
        previewAction.post()

        if recordingDuration < 60:
            # 未超过60秒，弹出提示框，只有ok按钮
            previewAction.dialogBtnClick(confirm=True)

            # 退出预览
            previewAction.quit()
        else:
            # 可以发布的作品
            # 超过60秒，弹出提示框，提示没有录制完成，确认进入下一步
            previewAction.dialogBtnClick(confirm=True)

            # 进入edit recording info页面
            self.waitActivity(Activity.RecordingEditInfo)

            # 编辑作品信息
            editInfoAction = RecordingEditInfoAction(self)
            editInfoAction.setDesc()
            editInfoAction.send()

            # 进入分享页面
            self.waitActivity(Activity.RecordingShare)
            share = RecordingShareAction(self)
            share.done()

            self.profile()

        self.profileReport()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PerformanceRecording)
    unittest.TextTestRunner(verbosity=2).run(suite)