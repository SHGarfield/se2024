<template>
	<view class="my">
		<!-- 未登录状态 -->
		<view class="user-card" v-if="!isLogin">
			<view class="user-info">
				<!-- 中间信息列 -->
				<view class="info-column">
					<text class="username">未登录</text>
					<view class="sub-info" @click="handleLogin">
						<text class="sub-text">点击登录账号</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 已登录状态 -->
		<view class="user-card" v-else>
			<view class="user-info">
				<!-- 中间信息列 -->
				<view class="info-column">
					<text class="username">{{nickname}}</text>
					<view class="sub-info" @click="handleEdit">
						<text class="sub-text">修改个人信息</text>
					</view>
				</view>
				<!-- 右侧设置按钮 -->
				<view class="setting-box" @click="logout">
					<text class="setting-text">退出登录</text>
				</view>
			</view>
		</view>
		<view class="list-section">
			<view>
				<text class="section-title">我的计划</text>
			</view>

			<view class="route-kind">
				<text :class="{ 'published-route-active': isPublishedActive, 'published-route': !isPublishedActive }"
					@click="setActive('published')">
					已发布
				</text>
				<text :class="{ 'private-route-active': isPrivateActive, 'private-route': !isPrivateActive }"
					@click="setActive('private')">
					草稿箱
				</text>
			</view>

			<swiper class="swiper" :indicator-dots="false" :current="swiperPage">
				<swiper-item>
					<scroll-view class="scroll-list" scroll-y :refresher-enabled="true"
						@refresherrefresh="handleRefresh" :refresher-triggered="isRefreshing">
						<view v-if="!isLogin" class="empty-message">请"登录"后使用</view>
						<view v-else-if="listData.length === 0" class="empty-message">这里空空如也</view>
						<view v-else class="list-content">
							<view class="item-card" v-for="(item, index) in listData" :key="index"
								@click="() => handlePlan(item)">
								<text class="item-title">{{item.title}}</text>
								<text class="item-content">{{item.content}}</text>
								<!-- <image class="item-image" :src="item.image" mode="aspectFill"></image> -->
								<map class="item-map" :markers="item.marks" :include-points="item.marks"
									:enable-zoom='false' :enable-scroll="false"></map>
							</view>
						</view>
					</scroll-view>
				</swiper-item>
				<swiper-item>
					<scroll-view class="scroll-list" scroll-y :refresher-enabled="true"
						@refresherrefresh="handleRefresh" :refresher-triggered="isRefreshing">
						<view v-if="!isLogin" class="empty-message">请"登录"后使用</view>
						<view v-else-if="listData.length === 0" class="empty-message">这里空空如也</view>
						<view v-else class="list-content">
							<view class="item-card" v-for="(item, index) in listData" :key="index"
								@click="() => handlePlan(item)">
								<text class="item-title">{{item.title}}</text>
								<text class="item-content">{{item.content}}</text>
								<!-- <image class="item-image" :src="item.image" mode="aspectFill"></image> -->
								<map class="item-map" :markers="item.marks" :include-points="item.marks"
									style="pointer-events: none;"></map>
							</view>
						</view>
					</scroll-view>
				</swiper-item>
			</swiper>
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
	const swiperPage = ref(1);
	const isRefreshing = ref(false);
	// const avatar_url = ref("../../static/un_login.jpg");
	const nickname = ref("");
	const isLogin = ref(false); // 自动暴露给模板使用
	const isprivate = ref(true);
	const listData = ref([])
	const isPublishedActive = ref(false);
	const isPrivateActive = ref(true);

	const setActive = (type) => {
		if (type === 'published') { //点击“已发布”按钮
			//调整按钮样式
			isPublishedActive.value = true;
			isPrivateActive.value = false;
			switch_to_publish();
		} else { //点击“草稿箱”按钮
			isPrivateActive.value = true;
			isPublishedActive.value = false;
			switch_to_private();
		}
	};

	//swiper切换到“已发布”
	const switch_to_publish = () => {
		swiperPage.value = 0;
		isprivate.value = false;
		updateListData();
	};

	//swiper切换到“草稿箱”
	const switch_to_private = () => {
		swiperPage.value = 1;
		isprivate.value = true;
		updateListData();
	};
	const handlePlan = (item) => {
		getApp().globalData.itemData = item;
		console.log("item:", item);
		wx.navigateTo({
			url: '/pages/my_map_detail/my_map_detail' // 替换为实际的目标页面路径
		});
	}
	onShow(() => {
		isLogin.value = getApp().globalData.isLogin;
		nickname.value = getApp().globalData.username;
		updateListData();
		// console.log("globalavatar(onshow)", getApp().globalData.avatar_url);
		// if (getApp().globalData.avatar_url) {
		// 	avatar_url.value = getApp().globalData.avatar_url;
		// 	nickname.value = getApp().globalData.username;
		// 	isLogin.value = true;
		// }
	});
	const handleRefresh = () => {
		isRefreshing.value = true;
		console.log("openid:", getApp().globalData.openid);
		updateListData();
	}
	const updateListData = () => {
		wx.request({
			url: 'http://111.229.117.144:8000/dealMarks/getMarks/', // 后端API地址
			method: 'POST',
			data: {
				openid: getApp().globalData.openid,
				isprivate: isprivate.value,
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

	function handleEdit() {
		uni.navigateTo({
			url: '/pages/login/login'
		})
	}

	function handleLogin() {
		if (getApp().globalData.username) {
			isLogin.value = true;
			nickname.value = getApp().globalData.username;
			getApp().globalData.isLogin=true;
		} else {
			uni.navigateTo({
				url: '/pages/login/login'
			})
		}
	}

	function logout() {
		isLogin.value = false;
		getApp().globalData.isLogin=false;
	}
</script>

<style lang="scss">
	.route-kind {
		// border: 1px solid black;
		display: flex;
		justify-content: center;
		/* 水平居中 */
		align-items: center;
	}

	.published-route,
	.private-route {
		border-bottom: 2px solid transparent;
		/* 初始化边框 */
		// font-weight: normal;
		font-weight: bold;
		color: gray;
		font-size: 35rpx;
		/* 初始化字体权重 */
		margin: 0 10rpx;
	}

	.published-route-active,
	.private-route-active {
		border-bottom: 2px solid blue;
		/* 点击后的边框颜色 */
		font-weight: bold;
		font-size: 35rpx;
		margin: 0 10rpx;
		/* 字体加粗 */
	}

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

	.username {
		color: #ffffff;
		font-size: 50rpx;
		font-weight: 1000;
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

	.list-section {
		position: relative;
		padding-top: 60rpx;
	}

	.section-title {
		position: absolute;
		top: 20rpx;
		left: 30rpx;
		font-size: 32rpx;
		color: #333;
		font-weight: 500;
	}

	.scroll-list {
		height: calc(75vh - 120rpx);
		margin-top: 20rpx;
		background-color: rgb(239, 239, 239);
	}
	.empty-message{
		margin-top: 50%;
		 text-align: center;
		 color:gray;
	}
	.swiper {
		height: calc(75vh - 120rpx);
		margin-top: 20rpx;
		background-color: rgb(239, 239, 239);
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
		overflow: hidden;
	}

	.item-map {
		width: 100%;
		height: 300rpx;
	}

	.item-title {
		padding: 20rpx 20rpx 5rpx 20rpx;
		font-size: 40rpx;
		font-weight: 800;
		
		 display: -webkit-box;
		  -webkit-box-orient: vertical;
		  -webkit-line-clamp: 1; /* 限制文本的行数为4行 */
		  overflow: hidden;
	}

	.item-content {
		padding: 0 20rpx;
		font-size: 35rpx;
		
		 display: -webkit-box;
		  -webkit-box-orient: vertical;
		  -webkit-line-clamp: 3; /* 限制文本的行数为4行 */
		  overflow: hidden;
		/* font-weight: 800; */
	}
</style>