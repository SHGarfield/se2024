<template>
	<view class="list-section">
		<scroll-view class="scroll-list" scroll-y :refresher-enabled="true" @refresherrefresh="handleRefresh"  :refresher-triggered="isRefreshing">
			<view v-if="listData.length === 0" class="empty-message">这里空空如也</view>
			<view v-else class="list-content">
				<view class="item-card" v-for="(item, index) in listData" :key="index"
					@click="() => handlePlan(item)">
					<text class="item-title">{{item.title}}</text>
					<text class="item-content" :overflow="ellipsis" :max-lines="4">{{item.content}}</text>
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
		ref
	} from 'vue'
	import { onShow } from '@dcloudio/uni-app';
	const isRefreshing = ref(false);
	const listData = ref([]);
	const handlePlan = (itemData) => {
		getApp().globalData.itemData = itemData;
		console.log("itemData",itemData);
		wx.navigateTo({
			url:'/pages/find_detail/find_detail'
		});
	}
	onShow(() => {
			updateListData();
		});
	const handleRefresh=()=>{
		isRefreshing.value=true;
		updateListData();
	}
	const updateListData = () => {
		wx.request({
			url: 'http://111.229.117.144:8000/dealMarks/getAllMarks/', // 后端API地址
			method: 'GET',
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
	.empty-message{
		margin-top: 50%;
		 text-align: center;
		 color:gray;
	}
	.list-section {
		position: relative;
		/* padding-top: 60rpx; */
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
		padding-top: 2vh;
		height: 100vh;
		/* 减去用户卡片的高度、tabbar高度和间距 */
		/* margin-top: 20rpx; */
		background-color: #f5f5f5;
		/* min-height: 100vh; */
	}

	.item-card {
		background-color: #ffffff;
		border-radius: 30rpx;
		display: flex;
		flex-direction: column;
		box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
		overflow:hidden;
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