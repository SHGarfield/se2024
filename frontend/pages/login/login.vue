<template>
	<view class="container">
		<view class="avatar">
			<button type="balanced" open-type="chooseAvatar" @chooseavatar="onChooseAvatar">
				<image :src="avatarUrl" class="refreshIcon"></image>
			</button>
		</view>
		<view class="nickname">
			<text>昵称：</text>
			<input class="inputNick" v-model="nickName" placeholder="请输入昵称" />
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
				avatarUrl: '../../static/un_login.jpg',
				nickName: ''
			};
		},
		methods: {
			//选择头像
			onChooseAvatar(e) {
				console.log(e.detail);
				this.avatarUrl = e.detail.avatarUrl;
			},

			// 上传头像（点击登陆后调用）
			async uploadAvatar(filePath) {
				return new Promise((resolve, reject) => {
					uni.uploadFile({
						url: "http://111.229.117.144:8000/login/upload_avatar/", // 确保 URL 是正确的
						filePath, // 临时文件路径
						name: "avatar", // 后端接收文件的字段名
						formData: {
							openid: getApp().globalData.openid,
						},
						success: (uploadFileRes) => {
							console.log("上传成功", uploadFileRes);
							const response = JSON.parse(uploadFileRes.data);
							if (response.code === 200) {
								uni.showToast({
									title: "上传成功",
									icon: "success",
								});
								setTimeout(function() {
									uni.navigateBack({
										delta: 1
									})
								}, 1000);
								resolve();
							} else {
								uni.showToast({
									title: "上传失败",
									icon: "error",
								});
								reject();
							}
						},
						fail: (error) => {
							console.error("上传失败", error);
							uni.showToast({
								title: "上传失败",
								icon: "error",
							});
							reject(error);
						},
					});
				});
			},


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
						getApp().globalData.nickName=this.nickname;
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
					if (this.avatarUrl === '../../static/un_login.jpg' || this.nickName === '') {
						wx.showToast({
							title: '缺少头像或昵称', // 提示内容
							icon: 'error', // 图标类型
							duration: 1500 // 提示框停留时间
						});
					} else {
						await this.uploadUsername(this.nickName);
						await this.uploadAvatar(this.avatarUrl);
						getApp().globalData.avatar_url = this.avatarUrl;
						console.log("getapp.aavatar:", getApp().globalData.avatar_url);
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
		padding: 80rpx 0 40rpx;
		background: #fff;
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