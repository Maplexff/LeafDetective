<template>
    <div>
        <div class="pageHeaderContent">
            <div class="avatar">
                <!-- <a-avatar size="large" :src="currentUser.avatar" /> -->
                <a-avatar size="large" :src= "fullUrl(state.user.avatar)" />
                  <!-- <a-avatar size="large" :src= "fullUrl(userStore.avatar)" /> -->
            </div>
            <div class="content" >
                <div class="contentTitle">
                    欢迎，
                    <!-- {{ state.user.userId }} -->
                      {{ state.user.userName }}
                    ，祝你开心每一天！
                </div>
                <!-- <div>{{ state.roleGroup }}  |  {{ state.user.dept.deptName }}</div> -->
                <div>{{ state.roleGroup }}</div>
                <!-- <div>{{ state.user.dept.deptName }}</div> -->
            </div>
            <div class="extraContent">
                <div class="statItem">
                    <a-statistic title="上报记录" :value=diseaseStats.currentuserrecord />
                </div>
                <!-- <div class="statItem">
                    <a-statistic title="团队内排名" :value="8" suffix="/ 24" />
                </div> -->
                <div class="statItem">
                    <a-statistic title="总历史记录" :value=diseaseStats.allrecord />
                </div>
            </div>
        </div>

        <div style="padding: 10px">
            <a-row :gutter="24">
                <a-col :xl="16" :lg="24" :md="24" :sm="24" :xs="24">
                    <a-card 
                        title="病害类型统计"
                        :bordered="true"
                        :style="{ marginBottom: '24px' }"
                        :body-style="{ padding: '16px' }">
                        <a-descriptions
                            layout="vertical"
                            :column="5"
                            bordered>
                            <a-descriptions-item label="黑斑病">{{ diseaseStats.type0 }}</a-descriptions-item>
                            <a-descriptions-item label="霜霉病">{{ diseaseStats.type1 }}</a-descriptions-item>
                            <a-descriptions-item label="花叶病">{{ diseaseStats.type4 }}</a-descriptions-item>
                            <a-descriptions-item label="虫害">{{ diseaseStats.type3 }}</a-descriptions-item>
                            <a-descriptions-item label="健康">{{ diseaseStats.type2 }}</a-descriptions-item>
                        </a-descriptions>
                    </a-card>
                    <!-- 项目统计表格 -->

                    <!-- <a-card
                        class="projectList"
                        :style="{ marginBottom: '24px' }"
                        title="进行中的项目"
                        :bordered="true"
                        :loading="false"
                        :body-style="{ padding: 0 }"
                    >
                        <a-card-grid
                            v-for="item in projectNotice"
                            :key="item.id"
                            class="projectGrid"
                        >
                            <a-card
                                :body-style="{ padding: 0 }"
                                style="box-shadow: none"
                                :bordered="false"
                            >
                                <a-card-meta
                                    :description="item.description"
                                    class="w-full"
                                >
                                    <template #title>
                                        <div class="cardTitle">
                                            <a-avatar
                                                size="small"
                                                :src="item.logo"
                                            />
                                            <a :href="item.href">
                                                {{ item.title }}
                                            </a>
                                        </div>
                                    </template>
                                </a-card-meta>
                                <div class="projectItemContent">
                                    <a :href="item.memberLink">
                                        {{ item.member || '' }}
                                    </a>
                                    <span
                                        class="datetime"
                                        ml-2
                                        :title="item.updatedAt"
                                    >
                                        {{ item.updatedAt }}
                                    </span>
                                </div>
                            </a-card>
                        </a-card-grid>
                    </a-card> -->
                    <a-card
                        :body-style="{ padding: 0 }"
                        :bordered="false"
                        class="activeCard"
                        title="动态"
                        :loading="false"
                    >
                        <a-list
                            :data-source="activities"
                            class="activitiesList"
                        >
                            <template #renderItem="{ item }">
                                <a-list-item :key="item.id">
                                    <a-list-item-meta>
                                        <template #title>
                                            <span>
                                                <a class="username">{{
                                                    item.user_name
                                                }}</a
                                                >&nbsp;
                                                <span class="event">
                                                    <span>{{
                                                        mything[0].template1
                                                    }}</span
                                                    >&nbsp;
                                                    <a
                                                       
                                                     
                                                    >
                                                        {{
                                                            item?.location
                                                        }} </a
                                                    >&nbsp;
                                                    <span>{{
                                                        mything[0].template2
                                                    }}</span
                                                    >&nbsp;
                                                    <a
                                                        
                                                        
                                                    >
                                                        {{
                                                            item?.predclass
                                                        }}
                                                    </a>
                                                </span>
                                            </span>
                                        </template>
                                        <template #avatar>
                                            <!-- <a-avatar :src="item.user.avatar" /> -->
                                            <a-avatar :src="mything[0].avatar"/>
                                        </template>
                                        <template #description>
                                            <span
                                                class="datetime"
                                                :title="item.updatedAt"
                                            >
                                                {{ item.updatedAt }}
                                            </span>
                                        </template>
                                    </a-list-item-meta>
                                </a-list-item>
                            </template>
                        </a-list>
                    </a-card>
                </a-col>
                <a-col :xl="8" :lg="24" :md="24" :sm="24" :xs="24">

                    <a-card
                        :style="{ marginBottom: '24px' }"
                        title="快速开始 / 便捷导航"
                        :bordered="false"
                        :body-style="{ padding: 0 }"
                    >
                        <EditableLinkGroup />
                    </a-card>



                    <a-card
                        class="projectList"
                        :style="{ marginBottom: '24px' }"
                        title="养护提示"
                        :bordered="true"
                        :loading="false"
                        :body-style="{ padding: 0 }"
                    >
                        
                            <a-carousel 
                            :autoplay = true
                            :dots = true
                            :arrows = true>
                                <div v-for="(item, index) in slides" :key="index" class="slide">
                                    <img :src="item.image" :alt="item.title" class="slide-image" />
                                    <div class="slide-text">
                                        <h3>{{ item.title }}</h3>
                                        <p>{{ item.description }}</p>
                                    </div>
                                </div>
                            </a-carousel>
                        
                    
                        <!-- <a-card-grid
                            v-for="item in projectNotice"
                            :key="item.id"
                            class="projectGrid"
                        >
                            <a-card
                                :body-style="{ padding: 0 }"
                                style="box-shadow: none"
                                :bordered="false"
                            >
                                <a-card-meta
                                    :description="item.description"
                                    class="w-full"
                                >
                                    <template #title>
                                        <div class="cardTitle">
                                            <a-avatar
                                                size="small"
                                                :src="item.logo"
                                            />
                                            <a :href="item.href">
                                                {{ item.title }}
                                            </a>
                                        </div>
                                    </template>
                                </a-card-meta>
                                <div class="projectItemContent">
                                    <a :href="item.memberLink">
                                        {{ item.member || '' }}
                                    </a>
                                    <span
                                        class="datetime"
                                        ml-2
                                        :title="item.updatedAt"
                                    >
                                        {{ item.updatedAt }}
                                    </span>
                                </div>
                            </a-card>
                        </a-card-grid> -->
                    </a-card>



                    <!-- <a-card
                        :style="{ marginBottom: '24px' }"
                        :bordered="false"
                        title="XX 指数"
                    >
                        <div class="chart">
                            <div ref="radarContainer" />
                        </div>
                    </a-card> -->
                    <!-- <a-card
                        :body-style="{
                            paddingTop: '12px',
                            paddingBottom: '12px'
                        }"
                        :bordered="false"
                        title="团队"
                    >
                        <div class="members">
                            <a-row :gutter="48">
                                <a-col
                                    v-for="item in projectNotice"
                                    :key="`members-item-${item.id}`"
                                    :span="12"
                                >
                                    <a :href="item.href">
                                        <a-avatar
                                            :src="item.logo"
                                            size="small"
                                        />
                                        <span class="member">{{
                                            item.member
                                        }}</span>
                                    </a>
                                </a-col>
                            </a-row>
                        </div>
                    </a-card> -->
                </a-col>
            </a-row>
        </div>
    </div>
</template>

<script>
import {
    Statistic,
    Row,
    Col,
    Card,
    CardGrid,
    CardMeta,
    List,
    ListItem,
    ListItemMeta,
    Avatar,
    Descriptions,
    DescriptionsItem,
    Table,
    Carousel,
    

} from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
// import { he } from 'element-plus/es/locales.mjs'
// import tongzhi from 'src/assets/images/通知.jpg';
// import blackspot from 'src/assets/images/BlackSpot (185).jpg';
// import shuangmei from 'src/assets/images/Augimage_75.jpg';
// import chonghai from 'src/assets/images/Insects Infected (383).jpg';
// import imageUrl from 'src/assets/images/Fungus(12).jpg';
// import imageUrl from '@/assets/images/your-image.jpg';
export default {
    components: {
        AStatistic: Statistic,
        ARow: Row,
        ACol: Col,
        ACard: Card,
        ACardGrid: CardGrid,
        ACardMeta: CardMeta,
        AList: List,
        AListItem: ListItem,
        AListItemMeta: ListItemMeta,
        AAvatar: Avatar,
        ADescriptions: Descriptions,
        ADescriptionsItem: DescriptionsItem,
        ATable: Table,
        ACarousel: Carousel

    }
}
</script>


<script setup>
// import { Radar } from '@antv/g2plot'
import EditableLinkGroup from './editable-link-group.vue'
import { ref, onMounted ,watch} from 'vue'
// 引入若依封装的请求方法
import request from '@/utils/request'
import { getUserProfile } from '@/api/system/user'

// // 引入 useUserStore
// import useUserStore from '@/store/modules/user'
defineOptions({
    name: 'DashBoard'
})




// 获取 user store
// const userStore = useUserStore()


const state = reactive({
    user: {},
    roleGroup: {},
    postGroup: {},
})

function getUser() {
    getUserProfile().then((response) => {
        state.user = response.data
        state.roleGroup = response.roleGroup
        state.postGroup = response.postGroup
        
    })

}



watch(
  () => state.user.userId,
  (newVal) => {
    if (newVal) {
      fetchDiseaseStats()
    }
  }
)





const slides = [
  {
    title: '月季黑斑病',
    // image: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
    image: '/images/BlackSpot (185).jpg',
    description: '及时清理病叶，避免喷水在叶片上，可使用代森锰锌防治。',
  },
  {
    title: '月季霜霉病',
    // image: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
    image: '/images/Augimage_75.jpg',
    description: '保持通风良好，减少湿度，发病初期可喷施霜霉威。',
  },
  {
    title: '月季花叶病',
    // image: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
    image: '/images/Fungus(12).JPG',
    description: '移除病株，控制蚜虫传播，选育抗病品种。',
  },
  {
    title: '月季虫害',
    // image: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
    image: '/images/Insects Infected (383).JPG',
    description: '检查嫩叶和花苞，可用吡虫啉或阿维菌素进行防治。',
  }
]

const mything = [
    {
        avatar: '/images/通知.png',
        template1: '在',
        template2: '上传记录',
    }
]
const diseaseStats = ref({})
const defaultdiseaseStats = {
  type0: 0,
  type1: 0,
  type2: 0,
  type3: 0,
  type4: 0,
  allrecord: 0,
  currentuserrecord: 0
}
const activities = ref([])
const defaultactivities = [
    {
        id: 'trend-1',
        user_name: 'admin',
        updatedAt: '2025-01-01 00:00:00',
        location: '北京',
        predclass: '黑斑病'
    },
    {
        id: 'trend-2',
        user_name: 'admin',
        updatedAt: '2025-01-01 00:00:00',
        location: '北京',
        predclass: '黑斑病'
    },
    {
        id: 'trend-3',
        user_name: 'admin',
        updatedAt: '2025-01-01 00:00:00',
        location: '北京',
        predclass: '黑斑病'
    },
    {
        id: 'trend-4',
        user_name: 'admin',
        updatedAt: '2025-01-01 00:00:00',
        location: '北京',
        predclass: '黑斑病'
    },
    {
        id: 'trend-5',
        user_name: 'admin',
        updatedAt: '2025-01-01 00:00:00',
        location: '北京',
        predclass: '黑斑病'
    },
    {
        id: 'trend-6',
        user_name: 'admin',
        updatedAt: '2025-01-01 00:00:00',
        location: '北京',
        predclass: '黑斑病'
    }
]

const currentUser = {
    avatar: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
    name: '吴彦祖',
    userid: '00000001',
    email: 'antdesign@alipay.com',
    signature: '海纳百川，有容乃大',
    title: '交互专家',
    group: 'FluxAdmin-技术部'
}

// 请求数据
const fetchDiseaseStats = async () => {
  try {
    const idnow = {
       id: state.user.userId
    }
    const res = await request({
      url: '/myvue/disease-stats',
      method: 'post',
      data: idnow
    })
    console.log('响应内容：', res)
    if (res.code === 200) {
      diseaseStats.value = res.data 
    } else {
      diseaseStats.value = defaultdiseaseStats
      message.error(`获取病害统计失败：${res.msg || '服务器返回错误'}`)
    }
  } catch (error) {
    diseaseStats.value = defaultdiseaseStats
    console.error('请求失败:', error)
    message.error('请求病害统计数据失败，请稍后重试')
  }
}

const loadHistoryData = async () => {
  try {
    const res = await request({
      url: '/myvue/HistoryData', // 替换成实际后端地址
      method: 'get',
    //   params: query
    })
    if (res.code === 200) {
      activities.value = res.data
    } else {
      // code 非 200，使用默认数据
      activities.value = defaultActivities
      console.warn('服务器响应失败，已加载默认数据')
    }
  } catch (error) {
    // 网络异常或请求失败
    activities.value = defaultactivities
    console.error('请求失败，已加载默认数据', err)
  }
}

// 页面加载时请求
onMounted(() => {
  getUser();
//   fetchDiseaseStats();
  loadHistoryData();
})



        


const radarContainer = ref()
const radarData = [
    {
        name: '个人',
        label: '引用',
        value: 10
    },
    {
        name: '个人',
        label: '口碑',
        value: 8
    },
    {
        name: '个人',
        label: '产量',
        value: 4
    },
    {
        name: '个人',
        label: '贡献',
        value: 5
    },
    {
        name: '个人',
        label: '热度',
        value: 7
    },
    {
        name: '团队',
        label: '引用',
        value: 3
    },
    {
        name: '团队',
        label: '口碑',
        value: 9
    },
    {
        name: '团队',
        label: '产量',
        value: 6
    },
    {
        name: '团队',
        label: '贡献',
        value: 3
    },
    {
        name: '团队',
        label: '热度',
        value: 1
    },
    {
        name: '部门',
        label: '引用',
        value: 4
    },
    {
        name: '部门',
        label: '口碑',
        value: 1
    },
    {
        name: '部门',
        label: '产量',
        value: 6
    },
    {
        name: '部门',
        label: '贡献',
        value: 5
    },
    {
        name: '部门',
        label: '热度',
        value: 7
    }
]
// let radar
// onMounted(() => {
//     radar = new Radar(radarContainer.value, {
//         data: radarData,
//         xField: 'label',
//         yField: 'value',
//         seriesField: 'name',
//         point: {
//             size: 4
//         },
//         legend: {
//             layout: 'horizontal',
//             position: 'bottom'
//         }
//     })
//     radar.render()
// })

onBeforeUnmount(() => {
//     radar?.destroy?.()
})
</script>

<style scoped lang="less">


// :deep(.slick-slide) {
//   text-align: center;
//   height: 160px;
//   line-height: 160px;
//   background: #00050e;
//   overflow: hidden;
// }
// :deep(.slick-slide h3) {
//   color: #000000;
// }

/* 修改未选中的 dot 颜色 */
// .slick-dots li button {
//   background-color: #bbb !important; /* 设置为灰色 */
//   border: 1px solid #bbb !important;
// }

// /* 修改选中 dot 颜色 */
// .slick-dots li.slick-active button {
//   background-color: #ff6347 !important; /* 设置为橙色 */
//   border: 1px solid #ff6347 !important;
// }
:deep(.slick-dots) {
  bottom: 0px; /* 调整 dots 距离底部的距离 */
}
:deep(.slick-dots) li button {
  background: #6a6b6b;
}
:deep(.slick-dots) li.slick-active button {
  background: #000000;
}
.carousel-wrapper {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px 0;
}

.slide {
  text-align: center;
  background: #fff;
  padding: 20px;
}

.slide-image {
  display: block;
  max-width: 100%;
  max-height: 300px;
  margin: 0 auto 15px;
  border-radius: 8px;
  object-fit: contain;
}

.slide-text h3 {
  font-size: 20px;
  margin-bottom: 8px;
}

.slide-text p {
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}



.textOverflow() {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    word-break: break-all;
}

// mixins for clearfix
// ------------------------
.clearfix() {
    zoom: 1;
    &::before,
    &::after {
        display: table;
        content: ' ';
    }
    &::after {
        clear: both;
        height: 0;
        font-size: 0;
        visibility: hidden;
    }
}

.activitiesList {
    padding: 0 24px 8px 24px;
    .username {
        color: rgba(0, 0, 0, 0.65);
    }
    .event {
        font-weight: normal;
    }
}

.pageHeaderContent {
    display: flex;
    padding: 12px;
    margin-bottom: 24px;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
    .avatar {
        flex: 0 1 72px;
        & > span {
            display: block;
            width: 72px;
            height: 72px;
            border-radius: 72px;
        }
    }
    .content {
        position: relative;
        top: 4px;
        flex: 1 1 auto;
        margin-left: 24px;
        color: rgba(0, 0, 0, 0.45);
        line-height: 22px;
        .contentTitle {
            margin-bottom: 12px;
            color: rgba(0, 0, 0, 0.85);
            font-weight: 500;
            font-size: 20px;
            line-height: 28px;
        }
    }
}

.extraContent {
    .clearfix();

    float: right;
    white-space: nowrap;
    .statItem {
        position: relative;
        display: inline-block;
        padding: 0 32px;
        > p:first-child {
            margin-bottom: 4px;
            color: rgba(0, 0, 0, 0.45);
            font-size: 14px;
            line-height: 22px;
        }
        > p {
            margin: 0;
            color: rgba(0, 0, 0, 0.85);
            font-size: 30px;
            line-height: 38px;
            > span {
                color: rgba(0, 0, 0, 0.45);
                font-size: 20px;
            }
        }
        &::after {
            position: absolute;
            top: 8px;
            right: 0;
            width: 1px;
            height: 40px;
            background-color: #e8e8e8;
            content: '';
        }
        &:last-child {
            padding-right: 0;
            &::after {
                display: none;
            }
        }
    }
}

.members {
    a {
        display: block;
        height: 24px;
        margin: 12px 0;
        color: rgba(0, 0, 0, 0.65);
        transition: all 0.3s;
        .textOverflow();
        .member {
            margin-left: 12px;
            font-size: 14px;
            line-height: 24px;
            vertical-align: top;
        }
        &:hover {
            color: #1890ff;
        }
    }
}

.projectList {
    :deep(.ant-card-meta-description) {
        height: 44px;
        overflow: hidden;
        color: rgba(0, 0, 0, 0.45);
        line-height: 22px;
    }
    .cardTitle {
        font-size: 0;
        a {
            display: inline-block;
            height: 24px;
            margin-left: 12px;
            color: rgba(0, 0, 0, 0.85);
            font-size: 14px;
            line-height: 24px;
            vertical-align: top;
            &:hover {
                color: #1890ff;
            }
        }
    }
    .projectGrid {
        width: 33.33%;
    }
    .projectItemContent {
        display: flex;
        flex-basis: 100%;
        height: 20px;
        margin-top: 8px;
        overflow: hidden;
        font-size: 12px;
        line-height: 20px;
        .textOverflow();
        a {
            display: inline-block;
            flex: 1 1 0;
            color: rgba(0, 0, 0, 0.45);
            .textOverflow();
            &:hover {
                color: #1890ff;
            }
        }
        .datetime {
            flex: 0 0 auto;
            float: right;
            color: rgba(0, 0, 0, 0.25);
        }
    }
}

.datetime {
    color: rgba(0, 0, 0, 0.25);
}

@media screen and (max-width: 1200px) and (min-width: 992px) {
    .activeCard {
        margin-bottom: 24px;
    }
    .members {
        margin-bottom: 0;
    }
    .extraContent {
        margin-left: -44px;
        .statItem {
            padding: 0 16px;
        }
    }
}

@media screen and (max-width: 992px) {
    .activeCard {
        margin-bottom: 24px;
    }
    .members {
        margin-bottom: 0;
    }
    .extraContent {
        float: none;
        margin-right: 0;
        .statItem {
            padding: 0 16px;
            text-align: left;
            &::after {
                display: none;
            }
        }
    }
}

@media screen and (max-width: 768px) {
    .extraContent {
        margin-left: -16px;
    }
    .projectList {
        .projectGrid {
            width: 50%;
        }
    }
}

@media screen and (max-width: 576px) {
    .pageHeaderContent {
        display: block;
        .content {
            margin-left: 0;
        }
    }
    .extraContent {
        .statItem {
            float: none;
        }
    }
}

@media screen and (max-width: 480px) {
    .projectList {
        .projectGrid {
            width: 100%;
        }
    }
}





</style>