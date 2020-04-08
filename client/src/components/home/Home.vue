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
          :default-active="active_path"
        >
          <el-menu-item index="/demands" @click="get_active_path('/demands')">全部需求</el-menu-item>
          <el-submenu index="2">
            <template slot="title">我的需求</template>
            <el-menu-item index="/my_pub_demands" @click="get_active_path('/my_pub_demands')">我发布的需求</el-menu-item>
            <el-menu-item
              index="/my_cancel_demands"
              @click="get_active_path('/my_cancel_demands')"
            >我撤销的需求</el-menu-item>
          </el-submenu>
        </el-menu>
      </div>
      <!-- 已登录显示发布和退出按钮否则显示登录和注册按钮 -->
      <div v-if="is_login">
        <el-button type="primary" @click="open_pub_dialog" style="margin-right:0.55rem">发布需求</el-button>
        <!-- 发布需求的dialog -->
        <el-dialog
          title="发布需求"
          :visible.sync="pub_dialog_visible"
          width="30%"
          :before-close="handle_close"
          v-loading="is_publishing"
        >
          <!-- 需求表单 -->
          <el-form
            :model="pub_demand_form"
            label-width="8rem"
            label-position="left"
            ref="pub_form_ref"
            :rules="pub_demand_form_rules"
          >
            <el-form-item label="所属医院或单位" prop="title">
              <el-input v-model="pub_demand_form.title" placeholder="请输入所在医院或单位的全称"></el-input>
            </el-form-item>
            <el-form-item v-for="(d, name) in pub_demand_form.content" :key="name" :label="d.name">
              <el-input
                v-model="d.num"
                :type="d.name === '其他'?'textarea':'text'"
                rows="5"
                class="demand-num"
                :placeholder="d.name === '其他'?'有其他的未在上方列出的需求可以写在这里':''"
              ></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="success" @click="do_publish">发布</el-button>
          </div>
        </el-dialog>
        <!-- 退出按钮带完善个人信息的下拉框 -->
        <el-dropdown split-button type="info" @click="do_logout">
          退出
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="open_personal_info_dialog">修改个人信息</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <!-- 完善个人信息的dialog -->
        <el-dialog
          title="修改个人信息"
          :visible.sync="personal_info_dialog_visible"
          width="30%"
          :before-close="handle_close"
          v-loading="is_updating"
        >
          <!-- 个人信息表单 -->
          <el-form
            :model="personal_info_form"
            label-width="8rem"
            label-position="left"
            ref="personal_info_form_ref"
            :rules="personal_info_form_rule"
          >
            <el-form-item label="用户名">
              <el-input :disabled="true" v-model="personal_info_form.nick"></el-input>
            </el-form-item>
            <el-form-item label="姓名" prop="name">
              <el-input v-model="personal_info_form.name"></el-input>
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="personal_info_form.gender">
                <el-radio-button label="男"></el-radio-button>
                <el-radio-button label="女"></el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="personal_info_form.phone"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="personal_info_form.email"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button type="success" @click="do_update_personal_info">提交修改</el-button>
          </div>
        </el-dialog>
      </div>
      <div v-else>
        <el-button type="primary" @click="go_login">去登录</el-button>
        <el-button type="primary" @click="go_register">去注册</el-button>
      </div>
    </el-header>
    <router-view></router-view>
    <!-- 主体部分 -->
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      active_path: "/demands",
      is_login: window.sessionStorage.getItem("token") ? true : false,
      pub_dialog_visible: false,
      is_publishing: false,
      is_updating: false,
      pub_demand_form: {
        title: "",
        content: [
          { name: "口罩", num: "0" },
          { name: "防护服", num: "0" },
          { name: "医用酒精", num: "0" },
          { name: "消毒液", num: "0" },
          { name: "其他", num: "" }
        ],
        publisher: window.sessionStorage.getItem("uid")
      },
      pub_demand_form_rules: {
        title: [
          { required: true, message: "请输入医院或单位名称", trigger: "blur" }
        ]
      },
      personal_info_dialog_visible: false,
      personal_info_form: {
        uid: window.sessionStorage.getItem("uid"),
        nick: null,
        name: null,
        gender: null,
        phone: null,
        email: null
      },
      personal_info_form_rule: {
        name: [{ required: true, message: "请输入真实姓名", trigger: "blur" }],
        gender: [{ required: true, message: "请选择性别", trigger: "change" }],
        phone: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          {
            pattern: /^1[34578]\d{9}$/,
            message: "请输入正确的手机号，暂时只支持中国大陆的手机号",
            trigger: "blur"
          }
        ]
      }
    };
  },
  created() {
    this.get_user_info();
    this.active_path = window.sessionStorage.getItem("active_path");
  },
  methods: {
    do_logout() {
      window.sessionStorage.removeItem("token");
      window.sessionStorage.removeItem("uid");
      this.active_path = "/demands";
      this.$message({
        message: "注销成功",
        type: "success"
      });
      this.$router.push("/demands");
      this.$router.go(0);
    },
    go_login() {
      this.$router.push("/login");
    },
    go_register() {
      this.$router.push("/register");
    },
    get_active_path(path) {
      window.sessionStorage.active_path = path;
      this.active_path = path;
    },
    open_pub_dialog() {
      this.pub_dialog_visible = true;
    },
    do_publish() {
      this.$refs.pub_form_ref.validate(valid => {
        if (valid) {
          this.is_publishing = true;
          this.$http.post("/publish_demand", this.pub_demand_form).then(
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
        }
      });
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
    open_personal_info_dialog() {
      this.personal_info_dialog_visible = true;
    },
    do_update_personal_info() {
      this.$refs.personal_info_form_ref.validate(valid => {
        if (valid) {
          console.log(this.personal_info_form);
          this.is_updating = true;
          this.$http
            .put(
              "/users/" + this.personal_info_form.uid,
              this.personal_info_form
            )
            .then(res => {
              console.log(res);
              if (res.data.code === 200) {
                this.is_updating = false;
                this.$message.success("修改成功");
                this.personal_info_dialog_visible = false;
              }
              if (res.data.code === 401) {
                this.is_updating = false;
                this.personal_info_dialog_visible = false;
                this.$message.waring("登录失效，请重新登录");
                this.$router.push("/login");
              }
            })
            .catch(() => {});
        }
      });
    },
    get_user_info() {
      this.$http.get("/users/" + this.personal_info_form.uid).then(res => {
        this.personal_info_form.nick = res.data.data[0].nick;
        this.personal_info_form.name = res.data.data[0].name;
        this.personal_info_form.gender = res.data.data[0].gender;
        this.personal_info_form.phone = res.data.data[0].phone;
        this.personal_info_form.email = res.data.data[0].email;
      });
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
</style>