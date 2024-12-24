<template>
	<view class="list-section">
		<scroll-view class="scroll-list" scroll-y>
			<view class="list-content">
				<map class="item-map" :markers="itemData.marks" :include-points="itemData.marks"></map>
				<view class="item-text">
					<text class="item-title">{{itemData.title}}</text>
					<text class="item-content">{{itemData.content}}</text>
					<text class="modified-time">{{itemData.modified_time}}</text>
				</view>
			</view>
		</scroll-view>
		<view class="bottom-bar">
			<picker mode="selector" :range="pickerRange" @change="onPickerChange">
				<button class="change_isprivate" >修改可见范围</button>
			</picker>
			<button class="save-route-button" @click="editRoute">编辑路线</button>
		</view>
	</view>
</template>


<script setup>
	import {
		ref,
		computed,
		onMounted
	} from 'vue'

	import {
		onShow
	} from '@dcloudio/uni-app';
	// const isRefreshing = ref(false);
	const itemData = ref({});
	const pickerRange=ref(["公开可见","仅自己可见"]);
	const modified_time = ref("");
	// const format_modified_time = () => {
	// 	let time = getApp().globalData.modified_time;
	// 	// 移除'T'和'Z'
	// 	modified_time.value = time.replace(/[TZ]/g, ' ');

	// };
	//重设time的格式
	const format_modified_time = () => {
		itemData.value.modified_time = '编辑于' + itemData.value.modified_time.replace(/T/, '  ').replace(/Z/, '');
	};
	onShow(() => {
		getItemData();
	});
	onMounted(() => {
		format_modified_time();
	});
	const editRoute = () => {
		wx.navigateTo({
			url: '/pages/my_map_edit/my_map_edit'
		})
	};
	const onPickerChange = (e) => {
		const pickerValue = pickerRange.value[e.detail.value];
		if (pickerValue == "公开可见") {
			//公开可见
			setRouteIsPrivate(false);
			console.log(1);
		} else {
			//仅自己可见
			setRouteIsPrivate(true);
			console.log(2);
		}
	};
	
	const setRouteIsPrivate = (isprivate) => {
		wx.request({
			url: 'http://111.229.117.144:8000/dealMarks/setRouteIsPrivate/', // 后端API地址
			method: 'PUT',
			data: {
				openid: getApp().globalData.openid,
				routeid: itemData.value.id,
				isprivate: isprivate
			},
			success: function(res) {
				console.log('修改可见范围成功', res);
				wx.showToast({
					title: '修改成功', // 提示内容
					icon: 'success', // 图标类型
					duration: 1000 // 提示框停留时间
				});
				setTimeout(function() {
					backToMap();
				}, 2000);
			},
			fail: function(err) {
				console.error('数据提交失败', err);
				wx.showToast({
					title: '修改失败', // 提示内容
					icon: 'error', // 图标类型
					duration: 1000 // 提示框停留时间
				});
			}
		});
	};
	
	const saveRoute = () => {
		//检查是否登录
		if (getApp().globalData.openid) {
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

	const getItemData = () => {
		itemData.value = getApp().globalData.itemData;
		console.log("itemData:(detail)", itemData.value);
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
				}, 2000);
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

	.change_isprivate {
		position: absolute;
		top: 15rpx;
		right: 300rpx;
		background-color: white;
		border: 1px solid #007AFF;
		color: #007AFF;
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
		color: gray;
		/* font-weight: 800; */
	}
</style>