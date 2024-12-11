<template>
	<view class="container">
		<button @click="showModal">点击弹出弹窗</button>
		<view class="modal" v-if="modalVisible">
			<view class="modalPage">
				<view class="picker-container">
					<text>添加日程到第</text>
					<picker mode="selector" :range="pickerRange" @change="onPickerChange1">
						<view class="picker">{{ pickerValue1 }}</view>
					</picker>
					<text>天</text>
				</view>
				<view class="picker-container">
					<text>当日第</text>
					<picker mode="selector" :range="pickerRange" @change="onPickerChange2">
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
		ref
	} from 'vue';

	const modalVisible = ref(false);
	const pickerRange = ref(Array.from({
		length: 50
	}, (_, index) => index + 1));
	const pickerValue1 = ref('请选择');
	const pickerValue2 = ref('请选择');
	
	const showModal = () => {
		modalVisible.value = true;
	};
	
	const hideModal = () => {
		modalVisible.value = false;
	};
	
	const onPickerChange1 = (e) => {
		pickerValue1.value = pickerRange.value[e.detail.value];
	};
	
	const onPickerChange2 = (e) => {
		pickerValue2.value = pickerRange.value[e.detail.value];
	};
	
	const confirmDate=()=>{
		hideModal();
		// addMarker();
	}
	
	const cancelDate=()=>{
		hideModal();
		pickerValue1.value='请选择';
		pickerValue2.value='请选择';
	}
	
</script>

<style>
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
</style>