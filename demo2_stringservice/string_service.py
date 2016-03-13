#-*- coding:utf-8 -*-


import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options,define
import textwrap
define('port',default=8000,help='run on port',type=int)

class ReverseHandler(tornado.web.RequestHandler):
	def get(self,input):
		self.write(input[::-1])
class WrapHandler(tornado.web.RequestHandler):
	def post(self):
		text=self.get_argument('text')
		width=self.get_argument('width')
		self.write(textwrap.fill(text,int(width)))
	
if __name__=='__main__':
	tornado.options.parse_command_line()
	app=tornado.web.Application(handlers=[(r'/reverse/(\w+)',ReverseHandler),(r'/wrap',WrapHandler)])
	httpserver=tornado.httpserver.HTTPServer(app)
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

		
