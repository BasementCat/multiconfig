import yaml
from config import MCBackend

class yaml(MCBackend):
	def load(self, file):
		with open(file, "r") as fp:
			self.configuration.append(yaml.load(fp))