<template>
	<view class="list-section">
		<text class="section-title" @click="updateListData">我的计划</text>
		<scroll-view class="scroll-list" scroll-y :refresher-enabled="true" @refresherrefresh="handleRefresh"  :refresher-triggered="isRefreshing">
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
</template>

<script setup>
	import {
		ref,
		onShow
	} from 'vue'
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
	const handlePlan = (markers) => {
		getApp().globalData.marks = markers;
		console.log(markers);
		wx.switchTab({
			url: '/pages/map/map' // 替换为实际的目标页面路径
		});
	}
	// onShow(() => {
	// 		updateListData();
	// 	});
	const handleRefresh=()=>{
		isRefreshing.value=true;
		updateListData();
	}
	const updateListData = () => {
		wx.request({
			url: 'http://111.229.117.144:8000/dealMarks/getAllMarks/', // 后端API地址
			method: 'POST',
			data: {
				openid: getApp().globalData.openid,
			},
			success: function(res) {
				console.log('我的旅程更新res', res);
				listData.value = res.data.data;
				console.log("res.data:", res.data);
				console.log("listData:", listData.value);
				isRefreshing.value=false;
			},
			fail: function(err) {
				console.error('数据提交失败', err);
				wx.showToast({
				  title: '数据提交失败', // 提示内容
				  icon: 'error', // 图标类型
				  duration: 1000 // 提示框停留时间
				});
				isRefreshing.value=false;
			}
		});
	}
</script>

<style scss>
	.list-section {
		position: relative;
		padding-top: 60rpx;
		/* 为标题留出空间 */
	}

	.section-title {
		position: absolute;
		top: 20rpx;
		left: 30rpx;
		font-size: 32rpx;
		color: #333;
		font-weight: 500;
	}

	.list-content {
		padding: 0 20rpx;
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}

	.scroll-list {
		height: calc(75vh - 120rpx);
		/* 减去用户卡片的高度、tabbar高度和间距 */
		margin-top: 20rpx;
		background-color: #f5f5f5;
		min-height: 100vh;
	}

	.item-card {
		background-color: #ffffff;
		border-radius: 30rpx;
		display: flex;
		flex-direction: column;
	}

	.item-map {
		width: 100%;
		height: 300rpx;
		border-radius: 0 30rpx 0 50rpx;
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