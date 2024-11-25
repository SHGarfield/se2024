import QQMapWX from '../qqmap/qqmap-wx-jssdk.js';

/**
 * 初始化腾讯地图SDK实例。
 * 此函数接收一个 Vue ref 对象，并将其实例化为腾讯地图SDK对象。
 * 通常在组件的 setup 阶段或生命周期钩子中调用此函数。
 *
 * @param {Ref<QQMapWX>} qqmapsdk - 一个 Vue ref 对象，用于存储腾讯地图SDK实例。
 */
export function setupQQMap(qqmapsdk) {
  qqmapsdk.value = new QQMapWX({
    key: 'U4QBZ-N44CV-ORXP5-5JEHC-AQMBO-3FB64'  // 腾讯地图SDK的密钥
  });
}