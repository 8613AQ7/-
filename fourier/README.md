# Fourier  

https://www.bilibili.com/video/av62763042?from=search&seid=9940687363140161930  
http://www.jezzamon.com/fourier/index.html   
 
## 实现思路：  
* 获取svg （path）     
* js解析path为坐标随时间的变化 保存为txt      
* python读取并解析txt为ft     
* python计算傅里叶级数    
* python绘制gif并保存       
 

## 细节：  
* 用svgdom及其附属模块(node_modules)解决svg.js中window的问题 使其可以在node中运行        
* svg.js中增加对window的定义及exports部分         
* 用python的os.system执行cmd命令依赖node执行svgToft.js 得到txt数据 
* fourier.py 进行调用、读取、计算     
* 命令行方式执行main.py 传入参数 调用fourier.py 得到返回的动画对象 保存       

## 使用  
* 安装python(依赖numpy matplotlib 保存依赖pillow)  
```python  
pip install numpy matplotlib pillow   
```     
* 安装node.js(环境变量)  
* 用网站https://convertio.co/zh/jpg-svg/ 或软件 PS AI 获得含path的svg文件 
* 将.py .js node_modules文件夹 放至同一目录下        
* 打开cmd 输入 python main.py N T inputPath outputPath（不需要联网）      
N -- 箭头个数 越多越精确运行速度越慢     
T -- 周期 绘制轨迹的速度     
inputPath svg文件路径(.svg)   
outputPath 导出文件路径(.gif)        
```python  
python main.py data.svg animation.gif  
```       

## 问题：  
* png/jpg等转换svg方法  ai有些复杂=-=   
* python直接读取js中的ft(execjs)会因为require而出问题 解决：用os.system调用node.js      
* 如果无法调用外部包svg.js 无法解析svg数据 解决：无奈破坏别人写好的代码=-=       
* 用python手动解析svg数据  不会  
* svg中含有多个path     

##可行改进
* tqdm增加进度条
* js处理所有path
* 用python图形处理提取图像轮廓 提交给网站获取svg 一条龙