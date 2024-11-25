<template>
	<view>
		<view class="page-body">
			<view class="page-section page-section-gap">
				<map style="width: 100%; height: 300px;" :latitude="latitude" :longitude="longitude" :markers="covers">
				</map>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 页面加载时的处理
onMounted(() => {
  console.log('首页加载完成')
})
</script>

<style lang="scss">

</style> 