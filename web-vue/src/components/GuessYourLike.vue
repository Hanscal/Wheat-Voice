<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElIcon } from "element-plus";
import { Search, Promotion } from '@element-plus/icons-vue';
import { marked } from 'marked';

const props = defineProps(['loading', 'result'])
const emits = defineEmits(['search-guess'])

const isPanelVisible = ref(false) // 控制面板显示状态
const togglePanel = (): void => {
  isPanelVisible.value = !isPanelVisible.value // 切换面板状态
  if (!isPanelVisible.value) {
    clearMessages(); // 面板隐藏时清空消息内容
  }
}
const search = (searchContent: string): void => {
  emits('search-guess', searchContent)
}

// 发送消息逻辑
const message = ref('') // 用于绑定消息输入框的内容
const messages = ref<string[]>([]); // 使用 ref 来定义响应式消息数组
// 编译 Markdown 内容为 HTML
const markdownContent = ref('');
const compiledMarkdown = computed(() => marked(markdownContent.value));
const fetchAIInterpretation = (title: string): void => {
  const eventSource = new EventSource(`/api/stream_generate?query=${encodeURIComponent(title)}`);
    markdownContent.value = "### AI解读：\n";
  eventSource.onmessage = (event) => {
    markdownContent.value += event.data; // 添加新消息到 Markdown 内容
  };

  eventSource.onerror = (error) => {
    console.error("EventSource failed:", error);
    eventSource.close(); // 关闭连接
  };
};

const handleGuessClick = (): void => {
  if (!message.value.trim()) return // 如果输入框为空则不发送消息
  clearMessages(); // 清空消息
  fetchAIInterpretation(message.value); // 调用 fetchAIInterpretation
  message.value = '' // 清空输入框
};

const clearMessages = (): void => {
  messages.value = []; // 清空消息数组
  markdownContent.value = ''; // 清空 Markdown 内容
};

</script>

<template>
  <!-- 圆形按钮，点击后显示右侧面板 -->
  <div class="toggle-button" @click="togglePanel">
   <ElIcon><Search /></ElIcon> <!-- 图标，您可以自定义 -->
  </div>

  <el-card v-if="isPanelVisible" class="mb-15 box-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>Guess You Like</span>
      </div>
    </template>
    <div class="guess-like-list" v-loading="props.loading">
      <ol v-show="props.result.length > 0">
        <li v-for="(itm, index) in props.result" :key="index" class="mb-5">
          <el-link @click="search(itm)">{{ itm }}</el-link>
        </li>
      </ol>
      <el-empty
        v-show="props.result.length <= 0"
        description="No guess result"
        :image-size="50"
      ></el-empty>
    </div>
<!--    <div style="font-size: 14px;" class="messages">{{ concatenatedMessage }}</div>-->
    <div style="font-size: 14px; padding-top: 10px;" class="markdown-result" v-html="compiledMarkdown"></div>
    <!-- 消息输入框和发送按钮 -->
    <div class="message-input">
      <el-input
        v-model="message"
        type="textarea"
        placeholder="Type your message..."
        class="input-field"
        clearable
        :autosize="{ minRows: 2, maxRows: 6 }"
        @keyup.enter="handleGuessClick"
      ></el-input>
      <ElIcon class="send-icon" @click="handleGuessClick"><Promotion /></ElIcon>
    </div>
  </el-card>
</template>

<style scoped>
.toggle-button {
  position: fixed;
  top: 35%;
  right: 0;
  width: 50px;
  height: 50px;
  background-color: #409EFF;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1000;
  transform: translateY(-50%);
  animation: idlePulse 2s infinite alternate; /* 添加动画效果 */
  transition: background-color 0.3s ease, box-shadow 0.3s ease; /* 增加过渡效果 */
}

/* 侧边面板样式 */
.toggle-button:hover {
  background-color: #66b1ff; /* 更亮的蓝色 */
  box-shadow: 0 0 10px #409EFF, 0 0 20px #6611ff; /* 添加阴影效果 */
}

@keyframes idlePulse {
  0% {
    background-color: #409EFF;
    transform: scale(1);
  }
  50% {
    background-color: #666fff; /* 轻微变亮 */
    transform: scale(1.1); /* 轻微放大 */
  }
  100% {
    background-color: #409EFF;
    transform: scale(1);
  }
}

.guess-like-list ol {
  padding-left: 15px;
}
.box-card {
  width: 160%;
  overflow-y: auto;
}

.message-input {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  padding-top: 12px;
}

.input-field {
  flex: 1;
  margin-right: 5px;
  height: 60px;
  font-size: 14px;
}

.send-icon {
  display: flex;
  font-size: 26px;
  color: #409EFF;
  align-items: center;
  cursor: pointer;
}

.card-header {
  display: flex;
  align-items: center;
}
</style>
