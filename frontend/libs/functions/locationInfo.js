import {
	onMounted,
	onUnmounted,
	ref
} from 'vue';
import QQMapWX from '../qqmap/qqmap-wx-jssdk.js';

// 定义一个响应式变量来存储qqmapsdk实例
// export const qqmapsdk = ref(null);

// 使用onMounted生命周期钩子来实例化API
// onMounted(() => {
// 	qqmapsdk.value = new QQMapWX({
// 		key: 'U4QBZ-N44CV-ORXP5-5JEHC-AQMBO-3FB64'
// 	});
// 	// 调用接口
// 	// searchLocation();
// });
////////

// 定义locationInfo函数来执行逆地理编码操作
export const locationInfo = (qqmapsdk,location) => {
	// 这里以经纬度为北京天安门为例
	// const location = {
	// 	latitude: 39.915,
	// 	longitude: 116.404
	// };
	// console.log("location:",location)
	// console.log("qqmap.value(locationInfo):",qqmapsdk.value)
	qqmapsdk.value.reverseGeocoder({
		location: location, // 经纬度坐标
		success: function(res) {
			// 逆地理编码成功的回调
			console.log(res);
		},
		fail: function(res) {
			// 逆地理编码失败的回调
			console.log(res);
		},
		complete: function(res) {
			// 逆地理编码完成后的回调，无论成功或失败都会执行
			console.log(res);
		}
	});
};
/////////

// 定义searchPlaces函数来执行搜索操作
export const searchPlaces = () => {
	qqmapsdk.value.search({
		keyword: '酒店',
		success: function(res) {
			console.log(res);
		},
		fail: function(res) {
			console.log(res);
		},
		complete: function(res) {
			console.log(res);
		}
	});
};

// 如果需要在组件卸载时进行清理工作，可以使用onUnmounted
// onUnmounted(() => {
// 	// 例如，取消未完成的请求等
// });