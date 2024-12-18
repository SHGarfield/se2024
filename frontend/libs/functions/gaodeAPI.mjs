// searchPOI.js
// export async function searchPoi(keyword) {
//   const url = `https://restapi.amap.com/v5/place/text?key=a740362743c88b599489eb7486e64bbd&keywords=${encodeURIComponent(keyword)}&show_fields=business`;

//   try {
//     const response = await fetch(url);
//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }
//     const data = await response.json();
//     console.log("data", data);

//     if (data.status === '1' && data.info === 'OK') {
//       const pois = data.pois.map((poi, index) => {
//         const location = poi.location.split(',');
//         return {
//           id: index, // 使用索引作为id
//           // name: poi.name,
//           // address: poi.address,
//           latitude: location[1], // 纬度
//           longitude: location[0], // 经度
//           width: 20,
//           height: 20,
//           opentime_week: poi.business.opentime_week,
//           tel: poi.business.tel,
//           rating: poi.business.rating,
//           cost: poi.business.cost,
//         };
//       });
//       return pois; // 返回处理后的搜索结果
//     } else {
//       console.error('搜索失败', data.info);
//       return { error: data.info }; // 搜索失败返回错误信息
//     }
//   } catch (error) {
//     console.error('请求失败', error);
//     return { error: error.message }; // 请求失败返回错误信息
//   }
// }
const KEY = 'a740362743c88b599489eb7486e64bbd';
// searchPOI.js
export function searchPoi(keyword) {
  return new Promise((resolve, reject) => {
    const url = `https://restapi.amap.com/v5/place/text?key=${KEY}&keywords=${encodeURIComponent(keyword)}&show_fields=business`;
    wx.request({
      url: url,
      method: 'GET',
      success: (res) => {
        console.log(1)
        if (res.data.status === '1' && res.data.info === 'OK') {
          console.log(res.data)
          const pois = res.data.pois.map((poi, index) => {
            const location = poi.location.split(',');
            return {
              id: index, // 使用索引作为id
              // name: poi.name,
              // address: poi.address,
              latitude: location[1], // 纬度
              longitude: location[0], // 经度
              width: 30,
              height: 50,
              standard_address:poi.name,
              district:poi.pname+poi.cityname+poi.adname,
              recommend:poi.address,
              opentime_week: poi.business.opentime_week,
              tel: poi.business.tel,
              rating: poi.business.rating,
              cost: poi.business.cost,
            };
          });
          console.log(pois);
          resolve(pois); // 返回处理后的搜索结果
        } else {
          console.error('搜索失败', res.data.info);
          reject({ error: res.data.info }); // 搜索失败返回错误信息
        }
      },
      fail: (error) => {
        console.error('请求失败', error);
        reject({ error: error.errMsg }); // 请求失败返回错误信息
      }
    });
  });
};

// weatherService.js
export async function getAmapWeather(cityAdcode) {
  try {
    const response=await fetch("https://api.open.geovisearth.com/v2/cn/city/basic?location=[39,110]&token=ea338fcde38203d86e1e52ae886f21b4");
    // const response = await fetch(`https://restapi.amap.com/v3/weather/weatherInfo?key=${KEY}&city=${cityAdcode}&extensions=all`);
    // if (!response.ok) {
    //   throw new Error(`HTTP error! status: ${response.status}`);
    // }
    console.log("response", response);
    const data = await response.json();
    console.log("data", data);
    console.log("cast:",data.forecasts);
    for (let i = 0; i < data.forecasts.length; i++) {
      console.log(data.forecasts[i].casts);
    }
    if (data.status === '1' && data.info === 'OK') {
      return {
        // temperature: weatherInfo.temperature,
        // weather: weatherInfo.weather,
        // windDirection: weatherInfo.winddirection,
        // windPower: weatherInfo.windpower,
        // reportTime: weatherInfo.reporttime
      };
    } else {
      throw new Error('未能获取天气信息');
    }
  } catch (error) {
    console.error('请求天气信息失败:', error);
    throw error; // 向外层抛出错误
  }
}

/**
 * 高德地图逆地址解析函数
 * @param {number} longitude - 经度
 * @param {number} latitude - 纬度
 * @param {string} apiKey - 高德地图API Key
 * @return {Promise} - 包含逆地址解析结果的Promise对象
 */
export function reverseGeocoder(longitude, latitude) {
  return new Promise((resolve, reject) => {
    const url = `https://restapi.amap.com/v3/geocode/regeo?key=${KEY}&location=${longitude},${latitude}`;

    fetch(url)
      .then(response => {
        if (!response.ok) {
          console.log(response)
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.status === '1' && data.info === 'OK') {
          // 逆地址解析成功，使用resolve返回结果
          resolve(data);
        } else {
          // 高德API返回错误信息，使用reject返回
          reject(new Error(data.info));
        }
      })
      .catch(error => {
        // 网络请求失败，使用reject返回错误信息
        reject(error);
      });
  });
}