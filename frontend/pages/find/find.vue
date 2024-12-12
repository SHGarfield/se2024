<template>
	<view class="list-section">
		<text class="section-title" @click="updateListData">我的计划</text>
		<scroll-view class="scroll-list" scroll-y>
			<view class="list-content">
				<view class="item-card" v-for="(item, index) in listData" :key="index" @click="handlePlan">
					<image class="item-image" :src="item.image" mode="aspectFill"></image>
					<text class="item-title">{{item.title}}</text>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script setup>
import { ref } from 'vue'

const listData = ref([{ image: '/static/logo.png', title: '标题1' },
  { image: '/static/logo.png', title: '标题2' },
  { image: '/static/logo.png', title: '标题3' },
  { image: '/static/logo.png', title: '标题4' },
  { image: '/static/logo.png', title: '标题5' },
])
// onShow(() => {
// 		updateListData();
// 	});
const updateListData=()=>{
	wx.request({
		url: 'http://111.229.117.144:8000/dealMarks/getMarks/', // 后端API地址
		method: 'POST',
		data: {
			openid:getApp().globalData.openid,
		},
		success: function(res) {
			console.log('我的旅程更新res', res);
			listData.value=res.data.data;
			console.log("res.data:",res.data);
			console.log("listData:",listData.value);
		},
		fail: function(err) {
			console.error('数据提交失败', err);
		}
	});
}
</script>

<style scss>
	/* .list-section {
		position: relative;
		padding-top: 60rpx; // 为标题留出空间
	
		.section-title {
			position: absolute;
			top: 20rpx;
			left: 30rpx;
			font-size: 32rpx;
			color: #333;
			font-weight: 500;
		}
	
		.scroll-list {
			height: calc(75vh - 120rpx); // 减去用户卡片的高度、tabbar高度和间距
			margin-top: 20rpx;
			background-color: #f5f5f5;
			min-height: 100vh;
	
			.list-content {
				padding: 0 20rpx;
				display: flex;
				flex-direction: column;
				gap: 20rpx;
	
				.item-card {
					background-color: #ffffff;
					border-radius: 12rpx;
					padding: 20rpx;
					display: flex;
					flex-direction: column;
					align-items: center;
	
					.item-image {
						width: 100%;
						height: 300rpx;
						border-radius: 8rpx;
					}
	
					.item-title {
						margin-top: 16rpx;
						font-size: 28rpx;
						color: #333;
					}
				}
			}
		}
	}
	 */
</style>