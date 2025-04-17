/*
 * @Author: 0x3E5
 * @Date: 2023-02-12 16:16:30
 * @LastEditTime: 2023-02-12 16:27:43
 * @LastEditors: 0x3E5
 * @Description:
 */
import request from '@/utils/axios'

// 定义参数类型
interface sendVerificationParams {
  phone: string;
}

// paper search
export const sendVerificationCodeApi = (params: sendVerificationParams) => {
  return request({
    url: '/send_verification_code',
    method: 'post',
    data: params
  });
}

// 定义参数类型
interface validateRegisterParams {
  phone: string;
  code: string;
  account: string;
  password: string;
}


// 注册验证 API
export const validateRegisterCodeApi = async (params: validateRegisterParams) => {
  return request({
    url: '/validate_register_code',
    method: 'post',
    data: params,
  });
}

interface LoginParams {
  username: string;
  password: string;
}

// 验证用户名是否符合格式
function validateUsername(username: string): string | null {
  if (!/^[a-zA-Z0-9_]{6,20}$/.test(username)) { // 假设用户名长度为6-20个字符
    return null;
  }
  return username;
}

// 用户登录
export const userLogin = (params: LoginParams) => {
  const validatedUsername = validateUsername(params.username);
  if (!validatedUsername) {
    throw new Error('Invalid username');
  }
  return request({
    url: '/login',
    method: 'post',
    data: { ...params, username: validatedUsername, password: params.password }
  });
}
