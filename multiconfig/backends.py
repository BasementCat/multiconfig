import json
import re

import yaml

exported_backends=[]

def register(extension, backend):
	global exported_backends
	exported_backends.append((extension, backend))

def getBackend(fname):
	global exported_backends
	for extension, backend in exported_backends:
		if re.search(r"\.%s$"%(extension,), fname):
			return backend
	return None

class MCBackend(object):
	@staticmethod
	def load(fname):
		raise NotImplementedError("load() must be overridden in a subclass")

	@staticmethod
	def set(key, value):
		raise NotImplementedError("The backend %s does not support set()"%(self.__class__.__name__,))

	@staticmethod
	def save(fname, reloadFile=True):
		raise NotImplementedError("The backend %s does not support save()"%(self.__class__.__name__,))

class YAML(MCBackend):
	@staticmethod
	def load(fname):
		with open(fname, "r") as fp:
			return yaml.load(fp)

class JSON(MCBackend):
	@staticmethod
	def load(fname):
		with open(fname, 'r') as fp:
			return json.load(fp)

register(r"ya?ml", YAML)
register(r"json", JSON)