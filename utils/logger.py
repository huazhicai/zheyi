# -*- coding: utf-8 -*-
import logging
import logging.config

# global logging manager
# 1MB=1024*1024Bit

"""
logging.basicConfig(format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
                    filename='log/pop.log',
                    level=logging.DEBUG,
                    filemode='w')
"""

output_list = ['file', 'console']

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            # 'format': '%(levelname)s %(message)s'
            'format': '[%(name)s:%(lineno)s] %(levelname)s  %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': logging.DEBUG,
            # 如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失, some problem
            # 'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            # 当达到10MB时分割日志
            'maxBytes': 1024 * 1024 * 10,
            # 最多保留30份文件
            'backupCount': 30,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            'filename': './log/log.txt',
            'formatter': 'verbose'
        },

        'console': {
            'level': logging.DEBUG,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            # 'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        # 不写名字，默认所有日志记录器
        '': {
            'handlers': ['console', 'file'],
            'level': logging.INFO
        },
    }
})


def getLogger(module_name):
    return logging.getLogger(module_name)
