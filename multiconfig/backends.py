import yaml
from config import MCBackend

class YAML(MCBackend):
	def load(self, file):
		with open(file, "r") as fp:
			self.configuration.append(yaml.load(fp))