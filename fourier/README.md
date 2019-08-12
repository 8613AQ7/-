1 用网站https://convertio.co/zh/jpg-svg/或软件 PS AI 获取svg （path）   
2 js解析path为坐标随时间的变化 保存为txt    
3 python读取并解析txt为ft  
4 python计算傅里叶级数  
5 python绘制gif并保存  

问题：
1 png转换svg方法 其中必须满足图像是一笔画  
2 python直接读取js中的ft(execjs)会因为require而出问题  
3 如果无法调用外部包svg.js 无法解析svg数据  
4 用python手动解析svg数据  不会  