<template>
  <div>
    <div v-if="task.task_type === 1">
      <div>
        <span>剧本: URA</span>
      </div>
      <div>
        <span>目标数值: {{task.detail?.expect_attribute}}</span>
      </div>
      <div v-if="task.detail.cultivate_result.factor_list !== undefined && task.detail.cultivate_result.factor_list.length !== 0">
        因子获取：<span class="mr-1" v-for="factor in task.detail.cultivate_result.factor_list">
          <span v-if="factor[0] === '速度' || factor[0] === '耐力'|| factor[0] === '力量'|| factor[0] === '毅力'|| factor[0] === '智力'"  style="background-color: #49BFF7;" class="badge badge-pill badge-secondary">{{factor[0]}}({{factor[1]}})</span>
          <span v-if="factor[0] === '短距离' || factor[0] === '英里'|| factor[0] === '中距离'|| factor[0] === '长距离'|| factor[0] === '泥地'|| factor[0] === '草地'|| factor[0] === '领跑'|| factor[0] === '跟前'|| factor[0] === '居中'|| factor[0] === '后追'"  style="background-color: #FF78B2;" class="badge badge-pill badge-secondary">{{factor[0]}}({{factor[1]}})</span>
          <span v-if="factor[0] !== '速度' && factor[0] !== '耐力'&& factor[0] !== '力量'&& factor[0] !== '毅力'&& factor[0] !== '智力'&& factor[0] !== '短距离' && factor[0] !== '英里'&& factor[0] !== '中距离'&& factor[0] !== '长距离'&& factor[0] !== '泥地'&& factor[0] !== '草地' &&factor[0] !== '领跑'&& factor[0] !== '跟前'&& factor[0] !== '居中'&& factor[0] !== '后追'" 
            style="background-color: #E0E0E0; color: #794016;" class="badge badge-pill badge-secondary">{{factor[0]}}({{factor[1]}})</span>
        </span>
      </div>
    </div>
    <div v-if="task.task_type === 2">
      <div>
        <span>对手: {{opponent_type[task.detail?.opponent_index]}}</span>
      </div>
      <div>
        耐力阈值: <span>{{task.detail.opponent_stamina}}</span>
      </div>
    </div>
    <div v-if="task.task_type === 3">
      <div>
        <span>请求: {{shoe_type_name[task.detail?.ask_shoe_type]}}</span>
      </div>
    </div>
    <div v-if="task.task_type === 4">
      <div>
        <span>目标赛事: {{daily_race_type[task.detail?.daily_race_type]}}</span>
      </div>
      <div>
        <span>难度: {{daily_race_difficulty[task.detail?.daily_race_difficulty]}}</span>
      </div>
    </div>
    <div v-if="task.task_type === 2 || task.task_type === 4">
      <div>
        <span>限时特卖: <span v-for="item in task.detail.time_sale" style="background-color: #49BFF7;" class="badge badge-pill badge-secondary">{{time_sale_item[item]}}</span></span>
      </div>
      <div v-if="task.detail.time_sale_bought !== undefined && task.detail.time_sale_bought.length !== 0">
        已购买：<br/>
        <span class="mr-1" v-for="bought in task.detail.time_sale_bought">
          <span v-for="item in bought" style="background-color: #E0E0E0; color: #794016;" class="badge badge-pill badge-secondary">{{time_sale_item[item]}}</span>
          <br/>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UmamusumeTaskDetailInfo",
  props: ["task"],
  data: function(){
    return{
      shoe_type_name: {
        1: "短距离跑鞋",
        2: "英里跑鞋",
        3: "中距离跑鞋",
        4: "长距离跑鞋",
        5: "泥地跑鞋",
        0: "任意"
      },
      opponent_type: {
        1: "上",
        2: "中",
        3: "下",
        0: "随意"
      },
      time_sale_item: {
        0: "碎片一",
        1: "碎片二",
        2: "闹钟",
        3: "甜点",
        4: "协助积分",
        5: "短距离跑鞋",
        6: "英里跑鞋",
        7: "中距离跑鞋",
        8: "长距离跑鞋",
        9: "泥地跑鞋"
      },
      daily_race_type:{
        0: "月光奖（金币）",
        1: "木星杯（协助积分）",
      },
      daily_race_difficulty:{
        0: "EASY",
        1: "NORMAL",
        2: "HARD",
      }
    }
  }
}
</script>

<style scoped>

</style>