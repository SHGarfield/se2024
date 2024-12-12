// //设置所有点串联的路线
// 	const planRoute = (markers,qqmapsdk) => {
// 		for (let i = 1; i < markers.length; i++) {
// 			console.log("route:", i)
// 			planRouteAtom(markers[i - 1], markers[i]);
// 		}
// 		route_planned.value = true; //bug
// 	}

// 	//设置相邻两点路线
// 	const planRouteAtom = (start, end) => {
// 		qqmapsdk.direction({
// 			mode: 'driving', // 可选值：'driving'（驾车）、'walking'（步行）、'bicycling'（骑行），不填默认：'driving',可不填
// 			from: start, // 从表单中获取起始点
// 			to: end, // 从表单中获取目的地
// 			// from: state.markers[state.markers.length - 2],
// 			// to: state.markers[state.markers.length - 1],
// 			success: function(res) {
// 				console.log("res(planRoute)", res);
// 				var ret = res;
// 				var coors = ret.result.routes[0].polyline,
// 					pl = [];
// 				// 坐标解压（返回的点串坐标，通过前向差分进行压缩）
// 				var kr = 1000000;
// 				for (var i = 2; i < coors.length; i++) {
// 					coors[i] = Number(coors[i - 2]) + Number(coors[i]) / kr;
// 				}
// 				// 将解压后的坐标放入点串数组pl中
// 				for (var i = 0; i < coors.length; i += 2) {
// 					pl.push({
// 						latitude: coors[i],
// 						longitude: coors[i + 1]
// 					});
// 				}
// 				console.log("pl:", pl);
// 				// 设置polyline属性，将路线显示出来,将解压坐标第一个数据作为起点
// 				// latitude.value = pl[0].latitude;
// 				// longitude.value = pl[0].longitude;
// 				polyline.value.push({
// 					points: pl,
// 					color: '#FF0000DD',
// 					width: 4,
// 					duration: res.result.routes[0].duration,
// 					distance: res.result.routes[0].distance,
// 					taxi_fare: res.result.routes[0].taxi_fare.fare
// 				});
// 				console.log("polyline:", polyline);
// 			},
// 			fail: function(error) {
// 				console.error(error);
// 			},
// 			complete: function(res) {
// 				console.log(res);
// 			}
// 		});
// 	}