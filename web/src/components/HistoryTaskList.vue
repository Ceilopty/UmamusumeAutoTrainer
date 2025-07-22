<template>
  <div>
    <div class="card">
      <div class="card-body">
        <div class="d-flex bd-highlight">
          <h5 class="card-title">已结束的任务</h5>
          <span v-on:click="clearAll" class="ml-auto btn auto-btn" >清空</span>
        </div>
      </div>
      <TaskList v-bind:task-list="historyTaskList" v-bind:no-data-label="'无已结束的任务'"></TaskList>
    </div>
  </div>
</template>

<script>
import TaskList from "./TaskList.vue";

export default {
  name: "HistoryTaskPanel",
  props:["historyTaskList"],
  components: {TaskList},
  methods:{
    clearAll: function() {
      let payload = []
      this.historyTaskList.forEach(element => {
        payload.push({"task_id": element.task_id})
      });
      console.log(JSON.stringify(payload))
      this.axios.delete("/task", JSON.stringify(payload)).then()
    },
  },
  data:function (){
    return{
    }
  }
}
</script>

<style scoped>
.card-title{
  margin-bottom: 0;
}
.start-time{
  color: #999;
}
.card-body{
  border-bottom: 1px solid rgba(0,0,0,.125);
}
.btn+.btn{
  margin-left: 5px;
}
</style>
