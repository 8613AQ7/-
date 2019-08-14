# Fourier  

https://www.bilibili.com/video/av62763042?from=search&seid=9940687363140161930  
http://www.jezzamon.com/fourier/index.html   
 
## 实现思路：  
* 用网站https://convertio.co/zh/jpg-svg/ 或软件 PS AI 获取svg （path）   
* js解析path为坐标随时间的变化 保存为txt    
* python读取并解析txt为ft   
* python计算傅里叶级数  
* python绘制gif并保存  
(6 删除本地ft数据)   
 

## 细节：  
* 用svgdom及其附属模块(node_modules)解决svg.js中window的问题 使其可以在node中运行      
* svg.js中增加import及export部分(虽然语法不是这样)    
* cmd命令依赖node执行svgToft.js 得到txt数据 
* fourier.py 集成上述操作    
* main.py 调用fourier.py 以命令行方式执行    

## 使用  
* 安装python(依赖numpy matplotlib 保存依赖pillow)  
```python  
pip install numpy matplotlib pillow   
```     
* 安装node.js(环境变量)  
* 获得含path的svg文件 
* 将.py .js node_modules文件夹 放至同一目录下(node_modules中为依赖文件 不可改名)      
* 打开cmd 输入 python main.py N T inputPath outputPath（不需要联网）    
N -- 箭头个数 越多越精确运行速度越慢   
T -- 周期 绘制轨迹的速度   
inputPath svg文件路径(.svg)  
outputPath 导出文件路径(.gif)     
```python  
python main.py data.svg animation.gif  
```       

## 问题：  
* png转换svg方法    
* python直接读取js中的ft(execjs)会因为require而出问题       解决：用os.system调用node.js    
* 如果无法调用外部包svg.js 无法解析svg数据      
* 用python手动解析svg数据  不会      
* 没空改md格式了 就这样看看吧=-=  