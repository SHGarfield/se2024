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
			<scroll-view class="scroll-list" scroll-y :refresher-enabled="true" @refresherrefresh="handleRefresh"
				:refresher-triggered="isRefreshing">
				<view class="list-content">
					<view class="item-card" v-for="(item, index) in listData" :key="index"
						@click="() => handlePlan(item.marks)">
						<text class="item-title">{{item.title}}</text>
						<text class="item-content">{{item.content}}</text>
						<!-- <image class="item-image" :src="item.image" mode="aspectFill"></image> -->
						<map class="item-map" :markers="item.marks" :include-points="item.marks"
							style="pointer-events: none;"></map>
					</view>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script setup>
	import {
		ref
	} from 'vue'
	import {
		onShow
	} from '@dcloudio/uni-app';
	const isRefreshing = ref(false);
	const listData = ref([{
			image: '/static/logo.png',
			title: '标题1'
		},
		{
			image: '/static/logo.png',
			title: '标题2',
			content: "这里是中文内容谭工后方弄i给i哦能够对弄i给我答复农人辜负你的哦个肉共哦代购哦i工具都是给弄"
		},
		{
			image: '/static/logo.png',
			title: '标题3'
		},
		{
			image: '/static/logo.png',
			title: '标题4'
		},
		{
			image: '/static/logo.png',
			title: '标题5'
		},
	])
	// const handlePlan = (markers) => {
	// 	getApp().globalData.marks = markers;
	// 	console.log(markers);
	// 	wx.switchTab({
	// 		url: '/pages/map/map' // 替换为实际的目标页面路径
	// 	});
	// }
	onShow(() => {
		updateListData();
	});
	const handleRefresh = () => {
		isRefreshing.value = true;
		updateListData();
	}
	const updateListData = () => {
		wx.request({
			url: 'http://111.229.117.144:8000/dealMarks/getMarks/', // 后端API地址
			method: 'POST',
			data: {
				openid: getApp().globalData.openid,
			},
			success: function(res) {
				console.log('我的旅程更新res', res);
				listData.value = res.data.data;
				console.log("res.data:", res.data);
				console.log("listData:", listData.value);
				isRefreshing.value = false;
			},
			fail: function(err) {
				console.error('数据提交失败', err);
				wx.showToast({
					title: '数据提交失败', // 提示内容
					icon: 'error', // 图标类型
					duration: 1000 // 提示框停留时间
				});
				isRefreshing.value = false;
			}
		});
	}
	const isLogin = ref(false) // 自动暴露给模板使用
	function handleEdit() {
		uni.navigateTo({
			url: '/pages/userinfo/userinfo'
		})
	}

	function handleLogin() {
		uni.navigateTo({
			url: '/pages/login/login'
		})
	}

	function handleOption() {
		uni.navigateTo({
			url: '/pages/option/option'
		})
	}

	// function handlePlan() {
	// 	uni.switchTab({
	// 		url: '/pages/find/find'
	// 	})
	// }
	
</script>

<style lang="scss">
	.my {
		background-color: #f5f5f5;
		min-height: 100vh;
	}

	.my .user-card {
		background-color: #2a82fe;
		height: 25vh;
		position: relative;
	}

	.my .user-card .user-info {
		display: flex;
		align-items: center;
		padding: 0 30rpx;
		position: absolute;
		bottom: 60rpx;
		width: 100%;
		box-sizing: border-box;
	}

	.my .user-card .user-info .avatar-box .avatar {
		width: 140rpx;
		height: 140rpx;
		border-radius: 50%;
		border: 4rpx solid #ffffff;
	}

	.my .user-card .user-info .info-column {
		flex: 1;
		margin-left: 30rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	.my .user-card .user-info .info-column .username {
		color: #ffffff;
		font-size: 36rpx;
		font-weight: 500;
		margin-bottom: 10rpx;
	}

	.my .user-card .user-info .info-column .sub-info .sub-text {
		color: rgba(229, 255, 255, 0.9);
		font-size: 28rpx;
	}

	.my .user-card .user-info .setting-box .setting-text {
		color: #ffffff;
		font-size: 28rpx;
		padding: 10rpx 20rpx;
	}

	.my .list-section {
		position: relative;
		padding-top: 60rpx;
	}

	.my .list-section .section-title {
		position: absolute;
		top: 20rpx;
		left: 30rpx;
		font-size: 32rpx;
		color: #333;
		font-weight: 500;
	}

	.my .scroll-list {
		height: calc(75vh - 120rpx);
		margin-top: 20rpx;
		background-color: rgb(239,239,239);
	}

	.my .scroll-list .list-content {
		padding: 0 20rpx;
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}

	.item-card {
		background-color: #ffffff;
		border-radius: 30rpx;
		display: flex;
		flex-direction: column;
		box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
		overflow:hidden;
	}
	
	.item-map {
		width: 100%;
		height: 300rpx;
	}
	
	.item-title {
		padding: 20rpx 20rpx 5rpx 20rpx;
		font-size: 40rpx;
		font-weight: 800;
	}
	
	.item-content {
		padding: 0 20rpx;
		font-size: 35rpx;
		/* font-weight: 800; */
	}
</style>