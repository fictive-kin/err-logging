# -*- coding: utf-8 -*-

import logging

from errbot import BotPlugin, botcmd

class Logging(BotPlugin):

    def __init__(self, *args, **kwargs):
        super(Logging, self).__init__(*args, **kwargs)
        self._loggers = {
            self.log.name: self.log
        }


    def _set_levels(self, level):
        for logger in self._loggers.values():
            logger.setLevel(level)


    def _add_logger(self, name):
        if name in self._loggers:
            return

        self._loggers.update({name: logging.getLogger(name)})


    @botcmd
    def logging_reset(self, message, args):
        """Resets the controlled loggers to defaults"""
        self._loggers = {
            self.log.name: self.log
        }
        return 'Controlled loggers reset'


    @botcmd
    def logging_rm(self, message, args):
        """Stop controlling the named logger"""
        if len(args) > 0:
            if args in self._loggers:
                self._loggers.pop(args)
                return 'Stopped controlling logger: {}'.format(args)

            return 'Nothing to do. Logger was not being controlled: {}'.format(args)

        return 'You must specify a logger name to stop controlling'


    @botcmd
    def logging_add(self, message, args):
        """Add a logger by name to the list of controlled loggers"""
        if len(args) > 0:
            self._add_logger(args)
            return 'Now controlling logger: {}'.format(args)

        return 'You must specify a logger to control'


    @botcmd
    def logging_list(self, message, args):
        """List loggers controlled by this plugin"""
        for name in sorted(self._loggers.keys()):
            yield name


    @botcmd
    def logging_get(self, message, args):
        """Return current logging level"""
        return logging.getLevelName(self.log.getEffectiveLevel())


    @botcmd
    def logging_set(self, message, args):
        """Set the logging level"""
        if len(args) > 0:
            self._set_levels(logging.getLevelName(args))
            return 'Set logging level to: {}'.format(args)

        return 'You must specify a level to set the logging to'
