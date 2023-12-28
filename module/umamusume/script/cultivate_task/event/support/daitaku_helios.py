print(__name__)

# 派对人派对夜！
s1 = '#bff #Party!', (
    ((1, {'power_incr': 10,
          'favor':5 ,
          }),
     ),
    ((1, {'speed_incr': 10,
          'favor':5 ,
          }),
     ),
    ), 2

s2 = '#lol #Party!  #2nd', (
    (('S', {'speed_incr': 10,
            'power_incr': 10,
            'favor': 5,
            'skill_hint': ('直线下坡', 3),
            }),
     ('F', {'power_incr': 10,
            'favor': 5,
            'skill_hint': ('直线下坡', 1),
          }),
     ),
    ((1, {'vital': 20,
          'favor': 5,
          'skill_hint': ('窥视展开', 1),
          }),
     ),
    ), 2

# Kyoutsuu
k1 = '笑容常在', (
    ((1, {'speed_incr': 5,
          'power_incr': 10,
          'favor': 5,
          }),
     ),
    ((1, {'favor': 5,
          'skill_hint': ('伏兵', 1),
          }),
     ),
    ), 1

k2 = '偶遇太阳☆', (
    ((1, {'power_incr': 10,
          'favor': 5,
          }),
     ),
    ((1, {'favor': 5,
          'condition': 'chuumokukabu',
          }),
     ),
    ), 1

__skill_hint:('加快步伐', '保留体力', '英里弯道', '变速', '吞噬速度',
              '共鸣', '尾流',)