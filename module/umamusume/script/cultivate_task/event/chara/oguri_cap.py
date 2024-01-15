print(__name__)

# SHOUBUFUKU_ORIGINAL
s1 = '背负的信念', (
    ((1, {'stamina_incr': 10,
          'power_incr': 10,
          }),
     ),
    ((1, {'wiz_incr': 20,
          }),
     ),
    ), 1

s2 = '小栗帽是森林向导？', (
    ((1, {'speed_incr': 20,
          }),
     ),
    ((1, {'power_incr': 20,
          }),
     ),
    ), 1

s3 = '超越娃娃', (
    (('P', {'guts_incr': 20,
          }),
     ('Q', {'guts_incr': 20,
          }),
     ),
    (('P', {'stamina_incr': 20,
            'condition': 'chuumokukabu',
          }),
     ('Q', {'stamina_incr': 20,
            'condition': 'chuumokukabu',
          }),
     ),
    ), 2


# SHOUBUFUKU_SHINISHOU

# CHARACTER
c1 = '隔壁的晚饭令人在意!', (
    ((1, {'speed_incr': 10,
          }),
     ),
    ((1, {'guts_incr': 10,
          }),
     ),
    ), 1

c2 = '强劲的对手', (
    ((1, {'speed_incr': 5,
          'stamina_incr': 5,
          }),
     ),
    ((1, {'power_incr': 5,
          'wiz_incr': 5,
          }),
     ),
    ), 1

c3 = '尽享比赛与美食', (
    ((1, {'vital': 10,
          'skill_point_incr': 15,
          }),
     ),
    ((1, {'skill_hint': ('中山赛场', 1),
          }),
     ),
    ), 1

c4 = '迷路的优骏少女', (
    ((1, {'guts_incr': 10,
          }),
     ),
    ((1, {'speed_incr': 10,
          }),
     ),
    ), 2

c5 = '在田间锻炼', (
    ((1, {'guts_incr': 10,
          }),
     ),
    ((1, {'power_incr': 10,
          }),
     ),
    ), 2

# Oogui
o1 = '大胃王可不是浪得虚名', (
    ((1, {'vital': 10,
          'skill_point_incr': 5,
          }),
     ),
    (('P', {'vital': 30,
            'skill_point_incr': 10,
            }),
     ('Q', {'vital': 30,
            'speed_incr': -5,
            'power_incr': 5,
            'skill_point_incr': 10,
            'condition': 'futorigimi',
            }),
     ),
    ), 2

o2 = '小栗帽的大胃王比赛', (
    (('P', {'vital': 30,
            'power_incr': 10,
            'skill_point_incr': 10,
            }),
     ('Q', {'vital': 30,
            'speed_incr': -5,
            'power_incr': 5,
            'skill_point_incr': 10,
            'condition': 'futorigimi',
            }),
     ),
    ((1, {'vital': 10,
          'power_incr': 5,
          'skill_point_incr': 5,
          }),
     ),
    ), 1

# TRIP
t1 = '小栗帽，下定决心', (
    ((1, {'speed_incr': 5,
          'wiz_incr': 5,
          }),
     ),
    ((1, {'stamina_incr': 5,
          'guts_incr': 5,
          }),
     ),
    ), 1

t2 = '小栗帽，很努力', (
    ((1, {'guts_incr': 10,
          }),
     ),
    ((1, {'power_incr': 10,
          }),
     ),
    ), 2

t3 = '小栗帽，不断成长', (
    ((1, {'wiz_incr': 10,
          }),
     ),
    ((1, {'stamina_incr': 10,
          }),
     ),
    ((1, {'power_incr': 10,
          }),
     ),
    ), 2

# ダンスレッスン
dance_lesson = '舞蹈课_小栗帽', (
    ((1, {'power_incr': 10,
          }),
     ),
    ((1, {'speed_incr': 10,
          }),
     ),
    ), 2

