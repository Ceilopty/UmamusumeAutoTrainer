from .. import Event, EventHolder

__all__ = EventHolder.get_all(__name__)

from . import *


class Chara(EventHolder):
    pass


# CHARACTER_KYOUTSUU
k1 = '保重身体！', (
    (('S', {'motivation': -1,
            'last_train': -5,
            }),
     ('F', {'motivation': -1,
            'last_train': -5,
            'condition': 'renshuubeta',
            }),
     ),
    (('R', {'motivation': -1,
            'last_train': -10,
            }),
     ('T', {'motivation': -1,
            'last_train': -10,
            'condition': 'renshuubeta',
            }),
     ('Q', {'condition': 'renshuujouzu_maru',
            })
     ),
), 1

k2 = '不许逞强！', (
    (('S', {'vital': 10,
            'motivation': -3,
            'last_train': -10,
            'random_attr': (2, -10),
            }),
     ('F', {'vital': 10,
            'motivation': -3,
            'last_train': -10,
            'random_attr': (2, -10),
            'condition': 'renshuubeta',
            }),
     ),
    (('P', {'motivation': -3,
            'last_train': -10,
            'random_attr': (2, -10),
            'condition': 'renshuubeta',
            }),
     ('Q', {'vital': 10,
            'condition': 'renshuujouzu_maru',
            })
     ),
), 1

k3 = '追加的自主训练', (
    ((1, {'vital': -5,
          'last_train': 5,
          'favor': 5,
          }),
     ),
    ((1, {'vital': 5,
          }),
     ),
), 2

# AFTER_RACE
r1 = '比赛胜利！', (
    ((1, {'vital': -15,
          'random_attr': (1, 10),  # 赛事等级、赛后、剧本影响
          'skill_point_incr': 45,
          }),
     ),
    (('S', {'vital': -5,
            'random_attr': (1, 10),
            'skill_point_incr': 45,
            }),
     ('F', {'vital': -20,
            'random_attr': (1, 10),
            'skill_point_incr': 45,
            }),
     ),
), 2

r2 = '赛事入围', (
    ((1, {'vital': -20,
          'random_attr': (1, 8),
          'skill_point_incr': 35,
          }),
     ),
    (('S', {'vital': -10,
            'random_attr': (1, 8),
            'skill_point_incr': 35,
            }),
     ('F', {'vital': -30,
            'random_attr': (1, 8),
            'skill_point_incr': 35,
            }),
     ),
), 1

r3 = '比赛落败', (
    ((1, {'vital': -25,
          'random_attr': (1, 6),
          'skill_point_incr': 25,
          }),
     ),
    (('S', {'vital': -15,
            'random_attr': (1, 6),
            'skill_point_incr': 25,
            }),
     ('F', {'vital': -35,
            'random_attr': (1, 6),
            'skill_point_incr': 25,
            }),
     ),
), 1

r4 = '下一次一定要赢！', (
    ((1, {'vital': -25,
          'motivation': 1,
          'random_attr': (1, 6),
          'skill_point_incr': 25,
          }),
     ),
    ((1, {'vital': -25,
          'random_attr': (1, 6),
          'skill_point_incr': 25,
          'skill_hint': ('伏兵', 1),
          }),
     ),
), 1


for chara in __all__:
    Chara.load(chara)

for event in (k1, k2, k3, r1, r2, r3, r4):
    Event(*event)
