from cdocs.contextual_docs import DocPath
from bdocs.rules.rule_types import RuleTypes
import os
import shutil
import logging
import datetime
import random
from typing import Tuple, List, Optional, Dict

class Rule(object):
    """
    rules are about time. there are five rules:
      > make available at a datetime or periodically
      > make unavailable at a datetime or periodically
      > delete at the unavailable datetime
      > replace with content from another docpath at the unavailable datetime or periodically
      > swap content with another docpath at the unavailable datetime or periodiacally

    many of the methods in this class are fluent
    """

    def __init__(self, rules, rule:Optional[Dict]={}):
        self._rules = rules
        self._cdocs = rules.cdocs
        self._has_rule = True
        self._triggered = rule.get('triggered')
        self._rootname = rule.get('rootname')
        self._docpath = rule.get('docpath')
        self._start_at = rule.get('start_at')
        self._to = rule.get('to')
        self._action = rule.get('action')
        self._paths:Tuple[str:DocPath] = rule.get('paths')

    #-----------------------
    def to_string(self):
        return self.__str__()

    def __str__(self):
        string = '{ '
        string = f'{string}"docpath":"{self.docpath}"\n   '
        string = f'{string}, "in_root":"{self.in_root}"\n   '
        if self.action:
            string = f'{string}, "action":"{self.action.value}"\n   '
        if self._triggered is not None:
            string = f'{string}, "triggered":"{self._triggered}"\n   '
        if self._start_at is not None:
            string = f'{string}, "start_at":"{self._start_at.strftime("%Y-%m-%dT%H:%M:%S")}"\n   '
        if self._to is not None:
            string = f'{string}, "to":"{self._to.strftime("%Y-%m-%dT%H:%M:%S")}"\n   '
        if self._paths and len(self._paths) > 0:
            string = f'{string}, "paths":['
            for i, path in enumerate(self._paths):
                string = f'{string}"{path}"'
                if i < len(self._paths) -1:
                    string += ','
            string = f'{string}]\n   '
        string = f'{string}' + '}'
        return string

    #-----------------------

    def has_started(self):
        if self.start_at is None:
            return True
        now = datetime.datetime.now()
        if self.start_at < now:
            return True
        return False

    def has_ended(self):
        if self.to is None:
            return False
        now = datetime.datetime.now()
        if self.to < now:
            return True
        return False

    def has_not_ended(self):
        return not self.has_ended()

    def is_happening(self):
        return self.has_started() and self.has_not_ended()

    def may_be_available(self):
        #print(f"rule.may_be_available: happening: {self.is_happening()} makes_available: {self.makes_available()}")
        if self.is_happening() and self.makes_available():
            return True
        return False

    def makes_available(self):
        return self.action == RuleTypes.AVAILABLE_DURING or \
               self.action == RuleTypes.REPLACE_AFTER or \
               self.action == RuleTypes.REPLACE_UNTIL or \
               self.action == RuleTypes.RANDOM_AFTER or \
               self.action == RuleTypes.RANDOM_UNTIL

    def has_been_triggered(self):
        return self.triggered

    def has_path(self):
        return self.paths is not None and len(self.paths) > 0

    def random_path(self):
        if not self.has_path():
            return None
        r = random.randint(0,len(self.paths)-1)
        return self.paths[r]


    #-----------------------
    #   _AFTER starts with self.has_started()
    #   _UNTIL starts with self.has_started() continues while self.is_happening()
    #-----------------------

    def get_doc(self):
        if self.action == RuleTypes.REPLACE_AFTER and not self.has_started():
            logging.info("rule.get_doc: replace after not started")
            return self._cdocs.get_doc(self.docpath)
        elif self.action == RuleTypes.REPLACE_AFTER and self.has_started() and self.has_path():
            logging.info("rule.get_doc: replace after started and path")
            return self._cdocs.get_doc(self.paths[0])
        elif self.action == RuleTypes.REPLACE_UNTIL and self.has_ended():
            logging.info("rule.get_doc: replace until and ended")
            return self._cdocs.get_doc(self.docpath)
        elif self.action == RuleTypes.REPLACE_UNTIL and self.is_happening() and self.has_path():
            logging.info("rule.get_doc: replace until is happening has path")
            return self._cdocs.get_doc(self.paths[0])
        elif self.action == RuleTypes.AVAILABLE_DURING and self.is_happening():
            logging.info(f"rule.get_doc: available during and happening: {self.docpath}")
            return self._cdocs.get_doc(self.docpath)
        elif self.action == RuleTypes.UNAVAILABLE_BEFORE and self.has_started():
            logging.info("rule.get_doc: unavailable and started")
            return self._cdocs.get_doc(self.docpath)
        elif self.action == RuleTypes.UNAVAILABLE_DURING and self.is_happening():
            logging.info("rule.get_doc: unavailable during and happening")
            return None
        elif self.action == RuleTypes.UNAVAILABLE_AFTER and self.has_started():
            logging.info("rule.get_doc: unavailable after and started")
            return None
        elif self.action == RuleTypes.RANDOM_UNTIL and self.is_happening() and self.has_path():
            logging.info("rule.get_doc: random until and happening and have path")
            return self._cdocs.get_doc(self.random_path())
        elif self.action == RuleTypes.RANDOM_AFTER and self.has_started() and self.has_path():
            logging.info("rule.get_doc: random after started and have path")
            return self._cdocs.get_doc(self.random_path())
        elif not self.may_be_available():
            logging.info("rule.get_doc: not available")
            return None
        else:
            print(f"Rule.get_doc: no match applied. cannot get a doc for: {self}")
        return None

    #-----------------------
    #-----------------------

    @property
    def triggered(self):
        return self._triggered

    @triggered.setter
    def triggered(self, t):
        self._triggered = t

    @property
    def docpath(self):
        return self._docpath

    @docpath.setter
    def docpath(self, docpath:DocPath):
        self._docpath = docpath
        return self


    @property
    def cdocs(self):
        return self._cdocs

    @cdocs.setter
    def cdocs(self, cdocs): #:Cdocs
        self._cdocs = cdocs
        return self


    @property
    def in_root(self):
        return self._rootname

    @in_root.setter
    def in_root(self, rootname:str):
        self._rootname = rootname
        return self

    @property
    def start_at(self):
        return self._start_at

    @start_at.setter
    def start_at(self, start:datetime) :
        self._start_at = start
        return self

    def has_start_at(self):
        return self.start_at is not None

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, stop:datetime):
        self._to = stop
        return self

    def has_to(self):
        return self.to is not None

    @property
    def action(self) -> RuleTypes:
        return self._action

    @action.setter
    def action(self, atype:RuleTypes):
        if not isinstance(atype, RuleTypes):
            raise Exception(f"cannot set {atype.__class__} as an action's RuleTypes")
        self._action = atype
        return self

    @property
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, paths:List[DocPath]):
        self._paths = paths
        return self


