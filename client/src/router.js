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

// 捐赠部分
import MyDonation from './components/demand/MyDonation.vue'

// 后台部分
import Admin from './components/admin/Admin.vue'
import Review from './components/admin/Review.vue'

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
                { path: '/my_demands', component: MyPub, meta: { requireAuth: true } },
                { path: '/my_donations', component: MyDonation, meta: { requireAuth: true } },
                { path: '/admin', component: Admin, meta: { requireAuth: true } },
                { path: '/review', component: Review, meta: { requireAuth: true } }
            ]
        },
    ],
    // mode: 'history'
})


router.beforeEach((to, from, next) => {
    let user_info = window.sessionStorage.getItem('user_info') ? JSON.parse(window.sessionStorage.getItem('user_info')) : null
    if (to.meta.requireAuth) {
        if (user_info.token && user_info.token !== null) {
            next();
        } else {
            next({
                path: '/login',
                query: { redirect: to.fullPath }
            })
        }
    } else {
        next()
    }
})

/*
if (to.path === '/login' || to.path === '/register' || to.path === '/demands') return next();
let tokenStr = window.sessionStorage.getItem('token');
if (!tokenStr) return next('/login')
next()
*/

export default router
