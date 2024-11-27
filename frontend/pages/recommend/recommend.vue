<template>
  <view class="recommend">
    <view class="content">
      <text>推荐内容</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'

onMounted(() => {
  console.log('推荐页面加载完成')
})
</script>

<style lang="scss">
.recommend {
  .content {
    padding: 20rpx;
  }
}
</style> 