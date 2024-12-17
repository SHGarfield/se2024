import { searchPoi,reverseGeocoder } from './gaodeAPI.mjs';


reverseGeocoder("116.411471","39.911225").then(results => {
  if (results.error) {
    console.error('测试失败:');
  } else {
    console.log('测试成功:',  results);
  }
});