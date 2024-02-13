"""
URA中未维护的成功育成事件信息，格式同success_events.br
还有一些未改版事件，在这里还原一下。
不再用json或brotli压缩了，直接使用字面值。
"""

success_events = {830029002: {"Id": 830029002,
                              "Choices": [
                                  [],
                                  [
                                      {
                                          "SelectIndex": 1,
                                          "Scenario": 0,
                                          "State": 1,
                                          "Effect": "体力+15、スタミナ+10、サトノダイヤモンドの絆ゲージ+5"
                                      },
                                      {
                                          "SelectIndex": 2,
                                          "Scenario": 0,
                                          "State": 2,
                                          "Effect": "やる気−1、根性+20"
                                      }
                                  ]
                              ]
                              },
                  830029003: {"Id": 830029003,
                              "Choices": [
                                  [
                                      {
                                          "SelectIndex": 1,
                                          "Scenario": 0,
                                          "State": 1,
                                          "Effect": "体力-20、スタミナ+30、「鋼の意志」のヒントLv+1、サトノダイヤモンドの絆ゲージ+5"
                                      }
                                  ],
                                  [
                                      {
                                          "SelectIndex": 1,
                                          "Scenario": 0,
                                          "State": 1,
                                          "Effect": "体力+5、根性+5、「鋼の意志」のヒントLv+1、サトノダイヤモンドの絆ゲージ+5"
                                      }
                                  ]
                              ]
                              },
                  501006710: {"Id": 501006710,
                              "Choices": [
                                  [
                                      {
                                          "SelectIndex": 1,
                                          "Scenario": 0,
                                          "State": 1,
                                          "Effect": "体力-25、ランダムな1つのステータス+4、スキルPt+25、確率でマイナススキル獲得"
                                      }
                                  ],
                                  [
                                      {
                                          "SelectIndex": 1,
                                          "Scenario": 0,
                                          "State": 1,
                                          "Effect": "体力-15、ランダムな1つのステータス+4、スキルPt+25、確率でマイナススキル獲得"
                                      },
                                      {
                                          "SelectIndex": 2,
                                          "Scenario": 0,
                                          "State": 0,
                                          "Effect": "体力-35、ランダムな1つのステータス+4、スキルPt+25、確率でマイナススキル獲得"
                                      },
                                  ]
                              ]
                              },
                  820017001: {'Id': 820017001,
                              'Choices': [
                                  [],
                                  [
                                      {
                                          'SelectIndex': 1,
                                          'Scenario': 0,
                                          'State': 1,
                                          'Effect': '体力の最大値+4、やる気+1、根性+5、賢さ+5、名将怒涛の絆ゲージ+5'
                                      },
                                      {
                                          'SelectIndex': 2,
                                          'Scenario': 0,
                                          'State': 0,
                                          'Effect': '体力-10、賢さ+5'
                                      }
                                  ]
                              ]
                              },
                  }
