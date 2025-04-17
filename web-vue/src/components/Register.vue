<template>
  <el-form ref="form" :model="registerUser" :rules="rules" label-width="18px" class="loginForm">
    <h3 class="login_title">{{ isRegister ? '注册' : '修改密码' }}</h3>
    <el-form-item label="昵称" prop="account">
      <el-input v-model="registerUser.account" placeholder="请输入用户昵称"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="registerUser.password" type="password" placeholder="请输入密码"></el-input>
    </el-form-item>
    <el-form-item label="手机号" prop="phone" style="display: flex; align-items: center;">
      <el-input v-model="registerUser.phone" placeholder="请输入手机号" style="flex: 1;"></el-input>
    </el-form-item>
    <el-form-item label="验证码" prop="verificationCode">
      <div class="input-button-group">
        <el-input v-model="registerUser.verificationCode" placeholder="请输入验证码" />
        <el-button @click="sendVerificationCode" :disabled="isSending" class="half-width-button">
          {{ verificationButtonText }}
        </el-button>
      </div>
    </el-form-item>
    <el-form-item style="width: 100%; display: flex; justify-content: center;">
      <el-button type="primary" style="width: 100%; background: #505458; border: none" @click="handleSubmit">{{ isRegister ? '注册' : '修改密码' }}</el-button>
    </el-form-item>
    <el-form-item style="width: 100%; display: flex; justify-content: center;">
      <el-button style="width: 100%;" @click="goToLogin()">已有账户？去登录</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { reactive, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter, useRoute } from 'vue-router';

export default {
  setup() {
    const registerUser = reactive({
      account: '',
      password: '',
      phone: '',
      verificationCode: ''
    });

    const rules = reactive({
      account: [
        { required: true, message: '请输入账号', trigger: 'blur' },
        { min: 6, message: '账号至少6个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' },
        { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,20}$/, message: '必须包含至少一个字母和一个数字', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' }
      ],
      verificationCode: [
        { required: true, message: '请输入验证码', trigger: 'blur' },
        { pattern: /^\d{4}$/, message: '请输入4位数字验证码', trigger: 'blur' }
      ]
    });

    const router = useRouter();
    const route = useRoute();
    const isRegister = route.query.isRegister === 'true';
    const isSending = ref(false);
    const verificationButtonText = ref('发送验证码'); // 确保初始化正确

    // 发送验证码
    const sendVerificationCode = async () => {
      if (!registerUser.phone || !registerUser.phone.match(/^1[3-9]\d{9}$/)) {
        ElMessage.error('请输入有效的手机号');
        return;
      }

      // 模拟发送验证码，启动倒计时
      startCountdown(60);

      console.log('发送验证码到手机号:', registerUser.phone);

      try {
        const response = await fetch('/api/send_verification_code', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ phone: registerUser.phone })
        });

        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        console.log('API Response:', data);

        if (data.success) {  // 根据你的API响应结构判断
          ElMessage.success('验证码已发送');
        } else {
          console.error('Send verification code failed:', data.message);
          ElMessage.error('发送验证码失败，请检查手机号是否有效');
        }
      } catch (error) {
        console.error('Send verification code failed:', error);
        ElMessage.error('发送验证码失败，请检查网络连接');
      }
    };

    // 倒计时功能
    let countdownTimeout;

    const startCountdown = (seconds) => {
      isSending.value = true;
      verificationButtonText.value = `${seconds}s 后重发`;

      const countdown = () => {
        seconds--;
        verificationButtonText.value = `${seconds}s 后重发`;
        if (seconds > 0) {
          countdownTimeout = setTimeout(countdown, 1000);
        } else {
          clearTimeout(countdownTimeout);
          verificationButtonText.value = '重新发送';
          isSending.value = false;
        }
      };

      countdown();
    };

    const handleSubmit = () => {
      // 提交表单，例如调用API进行注册
      if (isRegister) {
        console.log('进行注册操作');
        register();
      } else {
        console.log('进行修改密码操作');
        modifyPassword();
      }
    };

    const register = async () => {
      const isValid = await validateRegister(
        registerUser.phone,
        registerUser.verificationCode,
        registerUser.account,
        registerUser.password,
        isRegister
      );
      console.log('Validation result:', isValid);

      if (isValid === 'true') {
        try {
          ElMessage.success('注册成功');
          router.push('/login')
            .then(() => {
              console.log('成功跳转到登录页');
            })
            .catch((error) => {
              ElMessage.error('跳转登录页失败，请稍后再试');
              console.error('跳转登录页失败:', error);
            });
        } catch (error) {
          ElMessage.error('跳转登录页失败，请稍后再试');
          console.error('跳转登录页失败:', error);
        }
      } else {
        ElMessage.error(isValid);
      }
    };

    const modifyPassword = async () => {
      const isValid = await validateRegister(
        registerUser.phone,
        registerUser.verificationCode,
        registerUser.account,
        registerUser.password,
        isRegister
      );
      console.log('Validation result:', isValid);

      if (isValid === 'true') {
        try {
          ElMessage.success('修改密码成功');
          router.push('/login')
            .then(() => {
              console.log('成功跳转到登录页');
            })
            .catch((error) => {
              ElMessage.error('跳转登录页失败，请稍后再试');
              console.error('跳转登录页失败:', error);
            });
        } catch (error) {
          ElMessage.error('跳转登录页失败，请稍后再试');
          console.error('跳转登录页失败:', error);
        }
      } else {
        ElMessage.error(isValid);
      }
    };

    const validateRegister = async (phone, verificationCode, account, password, isRegister) => {
      if (!phone || !password || !verificationCode || account.length < 6) {
        console.error('Invalid input: account and password are required and must be at least 6 characters long.');
        return false;
      }

      try {
        const response = await fetch('/api/validate_register_code', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ phone, verificationCode, password, account, isRegister})
        });

        // if (!response.ok) {
        //   throw new Error(`API request failed with status ${response.status}`);
        // }

        const data = await response.json();
        console.log('API Response:', data);
        if (data.success) {
          return 'true';
        } else {
          return data.message;
        }

      } catch (error) {
        console.error('API call failed:', error);
        return 'false';
      }
    };

    const goToLogin = () => {
      router.push('/login')
        .then(() => {
          console.log('成功跳转到登录页面');
        })
        .catch((error) => {
          proxy.$message({
            message: '跳转登录页面失败，请稍后再试',
            type: 'error'
          })
          console.error('跳转登录页面失败:', error);
        });
    }


    return {
      registerUser,
      rules,
      handleSubmit,
      register,
      modifyPassword,
      goToLogin,
      sendVerificationCode,
      isRegister,
      isSending,
      verificationButtonText
    };
  }
};
</script>

<style>
:root {
  --primary-color: #505458;
  --border-color: #eaeaea;
  --shadow-color: #cac6c6;
}

.loginForm {
  border-radius: 15px;
  background-clip: padding-box;
  margin: 80px auto;
  width: 420px;
  padding: 35px;
  background: #fff;
  border: 1px solid var(--border-color);
  box-shadow: 0 0 25px var(--shadow-color);
}

.login_title {
  margin: 0 auto 40px;
  text-align: center;
  color: var(--primary-color);
}

.el-form-item__label {
  display: block;
  min-width: 70px; /* 设置最小宽度 */
  width: 70px; /* 固定宽度 */
}

.el-form-item {
  margin-bottom: 15px;
}

.input-button-group {
  display: flex;
  align-items: center;
}

.half-width-button {
  width: 50%;
  margin-left: 10px; /* 根据实际需求调整间距 */
}
</style>
