print(__name__)

# 超越那前方的背影
s2 = '光钻的执著', (
    ((1, {'wiz_incr': 10,
          'favor': 5,
          }),
     ),
    (('S', {'vital': 15,
            'stamina_incr': 10,
            'favor': 5,
            }),
     ('F', {'motivation': -1,
            'guts_incr': 20,
            }),
     ),
    ), 2

s3 = '唯独不能输给你', (
    ((1, {'vital': -20,
          'stamina_incr': 30,
          'favor': 5,
          'skill_hint': ('钢铁意志', 1),
          }),
     ),
    ((1, {'vital': 5,
          'guts_incr': 5,
          'favor': 5,
          'skill_hint': ('钢铁意志', 1),
          }),
     ),
    ), 1

# Kyoutsuu
k1 = '最喜欢困难事了！', (
    ((1, {'stamina_incr': 5,
          'guts_incr': 10,
          'favor': 5,
          }),
     ),
    ((1, {'favor': 5,
          'skill_hint': ('领跑踌躇', 1),
          }),
     ),
    ), 1

k2 = '最喜欢新事物了', (
    ((1, {'guts_incr': 10,
          'favor': 5,
          }),
     ),
    ((1, {'favor': 5,
          'vital': -10,
          'stamina_incr': 20,
          }),
     ),
    ), 2

__skill_hint: ('良场地', '晴天', '领跑焦躁', '中距离弯道', '束缚',
               '稍作休息', '观察能力',)
