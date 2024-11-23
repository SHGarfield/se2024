<template>
	<view class="full-screen">
		<map class="map" :latitude="39.906217" :longitude="116.391275" :scale="12" :markers="markers"
			@markertap.stop="onMarkerTap" @tap.stop="onCommonTap">
			<!-- @controltap="con" 
		    :controls="con"-->
		</map>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				tapEvent: "", //点击是marker tap还是common tap
				markers: [{ // 初始标记点数组
					// iconPath: "location.png",
					id: 0,
					latitude: 23.099,
					longitude: 113.325,
					// label:{
					//         content: '金水区绿地原盛国际1号楼A座9楼',  //文本
					//         color: '#FF0202',  //文本颜色
					//         borderRadius: 3,  //边框圆角
					//         borderWidth: 1,  //边框宽度
					//         borderColor: '#FF0202',  //边框颜色
					//         bgColor: '#ffffff',  //背景色
					//         padding: 5,  //文本边缘留白
					//         textAlign: 'center'  //文本对齐方式。有效值: left, right, center
					//       },
					//气泡callout
					callout: {
					          content: '这里是气泡内容',
					          display: 'BYCLICK', // 点击时显示
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

				}],
				// con: [{ // 控制数组，如果有需要可以添加
				//   id: 1,
				//   iconPath: 'location.png',
				//   position: {
				//     left: 0,
				//     top: 50,
				//     width: 50,
				//     height: 50
				//   },
				//   clickable: true
				// }]
			};
		},
		onLoad() {
			// 页面加载时执行的初始化操作
		},
		methods: {
			// 地图点击事件处理函数
			onCommonTap(e) {
				setTimeout(() => { //避免markertap和commontap同时触发
					if (this.tapEvent === "") {
						console.log("Common tapped: ", e);
						const newMarker = {
							id: this.markers.length, // 新增标记点的ID
							// iconPath: "location.png", // 标记点图标路径
							latitude: e.detail.latitude, // 点击事件返回的纬度
							longitude: e.detail.longitude, // 点击事件返回的经度
						};
						// 将新的标记点添加到数组中
						this.markers.push(newMarker);
						console.log(this.markers)
					}
				}, 100);
			},
			// 控制元素点击事件处理函数
			// onControlTap(e) {
			//   console.log("Control tapped: ", e);
			// },
			// 标记点点击事件处理函数
			onMarkerTap(e) {
				this.tapEvent = e.type;
				console.log("Marker tapped: ", e);
				setTimeout(() => {
					this.tapEvent = "";
				}, 200);

			}
		}
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
</style>