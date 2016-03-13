#-*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define,options
import uuid
define('port',default=8000,help='',type=int)

class ShopingCart(object):
	totalInventory=10
	callbacks=[]	
	carts={}
	def register(self,callback):
		self.callbacks.append(callback)
	def moveItemToCart(self,session):
		if session in self.carts:
			return 
		self.carts[session]=True
		self.notifyCallbacks()
	def removeItemFromCart(self,session):
		if session not in self.carts:
			return 	
		del(self.carts[session])
		self.notifyCallbbacks()
	def notifyCallbacks(self):
		for c in self.callbacks:
			self.callbackHelper(c)
		self.callbacks=[]
	def callbackHelper(self,callback):
		callback(self.getInventoryCount())
	def getInventoryCount(self):
		return self.totalInventory
class DetailHandler(tornado.web.RequestHandler):
	def get(self):
		session=uuid.uuid4()
		count=self.application.shoppingCart.getInventoryCount()
		self.render('index.html',session=session,count=count)
class CartHandler(tornado.web.RequestHandler):
	def post(self):
		action=self.get_argument('action')
		session=self.get_argument('session')
		if action=='add':
			self.application.shoppingCart.moveItemToCart(session)
		elif action=='remove':
			self.application.shoppingCart.removeItemFromCart(session)
		else:
			self.set_status(400)
class StatusHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.application.shoppingCart.register(self.on_message)
	def on_message(self,msg):
		self.write('{"inventoryCount":"%s"}'%msg)
		self.finish()
class Application(tornado.web.Application):
	def __init__(self):
		self.shoppingCart=ShoppingCart()
		handlers=[(r'/',DetailHandler),(r'/cart',CartHandler),(r'/cart/status',StatusHandler)]
		settings={
		'template_path':'templates',
		'static_path':'static'
		}
		super(Application,self).__init__(handlers=handlers,settings)
if __name__=='__main__':
	tornado.options.parse_command_line()
	httpsrv=tornado.httpserver.HTTPServer(Application)
	httpsrv.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
	
