<template>
  <view class="container">
    <button class="login-button" @click="getUserProfile">一键登录</button>
  </view>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    // 第一步：获取用户信息
    async getUserProfile() {
      try {
        const userProfile = await uni.getUserProfile({
          desc: '用于完善用户资料', // 授权说明
        });
        console.log('用户信息:', userProfile);

        // 将用户信息保存，并调用登录流程
        this.wxLogin(userProfile.userInfo);
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    },
    // 第二步：调用微信登录
    async wxLogin(userInfo) {
      try {
        // 获取微信登录的 code
        const loginRes = await uni.login({
          provider: 'weixin',
        });
        const { code } = loginRes;
        console.log('微信登录 code:', code);

        // 将 code 发送到后端
        await uni.request({
          url: 'http://111.229.117.144:8000/login/login/', 
          method: 'POST',
          data: {
            code:code,
			nickname:userInfo.nickName,
          },
          success: (res) => {
            console.log('登录成功:', res.data);
            // 处理后端返回的登录信息，比如存储 Token
            uni.setStorageSync('token', res.data.token);
          },
          fail: (err) => {
            console.error('登录失败:', err);
          },
        });
      } catch (error) {
        console.error('微信登录失败:', error);
      }
    },
  },
};
</script>

<style>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-button {
  background-color: #1aad19;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
}
</style>
