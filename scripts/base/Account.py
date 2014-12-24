# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class Account(KBEngine.Proxy):
	"""
	账号实体
	客户端登陆到服务端后，服务端将自动创建这个实体，通过这个实体与客户端进行交互
	"""
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		self.activeCharacter = None
		
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onEntitiesEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("Account[%i]::onEntitiesEnabled:entities enable. mailbox:%s, clientType(%i), hasAvatar=%s, accountName=%s" % \
			(self.id, self.client, self.getClientType(), self.activeCharacter, self.__ACCOUNT_NAME__))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG("Account[%i]::onLogOnAttempt: ip=%s, port=%i, selfclient=%s" % (self.id, ip, port, self.client))
		"""
		if self.activeCharacter != None:
			return KBEngine.LOG_ON_REJECT

		if ip == self.lastClientIpAddr and password == self.password:
			return KBEngine.LOG_ON_ACCEPT
		else:
			return KBEngine.LOG_ON_REJECT
		"""
		
		# 如果一个在线的账号被一个客户端登陆并且onLogOnAttempt返回允许
		# 那么会踢掉之前的客户端连接
		# 那么此时self.activeCharacter可能不为None， 常规的流程是销毁这个角色等新客户端上来重新选择角色进入
		if self.activeCharacter:
			self.activeCharacter.giveClientTo(self)
			self.relogin = time.time()
			self.activeCharacter.destroySelf()
			self.activeCharacter = None
			
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		if self.activeCharacter:
			self.activeCharacter.accountEntity = None
			self.activeCharacter = None

		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()
				
	

			

		