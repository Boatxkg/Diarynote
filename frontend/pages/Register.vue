<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '~/middleware/register.js'

const username = ref('')
const password = ref('')
const message = ref('')
const error = ref('')
const router = useRouter()
const handleRegister = async () => {
  error.value = ''
  try {
    const res = await registerUser(username.value, password.value)
    message.value = res.msg
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.msg || 'Registration failed'
  }
}
</script>

<template>
  <div class="flex-grow flex justify-center items-center h-[87.9vh]">
    <div class="w-[102vh] h-[56vh] rounded-xl flex shadow">
      <!-- ด้านซ้าย -->
      <div class="h-[56vh] flex-3 text-center bg-[rgba(142,142,142,0.2)] backdrop-blur-md rounded-s-lg">
        <h1 class="text-white text-[8vh]">Register</h1>
        <div class="flex justify-center mx-[-2vh]">
          <img src="../img/as.png" alt="" class="w-[42vh]">
        </div>
      </div>

      <!-- ด้านขวา -->
      <div class="flex-2 flex flex-col justify-center items-center pb-[10vh] bg-[rgba(142,142,142,1)] rounded-br-[1vh] rounded-tr-[1vh] text-[#DFDFDF] noto-sans-thai-slim">
        <div class="text-center">
          <h1 class="text-[3vh]">ระบบสมัครสมาชิก</h1>
        </div>
        
        <div class="flex flex-col justify-center items-center mt-[1vh]">
          <div>
            <h1>Username</h1>
            <input
              v-model="username"
              type="text"
              class="rounded transition-transform duration-300 ease-in-out focus:scale-105 focus:outline-none bg-gray-500"
            >
          </div>
          <div class="mt-2">
            <h1>Password</h1>
            <input
              v-model="password"
              type="password"
              class=" rounded transition-transform duration-300 ease-in-out focus:scale-105 focus:outline-none bg-gray-500"
            >
          </div>
        </div>

        <!-- ปุ่ม Register -->
        <button
          @click="handleRegister"
          class="bg-blue-500 cursor-pointer rounded w-[16vh] p-1 mt-4 text-white transition-transform duration-300 ease-in-out hover:scale-105"
        >
          Register
        </button>

        <!-- แสดงข้อความ -->
        <div v-if="message" class="mt-2 text-green-300">{{ message }}</div>
        <div v-if="error" class="mt-2 text-red-300">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

