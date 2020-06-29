from cdocs.simple_config import SimpleConfig
import logging

class BdocsConfig(SimpleConfig):

    def add_to_config(self, section, key, value) -> None:
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
        #with open(self.get_config_path(), 'w') as f:
        #    self._parser.write(f)


