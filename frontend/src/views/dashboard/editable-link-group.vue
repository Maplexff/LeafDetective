<template>
    <div class="linkGroup">
        <a v-for="(item, index) in links" :key="index" :href="item.href">
            {{ item.title }}
        </a>
        <router-link to="/history_hisory">
            <a>历史记录</a>
        </router-link>
        <router-link to="/user/profile">
            <a>个人中心</a>
        </router-link>
        <router-link to="/system/notice">
            <a>通知公告</a>
        </router-link>
        <!-- <a-button size="small" type="primary" ghost>
            <PlusOutlined /> 添加
        </a-button> -->
    </div>
</template>

<script>
import { Button } from 'ant-design-vue'

export default {
    components: {
        AButton: Button
    }
}
</script>

<script setup>
import { PlusOutlined } from '@ant-design/icons-vue'

// const links = [
//     {
//         title: '历史记录',
//         href: ''
//     },
//     {
//         title: '个人中心',
//         href: ''
//     },
//     {
//         title: '通知公告',
//         href: ''
//     },
    // {
    //     title: '操作四',
    //     href: ''
    // },
    // {
    //     title: '操作五',
    //     href: ''
    // },
    // {
    //     title: '操作六',
    //     href: ''
    // }
// ]
</script>

<style scoped lang="less">
.linkGroup {
    padding: 20px 0 8px 24px;
    font-size: 0;
    & > a {
        display: inline-block;
        width: 25%;
        margin-bottom: 13px;
        color: rgba(0, 0, 0, 0.65);
        font-size: 14px;
        &:hover {
            color: #1890ff;
        }
    }
}
</style>