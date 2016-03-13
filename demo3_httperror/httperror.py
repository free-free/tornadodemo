#-*- coding:utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options,define
define('port',default=8000,help='run on port',type=int)


class SetStatusHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_status(404)
		self.write("Hello")
	
class RewriteStatusHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_status(400)
		self.write("good")
	def write_error(self,status_code,**kw):
		self.write("%s BAD REQUEST"%status_code)
	

if __name__=='__main__':
	tornado.options.parse_command_line()
	app=tornado.web.Application(handlers=[(r'/status',SetStatusHandler),(r'/rewritestatus',RewriteStatusHandler)])
	httpsrv=tornado.httpserver.HTTPServer(app)
	httpsrv.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

		
