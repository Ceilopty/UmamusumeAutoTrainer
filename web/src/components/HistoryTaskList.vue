<template>
  <div>
    <div class="card">
      <div class="card-body">
        <div class="d-flex bd-highlight">
          <div class="form-inline">
            <div class="form-group">
              <h5 class="card-title">已结束的</h5>
              <select v-model="selectedDisplayTaskStatus" id="selectDisplayTaskStatus">
                <option :value=undefined>全部</option>
                <option :value=3>中断</option>
                <option :value=4>成功</option>
                <option :value=5>失败</option>
              </select>
              <h5 class="card-title">任务，结束原因：</h5>
              <select v-model="selectedEndTaskReason" id="selectEndTaskReason">
                <option :value=undefined>全部</option>
                <option v-for="reason in endTaskReasonList" :value=reason>{{reason}}</option>
              </select>
            </div>
          </div>
          <span v-on:click="clearAll" class="ml-auto btn auto-btn" >清空</span>
        </div>
      </div>
      <TaskList v-bind:task-list="selectedTasks" v-bind:no-data-label="'无已结束的'+statusDict[selectedDisplayTaskStatus]+'任务'"></TaskList>
    </div>
  </div>
</template>

<script>
import TaskList from "./TaskList.vue";

export default {
  name: "HistoryTaskPanel",
  props:["historyTaskList"],
  components: {TaskList},
  mounted:function(){
    let vue = this;
    setInterval(function () {
      vue.getSelectedTaskList();
    },1000)
  },
  methods:{
    clearAll: function() {
      let payload = []
      this.selectedTasks.forEach(element => {
        payload.push({"task_id": element.task_id})
      });
      console.log(JSON.stringify(payload))
      this.axios.delete("/task", JSON.stringify(payload)).then()
    },
    getSelectedTaskList: function() {
      this.selectedTasks = []
      this.endTaskReasonList = []
      this.historyTaskList.forEach(
         t=>{
          if(this.selectedDisplayTaskStatus === undefined || t['task_status'] === this.selectedDisplayTaskStatus){
            if(t['end_task_reason'] !== undefined){
              if(!this.endTaskReasonList.includes(t['end_task_reason'])){
                this.endTaskReasonList.push(t['end_task_reason'])
              }
            }
            if(this.selectedEndTaskReason === undefined || t['end_task_reason'] === this.selectedEndTaskReason){
              this.selectedTasks.push(t)
            }
          }
        }
      )
      if(!this.endTaskReasonList.includes(this.selectedEndTaskReason)){
        this.selectedEndTaskReason = undefined
      }
    },
  },
  data:function (){
    return{
      selectedDisplayTaskStatus: undefined,
      selectedTasks:[],
      endTaskReasonList:[],
      selectedEndTaskReason: undefined,
      statusDict:{
        3:"中断",
        4:"成功",
        5:"失败",
        undefined:"",
      }
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
