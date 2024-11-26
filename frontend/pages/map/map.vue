<template>
	<view class="full-screen">
		<view class="search-page">
			<input type="text" v-model="searchText" placeholder="请输入搜索内容" />
			<button @click="onSearch">搜索</button>
			<button @click="cancelSearch">取消</button>
		</view>
		<map class="map" :latitude="39.906217" :longitude="116.391275" :scale="12" :markers="state.markers"
			:polyline="polyline" @markertap="onMarkerTap" @tap="onCommonTap">
			<!-- @controltap="con" 
		    :controls="con"
			@tap="onMapTap"-->
		</map>
	</view>
	<scroll-view class="detail-panel" :style="{ height: '50%', width: '100%' }" v-show="showDetail">
		<view class="detail-content">
			<text>id：{{current_location.id}}\n</text>
			<text>地点名称：{{ current_location.standard_address}}\n</text>
			<text>地点描述：{{ current_location.recommend}}附近\n</text>
			<text>所在地区：{{current_location.district}}</text>
			<!-- <text v-if="current_location.id >= 1&&route">距离：{{polyline.value[current_location.id-1][0].distance}}</text> -->
			<!-- <text>距离：{{polyline[current_location.value.])}}</text> -->
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
	const searchText = ref('');
	const showDetail = ref(false);
	const current_location = ref({});
	const polyline = ref([]);
	const route_planned = ref(false);
	// function onSearch() {
	//   // 执行搜索操作，这里只是打印搜索内容，实际项目中你可能需要调用API
	//   console.log('搜索内容：', searchText.value);
	//   // 这里可以编写你的搜索逻辑，例如调用API获取数据
	// }
	const searched_markers = ref([]); // 使用ref创建响应式数据，用于存储地图标记
	const markers_store = ref([]);
	const onSearching = ref(false);

	const onSearch = () => {
		searchLocation(qqmapsdk, searchText.value);
		unshowDetailPanel();
	};
	// 事件触发，调用接口
	const searchLocation = (qqmapsdk, search_text) => {
		// 调用接口
		qqmapsdk.value.search({
			keyword: search_text, //搜索关键词
			location: '39.980014,116.313972', //设置周边搜索中心点
			success: function(res) { //搜索成功后的回调
				let mks = [];
				for (let i = 0; i < res.data.length; i++) {
					mks.push({ // 获取返回结果，放到mks数组中
						title: res.data[i].title,
						id: mks.length,
						latitude: res.data[i].location.lat,
						longitude: res.data[i].location.lng,
						// iconPath: "/resources/my_marker.png", //图标路径
						width: 20,
						height: 20
					});
				}
				searched_markers.value = mks; // 更新markers数组
				console.log("sercherdmarkers:", searched_markers.value);
				showResearchMarkers();
			},
			fail: function(res) {
				console.log(res);
			},
			complete: function(res) {
				console.log(res);
			}
		});
	};
	
	const cancelSearch=()=>{
		searchText.value="";
		unshowDetailPanel();
		unshowResearchMarkers();//恢复正常标点
	}

	const showResearchMarkers = () => {
		//如果第一次使用搜索，则存储当前的点
		if (!onSearching) {
			markers_store.value = state.markers;
		}
		//将显示数组变为搜索的点
		state.markers = searched_markers.value;
		//标记状态为搜索中
		onSearching.value = true;
	};

	const unshowResearchMarkers = () => {
		if (onSearching) {
			state.markers = markers_store.value;
		}
		console.log("state.markers:",state.markers);
		console.log("store_marker:",markers_store.value);
		onSearching.value = false;
	};
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
				// current_marker.value = newMarker;
				Object.assign(current_location.value, newMarker);
				// 将新的标记点添加到数组中
				state.markers.push(newMarker);
				console.log(state.markers);

				getSelectedLocationInfo(e.detail);
			}
		}, 100);
		//点击marker有问题
		// try {
		// 	const locationInfoRes = await locationInfo(qqmapsdk, e.detail);
		// 	showDetail.value = true;
		// 	// current_location.value = {
		// 	// 	standard_address: locationInfoRes.result.formatted_addresses.standard_address,
		// 	// 	recommend: locationInfoRes.result.formatted_addresses.recommend,
		// 	// 	district: locationInfoRes.result.ad_info.name,
		// 	// }
		// 	 Object.assign(current_location.value, {
		// 	    standard_address: locationInfoRes.result.formatted_addresses.standard_address,
		// 	    recommend: locationInfoRes.result.formatted_addresses.recommend,
		// 	    district: locationInfoRes.result.ad_info.name,
		// 	  });
		// 		console.log("current_marker:", current_marker);
		// } catch (error) {
		// 	console.error("Error in locationInfo:", error);
		// }

	};
	// 将try语句块封装成函数
	const getSelectedLocationInfo = async (location) => {
		try {
			const locationInfoRes = await locationInfo(qqmapsdk, location);
			showDetail.value = true;
			Object.assign(current_location.value, {
				standard_address: locationInfoRes.result.formatted_addresses.standard_address,
				recommend: locationInfoRes.result.formatted_addresses.recommend,
				district: locationInfoRes.result.ad_info.name,
			});
			console.log("current_location:", current_location);
		} catch (error) {
			console.error("Error in locationInfo:", error);
		}
	};

	// 定义标记点点击事件处理函数
	const onMarkerTap = (e) => {
		showDetailPanel();
		state.tapEvent = e.type;
		console.log("Marker tapped: ", e);
		setTimeout(() => {
			state.tapEvent = "";
			getSelectedLocationInfo(state.markers.find(item => item.id === e.markerId));
			Object.assign(current_location.value, {
				id: e.markerId
			});
		}, 200);
	};


	const addMarker = () => {
		state.marker_added = true;
		showDetailPanel();
	}
	const deleteMarker = () => {
		state.markers.splice(current_location.id, 1); //有bug，如果删除前面的点，index没办法更新
		unshowDetailPanel();
	}

	// 切换详情面板显示状态的方法
	// const toggleDetailPanel = () => {
	// 	showDetail.value = !showDetail.value;
	// }
	//展示详情面板
	const showDetailPanel =	() => {
		showDetail.value=true;
		}
	//关闭详情面板
	const unshowDetailPanel = () => {
		showDetail.value = false;
	}

	const planRoute = () => {
		for (let i = 1; i < state.markers.length; i++) {
			console.log("route:", i)
			planRouteAtom(state.markers[i - 1], state.markers[i]);
		}
		route_planned.value = true; //bug
	}
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
					taxi_fare: res.result.routes[0].taxi_fare.fare
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

	/* 搜索框 */
	.search-page {
		position: absolute;
		display: flex;
		align-items: center;
		width: 87%;
		padding: 10px;
		background-color: white;
		top: 2vh;
		/* 确保搜索栏在地图上方 */
		z-index: 10;
		border-radius: 20rpx;
		/* 水平偏移 0px，垂直偏移 4px，模糊半径 10px，颜色为黑色，透明度为 0.3 */
		box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
	}

	input[type="text"] {
		flex: 1;
		border-right: 1px solid #ccc;
		padding: 10px;
		border-radius: 4px;
	}

	button {
		padding: 0rpx 10px;
		font-size: 30rpx;
		background-color: #007aff;
		color: white;
		border: none;
		border-radius: 10rpx;
		margin-left: 10px;
	}
</style>