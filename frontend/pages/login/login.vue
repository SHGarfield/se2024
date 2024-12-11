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
		<button class="login-button" @click="getUserProfile">登录</button>
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
				avatarUrl: '',
				nickName: ''
			};
		},
		methods: {

			onChooseAvatar(e) {
				console.log(e.detail);
				// wx.saveFile({
				//             tempFilePath: e.detail,
				//             success: function(saveRes) {
				//                 const savedFilePath = saveRes.savedFilePath;
				//                 // 将 savedFilePath 设置为图片的 src
				//                 this.setData({
				//                     avatarUrl: savedFilePath,
				//                 });
				//             },
				//             fail: (err) => {
				//                 console.error('保存文件失败', err);
				//             }
				//         });
				this.avatarUrl = e.detail.avatarUrl;
			},
			//获取用户信息

			async getUserProfile() {
				try {
					const userProfile = await uni.getUserProfile({
						desc: '用于完善用户资料', // 授权
					});
					console.log('用户信息:', userProfile);

					// 将用户信息保存，并调用登录流程
					this.wxLogin(userProfile.userInfo);
				} catch (error) {
					console.error('获取用户信息失败:', error);
				}
			},
			//调用微信登录
			async wxLogin(userInfo) {
				try {
					// 获取微信登录的 code
					const loginRes = await uni.login({
						provider: 'weixin',
					});
					const {
						code
					} = loginRes;
					console.log('微信登录 code:', code);

					// 将 code 发送到后端
					await uni.request({
						url: 'http://111.229.117.144:8000/login/login/',
						method: 'POST',
						data: {
							code: code,
							nickname: userInfo.nickName,
						},
						success: (res) => {
							console.log('登录成功:', res.data);
							getApp().globalData.openid=res.data.openid;
							console.log(getApp().globalData.openid);
							// 处理后端返回的登录信息

						},
						fail: (err) => {
							console.error('登录失败:', err);
						},
					});
					uni.navigateBack();
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