<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 头像 -->
      <div class="avatar-box">
        <img src="../../assets/logo.png" alt />
      </div>
      <!-- 登录框体 -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
</script>

<style scoped>
.login-container {
  background-color: #f5f7fa;
  height: 100%;
}

.login-box {
  width: 40rem;
  height: 30rem;
  background-color: white;
  border-radius: 0.5rem;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 1rem #cccccc;
}

.avatar-box {
  height: 10rem;
  width: 10rem;
  border: 0.1rem solid #eeeeee;
  border-radius: 35%;
  padding: 0.8rem;
  box-shadow: 0 0 0.75rem #cccccc;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -35%);
  background-color: white;
}

.avatar-box > img {
  height: 100%;
  width: 100%;
  border-radius: 35%;
  background-color: #eeeeee;
}
</style>