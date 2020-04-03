<template>
  <!-- 登录框体 -->
  <el-form
    class="reg-form"
    :model="reg_form"
    :rules="reg_form_rules"
    ref="reg_form_ref"
    v-loading="is_loading"
  >
    <!-- 账号 -->
    <el-form-item prop="username">
      <el-popover
        ref="username_popover"
        placement="top-start"
        title="关于用户名"
        width="200"
        trigger="focus"
        content="用户名是用来登录验证使用的，并非您的真实姓名。"
      ></el-popover>
      <el-input
        prefix-icon="iconfont icon-user"
        v-model="reg_form.username"
        placeholder="请输入用户名"
        v-popover:username_popover
      ></el-input>
    </el-form-item>
    <!-- 密码 -->
    <el-form-item prop="password">
      <el-input
        prefix-icon="iconfont icon-lock"
        type="password"
        v-model="reg_form.password"
        placeholder="请输入密码"
        show-password
      ></el-input>
    </el-form-item>
    <!-- 确认密码 -->
    <el-form-item prop="check_pwd">
      <el-input
        prefix-icon="iconfont icon-lock"
        type="password"
        v-model="reg_form.check_pwd"
        placeholder="请再次输入密码"
        show-password
      ></el-input>
    </el-form-item>
    <!-- 手机号 -->
    <el-form-item prop="phone">
      <div slot="content"></div>
      <el-popover
        ref="phone_popover"
        placement="bottom-start"
        title="关于您的手机号码"
        width="200"
        trigger="focus"
        content="除非经过您的允许, 否则您的手机号码将仅作为身份验证使用。"
      ></el-popover>
      <el-input
        prefix-icon="iconfont icon-phone"
        v-model="reg_form.phone"
        v-popover:phone_popover
        placeholder="请输入手机号"
      ></el-input>
    </el-form-item>
    <el-form-item class="btns">
      <el-button type="primary" @click="do_register" style="margin-left:1rem">注册</el-button>
      <router-link to="/login">
        <el-button type="info" style="margin-left:1rem">去登录</el-button>
      </router-link>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    var validate_check_pwd = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.reg_form.password) {
        callback(new Error("两次输入密码不一致"));
      } else {
        callback();
      }
    };
    return {
      is_loading: false,
      reg_form: {
        username: "",
        password: "",
        check_pwd: "",
        phone: ""
      },
      reg_form_rules: {
        username: [{ required: true, message: "请输入账号", trigger: "blur" }],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 8,
            max: 32,
            message: "密码长度在 8 到 32 个字符",
            trigger: "blur"
          }
        ],
        check_pwd: [{ validator: validate_check_pwd, trigger: "blur" }],
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

  methods: {
    // 注册按钮对应函数
    do_register: function() {
      this.$refs.reg_form_ref.validate(valid => {
        if (valid) {
          this.is_loading = true;
          // 向服务器发送登录请求
          this.$http.post("/register", this.reg_form).then(
            res => {
              // console.log(res);
              if (res.data.code !== 200) {
                this.is_loading = false;
                return this.$message.error(res.data.data[0].msg);
              }
              this.$message.success(res.data.data[0].msg);
              // 跳转到登录页
              this.$router.push("/login");
            },
            // 登录超时处理
            () => {
              this.is_loading = false;
              this.$message.warning("请求超时，请重试");
            }
          );
        }
      });
    }
  }
};
</script>

<style scoped>
.reg-form {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 3rem;
  padding-bottom: 1rem;
  box-sizing: border-box;
}

.btns {
  float: right;
}
</style>