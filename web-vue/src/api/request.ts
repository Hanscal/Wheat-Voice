import axios, { AxiosError } from 'axios';
import { ElLoading } from 'element-plus';
import { ElMessage } from 'element-plus';

// 定义一个类型来访问 globalThis 的 loading 属性
declare global {
    interface GlobalThis {
        loading?: any;
    }
}

let loadingInstance: any = null;

// 初始化 globalThis 的 loading 属性
(globalThis as GlobalThis).loading = loadingInstance;

const startLoading = (): void => {
    interface Options {
        lock: boolean;
        text: string;
        background: string;
    }
    const options: Options = {
        lock: true,
        text: 'Loading',
        background: 'rgba(0, 0, 0, 0.7)'
    };
    (globalThis as GlobalThis).loading = ElLoading.service(options);
};

const endLoading = (): void => {
    const loadingInstance = (globalThis as GlobalThis).loading;
    if (loadingInstance) {
        loadingInstance.close();
        (globalThis as GlobalThis).loading = null; // 清空实例
    }
};

// 请求拦截
axios.interceptors.request.use((config: any) => {
    // 开始Loading
    startLoading();
    return config;
});

// 请求响应拦截
axios.interceptors.response.use(
    (response: any) => {
        // 成功直接返回响应数据
        if (response.status === 200) {
            endLoading();
            return response.data;
        }
    },
    (error: AxiosError) => {
        endLoading();

        let msg = '请求错误，请稍后重试';
        if (error.response && error.response.data) {
            if (typeof error.response.data === 'string') {
                msg = error.response.data;
            } else if (typeof error.response.data === 'object' && error.response.data !== null) {
                const data = error.response.data as Record<string, unknown>;
                if ('error' in data) {
                    if (typeof data.error === 'string') {
                        msg = data.error;
                    } else {
                        msg = String(data.error); // 将 data.error 转换为字符串
                    }
                }
            }
        } else if (error.code === 'ECONNABORTED') {
            msg = '请求超时，请稍后再试';
        } else if (!navigator.onLine) {
            msg = '网络连接已断开，请检查网络';
        }

        ElMessage.error(msg);
        return Promise.reject(error);
    }
);

export default axios;
