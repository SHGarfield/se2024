<script>
	export default {
		onLaunch: function() {
			console.log('App Launch');
			this.wxLogin();
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		},
		globalData: {
		  markers: [],
		  openid:"",
		  avatar_url:"",
		  username:"",
		  itemData:{},
		  isLogin:false,
		},
		methods: {
			// 调用微信登录
			async wxLogin() {
			  try {
			    // 获取微信登录的 code
			    const loginRes = await uni.login({
			      provider: 'weixin',
			    });
			    const {
			      code
			    } = loginRes;
			    console.log('微信登录 code:', code);
			    // 将 code 发送到后端
			    const requestRes = await uni.request({
			      url: 'http://111.229.117.144:8000/login/login/', 
			      method: 'POST',
			      data: {
			        code: code,
			      },
			    });
			    console.log('登录成功:', requestRes.data);
			    getApp().globalData.openid = requestRes.data.openid;
				if(requestRes.data.isInDatabase){
					getApp().globalData.isLogin=true;
					getApp().globalData.username=requestRes.data.username;
					getApp().globalData.avatar_url='http://111.229.117.144:8000'+requestRes.data.avatar_url;
				}
			    console.log('登录结束globaldata:',getApp().globalData);
			    // 处理后端返回的登录信息
			  } catch (error) {
			    console.error('微信登录失败:', error);
			  }
			},
		}
	}
	
</script>

<style>
	/*每个页面公共css */
</style>
