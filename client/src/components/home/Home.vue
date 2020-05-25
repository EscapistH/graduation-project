<template>
  <el-container class="home-container">
    <!-- 头部导航栏 -->
    <el-header>
      <!-- 左侧logo和名称 -->
      <div>
        <img src="../../assets/logo.png" class="home-logo" />
        <span>疫情物资援助登记系统</span>
      </div>
      <!-- 导航栏 -->
      <div>
        <el-menu
          mode="horizontal"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          :router="true"
          default-active="/demands"
        >
          <el-menu-item index="/demands">全部需求</el-menu-item>
          <el-menu-item
            index="/my_demands"
            v-if="logged_user_info && logged_user_info.role === 3"
          >我的需求</el-menu-item>
          <el-menu-item
            index="/my_donations"
            v-if="logged_user_info && logged_user_info.role === 4"
          >我的捐赠</el-menu-item>
        </el-menu>
      </div>
      <!-- 已登录显示发布和退出按钮否则显示登录和注册按钮 -->
      <div v-if="is_login">
        <el-button
          type="primary"
          @click="pub_dialog_visible === true?pub_dialog_visible = false:pub_dialog_visible = true"
          style="margin-right:0.55rem"
          v-if="logged_user_info && logged_user_info.role === 3"
        >发布需求</el-button>
        <el-button
          type="info"
          @click="do_logout"
          v-if="logged_user_info && (logged_user_info.role === 3 || logged_user_info.role === 4)"
        >退出</el-button>
        <!-- 下拉按钮组 -->
        <el-dropdown split-button type="info" @click="do_logout" v-else>
          退出
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item
              v-if="logged_user_info && logged_user_info.role === 1"
              @click.native="$router.push('/admin')"
            >管理页面</el-dropdown-item>
            <el-dropdown-item
              v-if="logged_user_info && logged_user_info.role === 2"
              @click.native="$router.push('/review')"
            >审核页面</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <div v-else>
        <el-button type="primary" @click="$router.push('/login')">去登录</el-button>
        <el-button type="primary" @click="$router.push('/register')">去注册</el-button>
      </div>
    </el-header>
    <!-- 发布需求的dialog -->
    <el-dialog
      title="发布需求"
      :visible.sync="pub_dialog_visible"
      width="50%"
      :before-close="handle_close"
      v-loading="is_publishing"
    >
      <!-- 需求表单 -->
      <el-form :model="pub_demand_form">
        <el-form-item v-for="(supply, index) in pub_demand_form.supplies" :key="index">
          <el-input v-model="supply.name" placeholder="物资" class="supply-name"></el-input>
          <el-input v-model="supply.specification" placeholder="规格" class="supply-specification"></el-input>
          <el-input v-model="supply.number" placeholder="数量, 不限请输入-1" class="supply-number"></el-input>
          <el-button @click="remove_supply(supply)" class="supply-remove-btn">删除</el-button>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="add_supply">新增物资</el-button>
        <el-button type="success" @click="do_publish">发布</el-button>
      </div>
    </el-dialog>
    <router-view :logged_user_info="logged_user_info"></router-view>
    <!-- 主体部分 -->
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      is_login: window.sessionStorage.getItem("user_info") ? true : false,
      pub_dialog_visible: false,
      is_publishing: false,

      pub_demand_form: {
        publisher: null,
        supplies: [
          { name: "口罩", specification: "", number: "" },
          { name: "防护服", specification: "", number: "" }
        ]
      },
      // 接收登录用户信息
      logged_user_info: sessionStorage.getItem("user_info")
        ? JSON.parse(sessionStorage.getItem("user_info"))
        : null
    };
  },

  methods: {
    do_logout() {
      window.sessionStorage.removeItem("user_info");
      this.active_path = "/demands";
      this.$message({
        message: "注销成功",
        type: "success"
      });
      this.$router.go(0);
    },

    do_publish() {
      this.is_publishing = true;
      this.pub_demand_form.publisher = this.logged_user_info.id;
      // console.log(this.pub_demand_form);
      this.$http.post("/demands", this.pub_demand_form).then(
        res => {
          // console.log(res);
          this.is_publishing = true;
          if (res.data.code === 200) {
            this.is_publishing = false;
            this.$message.success("发布需求成功");
            this.pub_dialog_visible = false;
            this.is_publishing = false;
            this.$router.go(0);
          }
          if (res.data.code === 401) {
            this.is_publishing = false;
            this.$message.waring("登录已过期，请重新登录");
            this.$router.push("/login");
          }
        },
        () => {
          this.is_modifying = false;
          this.$message.error("请求失败，请重试");
        }
      );
    },

    handle_close(done) {
      this.$confirm("还未提交修改,确认关闭吗?")
        .then(() => {
          this.demand = null;
          done();
          this.pub_dialog_visible = false;
        })
        .catch(() => {});
    },
    add_supply() {
      this.pub_demand_form.supplies.push({
        name: "",
        specification: "",
        number: ""
      });
    },
    remove_supply(item) {
      let index = this.pub_demand_form.supplies.indexOf(item);
      if (index !== -1) {
        this.pub_demand_form.supplies.splice(index, 1);
      }
    }
  }
};
</script>

<style scoped>
.home-container {
  height: 100%;
}

.home-logo {
  height: 3rem;
  width: 3rem;
}

.el-header {
  background-color: #545c64;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #ffffff;
  font-size: 1.5rem;
}
.el-header > div {
  display: flex;
  align-items: center;
}
.el-header > div > span {
  margin-left: 1rem;
}

.el-main {
  background-color: #f5f7fa;
}

.supply-name {
  width: 20%;
  margin-left: 5%;
}

.supply-specification {
  width: 40%;
  margin-left: 1%;
}

.supply-number {
  width: 20%;
  margin-left: 1%;
}

.supply-remove-btn {
  margin-left: 1%;
}
</style>