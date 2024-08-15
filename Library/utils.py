#/usr/bin/python

# General util specific to common purpose
import yaml
class YAML:
  @staicmethod
  def yaml_to_dict(filepath: str) -> dict:
    with(filepath, "r") as fileobj:
      data = yaml.safe_load(fileobj)
    return data
  @staticmethod
  def write_data_to_yaml():
    pass

class DateTime:
  def __init__(self):
    pass
  def getCurrentTime(self):
    pass


