<template>
  <el-form ref="form" :model="loginUser" :rules="rules" label-width="15px" class="loginForm">
    <h3 class="login_title">登录</h3>
    <el-form-item label="手机号" prop="phone">
      <el-input v-model="loginUser.phone" placeholder="请输入手机号"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="loginUser.password" type="password" placeholder="请输入密码"></el-input>
    </el-form-item>
    <el-form-item style="width: 100%">
      <el-button type="primary" style="width: 100%; background: #505458; border: none" @click="login()">登录</el-button>
    </el-form-item>
    <el-form-item style="width: 100%">
      <el-button style="width: 100%;" @click="goToRegister()">没有账户？去注册</el-button>
    </el-form-item>
    <el-form-item style="width: 100%">
      <el-button style="width: 100%;" @click="goToModify()">忘记密码？去修改</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import { reactive, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import { userLogin } from '@/api/user.js'

export default {
  name: 'Login',
  setup() {
    const { proxy } = getCurrentInstance() as any;

    // 表单字段
    const loginUser = reactive({
      phone: '',
      password: ''
    });

    // 登录表单校验
    const rules = reactive({
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    });

    const router = useRouter();

    const login = async () => {
      // 模拟登录验证
      const isValid = await validateLogin(loginUser.phone, loginUser.password);
      const { success, message } = isValid;
      console.log(success);
      if (success) {
        try {
          // 设置 userToken 并存储到 localStorage
          localStorage.setItem('userToken', 'your-token-here');

          proxy.$message({
            message: '登录成功',
            type: 'success'
          });
          await router.push('/')
            .then(() => {
              console.log('成功跳转到首页');
            })
            .catch((error) => {
              handleNavigationError(error);
            });
        } catch (error) {
          proxy.$message({
            message: '用户名或密码错误',
            type: 'error'
          });
        };
      } else {
        proxy.$message({
          message: '用户名或密码错误',
          type: 'error'
        });
      }
    }

    // 验证登录信息
    const validateLogin = async (phone: string, password: string): Promise<{success: boolean, message: string}> => {
      // 基本输入验证
      if (!phone || !password) {
        console.error('Invalid input: username and password are required.');
        return { success: false, message: '用户名或密码格式不正确' };
      }

      try {
         // 使用 CryptoJS 对密码进行哈希处理
        // const hashedPassword = CryptoJS.SHA256(password).toString();

        // 调用登录接口
        const res = await userLogin({ username: phone, password: password });
        if (res && res.data.success) {
          return { success: true, message: '登录成功' };
        } else {
          console.error('Login failed:', res.data.message);
          return { success: false, message: '用户名或密码错误' };
        }
      } catch (err) {
        console.error('Login failed with an error:', err);
        return { success: false, message: '登录失败，请稍后再试' };
      }
    };

    const handleNavigationError = (error: Error) => {
      proxy.$message({
        message: '跳转失败，请稍后再试',
        type: 'error'
      });
      console.error('跳转失败:', error);
    }

    const goToRegister = () => {
      router.push({ path: '/register', query: { isRegister: 'true' } })
        .then(() => {
          console.log('成功跳转到注册页面');
        })
        .catch((error) => {
          handleNavigationError(error);
        });
    }

    const goToModify = () => {
      router.push({path: '/register', query: { isRegister: 'false' } })
        .then(() => {
          console.log('成功跳转到修改密码页面');
        })
        .catch((error) => {
          handleNavigationError(error);
        });
    }

    return { loginUser, rules, login, goToRegister, goToModify }
  },
}
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

.el-form-item__item {
  display: block;
  min-width: 70px; /* 设置最小宽度 */
  width: 100px; /* 固定宽度 */
}

.login_title {
  margin: 0 auto 40px;
  text-align: center;
  color: var(--primary-color);
}
</style>
