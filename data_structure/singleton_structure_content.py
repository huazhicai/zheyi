# -*- coding:utf-8 -*-

global_config = None
global_meta = None

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def set_config(config):
    global global_config
    assert global_config is None
    global_config = config


def set_config_path(config_path):
    import json
    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)
        set_config(config)


def new_content():
    global global_meta, global_config
    if global_config is None:
        import os
        set_config_path(os.path.join(os.path.dirname(__file__), 'config/hemo_dialysis_data.json'))
    if global_meta is None:
        from data_structure.meta_info import TreeMetaInfo
        meta = TreeMetaInfo()
        meta.init(global_config)
        global_meta = meta
    from data_structure.data_tree import DataTree
    return DataTree(global_meta)


if __name__ == '__main__':
    import pprint

    data = [{
        'zhuyuan': [{
            30101: '张三',
            30102: '时间1',
            30131: '出院时间1',
            'chrujilu': [{
                30181: '主要',
                30134: '受伤'
            }, {
                30181: '次要',
                30134: '生病'
            }
            ],
            'ssjl': [{
                30145: 'A',
                30146: 'B'
            }]
        }, {
            30101: '张三',
            30102: '时间2',
            'chrujilu': [{
                30181: '主要'
            }, {
                30181: '次要'
            }
            ],
            'ssjl': [{
                30145: 'A',
                30146: 'B'
            }]
        }
        ]
    },
        {
            'zhuyuan': [{
                30101: '张三',
                30102: '时间3',
                'chrujilu': [{
                    30181: '主要'
                }, {
                    30181: '次要'
                }
                ],
                'ssjl': [{
                    30145: 'A',
                    30146: 'B'
                }]
            }, {
                30101: '张三',
                30102: '时间4',
                'chrujilu': [{
                    30181: '主要'
                }, {
                    30181: '次要'
                }
                ],
                'ssjl': [{
                    30145: 'A',
                    30146: 'B'
                }]
            }
            ]
        }
    ]
    content = new_content()

    content.push_group(data)
    # group1 = content.new_group()
    # content.push_source(20001, 'A', [group1])
    # content.push_source(20002, 'A', [group1])
    # content.push_source(20003, 'A', [group1])
    # group2 = content.new_group()
    # content.push_source(20005, 'A', [group1, group2])
    # content.push_source(20006, 'A', [group1, group2])
    # group3 = content.new_group()
    # content.push_source(20005, 'A', [group1, group3])
    # content.push_source(20006, 'A', [group1, group3])
    #
    # content.push_source(20007, 'A', [group1])
    #
    # group4 = content.new_group()
    # content.push_source(20001, 'A', [group4])
    # content.push_source(20002, 'A', [group4])
    # content.push_source(20003, 'A', [group4])
    # group5 = content.new_group()
    # content.push_source(20005, 'A', [group4, group5])
    # content.push_source(20006, 'A', [group4, group5])
    # group6 = content.new_group()
    # content.push_source(20005, 'A', [group4, group6])
    # content.push_source(20006, 'A', [group4, group6])
    #
    # content.push_source(20007, 'A', [group4])

    pprint.pprint(content.export())
