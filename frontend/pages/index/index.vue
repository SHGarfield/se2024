<template>
	<view class="full-screen">
		<map class="map" :latitude="39.906217" :longitude="116.391275" :scale="12" :markers="state.markers"
			:polyline="polyline" @markertap="onMarkerTap" @tap="onCommonTap">
			<!-- @controltap="con" 
		    :controls="con"
			@tap="onMapTap"-->
		</map>
	</view>
	<scroll-view class="detail-panel" :style="{ height: '50%', width: '100%' }" v-show="showDetail">
		<view class="detail-content">
			<text>地点名称：{{ current_location.standard_address}}\n</text>
			<text>地点描述：{{ current_location.recommend}}附近\n</text>
			<text>所在地区：{{current_location.district}}</text>
			<!-- <image :src="location.image" mode="aspectFill"></image> -->
			<button class="addMarkerButton" @click="addMarker">添加</button>
			<button class="deleteMarkerButton" @click="deleteMarker">取消</button>
			<button class="routePlanning" @click="planRoute">路径规划</button>
			<!-- <button class="floating-button" @click="toggleDetailPanel">关闭</button> -->
		</view>
	</scroll-view>
</template>



<script setup>
	import {
		ref,
		reactive,
		onMounted
	} from 'vue';
	import {
		setupQQMap
	} from '../../libs/functions/setupQQMap.js';
	import {
		locationInfo
	} from '../../libs/functions/locationInfo.js';
	const qqmapsdk = ref(null);
	// 定义生命周期钩子
	onMounted(() => {
		// 页面加载时执行的初始化操作
		setupQQMap(qqmapsdk);
	});
	// 定义响应式状态
	const state = reactive({
		marker_added: false,
		tapEvent: "", // 点击事件状态
		markers: [{ // 初始标记点数组
			id: 0,
			latitude: 39.906217,
			longitude: 116.391275,
			callout: {
				content: '这里是气泡内容',
				display: 'BYCLICK',
				borderRadius: 10,
				borderWidth: 2,
				borderColor: '#000',
				color: '#000',
				fontSize: 14,
				bgColor: '#fff',
				padding: 10,
				textAlign: 'center',
				anchorX: 0,
				anchorY: 0
			}
		}]
	});

	// 定义响应式数据
	// const showDetail = ref(false);
	// const location = ref({});

	// 定义响应式数据
	const showDetail = ref(false);
	const current_location = ref({});
	const current_marker = ref(null);
	const polyline = ref([]);

	// 定义地图点击事件处理函数
	const onCommonTap = async (e) => {
		// locationInfo(qqmapsdk, e.detail,current_marker);

		setTimeout(() => { // 避免markertap和commontap同时触发
			if (state.tapEvent === "") { // 是commontap
				//判断是否去除未保存点
				if (!state.marker_added) {
					state.markers.pop();
				}
				state.marker_added = false;
				
				console.log("Common tapped: ", e);
				// 创建新marker
				const newMarker = {
					id: state.markers.length, // 新增标记点的ID
					latitude: e.detail.latitude, // 点击事件返回的纬度
					longitude: e.detail.longitude, // 点击事件返回的经度
				};
				current_marker.value = newMarker;
				console.log("current_marker:", current_marker);
				// 将新的标记点添加到数组中
				state.markers.push(newMarker);
				console.log(state.markers);
			}
		}, 100);
		//点击marker有问题
		try {
			const locationInfoRes = await locationInfo(qqmapsdk, e.detail);
			showDetail.value = true;
			current_location.value = {
				standard_address: locationInfoRes.result.formatted_addresses.standard_address,
				recommend: locationInfoRes.result.formatted_addresses.recommend,
				district: locationInfoRes.result.ad_info.name,
			}
		} catch (error) {
			console.error("Error in locationInfo:", error);
		}

	};

	// 定义标记点点击事件处理函数
	const onMarkerTap = (e) => {
		toggleDetailPanel();
		state.tapEvent = e.type;
		console.log("Marker tapped: ", e);
		setTimeout(() => {
			state.tapEvent = "";
		}, 200);
	};


	const addMarker = () => {
		state.marker_added = true;
		toggleDetailPanel();
	}
	const deleteMarker = () => {
		state.markers.pop();
		toggleDetailPanel();
	}

	// 切换详情面板显示状态的方法
	const toggleDetailPanel = () => {
		showDetail.value = !showDetail.value;
	};

	const planRoute=()=>{
		for(let i=1;i<state.markers.length;i++){
			console.log("route:",i)
			planRouteAtom(state.markers[i-1],state.markers[i]);
		}
	}
	const planRouteAtom = (start,end) => {
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
				polyline.value.push ({
					points: pl,
					color: '#FF0000DD',
					width: 4
				});
			},
			fail: function(error) {
				console.error(error);
			},
			complete: function(res) {
				console.log(res);
			}
		});
	}
	const formSubmit = (e) => {
		// 调用距离计算接口
		qqmapsdk.direction({
			mode: 'driving', // 可选值：'driving'（驾车）、'walking'（步行）、'bicycling'（骑行），不填默认：'driving',可不填
			from: e.start, // 从表单中获取起始点
			to: e.dest, // 从表单中获取目的地
			success: function(res) {
				console.log(res);
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
				console.log(pl);
				// 设置polyline属性，将路线显示出来,将解压坐标第一个数据作为起点
				latitude.value = pl[0].latitude;
				longitude.value = pl[0].longitude;
				polyline.value = [{
					points: pl,
					color: '#FF0000DD',
					width: 4
				}];
			},
			fail: function(error) {
				console.error(error);
			},
			complete: function(res) {
				console.log(res);
			}
		});
	};
</script>


<style>
	.full-screen {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.map {
		height: 100vh;
		width: 100%;
	}

	.detail-panel {
		position: fixed;
		bottom: 0;
		left: 0;
		background-color: #fff;
		z-index: 100;
		transition: transform 0.3s ease-in-out;
	}

	.detail-panel-hidden {
		transform: translateY(100%);
	}

	.detail-content {
		padding: 15px;
	}


	.floating-button {
		position: fixed;
		bottom: 20px;
		right: 20px;
		padding: 10px;
		background-color: #007AFF;
		color: white;
		border: none;
		border-radius: 50%;
		z-index: 101;
	}
</style>