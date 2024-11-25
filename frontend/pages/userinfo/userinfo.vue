<template>
  <view class="user-info">
    <!-- 顶部导航 -->
    <view class="header">
      <view class="back" @tap="goBack">
        <uni-icons type="left" size="30"></uni-icons>
      </view>
      <text class="title">编辑资料</text>
      <text class="preview">预览</text>
    </view>

    <!-- 头像区域 -->
    <view class="avatar-section">
      <image class="avatar" :src="userInfo.avatar || '/static/logo.png'" mode="aspectFill" />
    </view>

    <!-- 信息列表 -->
    <view class="info-list">
      <view class="info-item" @tap="handleEdit('nickname')">
        <text class="label">名字</text>
        <view class="value">
          <text>{{ userInfo.nickname }}</text>
          <text class="iconfont icon-right"></text>
        </view>
      </view>

      <view class="info-item">
        <text class="label">小红书号</text>
        <view class="value">
          <text>{{ userInfo.redId }}</text>
          <text class="iconfont icon-right"></text>
        </view>
      </view>

      <view class="info-item" @tap="handleEdit('background')">
        <text class="label">背景图</text>
        <view class="value">
          <image class="bg-preview" :src="userInfo.background" mode="aspectFill" />
          <text class="iconfont icon-right"></text>
        </view>
      </view>
    </view>

    <view class="info-list">
      <view class="info-item" @tap="handleEdit('intro')">
        <text class="label">简介</text>
        <view class="value">
          <text>{{ userInfo.intro || '介绍一下自己' }}</text>
          <text class="iconfont icon-right"></text>
        </view>
      </view>
    </view>

    <view class="info-list">
      <view class="info-item" @tap="handleEdit('gender')">
        <text class="label">性别</text>
        <view class="value">
          <text>{{ userInfo.gender === 1 ? '男' : '女' }}</text>
          <text class="iconfont icon-right"></text>
        </view>
      </view>

      <view class="info-item" @tap="handleEdit('birthday')">
        <text class="label">生日</text>
        <view class="value">
          <text>{{ userInfo.birthday || '选择生日' }}</text>
          <text class="iconfont icon-right"></text>
        </view>
      </view>

      <view class="info-item" @tap="handleEdit('region')">
        <text class="label">地区</text>
        <view class="value">
          <text>{{ userInfo.region || '选择所在的地区' }}</text>
          <text class="iconfont icon-right"></text>
        </view>
      </view>

      <view class="info-item" @tap="handleEdit('occupation')">
        <text class="label">职业</text>
        <view class="value">
          <text>{{ userInfo.occupation || '选择职业' }}</text>
          <text class="iconfont icon-right"></text>
        </view>
      </view>

      <view class="info-item" @tap="handleEdit('school')">
        <text class="label">学校</text>
        <view class="value">
          <text>{{ userInfo.school || '选择学校' }}</text>
          <text class="iconfont icon-right"></text>
        </view>
      </view>
    </view>

    <!-- 保存按钮 -->
    <view class="save-btn" @tap="handleSave">保存</view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const userInfo = ref({
  nickname: 'guyfawkes',
  redId: '10367866169',
  avatar: '/static/logo.png',
  background: '/static/logo.png',
  intro: '介绍一下自己',
  gender: 1,
  birthday: '',
  region: '',
  occupation: '',
  school: ''
})

function goBack(){
  uni.navigateBack()
}

const handleEdit = (type) => {
  // 处理不同类型的编辑操作
  console.log('编辑', type)
}

const handleSave = () => {
  // 保存用户信息
  console.log('保存用户信息')
}
</script>

<style lang="scss" scoped>
.user-info {
  min-height: 100vh;
  background-color: #f8f8f8;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 15px;
  height: 44px;
  background-color: #fff;
  padding-top: var(--status-bar-height); // 添加这行
  
  .title {
    font-size: 16px;
    font-weight: 500;
  }
  
  .preview {
    font-size: 14px;
    color: #333;
  }
}

.avatar-section {
  display: flex;
  justify-content: center;
  padding: 30px 0;
  background-color: #fff;
  
  .avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
  }
}

.info-list {
  margin-top: 10px;
  background-color: #fff;
  
  .info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #f5f5f5;
    
    .label {
      color: #333;
      font-size: 14px;
    }
    
    .value {
      display: flex;
      align-items: center;
      color: #666;
      font-size: 14px;
      
      .icon-right {
        margin-left: 5px;
        color: #999;
      }
      
      .bg-preview {
        width: 40px;
        height: 40px;
        border-radius: 4px;
        margin-right: 5px;
      }
    }
  }
}

.save-btn {
  position: fixed;
  bottom: 20px;
  left: 15px;
  right: 15px;
  height: 44px;
  line-height: 44px;
  text-align: center;
  background-color: #ff2442;
  color: #fff;
  border-radius: 22px;
  font-size: 16px;
}
</style>