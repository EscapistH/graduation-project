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
        :placeholder="log_as_holder"
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
        v-model="login_form.log_as"
        active-color="#409EFF"
        inactive-color="#67C23A"
        active-text="个人登录"
        inactive-text="医院登录"
        active-value="user"
        inactive-value="hospital"
        @change="set_placeholder"
      ></el-switch>
      <el-button type="primary" @click="do_login" style="margin-left:1rem">登录</el-button>
      <el-button type="text" style="margin-left:1rem" @click="$router.push('/register')">还没有账号？</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      is_loading: false,
      log_as_holder: "请输入医院名",

      login_form: {
        log_as: "hospital",
        username: "",
        password: ""
      },

      login_form_rules: {
        username: [
          { required: true, message: "请输入医院名", trigger: "blur" }
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
          this.$http.post("/users/login", this.login_form).then(
            res => {
              // console.log(res);
              if (res.data.code !== 200) {
                this.is_loading = false;
                return this.$message.error("账号或密码错误");
              }
              // 保存token和uid
              window.sessionStorage.setItem(
                "user_info",
                JSON.stringify(res.data.data[0])
              );
              // window.sessionStorage.setItem("uid", res.data.data[0].id);
              // 跳转到主页
              this.$router.push("/home");
              this.$message.success("欢迎回来 " + res.data.data[0].name);
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

    // 设置登录框的placeholder
    set_placeholder: function() {
      this.log_as_holder =
        this.login_form.log_as === "hospital" ? "请输入医院名" : "请输入手机号";
      this.login_form_rules.username[0].message =
        this.login_form.log_as === "hospital" ? "请输入医院名" : "请输入手机号";
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