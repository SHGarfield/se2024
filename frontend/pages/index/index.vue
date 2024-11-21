<template>
	<view class="full-screen">
		<map class="map" latitude='23.099' longitude='113.325'  scale='12' 
		controls='{{con}}' markers='{{mar}}' bindcontroltap='con' bindmarkertap='mar'
		enable-rotate="true">
		</map>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {

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

	.map{
		height: 1300rpx;
		width: 100%;
	}
</style>

