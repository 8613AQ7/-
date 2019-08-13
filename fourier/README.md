实现思路：  
1 用网站https://convertio.co/zh/jpg-svg/ 或软件 PS AI 获取svg （path）   
2 js解析path为坐标随时间的变化 保存为txt    
3 python读取并解析txt为ft   
4 python计算傅里叶级数  
5 python绘制gif并保存  
(6 删除本地ft数据)   
 
使用：  
1 安装python(依赖numpy matplotlib)  
2 安装node.js(环境变量)  
3 获得含path的svg文件 命名为data.svg 
4 将.py .js .svg node_modules文件夹 放至同一目录下(node_modules中为依赖文件 不可改名)      
5 打开cmd 输入 python main.py N command（不需要联网）  
其中N为箭头个数 太大速度慢 太小无法绘出复杂的图像 建议符号类(简单)60 图像类(复杂)300 由用户自行调整    
command为play或save 即在本地播放或保存为当前目录下的'animation.gif'        

问题：  
1 png转换svg方法    
2 python直接读取js中的ft(execjs)会因为require而出问题       解决：用os.system调用node.js    
3 如果无法调用外部包svg.js 无法解析svg数据      
4 用python手动解析svg数据  不会      
5 没空改md格式了 就这样看看吧=-=  