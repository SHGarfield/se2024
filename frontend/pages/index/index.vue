<template>
	<view class="full-screen">
		<map class="map" :latitude="39.906217" :longitude="116.391275" :scale="12" :markers="state.markers"
			@markertap.stop="onMarkerTap" @tap.stop="onCommonTap">
			<!-- @controltap="con" 
		    :controls="con"-->
		</map>
	</view>
</template>



<script setup>
	import {
		ref,
		reactive,
		onMounted
	} from 'vue';
	import { setupQQMap } from '../../libs/functions/setupQQMap.js';
	import { locationInfo} from '../../libs/functions/locationInfo.js';
	
	const qqmapsdk = ref(null);
	// 定义响应式状态
	const state = reactive({
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

	// 定义生命周期钩子
	onMounted(() => {
		// 页面加载时执行的初始化操作
	setupQQMap(qqmapsdk);
	console.log("qqmapsdk:",qqmapsdk.value);
	});
	// const qqmapsdk = ref(null);
	// 定义地图点击事件处理函数
	const onCommonTap = (e) => {
		console.log("locationInfo",locationInfo(qqmapsdk,e.detail))
		setTimeout(() => { // 避免markertap和commontap同时触发
			if (state.tapEvent === "") { // 是commontap
				console.log("Common tapped: ", e);
				// 创建新marker
				const newMarker = {
					id: state.markers.length, // 新增标记点的ID
					latitude: e.detail.latitude, // 点击事件返回的纬度
					longitude: e.detail.longitude, // 点击事件返回的经度
				};
				// 将新的标记点添加到数组中
				state.markers.push(newMarker);
				console.log(state.markers);
			}
		}, 100);
	};

	// 定义标记点点击事件处理函数
	const onMarkerTap = (e) => {
		state.tapEvent = e.type;
		console.log("Marker tapped: ", e);
		setTimeout(() => {
			state.tapEvent = "";
		}, 200);
	};

	// 导入或定义 locationInfo 函数
	// import {
	// 	locationInfo
	// } from 'path/to/locationInfo'; // 假设 locationInfo 函数在外部文件中定义
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
</style>