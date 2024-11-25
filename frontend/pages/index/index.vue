<template>
	<view class="full-screen">
		<map class="map" :latitude="39.906217" :longitude="116.391275" :scale="12" :markers="state.markers"
			@markertap="onMarkerTap" @tap="onCommonTap">
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
		marker_added:false,
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
	const current_marker = ref(null)
	
	// 定义地图点击事件处理函数
	const onCommonTap = async (e) => {
		// locationInfo(qqmapsdk, e.detail,current_marker);

		if(!state.marker_added){
			state.markers.pop();
		}
		state.marker_added=false;
		setTimeout(() => { // 避免markertap和commontap同时触发
			if (state.tapEvent === "") { // 是commontap
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
		try {
			const locationInfoRes = await locationInfo(qqmapsdk, e.detail);
			showDetail.value = true;
			current_location.value = {
				standard_address: locationInfoRes.result.formatted_addresses.standard_address,
				recommend:locationInfoRes.result.formatted_addresses.recommend,
				district:locationInfoRes.result.ad_info.name,
			}
		} catch (error) {
			console.error("Error in locationInfo:", error);
		}

	};

	// 定义标记点点击事件处理函数
	const onMarkerTap = (e) => {
		state.tapEvent = e.type;
		console.log("Marker tapped: ", e);
		setTimeout(() => {
			state.tapEvent = "";
		}, 200);
	};

	const addMarker = () =>{
		state.marker_added=true;
		toggleDetailPanel();
	}
	const deleteMarker = () =>{
		state.markers.pop();
		toggleDetailPanel();
	}

	// 切换详情面板显示状态的方法
	const toggleDetailPanel = () => {
		showDetail.value = !showDetail.value;
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