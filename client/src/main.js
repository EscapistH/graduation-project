import Vue from 'vue'
import App from './App.vue'
import router from './router'
// 导入ElementUI库
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// 导入全局样式
import './assets/css/global.css'
// 导入字体图标
import '../src/assets/fonts/iconfont.css'
// 导入axios
import axios from 'axios'

// 生产环境用
axios.defaults.baseURL = 'http://bsapi.hxxl.world/api'
// 开发环境用
axios.defaults.baseURL = 'http://localhost:5000/api'
// 请求时在请求头带上token和uid
axios.interceptors.request.use(config => {
  // console.log(config)
  config.headers.token = window.sessionStorage.getItem('user_info') ? JSON.parse(window.sessionStorage.getItem('user_info')).token : null
  config.headers.uid = window.sessionStorage.getItem('user_info') ? JSON.parse(window.sessionStorage.getItem('user_info')).id : null
  return config
})

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next();
})

Vue.prototype.$http = axios

Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
