from cdocs.simple_config import SimpleConfig
import logging
from typing import Any,Optional

class BdocsConfig(SimpleConfig):

    def add_to_config(self, section, key, value:Optional[Any]=None, concat:str=',') -> None:
        """ adding None removes key """
        print(f"BdocsConfig.add_to_config: section: {section}, key: {key}, value: {value}, concat: {concat}")
        if value is None:
            self.remove_from_config(section, key)
        else:
            t = type(value).__name__
            print(f"BdocsConfig.add_to_config: type t: {t}")
            if t == "list":
                value = concat.join(value)
                print(f"BdocsConfig.add_to_config: joined {t} to make: {value}")
            self.just_add_to_config(section, key, value)
        self.save_config()

    def just_add_to_config(self, section, key, value) -> None:
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        self._parser.set(section, key, value)
        self.save_config()

    def save_config(self) -> None:
        with open(self.get_config_path(), 'w') as f:
            self._parser.write(f)

    def remove_from_config(self, section, key=None) -> None:
        if key is not None:
            self._parser.remove_option(section, key)
        else:
            self._parser.remove_section(section)
        self.save_config()



