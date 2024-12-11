<template>
  <view class="settings-page">
    <view class="header">
      <view class="back-icon" @tap="goBack">
        <uni-icons type="left" size="30"></uni-icons>
      </view>
      <text class="title">设置</text>
    </view>
    
    <!-- 只保留退出登录按钮 -->
    <view class="bottom-buttons">
        <button class="logout" @tap="logout">退出登录</button>
    </view>
    </view>
</template>
    
    <script setup>
    import { ref } from 'vue'
    
    const settingItems = ref([
      { title: '账号与安全', icon: 'icon-account' },
      { title: '通用设置', icon: 'icon-general' },
      { title: '通知设置', icon: 'icon-notification' },
      { title: '隐私设置', icon: 'icon-privacy' },
      { title: '内容偏好调节', icon: 'icon-preference' },
      { title: '帮助与客服', icon: 'icon-support' },
    ])
    
    const goBack = () => {
      uni.navigateBack()
    }
    
    const handleItemClick = (item) => {
      // 处理点击事件
    }
    
    const logout = () => {
      // 退出登录逻辑
    }
    </script>
    
    <style lang="scss">
    .settings-page {
      min-height: 100vh;
      background-color: #f8f8f8;
      
      .header {
        display: flex;
        align-items: center;
        padding: var(--status-bar-height) 15px 0;
        height: calc(44px + var(--status-bar-height));
        background-color: #fff;
        
        .back-icon {
          padding: 10px;
          margin-left: -10px;
        }
        
        .title {
          flex: 1;
          text-align: center;
          font-size: 16px;
          font-weight: 500;
        }
      }
      
      .settings-list {
        margin-top: 10px;
        
        .settings-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 15px;
          height: 54px;
          background-color: #fff;
          border-bottom: 0.5px solid #f0f0f0;
          
          .item-left {
            display: flex;
            align-items: center;
            
            .iconfont {
              font-size: 22px;
              margin-right: 12px;
              color: #333;
            }
            
            .item-text {
              font-size: 15px;
              color: #333;
            }
          }
          
          .item-right {
            display: flex;
            align-items: center;
            
            .value-text {
              font-size: 14px;
              color: #999;
              margin-right: 4px;
            }
            
            .icon-arrow-right {
              font-size: 16px;
              color: #ccc;
            }
          }
        }
      }
      
      .bottom-buttons {
        padding: 20px 15px;
        
        .logout {
          width: 100%;
          height: 44px;
          border-radius: 22px;
          font-size: 15px;
          background-color: #fff;
          color: #333;
        }
      }
    }
    </style>