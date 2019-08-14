var SVG = require('svg.min.js')
var fs = require('fs')

let info = process.argv.splice(2)
var T = info[0];	//自定义周期
var svgPath = info[1];	//由命令行(python)传入svg文件路径
var txtPath = info[2]
var deltat = 0.01;

function getPath()	//读取svg中的path数据
{
	let data = fs.readFileSync(svgPath,'utf-8')
	let begin = data.search('<g')
	let end = data.search('</g>') 
	data = data.slice(begin,end)
	
	begin = data.search('<path') + 9 //<path d="
	end = data.search('"/>')
	let path = data.slice(begin,end)
	path = path .replace('\r\n',' ')//不替换回车为空格svg无法解析
	return path
}


fs.writeFile(txtPath,'',function(){})//清空信息

var path = getPath()
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
	fs.writeFile(txtPath,content,{'flag':'a'},function(){})	//此处写入的文件应与python打开的文件相吻合
}







