<template>
	<view class="view-container">
	    <input type="text" class="input-text title-input" placeholder="输入标题" maxlength="30" @input="titleChange" />
	    <textarea class="textarea-content" placeholder="输入内容" maxlength=200 @input="contentChange"></textarea>
	    <button class="submit-button" @click="submitData">提交</button>
	</view>
</template>

<script setup>
	import {
		defineComponent,
		onMounted,
		ref
	} from 'vue';
	const markers = ref([]);
	onMounted(() =>{
		// console.log("options:");
		// markers.value = decodeURIComponent(query.storedData);
		// console.log(markers);
	});
	// 页面B的js文件
	const title = ref('');
	const content = ref('');

	const titleChange = (e) => {
		title.value = e.detail.value
	};
	const contentChange = (e) => {
		content.value = e.detail.value;
	};
	const submitData = () => {
		wx.request({
			url: 'http://111.229.117.144:8000/dealMarks/addMarks/', // 后端API地址
			method: 'POST',
			data: {
				openid:"TODO",
				title: title.value,
				content: content.value,
				marks: getApp().globalData.markers // 这里需要页面A的数据传递机制
			},
			success: function(res) {
				console.log('数据提交成功', res);
				wx.showToast({
				  title: '上传成功', // 提示内容
				  icon: 'success', // 图标类型
				  duration: 2000 // 提示框停留时间
				});
				setTimeout(function() {
				    backToMap();
				  }, 2000);
			},
			fail: function(err) {
				console.error('数据提交失败', err);
				wx.showToast({
				  title: '上传失败，请检查网络', // 提示内容
				  icon: 'error', // 图标类型
				  duration: 2000 // 提示框停留时间
				});
			}
		});
	};
	const backToMap=()=>{
		wx.navigateBack({
		  delta: 1
		})
	};
</script>

<style>
	/* 页面整体容器样式 */
	.view-container {
	  display: flex;
	  flex-direction: column;
	  height: 100vh; /* 使容器高度为视口高度 */
	  padding: 10px;
	}
	
	/* 输入框样式 */
	.input-text {
	  width: 100%;
	  padding: 8px;
	  height: 50px;
	  margin-bottom: 10px;
	  border: 1px solid #ccc;
	  border-radius: 4px;
	  box-sizing: border-box;
	}
	
	/* 标题样式 */
	.title-input {
	  font-size: 24px; /* 固定大号字 */
	  font-weight: bold; /* 加粗 */
	  margin-bottom: 10px; /* 与输入框间距 */
	}
	
	/* 文本区域样式 */
	.textarea-content {
	width: 100%;
	  flex: 1; /* 自适应填充剩余空间 */
	  padding: 8px;
	  border: 1px solid #ccc;
	  border-radius: 4px;
	  box-sizing: border-box;
	  margin-bottom: 10px;
	  resize: none; /* 禁止调整大小 */
	}
	
	/* 按钮样式 */
	.submit-button {
		width: 100%;
	  padding: 10px 20px;
	  background-color: #007bff;
	  color: white;
	  border: none;
	  border-radius: 4px;
	  cursor: pointer;
	  font-size: 16px;
	  margin-bottom: 40px; /* 与文本区域间距 */
	}
	
	.submit-button:hover {
	  background-color: #0056b3;
	}
</style>