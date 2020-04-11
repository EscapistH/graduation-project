<template>
  <el-form
    class="login-form"
    :model="login_form"
    :rules="login_form_rules"
    ref="login_form_ref"
    v-loading="is_loading"
  >
    <!-- 账号 -->
    <el-form-item prop="username">
      <el-input
        prefix-icon="iconfont icon-user"
        v-model="login_form.username"
        :placeholder="logby_holder"
      ></el-input>
    </el-form-item>
    <!-- 密码 -->
    <el-form-item prop="password">
      <el-input
        prefix-icon="iconfont icon-lock"
        type="password"
        v-model="login_form.password"
        show-password
        placeholder="请输入密码"
      ></el-input>
    </el-form-item>
    <el-form-item class="btns">
      <!-- 登录方式选择开关 -->
      <el-switch
        v-model="login_form.logby"
        active-color="#409EFF"
        inactive-color="#67C23A"
        active-text="手机号登录"
        inactive-text="用户名登录"
        active-value="phone"
        inactive-value="username"
        @change="set_placeholder"
      ></el-switch>
      <el-button type="primary" @click="do_login" style="margin-left:1rem">登录</el-button>
      <el-button type="info" style="margin-left:1rem" @click="$router.push('/register')">去注册</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      is_loading: false,
      logby_holder: "请输入用户名",

      login_form: {
        logby: "username",
        username: "",
        password: ""
      },

      login_form_rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 8,
            max: 32,
            message: "密码长度在 8 到 32 个字符",
            trigger: "blur"
          }
        ]
      }
    };
  },

  methods: {
    // 登录按钮对应函数
    do_login: function() {
      this.$refs.login_form_ref.validate(valid => {
        if (valid) {
          this.is_loading = true;
          // 向服务器发送登录请求
          this.$http.post("/login", this.login_form).then(
            res => {
              // console.log(res);
              if (res.data.code !== 200) {
                this.is_loading = false;
                return this.$message.error("账号或密码错误");
              }
              // 保存token和uid
              window.sessionStorage.setItem("token", res.data.data[0].token);
              window.sessionStorage.setItem("uid", res.data.data[0].id);
              // 跳转到主页
              this.$router.push("/home");
              if (res.data.data[0].name === null) {
                this.$message.success("欢迎回来 " + res.data.data[0].nick);
              } else {
                this.$message.success("欢迎回来 " + res.data.data[0].name);
              }
            },
            // 登录超时处理
            () => {
              this.is_loading = false;
              this.$message.warning("登录超时，请重试");
            }
          );
        }
      });
    },
    set_placeholder: function() {
      this.logby_holder =
        this.login_form.logby === "username" ? "请输入用户名" : "请输入手机号";
      this.login_form_rules.username[0].message =
        this.login_form.logby === "username" ? "请输入用户名" : "请输入手机号";
    }
  }
};
</script>

<style scoped>
.login-form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 3rem;
  padding-bottom: 6rem;
  box-sizing: border-box;
}

.btns {
  float: right;
}
</style>