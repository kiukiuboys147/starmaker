﻿环境准备
====
1.  安装git环境，拉取最新代码。
2.  安装AirtestIDE，使用AirtestIDE打开待测脚本（后缀为".air"的文件夹）。例如验证首页浏览性能，则打开`AirtestCase/case/性能测试/首页浏览.air`

脚本执行
====
1.  测试数据设置：代码的开头中文标注有"脚本执行次数、单次脚本执行时间"等变量可供修改；建议值为脚本执行5次以上、单次运行超过600s
2.  代码微调：修改setUp——代码中setUp作为启动app后，执行最短路径到待测页面，因不同的包元素ID不一致（逻辑混淆），需要使用AirtestIDE调整setUp中元素ID`Poco辅助窗，选择Android即可查看元素ID`
3.  测试前准备：手机电量大于75%且处于充电中；手机已安装待测app且未启动过；
4.  执行并收集数据分析
    * 单次数据取最大峰值
    * 5次数据去除最高与最低(如有明显异常数据则补充数据量≥3)后计算平均值

Help
====
* 性能测试方法：参见`T37163`
* 帮助文档：参见`AirtestCase/Help.air`
* 测试结果：参见`AirtestCase/test_data/Jalebee1.4.0测试数据.zip`

