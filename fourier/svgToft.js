var SVG = require('svg.min.js')
var fs = require('fs')

var dataPath = process.argv.splice(2)[0];	//由命令行(python)传入svg文件路径

var T = 4;		//自定义参数
var deltat = 0.01;
var info = String(T) + ' ' + String(deltat) + '\r\n';	//记录信息顺便清空
fs.writeFile('ft.txt',info,function(){})

function readData()	//读取svg中的path数据
{
	let data = fs.readFileSync(dataPath,'utf-8')
	let begin = data.search('<g')
	let end = data.search('</g>') 
	data = data.slice(begin,end)
	
	begin = data.search('<path') + 9 //<path d="
	end = data.search('"/>')
	let path = data.slice(begin,end)
	path = path .replace('\r\n',' ')//不替换回车为空格svg无法解析
	return path
}
var path = readData()

var pic = SVG.SVG().path(path);
var len = pic.length();

function f(t)
{
	let index = len * t / T;
	let loc = pic.pointAt(index);	//这个函数是关键 自动解析path信息
	return loc
}

for (let i = 0;i<T ;i += deltat)
{
	let loc = f(i)
	let content = String(loc.x)+' '+String(loc.y)+'\r\n'
	fs.writeFile('ft.txt',content,{'flag':'a'},function(){})	//此处写入的文件应与python打开的文件相吻合
}



