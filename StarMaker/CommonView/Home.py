# coding=utf-8
# ----------
# 首页
# ----------
from Utils.FindElement import find_element
from CommonView.VData import Home_VD


# 首页
class Home(object):
    def __init__(self):
        self.findID = find_element().ID
        self.findIDS = find_element().IDS
        self.findCla = find_element().Cla
        self.findClaS = find_element().ClaS
        self.findXpa = find_element().Xpa
        self.findAID = find_element().AID
        self.findAU = find_element().AU

    # ----------
    # 登陆后首页引导弹窗
    # ----------

    # 首页 New Feature 引导——Tips
    def HomePage_NewFeature_Tips(self):
        HomePage_NewFeature_Tips_AU = self.findAU(Home_VD.HomePage_NewFeature_AU)
        return HomePage_NewFeature_Tips_AU
    #
    # # 首页 New Feature 引导——Tips
    # def HomePage_NewFeature_Tips(self):
    #     HomePage_NewFeature_Tips_Class = self.findClaS(Home_VD.HomePage_NewFeature_Class, 1)
    #     return HomePage_NewFeature_Tips_Class
    #
    # # 首页 New Feature 引导——OK按钮
    # def HomePage_NewFeature_OK(self):
    #     HomePage_NewFeature_OK_Class = self.findClaS(Home_VD.HomePage_NewFeature_Class, 2)
    #     return HomePage_NewFeature_OK_Class
    #
    # # 首页 Ranking 引导（text="Ranking and Hashtag are moved here"）
    # def HomePage_Guide(self):
    #     HomePage_Guide_ID = self.findID(Home_VD.HomePage_Guide_ID)
    #     return HomePage_Guide_ID

    # ----------
    # 首页五Tab
    # ----------

    # 首页 Home-Tab
    def HomeTab_Home(self):
        HomeTab_Home_Class = self.findClaS(Home_VD.Home_Tab_ClaS, 0)
        return HomeTab_Home_Class

    # 首页 互娱大厅-Tab
    def HomeTab_KTV_Live(self):
        HomeTab_KTV_Live_Class = self.findClaS(Home_VD.Home_Tab_ClaS, 1)
        return HomeTab_KTV_Live_Class

    # 首页 点唱-Tab
    def HomeTab_Sing(self):
        HomeTab_Sing_Class = self.findClaS(Home_VD.Home_Tab_ClaS, 2)
        return HomeTab_Sing_Class

    # 首页 消息-Tab
    def HomeTab_Notification(self):
        HomeTab_Notification_Class = self.findClaS(Home_VD.Home_Tab_ClaS, 3)
        return HomeTab_Notification_Class

    # 首页 个人页-Tab
    def HomeTab_Profile(self):
        HomeTab_Profile_Class = self.findClaS(Home_VD.Home_Tab_ClaS, 4)
        return HomeTab_Profile_Class

    # ----------
    # 选择发布类型
    # ----------

    # 选择发布类型([0]Album/[1]Camera/[2]Text/[3]Sing/[4]关闭)
    def PostType_Album(self):
        PostType_ClaS = self.findClaS(Home_VD.PostType_ClaS, 0)
        return PostType_ClaS

    def PostType_Camera(self):
        PostType_ClaS = self.findClaS(Home_VD.PostType_ClaS, 1)
        return PostType_ClaS

    def PostType_Text(self):
        PostType_ClaS = self.findClaS(Home_VD.PostType_ClaS, 2)
        return PostType_ClaS

    def PostType_Sing(self):
        PostType_ClaS = self.findClaS(Home_VD.PostType_ClaS, 3)
        return PostType_ClaS

    def PostType_Close(self):
        PostType_ClaS = self.findClaS(Home_VD.PostType_ClaS, 4)
        return PostType_ClaS
