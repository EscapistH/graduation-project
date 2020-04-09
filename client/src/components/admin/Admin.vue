<template>
  <el-main>
    <el-tabs type="border-card">
      <el-tab-pane label="用户管理">
        <el-table :data="all_users_list" v-loading="is_loading_users">
          <el-table-column sortable prop="id" min-width="100" label="序号"></el-table-column>
          <el-table-column prop="nick" min-width="150" label="用户名"></el-table-column>
          <el-table-column prop="name" min-width="100" label="姓名"></el-table-column>
          <el-table-column prop="gender" min-width="50" label="性别"></el-table-column>
          <el-table-column prop="phone" min-width="200" label="联系电话"></el-table-column>
          <el-table-column prop="email" min-width="200" label="邮箱"></el-table-column>
          <el-table-column
            sortable
            :filters="[{text:'管理员', value:'管理员'},{text:'审核人员', value:'审核人员'},{text:'普通用户', value:'普通用户'}]"
            :filter-method="filter_role"
            prop="role"
            min-width="100"
            label="角色"
          ></el-table-column>
          <el-table-column sortable prop="create_time" min-width="200" label="创建时间"></el-table-column>
          <el-table-column sortable prop="last_login_time" min-width="200" label="上次登录时间"></el-table-column>
          <el-table-column align="right" min-width="200">
            <template slot="header">
              <el-button type="primary" @click="add_user">添加用户</el-button>
            </template>
            <template slot-scope="scope">
              <el-button-group>
                <el-button @click="edit_user(scope.row)" type="primary" size="mini">编辑</el-button>
                <el-button @click="reset_pwd(scope.row)" type="warning" size="mini">重置密码</el-button>
                <el-button @click="del_user(scope.row)" type="danger" size="mini">删除</el-button>
              </el-button-group>
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
      is_loading_users: false,
      show_edit: false
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
    },
    filter_role(value, row, column) {
      let property = column["property"];
      return row[property] === value;
    },
    add_user() {
      console.log("add user");
    },
    edit_user() {
      console.log("edit user");
    },
    del_user() {
      console.log("del user");
    },
    reset_pwd() {
      console.log("reset pwd");
    }
  }
};
</script>

<style scope>
</style>