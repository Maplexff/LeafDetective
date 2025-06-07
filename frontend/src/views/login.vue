<template>
    <div class="login">




            <!-- 左上角logo -->
        <div class="logo top-left">
          <img src="../assets/images/logo-left.png" alt="Logo Left" />
        </div>

        <!-- 右上角logo -->
        <div class="logo top-right">
          <img src="../assets/logo/logo.png" alt="Logo Right" />
        </div>

        <!-- 左侧logo -->
        <div class="logo left-side">
          <img src="../assets/images/logo-left-side.png" alt="Logo Left Side" />
        </div>
                <!-- 左侧logo -->
        <div class="logo left-side1">
          <img src="../assets/images/blue_text_image.png" alt="Logo Left Side" />
        </div>

        <!-- 右侧logo -->
        <div class="logo right-side">
          <img src="../assets/images/logo-right-side.png" alt="Logo Right Side" />
        </div>










        <el-form
            ref="loginRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
        >
            <h3 class="title">Leaf Detective</h3>
            <el-form-item prop="username">
                <el-input
                    v-model="loginForm.username"
                    type="text"
                    size="large"
                    auto-complete="off"
                    placeholder="账号"
                >
                    <template #prefix
                        ><svg-icon
                            icon-class="user"
                            class="el-input__icon input-icon"
                    /></template>
                </el-input>
            </el-form-item>
            <el-form-item prop="password">
                <el-input
                    v-model="loginForm.password"
                    type="password"
                    size="large"
                    auto-complete="off"
                    placeholder="密码"
                    @keyup.enter="handleLogin"
                >
                    <template #prefix
                        ><svg-icon
                            icon-class="password"
                            class="el-input__icon input-icon"
                    /></template>
                </el-input>
            </el-form-item>
            <el-form-item prop="code" v-if="captchaEnabled">
                <el-input
                    v-model="loginForm.code"
                    size="large"
                    auto-complete="off"
                    placeholder="验证码"
                    style="width: 63%"
                    @keyup.enter="handleLogin"
                >
                    <template #prefix
                        ><svg-icon
                            icon-class="validCode"
                            class="el-input__icon input-icon"
                    /></template>
                </el-input>
                <div class="login-code">
                    <img
                        :src="codeUrl"
                        @click="getCode"
                        class="login-code-img"
                    />
                </div>
            </el-form-item>
            <el-checkbox
                v-model="loginForm.rememberMe"
                style="margin: 0px 0px 25px 0px"
                >记住密码</el-checkbox
            >
            <el-form-item style="width: 100%">
                <el-button
                    :loading="loading"
                    size="large"
                    type="primary"
                    style="width: 100%"
                    
                    @click.prevent="handleLogin"
                >
                    <span v-if="!loading">登 录</span>
                    <span v-else>登 录 中...</span>
                </el-button>
                <div style="float: right" v-if="register">
                    <router-link class="link-type" :to="'/register'"
                        >立即注册</router-link
                    >
                </div>
            </el-form-item>
        </el-form>
        <!--  底部  -->
        <div class="el-login-footer">
            <!-- <span>Copyright © 2024 insistence.tech All Rights Reserved.</span> -->
            <span>浙江工业大学毕业课程设计 - 植物叶片病害识别方法及移动端应用设计</span>
        </div>
    </div>
</template>

<script setup>
import { getCodeImg } from '@/api/login'
import Cookies from 'js-cookie'
import { encrypt, decrypt } from '@/utils/jsencrypt'
import useUserStore from '@/store/modules/user'

const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const { proxy } = getCurrentInstance()

const loginForm = ref({
    username: '',
    password: '',
    rememberMe: false,
    code: '',
    uuid: ''
})

const loginRules = {
    username: [{ required: true, trigger: 'blur', message: '请输入您的账号' }],
    password: [{ required: true, trigger: 'blur', message: '请输入您的密码' }],
    code: [{ required: true, trigger: 'change', message: '请输入验证码' }]
}

const codeUrl = ref('')
const loading = ref(false)
// 验证码开关
const captchaEnabled = ref(true)
// 注册开关
const register = ref(false)
const redirect = ref(undefined)

watch(
    route,
    (newRoute) => {
        redirect.value = newRoute.query && newRoute.query.redirect
    },
    { immediate: true }
)

function handleLogin() {
    proxy.$refs.loginRef.validate((valid) => {
        if (valid) {
            loading.value = true
            // 勾选了需要记住密码设置在 cookie 中设置记住用户名和密码
            if (loginForm.value.rememberMe) {
                Cookies.set('username', loginForm.value.username, {
                    expires: 30
                })
                Cookies.set('password', encrypt(loginForm.value.password), {
                    expires: 30
                })
                Cookies.set('rememberMe', loginForm.value.rememberMe, {
                    expires: 30
                })
            } else {
                // 否则移除
                Cookies.remove('username')
                Cookies.remove('password')
                Cookies.remove('rememberMe')
            }
            // 调用action的登录方法
            userStore
                .login(loginForm.value)
                .then(() => {
                    const query = route.query
                    const otherQueryParams = Object.keys(query).reduce(
                        (acc, cur) => {
                            if (cur !== 'redirect') {
                                acc[cur] = query[cur]
                            }
                            return acc
                        },
                        {}
                    )
                    router.push({
                        path: redirect.value || '/',
                        query: otherQueryParams
                    })
                })
                .catch(() => {
                    loading.value = false
                    // 重新获取验证码
                    if (captchaEnabled.value) {
                        getCode()
                    }
                })
        }
    })
}

function getCode() {
    getCodeImg().then((res) => {
        captchaEnabled.value =
            res.captchaEnabled === undefined ? true : res.captchaEnabled
        register.value =
            res.registerEnabled === undefined ? false : res.registerEnabled
        if (captchaEnabled.value) {
            codeUrl.value = 'data:image/gif;base64,' + res.img
            loginForm.value.uuid = res.uuid
        }
    })
}

function getCookie() {
    const username = Cookies.get('username')
    const password = Cookies.get('password')
    const rememberMe = Cookies.get('rememberMe')
    loginForm.value = {
        username: username === undefined ? loginForm.value.username : username,
        password:
            password === undefined
                ? loginForm.value.password
                : decrypt(password),
        rememberMe: rememberMe === undefined ? false : Boolean(rememberMe)
    }
}

getCode()
getCookie()
</script>

<style lang='scss' scoped>
.login {
    display: flex;
    justify-content: center;
    align-items: center;
    // height: 100%;
    background: linear-gradient(to bottom, white, #e0f7fa); /* 从白色到浅蓝色的渐变 */
    height: 100vh;
    // background-color: #ffffff; /* 浅蓝色背景 */
    // background-image: url('../assets/images/login-background.jpg');
    background-size: cover;
}
.title {
    margin: 0px auto 30px auto;
    text-align: center;
    color: #707070;
}

.login-form {
    border-radius: 6px;
    background: #f3f3f3;
    width: 400px;
    padding: 25px 25px 5px 25px;
    .el-input {
        height: 40px;
        input {
            height: 40px;
        }
    }
    .input-icon {
        height: 39px;
        width: 14px;
        margin-left: 0px;
    }
}
.login-tip {
    font-size: 13px;
    text-align: center;
    color: #bfbfbf;
}
.login-code {
    width: 33%;
    height: 40px;
    float: right;
    img {
        cursor: pointer;
        vertical-align: middle;
    }
}
.el-login-footer {
    height: 40px;
    line-height: 40px;
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    color: #000000;
    font-family: Arial;
    font-size: 16px;
    letter-spacing: 1px;
}
.login-code-img {
    height: 40px;
    padding-left: 12px;
}


.logo {
  position: fixed;
  z-index: 10;
  pointer-events: none;
}

.logo img {
  width: auto;
  height: auto;
  object-fit: contain;
}

/* 左上角 logo - 固定大小 */
.top-left {
  top: 20px;
  left: 20px;
  width: 360px;
}
.top-left img {
  width: 360px;
}

/* 右上角 logo */
.top-right {
  top: 20px;
  right: 20px;
  width: 80px;
}
.top-right img {
  width: 80px;
}

/* 左侧中间 logo */
.left-side {
//   top: 50%; 
  bottom: 0;
  transform: translateY(0%);
  left: 0;
  width: 360px;
}
.left-side img {
  width: 360px;
}
/* 左侧中间 logo */
.left-side1 {
//   top: 50%; 
  bottom: 0;
  transform: translateY(-50%);
  left: 0;
  width: 300px;
}
.left-side1 img {
  width: 300px;
}

/* 右侧中间 logo - 只显示左半边 */
.right-side {
//   top: 50%;
  right: 0;
  bottom: 0;
  transform: translateY(-50%);
  width: 240px;
  overflow: hidden;
}
.right-side img {
  width: 480px; /* 双倍宽度只显示左半部分 */
  transform: translateX(0);
}

</style>
