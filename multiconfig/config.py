class MCBackend(object):
	def load(self, file):
		raise NotImplementedError("load() must be overridden in a subclass")

	def set(self, key, value):
		raise NotImplementedError("The backend %s does not support set()"%(self.__class__.__name__,))

	def save(self, file, reloadFile=True):
		raise NotImplementedError("The backend %s does not support save()"%(self.__class__.__name__,))

	def __init__(self):
		self.reset()

	def reset(self):
		self.configuration=list()

	def get(self, key, dfl=None, do_except=False):
		for conf_outer in self.configuration:
			conf=conf_outer
			for part in key.split("/"):
				if part in conf:
					conf=conf[part]
				else:
					conf=None
					break
		if conf is None:
			if do_except:
				raise KeyError("Configuration key not found: %s"%(key,))
			else:
				conf=dfl
		return conf

	@classmethod
	def _merged(self, *args):
		out=dict()
		def merge_dict(a, b):
			out=a.copy()
			for k,v in b.items():
				if k in out:
					if isinstance(v, dict):
						out[k]=merge_dict(out[k], v)
					else:
						out[k]=v
				else:
					out[k]=v
			return out
		for conf in args:
			out=merge_dict(out, conf)
		return out

config=None

def init(backend, *args):
	global config
	config=backend()
	for fname in args:
		config.load(fname)