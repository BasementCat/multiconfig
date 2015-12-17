import os

import backends

configs=dict()

class ConfigurationError(Exception):
	pass

class Config(object):
	def __init__(self, *args):
		self.configuration=None
		self.reset()
		for fname in args:
			self.load(fname)

	def reset(self):
		self.configuration=dict()

	def load(self, fname):
		backend=backends.getBackend(fname)
		if not backend:
			raise ConfigurationError("Unsupported filetype: *.%s"%(fname.split(".").pop(),))
		new_config=backend.load(fname)
		self.configuration=self._merged(self.configuration, new_config)

	def loadMany(self, candidate_directories=None, candidate_filenames=None, candidate_extensions=None, candidate_files=None):
		loaded_files = 0
		test_files = (candidate_files or [])[:]
		for directory in candidate_directories or []:
			for filename in candidate_filenames or []:
				if candidate_extensions:
					for extension in candidate_extensions:
						test_files.append(os.path.join(directory, filename + '.' + extension))
				else:
					test_files.append(os.path.join(directory, filename))

		for fname in test_files:
			if os.path.exists(fname) and os.path.isfile(fname):
				self.load(fname)
				loaded_files += 1

		if loaded_files == 0:
			raise ConfigurationError("Loaded 0/{} candidate files".format(len(test_files)), test_files)

	def get(self, key, default=None, do_except=False):
		conf=self.configuration
		for part in key.split("/"):
			if conf and part in conf:
				conf=conf[part]
			else:
				conf=None
				break
		if conf is None:
			if do_except:
				raise KeyError("Configuration key not found: %s"%(key,))
			else:
				conf=default
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

def getConfig(name):
	global configs
	if name not in configs:
		configs[name]=Config()
	return configs[name]