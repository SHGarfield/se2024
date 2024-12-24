<template>
	<view class="list-section">
		<scroll-view class="scroll-list" scroll-y>
			<view class="list-content">
				<map class="item-map" :markers="itemData.marks" :include-points="itemData.marks"
					:polyline="polyline"></map>
				<view class="item-text">
					<input type="text" class="item-title" placeholder="输入标题" maxlength="30" v-model="itemData.title"
						@input="titleChange" />
					<textarea class="item-content" placeholder="输入内容" maxlength=200 @input="contentChange"
						v-model="itemData.content"></textarea>
				</view>
			</view>
		</scroll-view>
		<view class="bottom-bar">
			<button class="save-button" @click="save_route">保存</button>
		</view>
	</view>
</template>

<script setup>
	import {
		defineComponent,
		onMounted,
		ref
	} from 'vue';
	import {
		onShow
	} from '@dcloudio/uni-app';
	import {
		setupQQMap
	} from '../../libs/functions/setupQQMap.js';
	//判断发布还是存到草稿箱
	const isprivate = ref(true);
	//存储帖子内容
	const itemData = ref({});
	const polyline = ref([]);


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
	//根据用户输入，更新title
	const titleChange = (e) => {
		itemData.value.title = e.detail.value
	};
	//根据用户输入，更新content
	const contentChange = (e) => {
		itemData.value.content = e.detail.value;
	};
	const save_route = () => {
		wx.request({
			url: 'http://111.229.117.144:8000/dealMarks/modifyMarks/', // 后端API地址
			method: 'PUT',
			data: {
				openid: getApp().globalData.openid,
				routeid: itemData.value.id,
				title: itemData.value.title,
				content: itemData.value.content,
				marks: itemData.value.marks, // 这里需要页面A的数据传递机制
			},
			success: function(res) {
				console.log('数据提交成功', res);
				wx.showToast({
					title: '上传成功', // 提示内容
					icon: 'success', // 图标类型
					duration: 2000 // 提示框停留时间
				});
				setTimeout(function() {
					backToMap();
				}, 2000);
			},
			fail: function(err) {
				console.error('数据提交失败', err);
				wx.showToast({
					title: '上传失败，请检查网络', // 提示内容
					icon: 'error', // 图标类型
					duration: 2000 // 提示框停留时间
				});
			}
		});
	};
	const backToMap = () => {
		wx.navigateBack({
			delta: 2
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
	.list-section {
		display: flex;
		flex-direction: column;
		height: 100vh;
		border: 2px solid green;
		/* 使容器高度为视口高度 */
	}

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

	button {
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

	.publish-button {
		right: 300rpx;
		background-color: white;
		border: 1px solid #007AFF;
		color: #007AFF;
		width: 180rpx;
	}


	.list-content {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}

	.scroll-list {
		display: flex;
		flex-direction: column;
		/* 减去用户卡片的高度、tabbar高度和间距 */
		/* margin-top: 20rpx; */
		background-color: #f5f5f5;
		height: 100vh;
	}

	.item-map {
		width: 100%;
		height: 800rpx;
	}

	.item-title {
		padding: 20rpx;
		font-size: 40rpx;
		font-weight: 800;
		border-bottom: 1px solid lightgrey;
	}

	.item-content {
		width: 96%;
		padding: 0 2%;
		font-size: 35rpx;
		height: 360rpx;
		/* font-weight: 800; */
	}

	.modified-time {
		padding: 0 20rpx;
		font-size: 30rpx;
		color: gray;
		/* font-weight: 800; */
	}

	/* //////////////////////////////////////////////////////////////// */
	/* 页面整体容器样式 */
	/* 	.view-container {
	  display: flex;
	  flex-direction: column;
	  height: 100vh; 
	  padding: 10px;
	} */

	/* 输入框样式 */
	/* 	.input-text {
	  width: 100%;
	  padding: 8px;
	  height: 50px;
	  margin-bottom: 10px;
	  border: 1px solid #ccc;
	  border-radius: 4px;
	  box-sizing: border-box;
	} */

	/* 标题样式 */
	/* 	.title-input {
	  font-size: 24px; 
	  font-weight: bold; 
	  margin-bottom: 10px;
	} */

	/* 文本区域样式 */
	/* 	.textarea-content {
	width: 100%;
	  flex: 1; 
	  padding: 8px;
	  border: 1px solid #ccc;
	  border-radius: 4px;
	  box-sizing: border-box;
	  margin-bottom: 10px;
	  resize: none; 
	} */

	/* button {
		width: 50%;
		padding: 10px 20px;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 16px;
		margin-bottom: 40px;
		border-radius: 40rpx;
	}

	button:hover {
		background-color: #0056b3;
	} */
</style>