import {
	onMounted,
	onUnmounted,
	ref
} from 'vue';
import QQMapWX from '../qqmap/qqmap-wx-jssdk.js';

// 定义一个响应式变量来存储 qqmapsdk 实例
// const qqmapsdk = ref(null);

// 定义 setupQQMapWX 函数来初始化 qqmapsdk
export function setupQQMap(qqmapsdk) {
	// onMounted(() => {
		qqmapsdk.value = new QQMapWX({
			key: 'U4QBZ-N44CV-ORXP5-5JEHC-AQMBO-3FB64'
		});
	// });

	// onUnmounted(() => {
		// 例如，取消未完成的请求等
		// 如果有需要，可以在这里添加清理代码
	// });
}