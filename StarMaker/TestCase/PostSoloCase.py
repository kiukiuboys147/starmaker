# coding=utf-8
import time
import unittest
from StarMaker.CommonView.Home import Home
from StarMaker.CommonView.Library import Library
from StarMaker.CommonView.Popup import Popup
from StarMaker.CommonView.Post import Sing
from StarMaker.Utils.Tools import Tools
from StarMaker.Utils.Tools import Screen
from StarMaker.Utils.GetAppiumDeriver import GetAppiumDeriver
# from StarMaker.CommonView.Profile import Profile
# from StarMaker.Utils.Tools import RegionalClick
# from StarMaker.Utils.ReadXMLData import ReadXMLData


# 录制发布
class PostSoloCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = GetAppiumDeriver().driver
        time.sleep(5)
        Popup().HomePopup_CheckIn_Close_LiveClick()

    def setUp(self):
        time.sleep(2)

    def tearDown(self):
        # 截图
        Tools().get_images()

    @classmethod
    def tearDownClass(cls):
        pass

    # 选择发布类型——校验跳转至Library页
    def test_Case001_SelectPostTypeCase(self):
        Home().HomeTab_Sing().click()
        time.sleep(2)
        Home().PostType_Sing().click()
        time.sleep(2)
        expValue = "HOT"
        actValue = Library().LibraryTab_HOT().text
        time.sleep(2)
        # 判断跳转正确
        self.assertEqual(expValue, actValue)

    # 查看第二首歌曲支持的录制模式
    def test_Case002_SongModeValidation(self):
        Library().LibraryPage_SecondSong_SingBtn().click()
        time.sleep(2)
        mode = self.driver.find_elements_by_class_name(Library().LibraryPage_SongMode())
        TextList = []
        for index in range(len(mode)):
            TextList.append(mode[index].text)
        try:
            if len(mode) == 3 and TextList == ['Solo', 'Join Collab', 'Start Collab']:
                print("不支持Chorus")
                return 3
            elif len(mode) == 4 and TextList == ['Solo', 'Join Collab', 'Start Collab', 'Chorus']:
                print("支持Chorus")
                return 4
        finally:
            self.driver.back()

    # 点击第二首歌曲——校验跳转至歌曲详情页
    def test_Case003_ClickSecondSongsCase(self):
        Library().LibraryPage_SecondSong().click()
        time.sleep(2)
        global SongName
        SongName = Library().SongInfoPage_SongInfo_SongName().text
        print(('%s:%s' % ("歌曲名", SongName)))
        expValue = "SING"
        actValue = Library().SongInfoPage_SongInfo_SING().text
        time.sleep(2)
        # 判断跳转正确
        self.assertEqual(expValue, actValue)

    # 点击Sing按钮，跳转至录制准备页
    def test_Case004_SINGSong_SoloCase(self):
        Library().SongInfoPage_SongInfo_SING().click()
        time.sleep(2)
        Library().SongInfoPage_SingType_Solo().click()
        time.sleep(5)
        Popup().SingPopup_Jurisdiction_LiveClick()
        expValue = "I KNOW"
        # actValue = Sing().RecordStart().get_attribute("bounds")  T32733
        actValue = Sing().HeadphonesRecommended().text
        time.sleep(2)
        # 判断跳转正确
        self.assertEqual(expValue, actValue)

    # 录制歌曲——录制完成跳转至预发布页面
    def test_Case005_RecordingCase(self):
        # Popup().SingPopup_HeadphonesRecommended_LiveClick()  T32733
        Sing().HeadphonesRecommended().click()
        time.sleep(2)
        Popup().SingPopup_PitchGuide_LiveClick()
        time.sleep(2)
        # RegionalClick(Sing().RecordStart()).CoreClick()  T32733
        Sing().START_Btn_Coordinate()
        time.sleep(2)
        # SongTime = Sing().RecordTime().text
        # print(('%s:%s' % ("歌曲时长", SongTime)))
        # Minute = SongTime[0:2]
        # Second = SongTime[3:5]
        # Time = int(Minute) * 60 + int(Second) + 3
        # # 等待歌曲录制完成
        # time.sleep(Time)
        Screen().DIYSwipe_Percentage(0.5, 0.65, 0.5, 0.2, 200)
        time.sleep(2)
        Screen().DIYSwipe_Percentage(0.5, 0.65, 0.5, 0.2, 200)
        time.sleep(2)
        Screen().DIYSwipe_Percentage(0.5, 0.65, 0.5, 0.2, 200)
        time.sleep(2)
        Screen().DIYSwipe_Percentage(0.5, 0.65, 0.5, 0.2, 200)
        time.sleep(2)
        Screen().DIYSwipe_Percentage(0.5, 0.65, 0.5, 0.2, 200)
        time.sleep(20)
        expValue = "POST"
        actValue = Sing().PostBtn().text
        time.sleep(2)
        # 判断跳转正确
        self.assertEqual(expValue, actValue)

    # 发布歌曲——发布完成跳转至首页
    def test_Case006_PostRecordCase(self):
        Sing().PostBtn().click()
        time.sleep(5)
        Sing().EditSend().click()
        time.sleep(2)
        Sing().ScoreDone().click()
        time.sleep(2)
        expValue = "true"
        # 获取首页Home-Tab按钮属性为选中状态
        actValue = Home().HomeTab_Home().get_attribute("selected")
        time.sleep(2)
        # 判断跳转正确
        self.assertEqual(expValue, actValue)
        time.sleep(2)

    # 现状不会实时更新
    # # 查看个人页Posts是否+1
    # def test_Case006_ProfilePostsCountCase(self):
    #     Home().HomeTab_Profile().click()
    #     time.sleep(2)
    #     Popup().HomePopup_VerifyEmail_Close_LiveClick()
    #     time.sleep(2)
    #     Screen().SWipeUp_Half()
    #     time.sleep(2)
    #     Profile().Profile_Tab_POSTS().click()
    #     time.sleep(2)
    #     Count = Profile().PostsCount().text
    #     PostsCount = ReadXMLData().returnXMLFile("ProfileText.xml", "ProfileText", "PostsCount")
    #     expValue = PostsCount
    #     # 提取当前作品数(判断两位数还是三位数)
    #     if Count[2].isdigit():
    #         actValue = Count[0:3]
    #     else:
    #         actValue = Count[0:2]
    #     time.sleep(2)
    #     # if expValue == actValue:
    #     #     Profile().PostsName_First().click()
    #     #     time.sleep(2)
    #     #     Profile().RepostBtn().click()
    #     #     Profile().ShareBtn().click()
    #     #     Screen().DIYSwipe_Percentage(0.9, 0.8, 0.1, 0.8, 500)
    #     #     Profile().CopyLink().click()
    #     #     self.driver.back()
    #     #     Home().HomeTab_Sing().click()
    #     #     Home().PostType_Sing().click()
    #     #     Library().Library_SearchBox().click()
    #     #     Action = TouchAction(self.driver)
    #     #     Action.long_press(Library().SearchPage_InputBox()).wait(2000).perform()
    #     #     Screen().AccurateClicks_Percentage(0.1736, 0.1953, 500)
    #     #     Link = Library().SearchPage_InputBox().text
    #     #     print(Link)
    #     # 判断作品数+1
    #     self.assertEqual(expValue, actValue)
