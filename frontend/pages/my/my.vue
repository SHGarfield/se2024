<template>
  <view class="my">
    <!-- 未登录状态 -->
    <view class="user-card" v-if=!isLogin.value>
      <view class="user-info">
        <!-- 左侧头像 -->
        <view class="avatar-box">
          <image class="avatar" src="/static/logo.png" mode="aspectFill"></image>
        </view>
        <!-- 中间信息列 -->
        <view class="info-column">
          <text class="username">未登录</text>
          <view class="sub-info" @click="handleLogin">
            <text class="sub-text">点击登录账号</text>
          </view>
        </view>
        <!-- 右侧设置按钮 -->
        <view class="setting-box" @click="updateListData">
          <text class="setting-text">设置</text>
        </view>
      </view>
    </view>

    <!-- 已登录状态 -->
    <view class="user-card" v-else>
      <view class="user-info">
        <!-- 左侧头像 -->
        <view class="avatar-box">
          <image class="avatar" src="/static/logo.png" mode="aspectFill"></image>
        </view>
        <!-- 中间信息列 -->
        <view class="info-column">
          <text class="username">用户名称</text>
          <view class="sub-info" @click="handleEdit">
            <text class="sub-text">修改个人信息</text>
          </view>
        </view>
        <!-- 右侧设置按钮 -->
        <view class="setting-box" @click="handleOption">
          <text class="setting-text">设置</text>
        </view>
      </view>
    </view>
	<view class="list-section">
		<text class="section-title">我的计划</text>
		<scroll-view class="scroll-list" scroll-y>
		  <view class="list-content">
		    <view class="item-card" v-for="(item, index) in listData" :key="index" @click="handlePlan">
		      <image class="item-image" :src="item.image" mode="aspectFill"></image>
		      <text class="item-title">{{item.title}}</text>
		    </view>
		  </view>
		</scroll-view>
	</view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const isLogin = ref(false)  // 自动暴露给模板使用
function handleEdit(){
  uni.navigateTo({
    url: '/pages/userinfo/userinfo'
  })
}
function handleLogin(){
  uni.navigateTo({
    url: '/pages/login/login'
  })
}
function handleOption(){
  uni.navigateTo({
  	url: '/pages/option/option'
  })
}
function handlePlan(){
  uni.switchTab({
  	url: '/pages/find/find'
  })
}
const listData = ref([
  { image: '/static/logo.png', title: '标题1' },
  { image: '/static/logo.png', title: '标题2' },
  { image: '/static/logo.png', title: '标题3' },
  { image: '/static/logo.png', title: '标题4' },
  { image: '/static/logo.png', title: '标题5' },
])
// onShow(() => {
// 		updateListData();
// 	});
const updateListData=()=>{
	wx.request({
		url: 'http://111.229.117.144:8000/dealMarks/getMarks/', // 后端API地址
		method: 'POST',
		data: {
			openid:getApp().globalData.openid,
		},
		success: function(res) {
			console.log('我的旅程更新res', res);
			listData.value=res.data.data;
			console.log("res.data:",res.data);
			console.log("listData:",listData.value);
		},
		fail: function(err) {
			console.error('数据提交失败', err);
		}
	});
}
</script>

<style lang="scss">
.my {
  background-color: #f5f5f5;
  min-height: 100vh;
  
  .user-card {
    background-color: #2a82fe;
    height: 25vh;
    position: relative;
    
    .user-info {
      display: flex;
      align-items: center;
      padding: 0 30rpx;
      position: absolute;
      bottom: 60rpx;
      width: 100%;
      box-sizing: border-box;
      
      .avatar-box {
        .avatar {
          width: 140rpx;
          height: 140rpx;
          border-radius: 50%;
          border: 4rpx solid #ffffff;
        }
      }
      
      // 新增 info-column 样式，用于垂直排列用户名和子信息
      .info-column {
        flex: 1;
        margin-left: 30rpx;
        display: flex;
        flex-direction: column;
        justify-content: center;
        
        .username {
          color: #ffffff;
          font-size: 36rpx;
          font-weight: 500;
          margin-bottom: 10rpx;
        }
        
        .sub-info {
          .sub-text {
            color: rgba(255, 255, 255, 0.9);
            font-size: 28rpx;
          }
        }
      }
      
      .setting-box {
        .setting-text {
          color: #ffffff;
          font-size: 28rpx;
          padding: 10rpx 20rpx;
        }
      }
    }
  }
  .list-section{
	  position: relative;
	      padding-top: 60rpx; // 为标题留出空间
	      
	      .section-title {
	        position: absolute;
	        top: 20rpx;
	        left: 30rpx;
	        font-size: 32rpx;
	        color: #333;
	        font-weight: 500;
	      }
		  
   .scroll-list {
      height: calc(75vh - 120rpx); // 减去用户卡片的高度、tabbar高度和间距
      margin-top: 20rpx;
      
      .list-content {
        padding: 0 20rpx;
        display: flex;
        flex-direction: column;
        gap: 20rpx;
        
        .item-card {
          background-color: #ffffff;
          border-radius: 12rpx;
          padding: 20rpx;
          display: flex;
          flex-direction: column;
          align-items: center;
          
          .item-image {
            width: 100%;
            height: 300rpx;
            border-radius: 8rpx;
          }
          
          .item-title {
            margin-top: 16rpx;
            font-size: 28rpx;
            color: #333;
          }
        }
      }
    }
	}
}
</style>