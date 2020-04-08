<template>
  <el-main>
    <el-tabs type="border-card">
      <el-tab-pane label="用户管理">
        <el-table :data="all_users_list" v-loading="is_loading_users">
          <el-table-column prop="id" min-width="100" label="序号"></el-table-column>
          <el-table-column prop="nick" min-width="150" label="用户名"></el-table-column>
          <el-table-column prop="name" min-width="100" label="姓名"></el-table-column>
          <el-table-column prop="gender" min-width="50" label="性别"></el-table-column>
          <el-table-column prop="phone" min-width="200" label="联系电话"></el-table-column>
          <el-table-column prop="email" min-width="200" label="邮箱"></el-table-column>
          <el-table-column prop="role" min-width="100" label="角色"></el-table-column>
          <el-table-column prop="create_time" min-width="200" label="创建时间"></el-table-column>
          <el-table-column prop="last_login_time" min-width="200" label="上次登录时间"></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
              <el-button type="text" size="small">编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="需求管理">需求管理</el-tab-pane>
    </el-tabs>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      all_users_list: [],
      is_loading_users: false
    };
  },
  created() {
    this.get_all_users();
  },
  methods: {
    get_all_users() {
      this.is_loading_users = true;
      this.$http.get("/users").then(res => {
        res.data.data.forEach(user => {
          this.all_users_list.push(user);
        });
        this.is_loading_users = false;
      });
    }
  }
};
</script>

<style scope>
</style>