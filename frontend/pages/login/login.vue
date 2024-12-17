<template>
	<view class="container">
		<view class="avatar">
			<text>请输入您的昵称：</text>
		</view>
		<view class="nickname">
			<text>昵称：</text>
			<input class="inputNick" v-model="nickName" placeholder="请输入昵称" maxlength="10" />
		</view>
		<button class="login-button" @click="login">登录</button>
	</view>
</template>

<script>
	import {
		reactive,
		toRefs
	} from 'vue';

	const globalState = reactive({
		openid: ''
	});

	export function useGlobalState() {
		return toRefs(globalState);
	}
	export default {
		data() {
			return {
				nickName: ''
			};
		},
		methods: {
			async uploadUsername(nickname) {
				console.log('nickname:', nickname);
				wx.request({
					url: 'http://111.229.117.144:8000/login/upload_username/', // 后端API地址
					method: 'POST',
					data: {
						openid: getApp().globalData.openid,
						nickname: nickname,
					},
					success: function(res) {
						console.log('nickname成功:', res);
						getApp().globalData.username = nickname;
						console.log('nickname', nickname, 'globalnick', getApp().globalData.username);
					},
					fail: function(err) {
						console.error('nickname失败', err);
					}
				});
			},
			// 点击登录按钮
			async login() {
				try {
					// 将用户信息保存，并调用登录流程
					// await this.wxLogin();
					if (this.nickName === '') {
						wx.showToast({
							title: '昵称不能为空', // 提示内容
							icon: 'error', // 图标类型
							duration: 1500 // 提示框停留时间
						});
					} else {
						await this.uploadUsername(this.nickName);
						wx.showToast({
							title: '更新信息成功', // 提示内容
							icon: 'success', // 图标类型
							duration: 1500 // 提示框停留时间
						});
						setTimeout(function() {
							wx.navigateBack({
								delta: 1
							})
						}, 2000);
					}
				} catch (error) {
					console.error('获取用户信息失败:', error);
				}
			},
		},
	};
</script>

<style>
	.container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	.avatar {
		padding: 380rpx 100rpx 140rpx 100rpx;
		background: #fff;
		font-size: 50rpx;
		font-weight: 600;
		
		
	}

	.avatar button {
		background: #fff;
		line-height: 80rpx;
		height: auto;
		width: auto;
		padding: 20rpx 30rpx;
		margin: 0;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.refreshIcon {
		width: 160rpx;
		height: 160rpx;
		border-radius: 50%;
	}

	.nickname {
		background: #fff;
		padding: 20rpx 30rpx 80rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.nickname input {
		padding-left: 60rpx;
	}

	.login-button {
		background-color: #2a82fe;
		color: white;
		padding: 10px 20px;
		border: none;
		border-radius: 5px;
		font-size: 16px;
	}
</style>