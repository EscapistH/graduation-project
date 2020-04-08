import Vue from 'vue'
import Router from 'vue-router'


// 登录注册部分
import Log from './components/sign/Log.vue'
import Login from './components/sign/Login.vue'
import Register from './components/sign/Register.vue'

// 主页(需求部分容器)部分
import Home from './components/home/Home.vue';

// 需求部分
import Demands from './components/demand/AllDemands.vue'
import MyPub from './components/demand/MyPub.vue'
import MyCancel from './components/demand/MyCancel.vue'

// 后台部分
import Admin from './components/admin/Admin.vue'

Vue.use(Router)

const router = new Router({
    routes: [
        { path: '/', redirect: '/demands', meta: { title: '疫情物资援助登记系统' } },
        {
            path: '/log', component: Log, redirect: '/login', children: [
                { path: '/login', component: Login, meta: { title: '登录' } },
                { path: '/register', component: Register, meta: { title: '注册' } },
            ]
        },
        {
            path: '/home',
            component: Home,
            redirect: '/demands',
            children: [
                { path: '/demands', component: Demands, meta: { title: '疫情物资援助登记系统' } },
                { path: '/my_pub_demands', component: MyPub },
                { path: '/my_cancel_demands', component: MyCancel },
                { path: '/admin', component: Admin, meta: { title: '管理' } },
            ]
        },
    ],
    // mode: 'history'
})

router.beforeEach((to, from, next) => {
    if (to.path === '/login' || to.path === '/register' || to.path === '/demands') return next();
    let tokenStr = window.sessionStorage.getItem('token');
    if (!tokenStr) return next('/login')
    next()
})

export default router
