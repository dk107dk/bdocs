from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict
from cdocs.cdocs import Cdocs
from cdocs.contextual_docs import ContextualDocs
from cdocs.context_metadata import ContextMetadata
from bdocs.bdocs import Bdocs
from bdocs.block import Block
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs_config import BdocsConfig
from bdocs.rules.rule import Rule
from bdocs.rules.rule_types import RuleTypes
import os
import shutil
import logging
import json
import datetime
import time
from typing import List, Optional, Dict

#
# use Rules to wrap a cdocs that supports rules so that
# any get_doc(path) that matches the docpath in the rules
# cdocs is rule checked before the path is requested in
# the wrapped cdocs.  the rules cdocs is a root with the
# name .myname_rules where myname is the name of the
# wrapped cdocs. note that roots with names beginning
# with '.' are considered system roots that are basically
# hidden roots.
#
# also TBD is what happens if you try to create rules for
# a root that doesn't accept cdocs. a non-cdocs docpath
# probably won't work, but it is untested atm.
#
class Rules(ContextualDocs):

    def __init__(self, cdocs:Cdocs):
        self._cdocs = cdocs
        self._check_rules_root()
        self._rdocs = None

    @property
    def cdocs(self):
        return self._cdocs

    @cdocs.setter
    def cdocs(self, m):
        self._cdocs = m

# ----------------------------
# contextual docs. only get_doc
# is rule checked at this time.
# ----------------------------

    def get_doc(self, path:DocPath):
        if path is None:
            return None
        rule = self.get_rule(path)
        if rule is not None:
            return rule.get_doc(path)
        return self.cdocs.get_doc(path)

    def get_concat_doc(self, path:DocPath) -> Optional[Doc]:
        return self.cdocs.get_concat_doc(path)

    def get_compose_doc(self, path:DocPath) -> Optional[Doc]:
        return self.cdocs.get_compose_doc(path)

    def get_labels(self, path:DocPath, recurse:Optional[bool]=True, addlabels:Optional[bool]=True) -> Optional[JsonDict]:
        return self.cdocs.get_labels(path, recurse, addlabels)

    def get_tokens(self, path:DocPath, recurse:Optional[bool]=True) -> JsonDict:
        return self.cdocs.get_tokens(path, recurse)

    def list_docs(self, path:DocPath) -> List[Doc]:
        return self.cdocs.list_docs(path)

    def list_next_layer(self, path: DocPath) -> List[Doc]:
        return self.cdocs.list_next_layer(path)

# ----------------------------

    def _check_rules_root(self) -> None:
        logging.info(f"Rules._check_rules_root: checking {self} for {self.get_rules_root()}")
        exists = os.path.exists(self.get_rules_root())
        logging.info(f"Rules._check_rules_root: exists: {exists}")
        if not exists:
            logging.info(f"Rules._check_rules_root: creating {self.get_rules_root()}")
            os.mkdir(self.get_rules_root())
        cpath = self.cdocs.config.get_config_path()
        logging.info(f"Rules._check_rules_root: cpath: {cpath}")
        config = BdocsConfig(cpath)
        #
        # may need to reload cdocs.config so do that here
        #
        self.cdocs.config = config
        rootname = f".{self.cdocs.rootname}_rules"
        logging.info(f"Rules._check_rules_root: checking config for rootname: {rootname}, docroot: {self.cdocs.get_doc_root()}")
        rootpath = config.get("docs", rootname)
        if rootpath is None:
            logging.info(f"Rules._check_rules_root: adding {rootname} to config")
            config.add_to_config(
                    "docs",
                    rootname,
                    self.get_rules_root()
            )
            config.add_to_config("formats", rootname, "rule")
        else:
            logging.info(f"Rules._check_rules_root: not adding {rootname} to config because already there: {rootpath}")


    def get_rules_root(self) -> FilePath:
        logging.info(f"Rules.get_rules_root. called")
        root = self.cdocs.config.get("locations", "docs_dir")
        (base,_) = os.path.split(root)
        rootname = self.cdocs.rootname
        return os.path.join(root, f'.{rootname}_rules')

    def delete_rules_root(self) -> None:
        root = self.get_rules_root()
        shutil.rmtree(root)

    def new_rule(self):
        rule = Rule(self)
        rule.in_root = self.cdocs.rootname
        return rule

    @property
    def rules_cdocs(self):
        if self._rdocs is None:
            #
            # metadata = BuildingMetadata(config)
            # rootinfo = metadata.get_root_info(rootname)
            # return rootinfo.rules
            #
            logging.info(f"Rules.rules_cdocs: rules root: {self.get_rules_root()}, config: {self.cdocs.config.get_config_path()}")
            self._check_rules_root()
            #logging.info(f"Rules.rules_cdocs: rulesroot: {self.get_rules_root()}, config: {self.cdocs.config.get_config_path()}")
            for r in self.cdocs.config.get_items("docs"):
                pass
                #logging.info(f"Rules.rules_cdocs: found a root: {r}")
            self._rdocs = Cdocs(self.get_rules_root(), self.cdocs.config)
        return self._rdocs

    def get_rule(self, path:DocPath):
        rdocs = self.rules_cdocs
        doc = rdocs.get_doc(path)
        if doc is None:
            return None
        return self.deserialize_rule(doc, path)

    def list_rules(self) -> List[str]:
        bdocs = self._get_rule_bdocs()
        metadata = BuildingMetadata(bdocs.config)
        building = Block(metadata)
        logging.info(f"\nRules.list_rules: root_name: {bdocs.root_name}")
        rules = building.list_trees([bdocs.root_name])
        for r in rules:
            logging.info(f"Rules.list_rules: a rule: {r}")
        return rules

    def delete_rule(self, rule:Rule):
        logging.info(f"Rules.delete_rule: rule: {rule}")
        bdocs = self._get_rule_bdocs()
        return bdocs.delete_doc(rule.docpath)

    def delete_rule_path(self, path:DocPath):
        bdocs = self._get_rule_bdocs()
        return bdocs.delete_doc(path)

    def put_rule(self, rule:Rule) -> None:
        if rule.docpath is None:
            raise RuleException(f"Rules.serialize_rule: rule must have a docpath: {rule}")
        rules = self.serialize_rule(rule)
        bdocs = self._get_rule_bdocs()
        bdocs.put_doc(rule.docpath, rules)

    def _get_rule_bdocs(self) -> Bdocs:
        root = self.rules_cdocs.get_doc_root()
        logging.info(f"Rules._get_rule_bdocs: root: {root}")
        cfgpath = self.rules_cdocs.config.get_config_path()
        bdocs = Bdocs(root, BuildingMetadata(BdocsConfig(cfgpath)) )
        return bdocs

    def serialize_rule(self, rule:Rule) -> str:
        return rule.to_string()

    def deserialize_rule(self, doc:str, path:str) -> Rule:
        logging.info(f"Rules.deserialize_rule: doc: {doc}, path: {path}")
        if doc is None:
            return doc
        rule = json.loads(doc)
        return self.rule_from_json(rule)

    def rule_from_json(self, rule:Dict) -> Rule:
        print(f"rule_from_json: rule: {rule}")
        so = rule.get('start_at')
        if so:
            rule['start_at'] = self.get_date(so)
        else:
            rule['start_at'] = None
        to = rule.get('to')
        if to:
            rule['to'] = self.get_date(to)
        else:
            rule['to'] = None
        rule['rootname'] = self.cdocs.rootname
        rule['paths'] = rule.get('paths')
        #
        # if we have an action
        #
        a = rule.get('action')
        if a:
            rule['action'] = RuleTypes.get_type(a)
        r = Rule(self, rule)
        return r

    def get_date(self, dates) :
        f = '%Y-%m-%d'
        if dates.find('T') > -1:
            f += 'T%H:%M:%S'
        logging.info(f"Rules.get_date: f: {f}, dates: {dates}")
        r = datetime.datetime.strptime(dates, f)
        return r

    def has_rule(self, path:DocPath):
        return self.get_rule(path) is not None


