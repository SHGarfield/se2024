<template>
	<view class="list-section">
		<!-- <scroll-view class="scroll-list" scroll-y :refresher-enabled="true" @refresherrefresh="handleRefresh" :refresher-triggered="isRefreshing"> -->
		<scroll-view class="scroll-list" scroll-y>
			<view class="list-content">
				<map class="item-map" :markers="itemData.marks" :include-points="itemData.marks" :polyline="polyline"></map>
				<view class="item-text">
					<text class="item-title">{{itemData.title}}</text>
					<text class="item-content">{{itemData.content}}</text>
					<text class="modified-time">{{itemData.modified_time}}</text>
				</view>

			</view>
		</scroll-view>
		<view class="bottom-bar">
			<button class="save-route-button" @click="saveRoute">保存路线</button>
		</view>
	</view>
</template>


<script setup>
	import {
		ref,onMounted 
	} from 'vue'

	import {
		onShow
	} from '@dcloudio/uni-app';
	// const isRefreshing = ref(false);
	const itemData = ref({});
	// const handlePlan = (markers) => {
	// 	getApp().globalData.marks = markers;
	// 	console.log(markers);
	// 	wx.switchTab({
	// 		url: '/pages/map/map' // 替换为实际的目标页面路径
	// 	});
	// }
	const modified_time = ref("");
	// const format_modified_time = () => {
	// 	let time = getApp().globalData.modified_time;
	// 	// 移除'T'和'Z'
	// 	modified_time.value = time.replace(/[TZ]/g, ' ');

	// };
	//重设time的格式
	const format_modified_time =() => {
	  itemData.value.modified_time='编辑于'+itemData.value.modified_time.replace(/T/,'  ').replace(/Z/,'');
	};
	const polyline = ref([]);
	import {
		setupQQMap
	} from '../../libs/functions/setupQQMap.js';
	
	const qqmapsdk = ref(null);
	//每次打开界面都获取帖子内容
	onShow(() => {
		setupQQMap(qqmapsdk);
		getItemData();
	});
	//获取帖子内容
	const getItemData = () => {
		itemData.value = getApp().globalData.itemData;
		console.log("itemData:(edit)", itemData.value);
		planRoute();
	};
	onMounted(()=>{
		format_modified_time();
	});
	const saveRoute = () => {
		//检查是否登录
		if (getApp().globalData.isLogin) {
			//已登录
			submitData();
		} else {
			//未登录，则展示登录提示框
			wx.showModal({
				title: '未登录', // 提示框的标题
				content: '登录后才可使用该功能', // 提示框的内容
				confirmText: '去登录', // 自定义确定按钮的文本
				cancelText: '取消',
				success: function(res) {
					if (res.confirm) {
						console.log('用户点击确定');
						wx.switchTab({
							url: '/pages/my/my'
						});
						// 在这里编写点击确定后想要执行的代码
					} else if (res.cancel) {
						console.log('用户点击取消');
						// 在这里编写点击取消后想要执行的代码
					}
				}
			});
		}
	};

	const submitData = () => {
		wx.request({
			url: 'http://111.229.117.144:8000/dealMarks/addMarks/', // 后端API地址
			method: 'POST',
			data: {
				openid: getApp().globalData.openid,
				title: getApp().globalData.itemData.title,
				content: getApp().globalData.itemData.content,
				marks: getApp().globalData.itemData.marks,
				isprivate: true,
			},
			success: function(res) {
				console.log('数据提交成功', res);
				wx.showToast({
					title: '保存成功', // 提示内容
					icon: 'success', // 图标类型
					duration: 1000 // 提示框停留时间
				});
				setTimeout(function() {
					backToMap();
				}, 1000);
			},
			fail: function(err) {
				console.error('数据提交失败', err);
				wx.showToast({
					title: '上传失败', // 提示内容
					icon: 'error', // 图标类型
					duration: 1000 // 提示框停留时间
				});
			}
		});
	};
	const backToMap = () => {
		wx.navigateBack({
			delta: 1
		})
	};
	//设置所有点串联的路线
	const planRoute = () => {
		for (let i = 1; i < itemData.value.marks.length; i++) {
			console.log("route:", i)
			planRouteAtom(itemData.value.marks[i - 1], itemData.value.marks[i]);
		}
	}
	
	//设置相邻两点路线
	const planRouteAtom = (start, end) => {
		qqmapsdk.value.direction({
			mode: 'driving', // 可选值：'driving'（驾车）、'walking'（步行）、'bicycling'（骑行），不填默认：'driving',可不填
			from: start, // 从表单中获取起始点
			to: end, // 从表单中获取目的地
			// from: state.markers[state.markers.length - 2],
			// to: state.markers[state.markers.length - 1],
			success: function(res) {
				console.log("res(planRoute)", res);
				var ret = res;
				var coors = ret.result.routes[0].polyline,
					pl = [];
				// 坐标解压（返回的点串坐标，通过前向差分进行压缩）
				var kr = 1000000;
				for (var i = 2; i < coors.length; i++) {
					coors[i] = Number(coors[i - 2]) + Number(coors[i]) / kr;
				}
				// 将解压后的坐标放入点串数组pl中
				for (var i = 0; i < coors.length; i += 2) {
					pl.push({
						latitude: coors[i],
						longitude: coors[i + 1]
					});
				}
				console.log("pl:", pl);
				// 设置polyline属性，将路线显示出来,将解压坐标第一个数据作为起点
				// latitude.value = pl[0].latitude;
				// longitude.value = pl[0].longitude;
				polyline.value.push({
					points: pl,
					color: '#FF0000DD',
					width: 4,
					duration: res.result.routes[0].duration,
					distance: res.result.routes[0].distance,
					taxi_fare: res.result.routes[0].taxi_fare.fare,
					arrowLine: true
				});
				console.log("polyline:", polyline);
			},
			fail: function(error) {
				console.error(error);
			},
			complete: function(res) {
				console.log(res);
			}
		});
	}
</script>

<style>
	.item-text {
		/* border: 10px solid black; */
		padding: 10rpx;
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}

	.bottom-bar {
		/* border: 10px solid black; */
		/* padding:100rpx; */
		position: absolute;
		background-color: #eaeaea;
		bottom: 0;
		padding: 10rpx;
		height: 120rpx;
		width: 98%;
	}

	.save-route-button {
		/* border: 10px solid black; */
		/* margin-left:60%; */
		position: absolute;
		top: 15rpx;
		right: 30rpx;
		background-color: #007AFF;
		color: white;
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		border-radius: 60rpx;
		font-weight: 400;
		font-size: 27rpx;
		width: 250rpx;
		height: 80rpx;
	}


	.list-content {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}

	.scroll-list {
		height: calc(75vh - 120rpx);
		/* 减去用户卡片的高度、tabbar高度和间距 */
		/* margin-top: 20rpx; */
		background-color: #f5f5f5;
		min-height: 100vh;
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
		height: 800rpx;
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
	
	.modified-time {
		padding: 0 20rpx;
		font-size: 30rpx;
		color:gray;
		/* font-weight: 800; */
	}
</style>