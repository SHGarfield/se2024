import QQMapWX from '../qqmap/qqmap-wx-jssdk.js';

/**
 * 执行逆地理编码操作，将经纬度坐标转换为具体的地址信息。
 * @param {Ref<QQMapWX>} qqmapsdk - 腾讯地图SDK的实例，必须已经初始化。
 * @param {Object} location - 包含经纬度信息的对象。
 * @param {number} location.latitude - 纬度值。
 * @param {number} location.longitude - 经度值。
 * 
 * 使用示例：
 * // 假设 qqmapsdk 是已经初始化的腾讯地图SDK实例
 * // 假设 location 是包含经纬度的对象
 * locationInfo(qqmapsdk, { latitude: 39.915, longitude: 116.404 });
 */
// export const locationInfo = (qqmapsdk,location,info) => {
// 	// console.log("location:",location)
// 	// console.log("qqmap.value(locationInfo):",qqmapsdk.value)
// 	qqmapsdk.value.reverseGeocoder({
// 		location: location, // 经纬度坐标
// 		success: function(res) {
// 			// 逆地理编码成功的回调
// 			console.log("locationInfo(success)",res);
// 			info=res;
// 		},
// 		fail: function(res) {
// 			// 逆地理编码失败的回调
// 			console.log("locationInfo(fail)",res);
// 		},
// 		complete: function(res) {
// 			// 逆地理编码完成后的回调，无论成功或失败都会执行
// 			// console.log(res);
// 		}
// 	});
// };
/////////
export const locationInfo = (qqmapsdk, location) => {
	return new Promise((resolve, reject) => {
		qqmapsdk.value.reverseGeocoder({
			location: location, // 经纬度坐标
			success: function(res) {
				// 逆地理编码成功的回调
				console.log("locationInfo(success)", res);
				resolve(res); // 在成功时解析 Promise 并返回结果
			},
			fail: function(res) {
				// 逆地理编码失败的回调
				console.log("locationInfo(fail)", res);
				console.log(location);
				reject(res); // 在失败时拒绝 Promise 并返回错误信息
			},
			complete: function(res) {
				// 逆地理编码完成后的回调，无论成功或失败都会执行
				// console.log(res);
			}
		});
	});
};

// 如果需要在组件卸载时进行清理工作，可以使用onUnmounted
// onUnmounted(() => {
// 	// 例如，取消未完成的请求等
// });