<template>
    <div class="login-container">
        <form
        @submit.prevent="submitLogin">
        <div class="input-group">
            <select id="country_code" v-model="countryCode">

                <!-- 添加其他国家的区号选项 -->
                <option v-for="country in countryCodes" :key="country.code" :value="country.code">{{ country.name }} ({{
                    country.code }})
                </option>

            </select>
            <input type="text" id="phone_number" v-model="phoneNumber" placeholder="请输入手机号" required>
        </div>
        <div class="input-group">
            <label for="verification_code" style="float: top;">验证码</label>
            <input type="text" class="verification_code" id="verification_code"  v-model="verificationCode"
                   style="width: calc(100%); float: top;" required>
                <button type="button" class="verification_code_button"
                @click="requestVerificationCode" :disabled="isSendingCode" style="float: bottom;">
                {{ buttonText }}
            </button>
        </div>
        <button type="submit">登录</button>
    </form>
    <div v-if="message" class="message">{{ message }}</div>
</div>
        </template>

<script>
import axios from 'axios';
import { countryCodes } from '../assets/countryCodes'; // 导入国家代码数据

export default {
  data() {
    return {
        countryCodes: countryCodes, // 使用导入的国家代码数据
      countryCode: '+86',
      phoneNumber: '',
      verificationCode: '',
      isSendingCode: false,
      countdown: 60,
       message: '', // 添加 message 状态
    };
  },
  computed: {
    buttonText() {
      return this.isSendingCode ? `${this.countdown} 秒后重新获取` :'获取验证码'  ;
    }
  },
  methods: {
    async requestVerificationCode() {
      if (!this.phoneNumber) {
       this.message = '请填写手机号';
       console.error(this.message);
        return;
      }
      this.isSendingCode = true;
      try {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const response = await axios.post('http://127.0.0.1:8000/api/request_verification_code/', {
          country_code: this.countryCode,
          phone_number: this.phoneNumber,
        }, {
      headers: {
      'Content-Type': 'application/json', // 指定请求的数据格式为 JSON
        'X-CSRFToken': csrftoken
      }
    });
        if (response.data.success) {
          this.isSendingCode = true;
          this.message = '验证码已发送';
          // 开始倒计时
          this.startCountdown();
        } else {
           this.message = '发送验证码失败';
           this.isSendingCode = false;
        }
      } catch (error) {
      console.error(error);
         this.message = '发送验证码失败';
         this.isSendingCode = false;
      }
    },
    async submitLogin() {
      if (!this.phoneNumber || !this.verificationCode) {
        this.message = '请填写完整信息';
        this.isSendingCode = false;
        return;
      }
      try {
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const response = await axios.post('http://127.0.0.1:8000/api/login_with_verification_code/', {
          country_code: this.countryCode,
          phone_number: this.phoneNumber,
          verification_code: this.verificationCode,
        }, {
      headers: {
      'Content-Type': 'application/json', // 指定请求的数据格式为 JSON
        'X-CSRFToken': csrftoken
      }
    }
        );
        if (response.data.success) {
           this.message = '登录成功';
           if (response.data.redirect_url) {
 window.location.href = response.data.redirect_url;  // 页面重定向到 Django 中的 post_list 页面
        } else {
          this.message = '验证码错误或登录失败';
          this.isSendingCode = false;
        }
        }
      } catch (error) {
        console.error(error);
         this.message = '登录失败';
         this.isSendingCode = false;
      }
    },
    startCountdown() {
      const countdownInterval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(countdownInterval);
          this.countdownTimer = null;
          this.isSendingCode = false;
          this.countdown = 60; // 重置倒计时时间
        }
      }, 1000);
    },
  },
};
</script>

<style scoped>
.login-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 200px;
  text-align: center;
}

.input-group {
  margin-bottom: 15px;
}


label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"], select {
  padding: 8px;
  margin-right: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.message {
  margin-top: 15px;
  color: red; /* 可以根据需要更改消息的样式 */
}
</style>
