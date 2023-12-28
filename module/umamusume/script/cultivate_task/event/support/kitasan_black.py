print(__name__)

# 身后迫近的热浪是动力
s2 = '好心总会有好报', (
    ((1, {'vital': 10,
          'motivation': 1,
          'favor': 5,
          }),
     ),
    (('S', {'speed_incr': 10,
            'favor': 5,
            'skill_hint': ('直线能手', 3),
            }),
     ('F', {'speed_incr': 5,
            'favor': 5,
            'skill_hint': ('直线能手', 1),
            }),
     ),
    ), 1

# Kyoutsuu
k1 = '啊，故乡', (
    ((1, {'speed_incr': 5,
          'power_incr': 10,
          'favor': 5,
          }),
     ),
    ((1, {'favor': 5,
          'condition': 'renshuujouzu_maru',
          }),
     ),
    ), 1

k2 = '啊，友情', (
    ((1, {'motivation': 1,
          'power_incr': 5,
          'favor': 5,
          }),
     ),
    ((1, {'favor': 5,
          'vital': 10,
          }),
     ),
    ), 1

__skill_hint: ('弯道能手', '弯道恢复', '直线恢复', '专注力', '大胃储备',
               '长距离弯道', '领跑直线', '危险回避',)
