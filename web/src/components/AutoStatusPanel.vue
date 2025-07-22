<template>
  <div>
    <div class="card">
      <div class="card-body">
        <div class="d-flex bd-highlight">
          <h5 class="card-title">UAT</h5>
          <span v-on:click="autoStart"  class="ml-auto btn auto-btn">启动</span>
          <span v-on:click="autoStop" class="btn auto-btn" >停止</span>
          <span  @click="createTask" class="btn auto-btn">创建任务</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AutoStatusPanel",
  inject:["schedulerpanel"],
  methods:{
    autoStart:function (){
      this.axios.post("/action/bot/start").then(
          ()=>{
          }
      )
    },
    autoStop:function (){
      this.axios.post("/action/bot/stop").then(
          ()=>{
          }
      )
    },
    createTask:function (){
      this.schedulerpanel.task = null
      $('#create-task-list-modal').modal('show')
    },
  }
}
</script>

<style scoped>
  .btn+.btn{
    margin-left: 5px;
  }
</style>