<template>
  <el-main>
    <el-tabs type="border-card">
      <el-tab-pane label="用户管理">
        <el-table :data="all_users_list" v-loading="is_loading_users" height="790">
          <el-table-column sortable prop="id" min-width="100" label="序号"></el-table-column>
          <el-table-column prop="nick" min-width="150" label="用户名"></el-table-column>
          <el-table-column label="个人信息">
            <el-table-column prop="name" min-width="100" label="姓名"></el-table-column>
            <el-table-column prop="gender" min-width="50" label="性别"></el-table-column>
            <el-table-column prop="phone" min-width="200" label="联系电话"></el-table-column>
            <el-table-column prop="email" min-width="200" label="邮箱"></el-table-column>
          </el-table-column>
          <el-table-column
            :filters="[{text:'管理员', value:'管理员'},{text:'审核人员', value:'审核人员'},{text:'普通用户', value:'普通用户'}]"
            :filter-method="filter_method"
            prop="role"
            min-width="100"
            label="角色"
          ></el-table-column>
          <el-table-column sortable prop="create_time" min-width="200" label="创建时间"></el-table-column>
          <el-table-column sortable prop="last_login_time" min-width="200" label="上次登录时间"></el-table-column>
          <el-table-column min-width="150" label="操作">
            <template slot-scope="scope">
              <el-popconfirm @onConfirm="reset_pwd(scope.row)" title="此操作会将密码重置为 12345678">
                <el-button slot="reference" type="warning" size="mini">重置密码</el-button>
              </el-popconfirm>
              <el-popconfirm @onConfirm="set_reviewer(scope.row)" title="确认将此用户设置为审核人员吗？">
                <el-button
                  slot="reference"
                  type="info"
                  size="mini"
                  :disabled="scope.row.role === '管理员'||scope.row.role === '审核人员'?true:false"
                >设为审核</el-button>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="需求管理">
        <el-table :data="all_demands_list" v-loading="is_loading_demands" height="790">
          <el-table-column sortable prop="id" min-width="50" label="序号"></el-table-column>
          <el-table-column prop="title" min-width="100" label="医院名称"></el-table-column>
          <el-table-column label="需求物资">
            <el-table-column prop="content[0].num" label="口罩"></el-table-column>
            <el-table-column prop="content[1].num" label="防护服"></el-table-column>
            <el-table-column prop="content[2].num" label="医用酒精"></el-table-column>
            <el-table-column prop="content[3].num" label="消毒液"></el-table-column>
            <el-table-column prop="content[4].num" show-overflow-tooltip label="其他"></el-table-column>
          </el-table-column>
          <el-table-column prop="publisher" min-width="50" label="发布人"></el-table-column>
          <el-table-column prop="phone" min-width="80" label="联系电话"></el-table-column>
          <el-table-column
            :filters="[{text:'已审核', value:'已审核'},{text:'未审核', value:'未审核'}]"
            :filter-method="filter_method"
            prop="is_review"
            min-width="50"
            label="审核状态"
          ></el-table-column>
          <el-table-column prop="reviewer" min-width="50" label="审核人"></el-table-column>
          <el-table-column
            :filters="[{text:'已撤销', value:'已撤销'},{text:'展示中', value:'展示中'}]"
            :filter-method="filter_method"
            prop="is_cancel"
            min-width="50"
            label="展示状态"
          ></el-table-column>
          <el-table-column sortable prop="pub_time" min-width="120" label="发布时间"></el-table-column>
          <el-table-column min-width="60" label="操作">
            <template slot-scope="scope">
              <el-button
                @click="pass_review(scope.row)"
                type="success"
                size="mini"
                :disabled="scope.row.is_review==='已审核'||scope.row.is_cancel==='已撤销'?true:false"
              >通过审核</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-main>
</template>

<script>
export default {
  // 接收父组件Home传来的值
  props: ["now_login_user_name"],
  data() {
    return {
      all_users_list: [],
      is_loading_users: false,
      all_demands_list: [],
      is_loading_demands: false
    };
  },
  created() {
    this.get_all_users();
    this.get_all_demands();
  },
  methods: {
    get_all_users() {
      this.is_loading_users = true;
      this.$http.get("/users").then(
        res => {
          if (res.data.code === 200) {
            this.is_loading_users = false;
            res.data.data.forEach(user => {
              this.all_users_list.push(user);
            });
          }
          if (res.data.code === 401) {
            this.is_loading_users = false;
            this.$message.warning("登录已过期，请重新登录");
            this.$router.push("/login");
          }
        },
        () => {
          this.is_loading_users = false;
          this.$message.error("获取数据失败，请重试");
        }
      );
    },
    get_all_demands() {
      this.is_loading_demands = true;
      this.$http.get("/all_demands").then(
        res => {
          // console.log(res);
          if (res.data.code === 200) {
            this.is_loading_demands = false;
            this.all_demands_list = res.data.data;
          }
          if (res.data.code === 401) {
            this.is_loading_demands = false;
            this.$message.warning("登录已过期，请重新登录");
            this.$router.push("/login");
          }
        },
        // 获取数据超时的超时信息
        () => {
          this.is_loading_demands = false;
          this.$message.error("获取数据失败，请重试");
        }
      );
    },
    filter_method(value, row, column) {
      let property = column["property"];
      return row[property] === value;
    },
    set_reviewer(row) {
      this.is_loading_users = true;
      this.$http.put("/set_reviewer", { new_reviewer: row.id }).then(
        res => {
          if (res.data.code === 200) {
            this.is_loading_users = false;
            this.$message.success("提交成功");
            row.role = "审核人员";
          }
          if (res.data.code === 401) {
            this.is_loading_demands = false;
            this.$message.warning("登录已过期，请重新登录");
            this.$router.push("/login");
          }
        },
        () => {
          this.is_loading_demands = false;
          this.$message.error("提交失败，请重试");
        }
      );
    },
    reset_pwd(row) {
      this.is_loading_users = true;
      this.$http.put("/reset_pwd", { u_id: row.id }).then(
        res => {
          if (res.data.code === 200) {
            this.is_loading_users = false;
            this.$message.success("密码已重置为 12345678，请及时修改");
          }
          if (res.data.code === 401) {
            this.is_loading_demands = false;
            this.$message.warning("登录已过期，请重新登录");
            this.$router.push("/login");
          }
        },
        () => {
          this.is_loading_demands = false;
          this.$message.error("提交失败，请重试");
        }
      );
    },
    pass_review(row) {
      this.is_loading_demands = true;
      this.$http.put("/do_review", { d_id: row.id }).then(
        res => {
          // console.log(res);
          if (res.data.code === 200) {
            this.is_loading_demands = false;
            this.$message.success("提交成功");
            row.is_review = "已审核";
            row.reviewer = this.now_login_user_name;
          }
          if (res.data.code === 401) {
            this.is_loading_demands = false;
            this.$message.warning("登录已过期，请重新登录");
            this.$router.push("/login");
          }
        },
        () => {
          this.is_loading_demands = false;
          this.$message.error("提交失败，请重试");
        }
      );
    }
  }
};
</script>

<style scope>
</style>