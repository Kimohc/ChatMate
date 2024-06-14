<template>
  <div class="toast" :class="{ active: isToastActive }">
    <div class="toast-content">
      <div v-if="localIsGood">
        <svg class="check" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10.5858 13.4142L7.75735 10.5858L6.34314 12L10.5858 16.2427L17.6568 9.1716L16.2426 7.75739L10.5858 13.4142Z" fill="currentColor" /></svg>
      </div>
      <div v-else>
        <svg class="cross" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.2253 4.81108C5.83477 4.42056 5.20161 4.42056 4.81108 4.81108C4.42056 5.20161 4.42056 5.83477 4.81108 6.2253L10.5858 12L4.81114 17.7747C4.42062 18.1652 4.42062 18.7984 4.81114 19.1889C5.20167 19.5794 5.83483 19.5794 6.22535 19.1889L12 13.4142L17.7747 19.1889C18.1652 19.5794 18.7984 19.5794 19.1889 19.1889C19.5794 18.7984 19.5794 18.1652 19.1889 17.7747L13.4142 12L19.189 6.2253C19.5795 5.83477 19.5795 5.20161 19.189 4.81108C18.7985 4.42056 18.1653 4.42056 17.7748 4.81108L12 10.5858L6.2253 4.81108Z" fill="currentColor" /></svg>
      </div>
      <div class="message">
        <h3 v-if="localIsGood">Success</h3>
        <h3 v-else>Error</h3>
        <span class="text text-2">{{ localMessage }}</span>
      </div>
    </div>
    <svg class="close" @click="closeToast" width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16.3394 9.32245C16.7434 8.94589 16.7657 8.31312 16.3891 7.90911C16.0126 7.50509 15.3798 7.48283 14.9758 7.85938L12.0497 10.5866L9.32245 7.66048C8.94589 7.25647 8.31312 7.23421 7.90911 7.61076C7.50509 7.98731 7.48283 8.62008 7.85938 9.0241L10.5866 11.9502L7.66048 14.6775C7.25647 15.054 7.23421 15.6868 7.61076 16.0908C7.98731 16.4948 8.62008 16.5171 9.0241 16.1405L11.9502 13.4133L14.6775 16.3394C15.054 16.7434 15.6868 16.7657 16.0908 16.3891C16.4948 16.0126 16.5171 15.3798 16.1405 14.9758L13.4133 12.0497L16.3394 9.32245Z" fill="currentColor" /><path fill-rule="evenodd" clip-rule="evenodd" d="M1 12C1 5.92487 5.92487 1 12 1C18.0751 1 23 5.92487 23 12C23 18.0751 18.0751 23 12 23C5.92487 23 1 18.0751 1 12ZM12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21Z" fill="currentColor" /></svg>
    <div class="progress" :class="{ active: isProgressActive, 'progress-red': !localIsGood }"></div>
  </div>
</template>

<script>
export default {
  name: 'MyAlert',
  props: {
    message: {
      type: String,
      default: 'This is a message',
    },
    isGood: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isToastActive: false,
      isProgressActive: false,
      localMessage: this.message,
      localIsGood: this.isGood,
      timer1: null,
      timer2: null,
    };
  },
  watch: {
    message(newMessage) {
      this.localMessage = newMessage;
    },
    isGood(newIsGood) {
      this.localIsGood = newIsGood;
    }
  },
  methods: {
    showToast() {
      this.isToastActive = true;
      this.isProgressActive = true;

      this.timer1 = setTimeout(() => {
        this.isToastActive = false;
      }, 5000);

      this.timer2 = setTimeout(() => {
        this.isProgressActive = false;
      }, 5300);
    },
    closeToast() {
      this.isToastActive = false;

      setTimeout(() => {
        this.isProgressActive = false;
      }, 300);

      clearTimeout(this.timer1);
      clearTimeout(this.timer2);
    },
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
}
.toast .progress.progress-red:before {
  background-color: red;
}
body {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f4f7ff;
  overflow: hidden;
}
.toast {
  position: fixed;
  top: 25px;
  right: 30px;
  border-radius: 12px;
  background: #fff;
  padding: 20px 35px 20px 25px;
  box-shadow: 0 6px 20px -5px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transform: translateX(calc(100% + 30px));
  transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.35);
  z-index: 10000;
}
.toast.active {
  transform: translateX(0%);
}
.toast .toast-content {
  display: flex;
  align-items: center;
}
.toast-content .check, .cross {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 35px;
  min-width: 35px;
  background-color: #2770ff;
  color: #fff;
  font-size: 20px;
  border-radius: 50%;
}
.cross {
  background-color: red;
}
.toast-content .message {
  display: flex;
  flex-direction: column;
  margin: 0 20px;
}
.message .text {
  font-size: 16px;
  font-weight: 400;
  color: #666666;
}
.message .text.text-1 {
  font-weight: 600;
  color: #333;
}
.toast .close {
  position: absolute;
  top: 10px;
  right: 15px;
  padding: 5px;
  cursor: pointer;
  opacity: 0.7;
}
.toast .close:hover {
  opacity: 1;
}
.toast .progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 100%;
  background-color: #ddd;
}
.toast .progress:before {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: #2bc156;
  transition: all 5s linear;
}
.toast .progress.active:before {
  width: 0%;
}
</style>
