<template>
	<view class="full-screen">
		<view class="search-page" v-if="!modalVisible">
			<input type="text" v-model="searchText" placeholder="请输入搜索内容" />
			<button v-if="!onSearching" class="searchBarButton" @click="onSearch">搜索</button>
			<button v-else class="searchBarButton" @click="cancelSearch">取消</button>
		</view>
		<map class="map" :longitude="mapCenterProxy.longitude" :latitude="mapCenterProxy.latitude"
			:include-points="focusMarker" :markers="state.markers" :polyline="polyline" @markertap="onMarkerTap"
			@tap="onCommonTap" @poitap="onPoiTap" @regionchange="onRegionChange">
			<!-- @controltap="con" 
		    :controls="con":scale="scale.value"
			@tap="onMapTap"-->
		</map>
	</view>

	<page-container class="detail-panel" :show="showDetail" :overlay="false" :round="true" :close-on-slide-down="true">
		<view class="detail-content">
			<text v-if="current_location.tourDate" class="dateDetail">第{{current_location.tourDate}}天
				第{{current_location.tourOrder}}个行程</text>
			<text>id：{{current_location.id}}\n</text>
			<view class="detail-title">
				<text class="locationStandard">{{ current_location.standard_address}}</text>
				<text v-if="current_location.rating" class="rating">{{current_location.rating}}分️</text>
			</view>
			<text class="locationRecommend">{{current_location.district}} - {{ current_location.recommend}}附近</text>
			<view class="detail-title">
				<text v-if="current_location.opentime_week" class="opentime">{{current_location.opentime_week}}</text>
				<text v-if="current_location.opentime_week&&current_location.cost" class="opentime"> | </text>
				<text v-if="current_location.cost" class="cost">￥{{current_location.cost}}/人</text>
			</view>
			<text v-if="current_location.tel" class="tel">联系方式：{{current_location.tel}}</text>
			<text>\n\n</text>
			<!-- <text v-if="current_location.id >= 1&&route">距离：{{polyline.value[current_location.id-1][0].distance}}</text> -->
			<!-- <text>距离：{{polyline[current_location.value.])}}</text> -->
			<!-- <image :src="location.image" mode="aspectFill"></image> -->
			<button class="unshowDetailPanel" @click="unshowDetailPanel">×</button>
			<!-- <button class="floating-button" @click="toggleDetailPanel">关闭</button> -->
		</view>
		<view class="bottomBar">
			<picker mode="date" :value="beginDate" @change="onDateChange">
				<view class="pickerStartOff">
					{{ beginDate }}出发
				</view>
			</picker>
			<button class="deleteMarkerButton" @click="deleteMarker" v-show="!onSearching">移出行程</button>
			<button v-if="!current_location.tourOrder" class="addMarkerButton" @click="addMarkerToRoute">加入行程</button>
		</view>
	</page-container>
	<button v-if="!route_planned" class="routePlanning" @click="planRoute" v-show="!onSearching">路径规划</button>
	<button v-else class="routePlanning" @click="clearRoute" v-show="!onSearching">隐藏路径</button>
	<button class="saveRoute" @click="sendMarkersToServer" v-show="!onSearching&&!modalVisible">发送标记</button>
	<view class="container">
		<view class="modal" v-if="modalVisible">
			<view class="modalPage">
				<view class="picker-container">
					<text>添加日程到第</text>
					<picker mode="selector" :range="pickerRangeDate" @change="onPickerChange1">
						<view class="picker">{{ pickerValue1 }}</view>
					</picker>
					<text>天</text>
				</view>
				<view class="picker-container">
					<text>当日第</text>
					<picker mode="selector" :range="pickerRangeOrder" @change="onPickerChange2"
						:disabled="!isPicker2Available">
						<view class="picker">{{ pickerValue2 }}</view>
					</picker>
					<text>个行程</text>
				</view>
				<view class="buttonDate">
					<button class="cancelDate" @click="cancelDate">取消</button>
					<button class="confirmDate" @click="confirmDate">确定</button>
				</view>
			</view>
		</view>
	</view>
</template>



<script setup>
	import {
		ref,
		reactive,
		onMounted,
		toValue,
		computed
	} from 'vue';
	import {
		onShow,
		onHide
	} from '@dcloudio/uni-app';
	import {
		setupQQMap
	} from '../../libs/functions/setupQQMap.js';
	import {
		searchPoi
	} from '../../libs/functions/gaodeAPI.mjs';
	import {
		locationInfo
	} from '../../libs/functions/locationInfo.js';
	const qqmapsdk = ref(null);

	// 定义响应式状态
	const state = reactive({
		marker_added: false,
		tapEvent: "", // 点击事件状态
		markers: [] //初始标记点数组
	});
	const focusMarker = ref([]);
	// 定义生命周期钩子
	onMounted(() => {
		// 页面加载时执行的初始化操作
		setupQQMap(qqmapsdk);
	});
	onShow(() => {
		if (getApp().globalData.marks) {
			state.markers = getApp().globalData.marks;
		}
		console.log("statet.marke4s:", state.markers)
	})
	onHide(() => {
		getApp().globalData.marks = state.markers;
	})
	const sendMarkersToServer = async () => {


		// getApp().globalData.markers=state.markers;
		getApp().globalData.itemData = {
			marks: state.markers,
			title: '',
			content: '',
		}
		wx.navigateTo({
			url: '/pages/my_map_edit/my_map_edit'
		});
		console.log(getApp().globalData.markers);
		// wx.request({
		// 	url: 'http://111.229.117.144:8000/dealMarks/addMarks/', // 你的后端服务器地址
		// 	method: 'POST',
		// 	data: {
		// 		openid:"openid",
		// 		title:"title",
		// 		content:"content",
		// 		marks:state.markers,
		// 	},
		// 	header: {
		// 		'content-type': 'application/json' // 设置请求的 header
		// 	},
		// 	success: function(res) {
		// 		console.log("success")
		// 	},
		// 	fail: function(error) {
		// 		console.log("error")
		// 	}
		// });
	};


	// 将markers和sendMarkersToServer方法暴露给模板
	// return {
	// 	markers,
	// 	sendMarkersToServer,
	// };

	const isPicker2Available = ref(false);
	const getAllDate = () => {
		//非搜索情况，从state.markers里搜
		if (!onSearching.value && state.markers.length > 1 && state.markers[state.markers.length - 2].tourDate) {
			console.log("state markers(getAllDate)", state.markers);
			return state.markers[state.markers.length - 2].tourDate;
		}
		//搜索情况，从markers.store里搜
		if (onSearching.value && markers_store.value.length > 0 && markers_store.value[markers_store.value.length - 1]
			.tourDate) {
			console.log("markers_store(getallDate)", markers_store.value);
			return markers_store.value[markers_store.value.length - 1].tourDate;
		}
		return 0;
	}

	const getAllOrder = () => {
		if (!onSearching.value) {
			console.log("state markers(getAllOrder)", state.markers);
			for (let i = state.markers.length - 2; i >= 0; i--) {
				// 	console.log("markerDate", state.markers[i].tourDate);
				// 	console.log("value1", pickerValue1.value);
				if (state.markers[i].tourDate == pickerValue1.value) {
					return state.markers[i].tourOrder;
				}
			}
		} else {
			console.log("markers_store(getAllOrder)", state.markers);
			for (let i = markers_store.value.length - 1; i >= 0; i--) {
				// 	console.log("markerDate", state.markers[i].tourDate);
				// 	console.log("value1", pickerValue1.value);
				if (markers_store.value[i].tourDate == pickerValue1.value) {
					return markers_store.value[i].tourOrder;
				}
			}
		}
		return 0;
	}
	const modalVisible = ref(false);
	// const pickerRange = ref(Array.from({
	// 	length: state.markers.length
	// }, (_, index) => index + 1));
	const pickerRangeDate = computed(() => {
		return Array.from({
			length: getAllDate() + 1
		}, (_, index) => index + 1);
	});
	const pickerRangeOrder = computed(() => {
		return Array.from({
			length: getAllOrder() + 1
		}, (_, index) => index + 1);
	});

	const pickerValue1 = ref('请选择');
	const pickerValue2 = ref('请选择');
	const addMarkerToRoute = () => {
		showModal();
		unshowDetailPanel();
	}

	//展示地点详情页
	const showModal = () => {
		modalVisible.value = true;
		isPicker2Available.value = false;
	};

	//隐藏地点详情页
	const hideModal = () => {
		modalVisible.value = false;
	};

	const onPickerChange1 = (e) => {
		pickerValue1.value = pickerRangeDate.value[e.detail.value];
		if (pickerValue1.value == "请选择") {
			isPicker2Available.value = false;
		} else {
			isPicker2Available.value = true;
		}
	};

	const onPickerChange2 = (e) => {
		pickerValue2.value = pickerRangeOrder.value[e.detail.value];
	};

	const confirmDate = () => {
		hideModal();
		addMarker();
		updateAddedOrder();
		updateId();
		clearDateSelecter();
	}
	const findMarkerIndexByDate = (targetTourDate, targetTourOrder) => {
		const index = state.markers.findIndex(marker =>
			marker.tourDate === targetTourDate && marker.tourOrder === targetTourOrder
		);
		return index;
	};
	const updateAddedOrder = () => {
		const index = findMarkerIndexByDate(state.markers[state.markers.length - 1].tourDate, state.markers[state
			.markers.length - 1].tourOrder);
		// 使用临时变量来交换属性值
		// const tmpMark = {
		// 	id: state.markers[state.markers.length - 1].id,
		// 	latitude: state.markers[state.markers.length - 1].latitude,
		// 	longitude: state.markers[state.markers.length - 1].longitude,
		// 	tourDate: state.markers[state.markers.length - 1].tourDate,
		// 	tourOrder: state.markers[state.markers.length - 1].tourOrder,
		// };
		const tmpMark = state.markers[state.markers.length - 1];
		state.markers.splice(index, 0, tmpMark);
		state.markers.pop();

		for (let i = index + 1; i < state.markers.length; i++) {
			if (state.markers[i].tourDate == state.markers[index].tourDate) {
				state.markers[i].tourOrder++;
			} else {
				break;
			}
		}
		//
	}

	const clearDateSelecter = () => {
		pickerValue1.value = '请选择';
		pickerValue2.value = '请选择';
	}
	const cancelDate = () => {
		hideModal();
		clearDateSelecter();
	}


	const beginDate = ref(new Date().toISOString().slice(0, 10)); // 使用ref创建响应式数据

	const onDateChange = (e) => {
		beginDate.value = e.detail.value; // 更新选择的日期
	};


	// 定义响应式数据
	// const showDetail = ref(false);
	// const location = ref({});

	// 定义响应式数据
	const searchText = ref('');
	const showDetail = ref(false);
	const current_location = ref({});
	const polyline = ref([]);
	const route_planned = ref(false);
	const mapCenterProxy = ref({
		latitude: 39.906217,
		longitude: 116.391275
	})
	const scale = (16);
	// function onSearch() {
	//   // 执行搜索操作，这里只是打印搜索内容，实际项目中你可能需要调用API
	//   console.log('搜索内容：', searchText.value);
	//   // 这里可以编写你的搜索逻辑，例如调用API获取数据
	// }
	const searched_markers = ref([]); // 使用ref创建响应式数据，用于存储地图标记
	const markers_store = ref([]);
	const onSearching = ref(false);

	const onSearch = () => {
		searchLocation(searchText.value);
		unshowDetailPanel();
	};


	const cancelSearch = () => {
		searchText.value = "";
		unshowDetailPanel();
		unshowResearchMarkers(); //恢复正常标点
	}

	const showResearchMarkers = () => {
		//如果第一次使用搜索，则存储当前的点
		if (!onSearching.value) {
			console.log("brfore", markers_store.value);
			console.log("state.markers", state.markers.length);

			// for (let i = 0; i < state.markers.length; i++) {
			// 	console.log(i,"state.markers[]", state.markers[i]);
			// 	markers_store.value.push(state.markers[i]);
			// 	console.log("storein", markers_store);
			// }
			markers_store.value = state.markers;
			console.log("store", markers_store.value);
		}
		//将显示数组变为搜索的点
		state.markers = searched_markers.value;
		focusMarker.value.pop();
		focusMarker.value.push(state.markers[0]);
		//标记状态为搜索中
		onSearching.value = true;
	};

	const unshowResearchMarkers = () => {
		if (onSearching.value) {
			state.markers = markers_store.value;
		}
		console.log("state.markers:", state.markers);
		console.log("store_marker:", markers_store.value);
		onSearching.value = false;
	};
	const onPoiTap = (e) => {
		console.log("poi tapped:", e);
		onCommonTap(e);
	}
	// 定义地图点击事件处理函数
	const onCommonTap = async (e) => {
		// locationInfo(qqmapsdk, e.detail,current_marker);

		setTimeout(() => { // 避免markertap和commontap同时触发
			if (state.tapEvent === "" && !onSearching.value) { // 是commontap
				//判断是否去除未保存点
				if (state.markers.length > 0 && !state.markers[state.markers.length - 1].tourDate) {
					state.markers.pop();
				}
				state.marker_added = false;

				console.log("Common tapped: ", e);
				// 创建新marker
				const newMarker = {
					id: state.markers.length, // 新增标记点的ID
					latitude: e.detail.latitude, // 点击事件返回的纬度
					longitude: e.detail.longitude, // 点击事件返回的经度
					standard_address: e.detail.name,
					tourOrder: undefined,
					tourDate: undefined,
					width: 30,
					height: 50,
				};
				// current_marker.value = newMarker;
				Object.assign(current_location.value, newMarker);
				// 将新的标记点添加到数组中,展示
				state.markers.push(newMarker);
				getSelectedLocationInfo(e.detail);
			}
		}, 100);
	};
	// 将try语句块封装成函数
	const getSelectedLocationInfo = async (location) => {
		try {
			const locationInfoRes = await locationInfo(qqmapsdk, location);
			showDetail.value = true;
			if (location.name) {
				Object.assign(current_location.value, {
					recommend: locationInfoRes.result.formatted_addresses.standard_address,
					standard_address: locationInfoRes.result.formatted_addresses.recommend,
					district: locationInfoRes.result.ad_info.name,
				});
			} else {
				Object.assign(current_location.value, {
					standard_address: locationInfoRes.result.formatted_addresses.standard_address,
					recommend: locationInfoRes.result.formatted_addresses.recommend,
					district: locationInfoRes.result.ad_info.name,
				});
			}
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
			// Object.assign(current_location.value, {
			// 	id: e.markerId,
			// 	latitude: state.markers[e.markerId].latitude,
			// 	longitude: state.markers[e.markerId].longitude,
			// 	standard_address: state.markers[e.markerId].standard_address,
			// 	district: state.markers[e.markerId].district,
			// 	recommend: state.markers[e.markerId].recommend,
			// 	tourDate: state.markers[e.markerId].tourDate,
			// 	tourOrder: state.markers[e.markerId].tourOrder,
			// 	opentime_week: state.markers[e.markerId].opentime_week,
			// 	tel: state.markers[e.markerId].tel,
			// 	rating: state.markers[e.markerId].rating,
			// 	cost: state.markers[e.markerId].cost,
			// });
			current_location.value = state.markers[e.markerId];
			console.log("st:", state.markers[e.markerId]);
			console.log("cu:", current_location.value);
			if (!onSearching.value) {
				if (current_location.value.standard_address) {
					const standard_address = current_location.value.standard_address;
					getSelectedLocationInfo(state.markers.find(item => item.id === e.markerId));
					state.markers.find(item => item.id === e.markerId).standard_address = standard_address;
				} else {
					getSelectedLocationInfo(state.markers.find(item => item.id === e.markerId));
				}
			}
		}, 200);
	};
	//视野变化则更新地图中心坐标
	// const onRegionChange = (e) => {
	// 	// console.log(e);
	// 	if (e.type == "end") {
	// 		setMapCenterProxy(e.detail.centerLocation.latitude, e.detail.centerLocation.longitude);
	// 	}
	// }

	//增加新标注点到地图
	const addMarker = () => {
		state.marker_added = true;
		console.log(pickerValue1.value);
		if (!onSearching.value) {
			// showDetailPanel();
			Object.assign(
				state.markers[state.markers.length - 1], {
					tourDate: pickerValue1.value,
					tourOrder: pickerValue2.value,
					standard_address: current_location.value.standard_address,
				});
			console.log("state markers(add marker)", state.markers);
		} else {
			console.log(current_location.value);
			markers_store.value.push(getContentFromObject(current_location));
			// const m=getContentFromObject(current_location);
			// const m=getContentFromObject(current_location);
			// console.log("m",m);
			// markers_store.value.push(m);
			// console.log(markers_store.value[markers_store.value.length-1].rating);
			// Object.assign(markers_store.value[markers_store.value.length-1],m);
			console.log("markers_store", markers_store.value);
			unshowResearchMarkers();
		}
	}

	const getContentFromObject = (object) => {
		const objectvalue = object.value;
		console.log("pickerValue:", pickerValue1.value);
		const newMarker = {
			id: objectvalue.id,
			latitude: objectvalue.latitude,
			longitude: objectvalue.longitude,
			tourDate: pickerValue1.value,
			tourOrder: pickerValue2.value,
			standard_address: objectvalue.standard_address,
			recommend: objectvalue.recommend,
			district: objectvalue.district,
			opentime_week: objectvalue.opentime_week,
			tel: objectvalue.tel,
			rating: objectvalue.rating,
			cost: objectvalue.cost,
			// 复制其他需要的属性
		};
		console.log("newMarker(getContentFromObject)", newMarker);
		console.log("newValue:", newMarker.tourDate);
		return newMarker;
	}

	const deleteMarker = () => {
		// state.markers.splice(current_location.id, 1); //有bug，如果删除前面的点，index没办法更新
		console.log("current:", current_location.value.id);
		console.log("state.markers", state.markers);
		state.markers.splice(findMarkerById(state.markers, current_location.value.id), 1);
		updateId();
		unshowDetailPanel();
	}

	const updateId = () => {
		state.markers.forEach((marker, index) => {
			marker.id = index;
		});
	}
	//
	const findMarkerById = (markers, id) => {
		return markers.findIndex(item => item.id === id);
	}

	//展示详情面板
	const showDetailPanel = () => {
		showDetail.value = true;
	}

	//关闭详情面板
	const unshowDetailPanel = () => {
		showDetail.value = false;
	}

	//设置地图中心点
	const setMapCenterProxy = (latitude, longitude) => {
		// console.log(latitude, longitude);
		mapCenterProxy.value.latitude = latitude;
		mapCenterProxy.value.longitude = longitude;
		// console.log(latitude, longitude);
	}

	// 地点搜索
	const searchLocation = async (keyword) => {
		if (keyword) {
			try {
				const results = await searchPoi(keyword);
				console.log("search results:", results);
				if (results.length) {
					searched_markers.value = results;
					showResearchMarkers();
					// setMapCenterProxy(searched_markers.value[0].latitude, searched_markers.value[0].longitude);
				} else {
					wx.showToast({
						title: '无结果', // 提示内容
						icon: 'none', // 图标类型，无结果时通常使用'none'
						duration: 1000 // 提示框停留时间
					});
				}
			} catch (error) {
				wx.showToast({
					title: '请求失败', // 提示内容
					icon: 'error', // 图标类型
					duration: 1000 // 提示框停留时间
				});
			}
		}
	}

	const clearRoute = () => {
		route_planned.value = false;
		polyline.value.length=0;
	};

	//设置所有点串联的路线
	const planRoute = () => {
		if (state.markers.length > 1) {
			for (let i = 1; i < state.markers.length; i++) {
				console.log("route:", i)
				planRouteAtom(state.markers[i - 1], state.markers[i]);
			}
			route_planned.value = true; //bug
		} else {
			wx.showToast({
				title: '标记点过少', // 提示内容
				icon: 'error', // 图标类型
				duration: 1500 // 提示框停留时间
			});
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
					arrowLine:true
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
	.detail-title {
		/* display: flex;
		flex-direction: row; */
	}

	.opentime,
	.tel,
	.cost {
		vertical-align: middle;
		font-size: 25rpx;
	}

	.rating {
		font-weight: 1000;
		background-color: #fce9c4;
		color: #f88326;
		border-radius: 10rpx;
		padding: 0 5rpx 0 8rpx;
		margin-left: 10rpx;
	}

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

	/* 	.detail-panel {
		height: 500rpx;
	} */

	/* 	.detail-panel-hidden {
		transform: translateY(100%);
	} */

	.detail-content {
		display: flex;
		flex-direction: column;
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

	.saveRoute {
		position: absolute;
		display: flex;
		align-items: center;
		font-size: 30rpx;
		line-height: 1.1;
		width: 120rpx;
		height: 120rpx;
		padding: 20rpx;
		color: white;
		background-color: #007aff;
		bottom: 5vh;
		left: 50rpx;
		/* 确保搜索栏在地图上方 */
		z-index: 10;
		border-radius: 50%;
		/* 水平偏移 0px，垂直偏移 4px，模糊半径 10px，颜色为黑色，透明度为 0.3 */
		box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
	}

	.routePlanning {
		position: absolute;
		display: flex;
		align-items: center;
		font-size: 30rpx;
		line-height: 1.1;
		width: 120rpx;
		height: 120rpx;
		padding: 20rpx;
		color: white;
		background-color: #007aff;
		bottom: 5vh;
		right: 50rpx;
		/* 确保搜索栏在地图上方 */
		z-index: 10;
		border-radius: 50%;
		/* 水平偏移 0px，垂直偏移 4px，模糊半径 10px，颜色为黑色，透明度为 0.3 */
		box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
	}

	input[type="text"] {
		flex: 1;
		border-right: 1px solid #ccc;
		padding: 10px;
		border-radius: 4px;
	}

	.searchBarButton {
		padding: 0rpx 10px;
		font-size: 30rpx;
		background-color: #007aff;
		color: white;
		border: none;
		border-radius: 10rpx;
		margin-left: 10px;
	}

	.container {
		padding: 20px;
		background-color: black;
	}

	.modal {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.modalPage {
		background-color: #fff;
		width: 80%;
		border-radius: 30rpx;
	}

	.picker-container {
		margin: 20px;
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
	}

	.picker {
		padding: 10rpx;
		margin: 20rpx;
		border-color: black;
		border-width: 10rpx;
		background-color: #f6ede5;
		color: #2a82fe;
		font-weight: 1000;
		font-size: 45rpx;
		border-radius: 10rpx;
		text-align: center;
	}

	.pickerStartOff {
		padding: 10rpx;
		border-color: black;
		border-width: 10rpx;
		background-color: #f6ede5;
		color: #2a82fe;
		font-weight: 1000;
		font-size: 40rpx;
		border-radius: 10rpx;
		text-align: center;
	}

	.buttonDate {
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
	}

	.confirmDate,
	.cancelDate {
		border-color: white;
		border-width: 30rpx;
		border-radius: 0 0 0 30rpx;
		background-color: white;
		width: 50%;
		background-color: #f1f1f1;
	}

	.confirmDate {
		background-color: #2a82fe;
		border-radius: 0 0 30rpx 0;
		color: white;
	}

	.dateDetail {
		font-size: 50rpx;
		font-weight: 1000;

	}

	.locationStandard {
		font-size: 33rpx;
		font-weight: 600;
	}

	.locationRecommend {
		font-size: 25rpx;
	}

	.bottomBar {
		display: flex;
		flex-direction: row;
		position: absolute;
		bottom: 0;
		/* border: 2px solid green; */
		padding: 10rpx;
		width: 98%;
		/* justify-content: stretch; */
		align-items: center;
	}

	.addMarkerButton {
		background-color: #007AFF;
		color: white;
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		border-radius: 60rpx;
		font-weight: 400;
		font-size: 27rpx;
		width: 26%;
		height: 80rpx;
	}

	.deleteMarkerButton {
		border: 2px solid #007AFF;
		color: #007AFF;
		/* 2px宽的实线边框，颜色为黑色 */
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		border-radius: 60rpx;
		font-weight: 400;
		font-size: 27rpx;
		width: 26%;
		height: 80rpx;
	}

	.unshowDetailPanel {
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		position: absolute;
		width: 30px;
		height: 30px;
		top: 10px;
		right: 10px;
		border-radius: 50%;
	}
</style>